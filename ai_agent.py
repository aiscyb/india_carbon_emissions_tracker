"""
AI Agent Module for India Carbon Emissions Tracker
Uses Anthropic Claude API as an intelligent policy analyst
"""

import os
import json
import pandas as pd
from anthropic import Anthropic
from typing import Dict, Any, Optional


# System prompt for EmissionsIQ
SYSTEM_PROMPT = """You are EmissionsIQ, an AI policy analyst for India's carbon statistics.

You help government officials and researchers understand state-wise emission trends, 
net-zero gaps, and policy priorities for India's path to net-zero by 2070.

Your capabilities:
- Analyze state-level emission trends and forecasts
- Calculate net-zero gaps and reduction requirements
- Compare states on emission performance
- Identify top polluting sectors
- Generate concise, actionable policy recommendations

Guidelines:
- Always cite specific data points (numbers, percentages, years)
- Be concise and actionable - government officials are busy
- Focus on policy implications, not just statistics
- Use Indian context and terminology
- Acknowledge uncertainty in forecasts
- Prioritize equity alongside emissions (consider state development needs)

Response format:
- Start with the key finding (1 sentence)
- Support with 2-3 data points
- End with 1-2 actionable recommendations
"""


class EmissionsIQAgent:
    """AI Agent for analyzing India's carbon emissions data."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the EmissionsIQ agent.
        
        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            print("⚠ Warning: ANTHROPIC_API_KEY not set. Agent will run in demo mode.")
            self.client = None
        else:
            self.client = Anthropic(api_key=self.api_key)
        
        # Load data files
        self.forecast_df = self._load_csv("data/emissions_forecast.csv")
        self.tier_df = self._load_csv("data/state_tiers.csv")
        self.state_df = self._load_csv("data/state_emissions.csv")
        self.gap_df = self._load_csv("data/net_zero_gaps.csv")
    
    def _load_csv(self, path: str) -> pd.DataFrame:
        """Load CSV file if it exists, else return empty DataFrame."""
        if os.path.exists(path):
            return pd.read_csv(path)
        return pd.DataFrame()
    
    def get_state_emissions(self, state_name: str) -> Dict[str, Any]:
        """
        Get emission trend and tier for a specific state.
        
        Args:
            state_name: Name of the state
        
        Returns:
            Dict with emission data and tier classification
        """
        if self.forecast_df.empty or self.tier_df.empty:
            return {"error": "Data not available. Run data pipeline first."}
        
        # Get state forecast
        state_forecast = self.forecast_df[
            self.forecast_df['state'] == state_name
        ].sort_values('year')
        
        if state_forecast.empty:
            return {"error": f"State '{state_name}' not found in dataset."}
        
        # Get tier info
        state_tier = self.tier_df[self.tier_df['state'] == state_name]
        
        # Separate historical and forecast
        historical = state_forecast[~state_forecast['is_forecast']]
        forecast = state_forecast[state_forecast['is_forecast']]
        
        return {
            "state": state_name,
            "tier": state_tier['tier'].iloc[0] if not state_tier.empty else "Unknown",
            "avg_growth_rate_pct": state_tier['avg_growth_rate'].iloc[0] if not state_tier.empty else 0,
            "peak_year": int(state_tier['peak_year'].iloc[0]) if not state_tier.empty else None,
            "current_emission_mt": state_tier['current_emission_mt'].iloc[0] if not state_tier.empty else 0,
            "forecast_2035_mt": state_tier['forecast_2035_mt'].iloc[0] if not state_tier.empty else 0,
            "historical_years": historical['year'].tolist(),
            "historical_emissions": historical['co2_mt'].tolist(),
            "forecast_years": forecast['year'].tolist(),
            "forecast_emissions": forecast['co2_mt'].tolist()
        }
    
    def get_net_zero_gap(self, state_name: str) -> Dict[str, Any]:
        """
        Get net-zero gap for a specific state.
        
        Args:
            state_name: Name of the state
        
        Returns:
            Dict with gap analysis
        """
        if self.gap_df.empty:
            return {"error": "Gap data not available."}
        
        state_gap = self.gap_df[self.gap_df['state'] == state_name]
        
        if state_gap.empty:
            return {"error": f"State '{state_name}' not found."}
        
        return {
            "state": state_name,
            "current_emission_mt": float(state_gap['current_emission_mt'].iloc[0]),
            "target_emission_mt": float(state_gap['target_emission_mt'].iloc[0]),
            "net_zero_gap_mt": float(state_gap['net_zero_gap_mt'].iloc[0]),
            "reduction_needed_pct": float(state_gap['reduction_needed_pct'].iloc[0])
        }
    
    def compare_states(self, state1: str, state2: str) -> Dict[str, Any]:
        """
        Compare two states side-by-side.
        
        Args:
            state1: First state name
            state2: Second state name
        
        Returns:
            Dict with comparison data
        """
        data1 = self.get_state_emissions(state1)
        data2 = self.get_state_emissions(state2)
        
        if "error" in data1 or "error" in data2:
            return {"error": "One or both states not found."}
        
        gap1 = self.get_net_zero_gap(state1)
        gap2 = self.get_net_zero_gap(state2)
        
        return {
            "state1": {
                "name": state1,
                "tier": data1['tier'],
                "current_emission_mt": data1['current_emission_mt'],
                "forecast_2035_mt": data1['forecast_2035_mt'],
                "growth_rate_pct": data1['avg_growth_rate_pct'],
                "net_zero_gap_mt": gap1.get('net_zero_gap_mt', 0)
            },
            "state2": {
                "name": state2,
                "tier": data2['tier'],
                "current_emission_mt": data2['current_emission_mt'],
                "forecast_2035_mt": data2['forecast_2035_mt'],
                "growth_rate_pct": data2['avg_growth_rate_pct'],
                "net_zero_gap_mt": gap2.get('net_zero_gap_mt', 0)
            }
        }
    
    def get_top_polluting_sectors(self, state_name: str) -> Dict[str, Any]:
        """
        Get sector-wise emission breakdown for a state.
        
        Args:
            state_name: Name of the state
        
        Returns:
            Dict with sector breakdown
        """
        if self.state_df.empty:
            return {"error": "State data not available."}
        
        # Get latest year data
        latest_year = self.state_df['year'].max()
        state_latest = self.state_df[
            (self.state_df['state'] == state_name) & 
            (self.state_df['year'] == latest_year)
        ]
        
        if state_latest.empty:
            return {"error": f"State '{state_name}' not found."}
        
        # Aggregate by sector
        sector_emissions = state_latest.groupby('sector')['co2_mt'].sum().sort_values(ascending=False)
        
        total = sector_emissions.sum()
        
        return {
            "state": state_name,
            "year": int(latest_year),
            "total_emission_mt": round(total, 2),
            "sectors": {
                sector: {
                    "emission_mt": round(emission, 2),
                    "percentage": round((emission / total) * 100, 1)
                }
                for sector, emission in sector_emissions.items()
            }
        }
    
    def generate_policy_brief(self, state_name: str) -> str:
        """
        Generate an AI-powered policy brief for a state using Claude.
        
        Args:
            state_name: Name of the state
        
        Returns:
            str: Policy brief text
        """
        # Gather all relevant data
        emissions_data = self.get_state_emissions(state_name)
        gap_data = self.get_net_zero_gap(state_name)
        sector_data = self.get_top_polluting_sectors(state_name)
        
        if "error" in emissions_data:
            return f"Error: {emissions_data['error']}"
        
        # Prepare context for Claude
        context = f"""
