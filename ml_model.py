"""
ML Model Module for India Carbon Emissions Tracker
Forecasts state-level emissions using Linear Regression and classifies states by tier
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from typing import Dict, Tuple
import os


# Tier thresholds based on YoY emission growth rate
TIER_THRESHOLDS = {
    'On Track': 0.02,  # < 2% annual growth
    'Needs Attention': 0.05,  # 2-5% annual growth
    'Critical': float('inf')  # > 5% annual growth
}


def load_state_data() -> pd.DataFrame:
    """
    Load state emissions data from CSV.
    
    Returns:
        pd.DataFrame: State emissions data
    """
    csv_path = os.path.join("data", "state_emissions.csv")
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"State emissions data not found at {csv_path}. "
            "Run data_fetcher.py first."
        )
    
    df = pd.read_csv(csv_path)
    print(f"✓ Loaded {len(df)} emission records")
    
    return df


def train_forecast_model(state_df: pd.DataFrame, state_name: str) -> LinearRegression:
    """
    Train a Linear Regression model for a specific state's emission forecast.
    
    Args:
        state_df: State emissions DataFrame
        state_name: Name of the state to train for
    
    Returns:
        Trained LinearRegression model
    """
    # Filter for this state and aggregate by year
    state_data = state_df[state_df['state'] == state_name].copy()
    yearly_emissions = state_data.groupby('year')['co2_mt'].sum().reset_index()
    
    # Prepare features (year) and target (emissions)
    X = yearly_emissions['year'].values.reshape(-1, 1)
    y = yearly_emissions['co2_mt'].values
    
    # Train model
    model = LinearRegression()
    model.fit(X, y)
    
    return model


def forecast_emissions(
    state_df: pd.DataFrame, 
    forecast_years: list = None
) -> pd.DataFrame:
    """
    Forecast emissions for all states up to 2035.
    
    Args:
        state_df: State emissions DataFrame
        forecast_years: Years to forecast (default: 2024-2035)
    
    Returns:
        pd.DataFrame: Historical + forecasted emissions with columns:
            state, year, co2_mt, is_forecast
    """
    if forecast_years is None:
        forecast_years = list(range(2024, 2036))
    
    print(f"Forecasting emissions for {len(state_df['state'].unique())} states...")
    
    forecast_records = []
    
    # Get unique states
    states = state_df['state'].unique()
    
    for state in states:
        # Historical data
        state_data = state_df[state_df['state'] == state].copy()
        yearly_historical = state_data.groupby('year')['co2_mt'].sum().reset_index()
        
        for _, row in yearly_historical.iterrows():
            forecast_records.append({
                'state': state,
                'year': int(row['year']),
                'co2_mt': round(row['co2_mt'], 2),
                'is_forecast': False
            })
        
        # Train model for this state
        model = train_forecast_model(state_df, state)
        
        # Forecast future years
        X_future = np.array(forecast_years).reshape(-1, 1)
        y_future = model.predict(X_future)
        
        for year, emission in zip(forecast_years, y_future):
            forecast_records.append({
                'state': state,
                'year': int(year),
                'co2_mt': round(max(0, emission), 2),  # Ensure non-negative
                'is_forecast': True
            })
    
    forecast_df = pd.DataFrame(forecast_records)
    print(f"✓ Forecasted emissions through {max(forecast_years)}")
    
    return forecast_df


def calculate_peak_year(forecast_df: pd.DataFrame, state_name: str) -> int:
    """
    Calculate the projected year when a state's emissions will peak.
    
    Args:
        forecast_df: Forecast DataFrame with historical + predicted emissions
        state_name: Name of the state
    
    Returns:
        int: Year when emissions peak (or last forecast year if still growing)
    """
    state_data = forecast_df[forecast_df['state'] == state_name].sort_values('year')
    
    # Find year with maximum emissions
    peak_idx = state_data['co2_mt'].idxmax()
    peak_year = int(state_data.loc[peak_idx, 'year'])
    
    return peak_year


def calculate_growth_rate(forecast_df: pd.DataFrame, state_name: str) -> float:
    """
    Calculate average annual emission growth rate for a state.
    
    Args:
        forecast_df: Forecast DataFrame
        state_name: Name of the state
    
    Returns:
        float: Average annual growth rate (as decimal, e.g., 0.03 = 3%)
    """
    state_data = forecast_df[
        (forecast_df['state'] == state_name) & 
        (~forecast_df['is_forecast'])
    ].sort_values('year')
    
    if len(state_data) < 2:
        return 0.0
    
    # Calculate year-over-year growth rates
    emissions = state_data['co2_mt'].values
    growth_rates = []
    
    for i in range(1, len(emissions)):
        if emissions[i-1] > 0:
            growth = (emissions[i] - emissions[i-1]) / emissions[i-1]
            growth_rates.append(growth)
    
    # Return average growth rate
    avg_growth = np.mean(growth_rates) if growth_rates else 0.0
    
    return avg_growth


def classify_state_tier(growth_rate: float) -> str:
    """
    Classify a state into a tier based on its emission growth rate.
    
    Args:
        growth_rate: Average annual growth rate (decimal)
    
    Returns:
        str: Tier classification ('On Track', 'Needs Attention', or 'Critical')
    """
    if growth_rate < TIER_THRESHOLDS['On Track']:
        return 'On Track'
    elif growth_rate < TIER_THRESHOLDS['Needs Attention']:
        return 'Needs Attention'
    else:
        return 'Critical'


def generate_tier_classifications(forecast_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate tier classifications for all states.
    
    Args:
        forecast_df: Forecast DataFrame
    
    Returns:
        pd.DataFrame: State classifications with columns:
            state, avg_growth_rate, tier, peak_year, current_emission, forecast_2035
    """
    print("Classifying states into tiers...")
    
    states = forecast_df['state'].unique()
    classifications = []
    
    for state in states:
        growth_rate = calculate_growth_rate(forecast_df, state)
        tier = classify_state_tier(growth_rate)
        peak_year = calculate_peak_year(forecast_df, state)
        
        # Current emission (latest historical year)
        state_historical = forecast_df[
            (forecast_df['state'] == state) & 
            (~forecast_df['is_forecast'])
        ]
        current_emission = state_historical['co2_mt'].iloc[-1] if len(state_historical) > 0 else 0
        
        # Forecasted 2035 emission
        state_2035 = forecast_df[
            (forecast_df['state'] == state) & 
            (forecast_df['year'] == 2035)
        ]
        forecast_2035 = state_2035['co2_mt'].iloc[0] if len(state_2035) > 0 else 0
        
        classifications.append({
            'state': state,
            'avg_growth_rate': round(growth_rate * 100, 2),  # Convert to percentage
            'tier': tier,
            'peak_year': peak_year,
            'current_emission_mt': round(current_emission, 2),
            'forecast_2035_mt': round(forecast_2035, 2)
        })
    
    tier_df = pd.DataFrame(classifications)
    
    # Sort by tier severity (Critical first) then by growth rate
    tier_order = {'Critical': 0, 'Needs Attention': 1, 'On Track': 2}
    tier_df['tier_rank'] = tier_df['tier'].map(tier_order)
    tier_df = tier_df.sort_values(['tier_rank', 'avg_growth_rate'], ascending=[True, False])
    tier_df = tier_df.drop('tier_rank', axis=1)
    
    print(f"✓ Classified {len(tier_df)} states")
    print(f"  - On Track: {len(tier_df[tier_df['tier'] == 'On Track'])}")
    print(f"  - Needs Attention: {len(tier_df[tier_df['tier'] == 'Needs Attention'])}")
    print(f"  - Critical: {len(tier_df[tier_df['tier'] == 'Critical'])}")
    
    return tier_df


