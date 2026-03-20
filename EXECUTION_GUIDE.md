# India Carbon Emissions Tracker - Complete Execution Guide

## Quick Start (3 Options)

### Option 1: Run Batch File (Recommended for Windows)
1. Open File Explorer
2. Navigate to: `c:\Users\KIIT0001\OneDrive\Desktop\tryingit`
3. Double-click: `RUN_COMPLETE_PIPELINE.bat`
4. The script will automatically:
   - Verify Python installation
   - Install dependencies
   - Run the data pipeline
   - Start Streamlit dashboard

### Option 2: Run Python Script
Open Command Prompt (Win + R → cmd → Enter) and type:
```
cd c:\Users\KIIT0001\OneDrive\Desktop\tryingit
python COMPLETE_EXECUTION.py
```

### Option 3: Run Manual Steps
Open Command Prompt and run these commands one by one:
```
cd c:\Users\KIIT0001\OneDrive\Desktop\tryingit
mkdir data
python data_fetcher.py
python ml_model.py
streamlit run app.py
```

---

## What Each Script Does

### 1. data_fetcher.py
**Purpose**: Downloads OWID CO2 emissions data and generates state-level emissions

**Output Files Created**:
- `data/owid_co2_data.csv` - Global CO2 emissions from Our World in Data
- `data/state_emissions.csv` - India's 15 major states emissions by sector
- `data/net_zero_gaps.csv` - Gap analysis for each state's net-zero targets

**Data Generated**:
- 15 Indian states: Maharashtra, Uttar Pradesh, Gujarat, Rajasthan, Madhya Pradesh, Tamil Nadu, West Bengal, Karnataka, Andhra Pradesh, Odisha, Punjab, Haryana, Bihar, Jharkhand, Chhattisgarh
- 5 Sectors: Energy, Industry, Transport, Agriculture, Waste
- Historical data with projections

### 2. ml_model.py
**Purpose**: Trains machine learning models and generates forecasts

**Output Files Created**:
- `data/emissions_forecast.csv` - Emissions forecasts for each state through 2035
- `data/state_tiers.csv` - Classification of states into performance tiers

**Models Trained**:
- Linear Regression models for each state
- Forecasting emissions trends for the next 10+ years
- State tier classification (On Track / Needs Attention / Critical)

**Forecast Data**:
- Years: 2020-2035 (with 2025-2035 as forecast period)
- 465 rows of forecast data (31 years × 15 states)

### 3. app.py (Streamlit Dashboard)
**Purpose**: Interactive visualization and analysis dashboard

**Features**:
- Dashboard maps showing state-level emissions
- Time-series visualizations of emissions trends
- Forecasts and targets comparison
- AI-powered analysis through EmissionsIQ agent
- State comparison tools
- Export functionality

**Access**:
- URL: http://localhost:8501
- Keep running while exploring

---

## Expected CSV Files Output

After successful execution, you'll see these files in `data/` directory:

| File | Size | Rows | Description |
|------|------|------|-------------|
| state_emissions.csv | ~100-150 KB | ~1,425 | State-level emissions by sector and year |
| net_zero_gaps.csv | ~2-3 KB | 15 | Net-zero reduction targets for each state |
| emissions_forecast.csv | ~30-50 KB | ~465 | Forecasts for 2020-2035 by state |
| state_tiers.csv | ~1-2 KB | 15 | State classification into performance tiers |

---

## Troubleshooting

### Python Not Found
**Error**: "Python is not installed or not in PATH"
**Solution**:
1. Install Python from https://www.python.org/
2. Make sure to check "Add Python to PATH" during installation
3. Restart Command Prompt and try again

### Dependencies Not Installed
**Error**: "ModuleNotFoundError: No module named..."
**Solution**: Run in Command Prompt:
```
pip install -r requirements.txt
```

### Internet Connection Issues
**Error**: "Connection error downloading OWID data"
**Solution**:
- Check your internet connection
- The script tries to download from GitHub. If firewall blocks it, disable temporarily
- Re-run the script after connection is restored

### Permission Denied
**Error**: "Permission denied" when creating data directory
**Solution**:
1. Run Command Prompt as Administrator
2. Try again

### Streamlit Port Already in Use
**Error**: "Port 8501 already in use"
**Solution**: Use a different port:
```
streamlit run app.py --server.port 8502
```

---

## File Structure After Execution

```
c:\Users\KIIT0001\OneDrive\Desktop\tryingit\
├── data/
│   ├── state_emissions.csv
│   ├── emissions_forecast.csv
│   ├── state_tiers.csv
│   ├── net_zero_gaps.csv
│   └── owid_co2_data.csv (if downloaded)
├── data_fetcher.py
├── ml_model.py
├── app.py
├── ai_agent.py
├── requirements.txt
├── EXECUTE_ALL.py
├── COMPLETE_EXECUTION.py
├── RUN_COMPLETE_PIPELINE.bat
└── [other files...]
```

---

## What to Expect During Execution

### data_fetcher.py execution (2-5 minutes):
- ✓ Downloads OWID CO2 dataset (~30 MB)
- ✓ Processes data for India
- ✓ Generates state-level emissions
- ✓ Creates net_zero_gaps.csv
- ✓ Outputs: 3 CSV files

### ml_model.py execution (1-3 minutes):
- ✓ Trains 15 Linear Regression models
- ✓ Generates forecasts through 2035
- ✓ Classifies states into tiers
- ✓ Outputs: 2 CSV files

### Dashboard startup (30-60 seconds):
- ✓ Loads Streamlit
- ✓ Reads CSV files
- ✓ Renders visualizations
- ✓ Starts local server on port 8501

---

## Using the Streamlit Dashboard

Once the dashboard starts:

1. **Navigate to**: http://localhost:8501
2. **Main Tabs**:
   - **Dashboard**: Overview of India's emissions
   - **State Analysis**: Individual state data and trends
   - **Forecasts**: Future emissions projections
   - **AI Assistant**: Ask questions about emissions data

3. **Interactive Features**:
   - Click on states in the map
   - Use filters and date ranges
   - View state-by-state comparisons
   - Export data as CSV

4. **To Stop Dashboard**: Press Ctrl+C in Command Prompt

---

## Required Dependencies

The project requires:
- Python 3.8+
- pandas>=2.0.0
- numpy>=1.24.0
- requests>=2.31.0
- scikit-learn>=1.3.0
- streamlit>=1.40.0
- plotly>=5.17.0
- folium>=0.15.0

All will be automatically installed when you run the scripts.

---

## Project Summary

This is the **India Carbon Emissions Tracker** - an AI-powered system for:
- Tracking India's state-level CO2 emissions
- Analyzing emissions by sector
- Forecasting future trends
- Supporting climate policy decisions
- Interactive data visualization

**Key Features**:
- Historical emissions data (2010-2023)
- 15 major Indian states covered
- 5 emission sectors analyzed
- Machine learning forecasts (2024-2035)
- Interactive Streamlit dashboard
- AI-powered analysis assistant

---

## Getting Help

For more information, see:
- README.md - Project overview
- ARCHITECTURE.md - Technical details
- QUICKSTART.md - Quick start guide
- START_HERE.txt - Initial setup instructions

---

## Next Steps After Execution

1. **Verify Data**: Check that CSV files were created in `data/` directory
2. **Launch Dashboard**: Start Streamlit with `streamlit run app.py`
3. **Explore Data**: Use the interactive dashboard to explore emissions
4. **Ask Questions**: Use the AI assistant tab for data insights
5. **Export Results**: Download CSV files for further analysis

Enjoy exploring India's carbon emissions data! 🌍📊