State: {state_name}
Tier Classification: {emissions_data['tier']}
Current Emission: {emissions_data['current_emission_mt']} MT CO2
Projected 2035 Emission: {emissions_data['forecast_2035_mt']} MT CO2
Average Growth Rate: {emissions_data['avg_growth_rate_pct']}% per year
Peak Emission Year: {emissions_data['peak_year']}

Net-Zero Gap:
- Current: {gap_data['current_emission_mt']} MT
- Target (2030): {gap_data['target_emission_mt']} MT
- Gap: {gap_data['net_zero_gap_mt']} MT
- Reduction Needed: {gap_data['reduction_needed_pct']}%

Top Polluting Sectors:
{json.dumps(sector_data['sectors'], indent=2)}
"""
        
        # If API key is not available, return a template
        if not self.client:
            return self._generate_template_brief(state_name, emissions_data, gap_data, sector_data)
        
        # Call Claude API
        try:
            message = self.client.messages.create(
                model="claude-haiku-20241022",
                max_tokens=500,
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": f"Generate a concise 3-point policy brief for {state_name} based on this data:\n\n{context}"
                    }
                ]
            )
            
            return message.content[0].text
        
        except Exception as e:
            print(f"⚠ Error calling Claude API: {e}")
            return self._generate_template_brief(state_name, emissions_data, gap_data, sector_data)
    
    def _generate_template_brief(
        self, 
        state_name: str, 
        emissions_data: Dict, 
        gap_data: Dict, 
        sector_data: Dict
    ) -> str:
        """Generate a template policy brief without AI (fallback)."""
        
        tier = emissions_data['tier']
        growth = emissions_data['avg_growth_rate_pct']
        gap = gap_data['net_zero_gap_mt']
        
        top_sector = list(sector_data['sectors'].keys())[0]
        top_sector_pct = sector_data['sectors'][top_sector]['percentage']
        
        brief = f"""
