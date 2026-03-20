# 🌍 India Carbon Emissions Tracker

**EmissionsIQ — AI-Powered Carbon Analytics for Policy Makers**

A full-stack AI-powered dashboard analyzing India's state-wise carbon emissions, forecasting trends through 2035, and providing intelligent policy recommendations to support India's net-zero 2070 commitment.

---

## 🎯 Why This Matters for MoSPI

The Ministry of Statistics & Programme Implementation (MoSPI) plays a critical role in India's climate action through:
- **Data-Driven Policymaking**: Accurate emission tracking enables evidence-based climate policies
- **State-Level Monitoring**: Granular data helps identify high-emission states requiring intervention
- **Net-Zero Progress Tracking**: Monitor India's trajectory toward the 2070 net-zero target

This project demonstrates how AI can augment statistical analysis to provide actionable insights for climate governance.

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | Python 3.10+ | Data processing & ML |
| **Web Framework** | Streamlit | Interactive dashboard |
| **ML/Forecasting** | scikit-learn | Linear regression for emission trends |
| **AI Agent** | Anthropic Claude (Haiku) | Intelligent policy analyst |
| **Data Processing** | pandas, NumPy | Data manipulation |
| **Visualization** | Plotly, Folium | Interactive charts & maps |
| **Data Sources** | OWID CO2 Dataset | Global carbon emission statistics |

---

## 🚀 How to Run

