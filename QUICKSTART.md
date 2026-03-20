# 🚀 Quick Start Guide

## For Windows Users

### Option 1: Automated Setup (Recommended)
```bash
# Double-click setup.bat or run:
setup.bat
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate data
python run_tests.py

# 3. Start the dashboard
streamlit run app.py
```

## For Mac/Linux Users

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Generate data
python3 run_tests.py

# 3. Start the dashboard
streamlit run app.py
```

## ⚙️ Optional: Enable AI Features

To use the AI Policy Assistant (EmissionsIQ):

1. Get an Anthropic API key from: https://console.anthropic.com
2. Copy `.env.example` to `.env`
3. Edit `.env` and add your API key:
   ```
   ANTHROPIC_API_KEY=your_api_key_here
   ```

**Note**: The app works without the API key, but the AI assistant will use template responses instead of Claude AI.

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt --upgrade
```

### Data files not generating
```bash
# Manually run each module:
python data_fetcher.py
python ml_model.py
```

### Streamlit won't start
```bash
# Try:
python -m streamlit run app.py

# Or check Streamlit installation:
pip install streamlit --upgrade
```

### Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

## 📂 Expected Project Structure After Setup

```
tryingit/
│
├── data/                           # Generated after running setup
│   ├── state_emissions.csv
│   ├── emissions_forecast.csv
│   ├── state_tiers.csv
│   ├── net_zero_gaps.csv
│   └── owid_co2_data.csv
│
├── app.py                          # Main Streamlit dashboard
├── data_fetcher.py                 # Data pipeline module
├── ml_model.py                     # ML forecasting module
├── ai_agent.py                     # AI agent module
├── requirements.txt
├── README.md
├── .env.example
├── setup.bat                       # Windows quick setup
└── run_tests.py                    # Test runner
```

## ✅ Verification Checklist

After running setup, verify:

- [ ] `data/` folder exists with 4-5 CSV files
- [ ] Running `python data_fetcher.py` shows "DATA PIPELINE COMPLETE"
- [ ] Running `python ml_model.py` shows tier classifications
- [ ] Running `streamlit run app.py` opens browser to localhost:8501
- [ ] Dashboard shows all 4 pages (National Overview, State Deep Dive, etc.)

## 🎯 Using the Dashboard

1. **National Overview**: Start here for India-wide statistics
2. **State Deep Dive**: Select a state to see detailed forecasts
3. **Net-Zero Gap Analyzer**: Compare all states' reduction challenges
4. **AI Policy Assistant**: Ask questions in natural language

## 💡 Demo Questions for AI Assistant

Try these in the AI chat:
- "Which states are most critical?"
- "Compare Maharashtra and Gujarat"
- "What's Tamil Nadu's net-zero gap?"
- "Show me top polluting sectors for Punjab"
- "Generate a policy brief for Odisha"

---

**Need Help?** Check README.md for full documentation.
