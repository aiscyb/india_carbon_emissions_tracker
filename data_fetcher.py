"""
Data Fetcher Module for India Carbon Emissions Tracker
Downloads OWID CO2 data and generates state-level emission estimates
"""

import pandas as pd
import requests
import os
from typing import Tuple

# OWID CO2 dataset URL (no API key needed)
OWID_CO2_URL = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"

# Indian states for state-level analysis
INDIAN_STATES = [
    "Maharashtra", "Uttar Pradesh", "Gujarat", "Rajasthan", "Madhya Pradesh",
    "Tamil Nadu", "West Bengal", "Karnataka", "Andhra Pradesh", "Odisha",
    "Punjab", "Haryana", "Bihar", "Jharkhand", "Chhattisgarh"
]

# Sector-wise emission weights (based on India's typical distribution)
SECTOR_WEIGHTS = {
    "Energy": 0.45,
    "Industry": 0.25,
    "Transport": 0.15,
    "Agriculture": 0.10,
    "Waste": 0.05
}

# State-wise emission multipliers (proportional to industrial activity + population)
# Based on approximate state contributions to national emissions
STATE_MULTIPLIERS = {
    "Maharashtra": 0.12,
    "Uttar Pradesh": 0.11,
    "Gujarat": 0.10,
    "Rajasthan": 0.07,
    "Madhya Pradesh": 0.07,
    "Tamil Nadu": 0.08,
    "West Bengal": 0.07,
    "Karnataka": 0.06,
    "Andhra Pradesh": 0.06,
    "Odisha": 0.05,
    "Punjab": 0.04,
    "Haryana": 0.04,
    "Bihar": 0.05,
    "Jharkhand": 0.04,
    "Chhattisgarh": 0.04
}

# Approximate state populations (in millions, 2023 estimates)
STATE_POPULATIONS = {
    "Maharashtra": 124, "Uttar Pradesh": 240, "Gujarat": 70, "Rajasthan": 82,
    "Madhya Pradesh": 88, "Tamil Nadu": 77, "West Bengal": 100, "Karnataka": 68,
    "Andhra Pradesh": 54, "Odisha": 47, "Punjab": 30, "Haryana": 29,
    "Bihar": 128, "Jharkhand": 40, "Chhattisgarh": 30
}

# Approximate state GDP (in billion USD, 2023 estimates)
STATE_GDP = {
    "Maharashtra": 400, "Uttar Pradesh": 240, "Gujarat": 250, "Rajasthan": 150,
    "Madhya Pradesh": 130, "Tamil Nadu": 280, "West Bengal": 180, "Karnataka": 240,
    "Andhra Pradesh": 120, "Odisha": 80, "Punjab": 85, "Haryana": 110,
    "Bihar": 90, "Jharkhand": 60, "Chhattisgarh": 55
}


def download_owid_data() -> pd.DataFrame:
    """
    Download OWID CO2 dataset and filter for India.
    
    Returns:
        pd.DataFrame: India's national emission data
    """
    print("Downloading OWID CO2 dataset...")
    
    try:
        response = requests.get(OWID_CO2_URL, timeout=30)
        response.raise_for_status()
        
        # Save to local cache
        cache_path = os.path.join("data", "owid_co2_data.csv")
        with open(cache_path, 'wb') as f:
            f.write(response.content)
        
        # Load and filter for India
        df = pd.read_csv(cache_path)
        india_df = df[df['country'] == 'India'].copy()
        
        print(f"✓ Downloaded {len(india_df)} records for India")
        return india_df
    
    except Exception as e:
        print(f"⚠ Error downloading OWID data: {e}")
        print("Using fallback mode...")
        return pd.DataFrame()