def run_ml_pipeline() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Main ML pipeline: load data, forecast, and classify states.
    
    Returns:
        Tuple of (forecast_df, tier_classification_df)
    """
    print("=" * 60)
    print("INDIA CARBON EMISSIONS TRACKER - ML PIPELINE")
    print("=" * 60)
    
    # Step 1: Load data
    state_df = load_state_data()
    
    # Step 2: Forecast emissions
    forecast_df = forecast_emissions(state_df)
    
    # Step 3: Classify states
    tier_df = generate_tier_classifications(forecast_df)
    
    # Step 4: Save outputs
    forecast_csv = os.path.join("data", "emissions_forecast.csv")
    forecast_df.to_csv(forecast_csv, index=False)
    print(f"✓ Saved forecast to {forecast_csv}")
    
    tier_csv = os.path.join("data", "state_tiers.csv")
    tier_df.to_csv(tier_csv, index=False)
    print(f"✓ Saved tier classifications to {tier_csv}")
    
    print("=" * 60)
    print("ML PIPELINE COMPLETE")
    print("=" * 60)
    
    return forecast_df, tier_df


if __name__ == "__main__":
    # Test the ML pipeline
    forecast_df, tier_df = run_ml_pipeline()
    
    print("\n📊 FORECAST SAMPLE:")
    print(forecast_df[forecast_df['state'] == 'Maharashtra'].tail(15))
    
    print("\n🎯 TIER CLASSIFICATIONS:")
    print(tier_df.to_string(index=False))