📋 POLICY BRIEF: {state_name}

Status: {tier} (Growing at {growth}% annually)

Key Findings:
1. Emission Trajectory: {state_name} is currently emitting {emissions_data['current_emission_mt']} MT CO2 
   and is projected to reach {emissions_data['forecast_2035_mt']} MT by 2035.

2. Net-Zero Gap: To meet India's 2030 interim targets, {state_name} must reduce emissions 
   by {gap} MT ({gap_data['reduction_needed_pct']}% reduction from current levels).

3. Sector Focus: {top_sector} accounts for {top_sector_pct}% of emissions - 
   this should be the primary focus for mitigation strategies.

Recommendations:
• Accelerate renewable energy deployment in {top_sector.lower()} sector
• Implement state-level carbon pricing or intensity targets
• Establish monitoring & verification system for emission tracking
        """
        
        return brief.strip()
    
    def chat(self, user_query: str) -> str:
        """
        Handle a natural language query from the user.
        Uses Claude to decide which tool to call and format the response.
        
        Args:
            user_query: User's natural language question
        
        Returns:
            str: AI-generated response with relevant data
        """
        # Tool selection logic (simplified - in production, use Claude tool calling)
        query_lower = user_query.lower()
        
        # Extract state names from query
        states = [s for s in self.tier_df['state'].unique() if s.lower() in query_lower]
        
        # Decide which tool to use
        if "compare" in query_lower and len(states) >= 2:
            data = self.compare_states(states[0], states[1])
            return self._format_comparison_response(data)
        
        elif "gap" in query_lower and len(states) >= 1:
            data = self.get_net_zero_gap(states[0])
            return self._format_gap_response(data)
        
        elif "sector" in query_lower and len(states) >= 1:
            data = self.get_top_polluting_sectors(states[0])
            return self._format_sector_response(data)
        
        elif "policy" in query_lower or "brief" in query_lower and len(states) >= 1:
            return self.generate_policy_brief(states[0])
        
        elif "critical" in query_lower or "worst" in query_lower:
            critical = self.tier_df[self.tier_df['tier'] == 'Critical']
            return self._format_critical_states(critical)
        
        elif len(states) >= 1:
            data = self.get_state_emissions(states[0])
            return self._format_emissions_response(data)
        
        else:
            return "I can help you analyze state emissions. Try asking about specific states or use commands like 'compare Maharashtra and Gujarat' or 'show critical states'."
    
    def _format_emissions_response(self, data: Dict) -> str:
        """Format emission data into readable response."""
        if "error" in data:
            return data["error"]
        
        return f"""
📊 {data['state']} Emission Analysis