### Prerequisites
- Python 3.10 or higher
- Anthropic API key (get from [console.anthropic.com](https://console.anthropic.com))

### Installation

1. **Clone or download this project**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key (optional, for AI features)**
   ```bash
   # Create .env file
   cp .env.example .env
   
   # Edit .env and add your Anthropic API key
   # ANTHROPIC_API_KEY=your_key_here
   ```

4. **Generate data**
   ```bash
   python data_fetcher.py
   python ml_model.py
   ```

5. **Run the dashboard**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   Navigate to `http://localhost:8501`

---

## 📊 Features

### 1. 🌍 National Overview
- **India Heatmap**: Visualize state-wise emissions
- **KPI Dashboard**: Total emissions, YoY change, tier classification counts
- **Sector Analysis**: Stacked area chart showing emission sources over time

### 2. 🔍 State Deep Dive
- **Emission Trajectory**: Historical data (2005-2023) + ML forecasts (2024-2035)
- **Tier Classification**: 
  - 🟢 **On Track** (< 2% growth)
  - 🟡 **Needs Attention** (2-5% growth)
  - 🔴 **Critical** (> 5% growth)
- **Sector Breakdown**: Pie chart showing Energy, Industry, Transport, Agriculture, Waste
- **Net-Zero Gap**: Progress bar showing reduction needed for 2030 targets

### 3. 🎯 Net-Zero Gap Analyzer
- **Ranking Chart**: States ordered by emission reduction challenge
- **Detailed Table**: Current vs target emissions, gap in MT, tier classification
- **Policy Context**: India's 2070 net-zero and 2030 intensity reduction commitments

### 4. 🤖 AI Policy Assistant (EmissionsIQ)
Powered by Claude Haiku, the AI agent can:
- Analyze state emission trends
- Calculate net-zero gaps
- Compare states side-by-side
- Identify top polluting sectors
- Generate 3-point policy briefs

**Example queries:**
- "Which states are most critical?"
- "Compare Maharashtra and Gujarat"
- "What's Odisha's net-zero gap?"
- "Generate a policy brief for Punjab"

---

## 📁 Project Structure

```
india-carbon-tracker/
│
├── app.py                  # Streamlit dashboard (main app)
├── data_fetcher.py         # Download OWID data + generate state estimates
├── ml_model.py             # Linear regression forecasting + tier classification
├── ai_agent.py             # Claude-powered AI policy analyst
│
├── data/
│   ├── state_emissions.csv        # State-level emission data (2005-2023)
│   ├── emissions_forecast.csv     # Historical + forecasted data (2005-2035)
│   ├── state_tiers.csv            # Tier classifications per state
│   ├── net_zero_gaps.csv          # Net-zero gap analysis
│   └── owid_co2_data.csv          # OWID national India data (cached)
│
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```

---

## 📸 Screenshots

> **Note**: Add screenshots after deploying the app

1. **National Overview Dashboard**
   - India heatmap with emission intensity
   - Sector-wise breakdown chart
   - KPI cards showing national statistics

2. **State Deep Dive**
   - Maharashtra emission trajectory (historical + forecast)
   - Tier badge and growth metrics
   - Sector breakdown pie chart

3. **Net-Zero Gap Analyzer**
   - Bar chart ranking states by gap
   - Detailed data table with tier coloring

4. **AI Assistant Chat**
   - EmissionsIQ answering policy questions
   - Interactive chat interface

---

## 📚 Data Sources

1. **Our World in Data (OWID) CO2 Dataset**
   - URL: https://github.com/owid/co2-data
   - License: Creative Commons BY
   - Coverage: Global emissions data (1750-2023)
   - India national data used as baseline

2. **State-Level Estimates**
   - Generated using proportional allocation from national totals
   - Sector weights based on India's emission profile:
     - Energy: 45%
     - Industry: 25%
     - Transport: 15%
     - Agriculture: 10%
     - Waste: 5%
   - State multipliers derived from industrial activity + population data
   - Sources: CEEW reports, MoEFCC publications (publicly available estimates)

3. **Net-Zero Targets**
   - India's 2070 net-zero commitment (COP26, Glasgow)
   - 2030 interim target: 45% reduction in emission intensity
   - State targets calculated using fair-share allocation

---

## 🔬 ML Methodology

### Forecasting Model
- **Algorithm**: Linear Regression (scikit-learn)
- **Features**: Year (time series)
- **Target**: CO2 emissions (MT)
- **Training Data**: Historical emissions 2005-2023
- **Forecast Horizon**: 2024-2035
- **Validation**: Models trained per-state to capture regional trends

### Tier Classification
States classified based on average annual emission growth rate:
- **On Track**: < 2% annual growth
- **Needs Attention**: 2-5% annual growth
- **Critical**: > 5% annual growth

---

## 🤖 AI Agent Architecture

### EmissionsIQ Tools
1. `get_state_emissions(state_name)` — Trend + tier classification
2. `get_net_zero_gap(state_name)` — Gap analysis
3. `compare_states(state1, state2)` — Side-by-side comparison
4. `get_top_polluting_sectors(state_name)` — Sector breakdown
5. `generate_policy_brief(state_name)` — AI-generated 3-point brief

### System Prompt
```
You are EmissionsIQ, an AI policy analyst for India's carbon statistics.
You help government officials and researchers understand state-wise 
emission trends, net-zero gaps, and policy priorities.
Always cite data. Be concise and actionable.
```

---

## 🎓 For MoSPI Reviewers

**Key Highlights for Interview:**

1. **Real-World Data Integration**: Uses OWID's authoritative CO2 dataset
2. **ML Forecasting**: Predictive analytics for policy planning
3. **AI Augmentation**: Claude API demonstrates modern AI integration
4. **Scalable Architecture**: Modular design (data → ML → UI)
5. **Policy Focus**: Not just analytics, but actionable recommendations

**Discussion Points:**
- How would you extend this to include sector-specific policies?
- What additional data sources would improve accuracy?
- How can this integrate with existing MoSPI data infrastructure?

---

## 🚧 Future Enhancements

- [ ] Real geospatial map using India shapefile
- [ ] Advanced ML models (LSTM, Prophet) for better forecasting
- [ ] Integration with India's National Emissions Inventory
- [ ] Multi-scenario forecasting (business-as-usual vs policy intervention)
- [ ] Export reports as PDF for policy briefs
- [ ] Real-time data updates via APIs

---

## 📝 License

This project is created for educational and portfolio purposes as part of a MoSPI internship application.

Data sources:
- OWID CO2 Dataset: Creative Commons BY 4.0
- State estimates: Based on publicly available government reports

---

## 👨‍💻 Author

Created as a demonstration of full-stack AI capabilities for climate policy analytics.

**Technologies Demonstrated:**
✅ Python Backend Development  
✅ Machine Learning (scikit-learn)  
✅ AI Integration (Anthropic Claude)  
✅ Data Visualization (Plotly)  
✅ Web Dashboard (Streamlit)  
✅ Statistical Analysis (pandas)  

---

## 🙏 Acknowledgments

- **Our World in Data** for open-access emission datasets
- **Anthropic** for Claude API access
- **MoSPI** for inspiring this climate analytics project
- **CEEW & MoEFCC** for publicly available India emission research

---

**Built with 💚 for India's Climate Goals**

*Supporting the journey to Net-Zero by 2070* 🌱