def generate_state_emissions(india_national_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate realistic state-level emission estimates based on national data.
    
    Args:
        india_national_df: National India emissions data from OWID
    
    Returns:
        pd.DataFrame: State-level emissions with columns:
            state, year, sector, co2_mt, gdp_usd, population
    """
    print("Generating state-level emission estimates...")
    
    # If we have national data, use it as baseline
    if not india_national_df.empty and 'year' in india_national_df.columns and 'co2' in india_national_df.columns:
        national_data = india_national_df[['year', 'co2']].copy()
        national_data = national_data[
            (national_data['year'] >= 2005) & 
            (national_data['year'] <= 2023)
        ]
    else:
        # Fallback: use estimated national emissions
        years = list(range(2005, 2024))
        # India's CO2 emissions grew from ~1200 MT (2005) to ~2700 MT (2023)
        national_emissions = [1200 + (i * 80) for i in range(len(years))]
        national_data = pd.DataFrame({
            'year': years,
            'co2': national_emissions
        })
    
    # Generate state-level data
    state_records = []
    
    for state in INDIAN_STATES:
        state_multiplier = STATE_MULTIPLIERS[state]
        population = STATE_POPULATIONS[state]
        gdp = STATE_GDP[state]
        
        for _, row in national_data.iterrows():
            year = int(row['year'])
            national_emission = row['co2']
            
            # Allocate national emissions to state
            state_total_emission = national_emission * state_multiplier
            
            # Break down by sector
            for sector, weight in SECTOR_WEIGHTS.items():
                sector_emission = state_total_emission * weight
                
                # Add some year-over-year variation (±5%)
                import random
                random.seed(hash(f"{state}{year}{sector}"))
                variation = random.uniform(0.95, 1.05)
                sector_emission *= variation
                
                state_records.append({
                    'state': state,
                    'year': year,
                    'sector': sector,
                    'co2_mt': round(sector_emission, 2),
                    'gdp_usd': gdp,
                    'population': population
                })
    
    state_df = pd.DataFrame(state_records)
    print(f"✓ Generated {len(state_df)} state-sector-year records")
    
    return state_df


def calculate_net_zero_gap(state_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate net-zero gap for each state.
    India's 2070 net-zero target means fair-share allocation per state.
    
    Args:
        state_df: State-level emissions DataFrame
    
    Returns:
        pd.DataFrame: State data with net_zero_gap column added
    """
    print("Calculating net-zero gaps...")
    
    # Get latest year data (2023)
    latest_year = state_df['year'].max()
    latest_data = state_df[state_df['year'] == latest_year].copy()
    
    # Total national emissions in latest year
    total_national = latest_data.groupby('state')['co2_mt'].sum().sum()
    
    # Total population
    total_population = sum(STATE_POPULATIONS.values())
    
    # For 2070 net-zero, assume fair-share is 0 (net-zero means balanced)
    # But for interim 2030 target, India aims to reduce emission intensity by 45%
    # We'll use a simplified approach: states should reduce by 45% by 2030
    TARGET_REDUCTION = 0.45  # 45% reduction from current levels
    
    # Calculate gap for each state
    state_gaps = []
    
    for state in INDIAN_STATES:
        state_latest = latest_data[latest_data['state'] == state]
        current_emission = state_latest['co2_mt'].sum()
        
        # Target: 45% reduction
        target_emission = current_emission * (1 - TARGET_REDUCTION)
        gap = current_emission - target_emission
        
        state_gaps.append({
            'state': state,
            'current_emission_mt': round(current_emission, 2),
            'target_emission_mt': round(target_emission, 2),
            'net_zero_gap_mt': round(gap, 2),
            'reduction_needed_pct': round(TARGET_REDUCTION * 100, 1)
        })
    
    gap_df = pd.DataFrame(state_gaps)
    
    # Merge gap back to original dataframe
    state_df = state_df.merge(
        gap_df[['state', 'net_zero_gap_mt']], 
        on='state', 
        how='left'
    )
    
    print(f"✓ Calculated net-zero gaps for {len(INDIAN_STATES)} states")
    
    return state_df, gap_df


def fetch_all_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Main function to fetch and prepare all datasets.
    
    Returns:
        Tuple of (india_national_df, state_emissions_df, gap_summary_df)
    """
    print("=" * 60)
    print("INDIA CARBON EMISSIONS TRACKER - DATA PIPELINE")
    print("=" * 60)
    
    # Step 1: Download OWID data
    india_national_df = download_owid_data()
    
    # Step 2: Generate state-level data
    state_emissions_df = generate_state_emissions(india_national_df)
    
    # Step 3: Calculate net-zero gaps
    state_emissions_df, gap_summary_df = calculate_net_zero_gap(state_emissions_df)
    
    # Step 4: Save to CSV
    state_csv_path = os.path.join("data", "state_emissions.csv")
    state_emissions_df.to_csv(state_csv_path, index=False)
    print(f"✓ Saved state emissions to {state_csv_path}")
    
    gap_csv_path = os.path.join("data", "net_zero_gaps.csv")
    gap_summary_df.to_csv(gap_csv_path, index=False)
    print(f"✓ Saved net-zero gaps to {gap_csv_path}")
    
    if not india_national_df.empty:
        national_csv_path = os.path.join("data", "india_national.csv")
        india_national_df.to_csv(national_csv_path, index=False)
        print(f"✓ Saved national data to {national_csv_path}")
    
    print("=" * 60)
    print("DATA PIPELINE COMPLETE")
    print("=" * 60)
    
    return india_national_df, state_emissions_df, gap_summary_df


if __name__ == "__main__":
    # Test the data fetcher
    india_df, state_df, gap_df = fetch_all_data()
    
    print("\n📊 DATA SAMPLE - State Emissions:")
    print(state_df.head(10))
    
    print("\n📊 DATA SAMPLE - Net-Zero Gaps:")
    print(gap_df.head())
    
    print("\n📈 STATISTICS:")
    print(f"Total records: {len(state_df)}")
    print(f"Years covered: {state_df['year'].min()} - {state_df['year'].max()}")
    print(f"States covered: {state_df['state'].nunique()}")
    print(f"Sectors: {', '.join(state_df['sector'].unique())}")