Tier: {data['tier']} ({'🟢' if data['tier'] == 'On Track' else '🟡' if data['tier'] == 'Needs Attention' else '🔴'})
Current Emissions: {data['current_emission_mt']} MT CO2
Forecast (2035): {data['forecast_2035_mt']} MT CO2
Growth Rate: {data['avg_growth_rate_pct']}% per year
Peak Year: {data['peak_year']}

The state's emissions are {"decreasing" if data['avg_growth_rate_pct'] < 0 else "increasing"} 
{"slowly" if abs(data['avg_growth_rate_pct']) < 3 else "rapidly"}.
        """.strip()
    
    def _format_gap_response(self, data: Dict) -> str:
        """Format net-zero gap data."""
        if "error" in data:
            return data["error"]
        
        return f"""
🎯 {data['state']} Net-Zero Gap

Current: {data['current_emission_mt']} MT CO2
Target (2030): {data['target_emission_mt']} MT CO2
Gap: {data['net_zero_gap_mt']} MT CO2
Reduction Needed: {data['reduction_needed_pct']}%

{data['state']} needs to reduce emissions by {data['reduction_needed_pct']}% 
to meet India's 2030 climate commitments.
        """.strip()
    
    def _format_sector_response(self, data: Dict) -> str:
        """Format sector breakdown."""
        if "error" in data:
            return data["error"]
        
        sectors_text = "\n".join([
            f"  • {sector}: {info['emission_mt']} MT ({info['percentage']}%)"
            for sector, info in data['sectors'].items()
        ])
        
        return f"""
🏭 {data['state']} Sector Breakdown ({data['year']})

Total: {data['total_emission_mt']} MT CO2

{sectors_text}
        """.strip()
    
    def _format_comparison_response(self, data: Dict) -> str:
        """Format state comparison."""
        if "error" in data:
            return data["error"]
        
        s1 = data['state1']
        s2 = data['state2']
        
        return f"""
⚖️ State Comparison

{s1['name']} vs {s2['name']}

Tier: {s1['tier']} vs {s2['tier']}
Current: {s1['current_emission_mt']} MT vs {s2['current_emission_mt']} MT
Growth: {s1['growth_rate_pct']}% vs {s2['growth_rate_pct']}%
Gap: {s1['net_zero_gap_mt']} MT vs {s2['net_zero_gap_mt']} MT

{s1['name'] if s1['current_emission_mt'] < s2['current_emission_mt'] else s2['name']} 
has lower current emissions, but both states need significant action.
        """.strip()
    
    def _format_critical_states(self, df: pd.DataFrame) -> str:
        """Format list of critical states."""
        if df.empty:
            return "✓ Good news: No states are in the Critical tier!"
        
        states_list = "\n".join([
            f"  • {row['state']}: {row['avg_growth_rate']}% growth, {row['current_emission_mt']} MT"
            for _, row in df.iterrows()
        ])
        
        return f"""
🔴 Critical States ({len(df)} total)

{states_list}

These states have emission growth rates exceeding 5% per year and require 
immediate policy intervention.
        """.strip()


if __name__ == "__main__":
    # Test the AI agent
    print("=" * 60)
    print("INDIA CARBON EMISSIONS TRACKER - AI AGENT TEST")
    print("=" * 60)
    
    agent = EmissionsIQAgent()
    
    # Test various tools
    print("\n🧪 Test 1: Get state emissions")
    result = agent.get_state_emissions("Maharashtra")
    print(json.dumps(result, indent=2))
    
    print("\n🧪 Test 2: Get net-zero gap")
    result = agent.get_net_zero_gap("Gujarat")
    print(json.dumps(result, indent=2))
    
    print("\n🧪 Test 3: Compare states")
    result = agent.compare_states("Maharashtra", "Gujarat")
    print(json.dumps(result, indent=2))
    
    print("\n🧪 Test 4: Get top sectors")
    result = agent.get_top_polluting_sectors("Tamil Nadu")
    print(json.dumps(result, indent=2))
    
    print("\n🧪 Test 5: Generate policy brief")
    brief = agent.generate_policy_brief("Odisha")
    print(brief)
    
    print("\n🧪 Test 6: Chat interface")
    response = agent.chat("Which states are most critical?")
    print(response)
