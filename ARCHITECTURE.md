# 📐 Project Architecture - India Carbon Emissions Tracker

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                          │
│                    (Streamlit Dashboard)                          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   National   │  │    State     │  │  Net-Zero    │          │
│  │   Overview   │  │  Deep Dive   │  │    Gap       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌─────────────────────────────────────────────────┐            │
│  │      AI Policy Assistant (EmissionsIQ)          │            │
│  │      Natural Language Interface                 │            │
│  └─────────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                             │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │data_fetcher.py│  │  ml_model.py │  │ ai_agent.py  │          │
│  │              │  │              │  │              │          │
│  │ • OWID API   │  │ • sklearn    │  │ • Claude API │          │
│  │ • State      │  │ • Forecasting│  │ • Tool       │          │
│  │   Generation │  │ • Tiers      │  │   Calling    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        DATA LAYER                                 │
│                                                                   │
│  ┌──────────────────────────────────────────────────┐            │
│  │              data/ directory                     │            │
│  │                                                  │            │
│  │  • state_emissions.csv      (raw data)          │            │
│  │  • emissions_forecast.csv   (ML output)         │            │
│  │  • state_tiers.csv          (classifications)   │            │
│  │  • net_zero_gaps.csv        (gap analysis)      │            │
│  │  • owid_co2_data.csv        (cached OWID)       │            │
│  └──────────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Data Flow

```
1. DATA INGESTION
   ↓
   data_fetcher.py
   • Downloads OWID CO2 dataset (national India data)
   • Generates state-level estimates (15 states)
   • Applies sector weights (Energy, Industry, Transport, etc.)
   • Calculates net-zero gaps
   ↓
   Output: state_emissions.csv, net_zero_gaps.csv

2. ML FORECASTING
   ↓
   ml_model.py
   • Loads state emissions
   • Trains Linear Regression per state
   • Forecasts 2024-2035
   • Classifies tiers (On Track / Needs Attention / Critical)
   ↓
   Output: emissions_forecast.csv, state_tiers.csv

3. AI ENHANCEMENT
   ↓
   ai_agent.py
   • Loads all CSV data
   • Provides 5 tools for analysis
   • Integrates Claude Haiku for natural language
   • Generates policy briefs
   ↓
   Output: Real-time AI responses

4. VISUALIZATION
   ↓
   app.py
   • Reads all data files
   • Renders interactive Plotly charts
   • Provides 4-page dashboard
   • Enables AI chat interface
   ↓
   Output: Streamlit web app (localhost:8501)
```

## 🧩 Module Breakdown

### 1. data_fetcher.py (288 lines)
**Purpose**: Data acquisition and preprocessing

**Key Functions:**
- `download_owid_data()` - Fetches global CO2 dataset
- `generate_state_emissions()` - Creates state-level estimates
- `calculate_net_zero_gap()` - Computes reduction targets
- `fetch_all_data()` - Main pipeline orchestrator

**Inputs**: 
- OWID CO2 CSV (online)
- Hardcoded state parameters (multipliers, population, GDP)

**Outputs**:
- `state_emissions.csv` (1425 rows: 15 states × 19 years × 5 sectors)
- `net_zero_gaps.csv` (15 rows: 1 per state)

### 2. ml_model.py (282 lines)
**Purpose**: Emission forecasting and tier classification

**Key Functions:**
- `train_forecast_model()` - Linear regression per state
- `forecast_emissions()` - Predict 2024-2035
- `calculate_growth_rate()` - YoY emission change
- `classify_state_tier()` - Categorize by growth rate

**ML Model:**
- Algorithm: Linear Regression (sklearn)
- Features: Year
- Target: CO2 emissions (MT)
- Training: Per-state models (15 total)

**Outputs**:
- `emissions_forecast.csv` (465 rows: 15 states × 31 years)
- `state_tiers.csv` (15 rows with tier classifications)

### 3. ai_agent.py (525 lines)
**Purpose**: AI-powered policy analysis

**Key Classes:**
- `EmissionsIQAgent` - Main agent orchestrator

**AI Tools** (5 total):
1. `get_state_emissions()` - Trend analysis
2. `get_net_zero_gap()` - Gap calculation
3. `compare_states()` - Side-by-side comparison
4. `get_top_polluting_sectors()` - Sector breakdown
5. `generate_policy_brief()` - AI-generated brief

**Claude Integration:**
- Model: claude-haiku-20241022 (fast, cost-effective)
- System Prompt: Policy analyst persona
- Max Tokens: 500 (concise responses)
- Fallback: Template responses if no API key

### 4. app.py (513 lines)
**Purpose**: Interactive web dashboard

**Pages** (4 total):
1. **National Overview** - India-wide KPIs + sector trends
2. **State Deep Dive** - Per-state forecast + gap analysis
3. **Net-Zero Gap Analyzer** - Ranking table + gap chart
4. **AI Policy Assistant** - Chat interface with EmissionsIQ

**Visualization:**
- Plotly charts (line, bar, pie, area)
- Folium map (placeholder for choropleth)
- Custom CSS (dark theme with green accents)

## 🔧 Technology Choices - Rationale

| Tech | Why? |
|------|------|
| **Streamlit** | Fastest prototyping for data apps; single-file deployment |
| **Plotly** | Interactive charts; better than matplotlib for dashboards |
| **scikit-learn** | Industry standard for ML; simple API for linear regression |
| **Claude Haiku** | Cost-effective AI; fast responses; good for structured tasks |
| **pandas** | De facto standard for data manipulation in Python |
| **OWID Dataset** | Open access; authoritative; regularly updated |

## 📈 Scalability Considerations

### Current Limitations
- **Static Data**: Data must be regenerated manually
- **Simple ML**: Linear regression may not capture complex trends
- **State Estimates**: Generated, not ground-truth measurements
- **No Caching**: Dashboard reloads data on every page change

### Production Enhancements
1. **Data Pipeline**
   - Automated daily/weekly data refresh
   - Integration with India's National Emissions Inventory
   - Real-time API connections

2. **ML Improvements**
   - LSTM/GRU for time series
   - Prophet for seasonality
   - Ensemble methods for better accuracy
   - Uncertainty quantification

3. **AI Enhancements**
   - Function calling (Claude's native tool use)
   - Multi-turn conversations with memory
   - RAG (Retrieval-Augmented Generation) for policy documents
   - Fine-tuning on India-specific climate data

4. **Infrastructure**
   - PostgreSQL for data storage
   - Redis for caching
   - Docker containerization
   - Cloud deployment (AWS/GCP/Azure)

## 🎯 MoSPI Integration Pathways

### How This Could Integrate with MoSPI Systems

1. **Data Integration**
   - Connect to MoSPI's statistical databases
   - Import state-level energy consumption data
   - Link with industrial production statistics

2. **API Layer**
   - Expose emission forecasts via REST API
   - Webhook notifications for tier changes
   - Export reports to PDF/Excel

3. **Dashboard Embedding**
   - iframe integration into existing portals
   - Single Sign-On (SSO) with government systems
   - Role-based access control

4. **Reporting Pipeline**
   - Automated monthly reports to policymakers
   - Quarterly briefings with AI-generated insights
   - Annual progress tracking for net-zero targets

## 🔒 Security Considerations

- **API Keys**: Never commit to git; use environment variables
- **Data Privacy**: No PII collected; only aggregate statistics
- **Input Validation**: Sanitize user queries before AI processing
- **Rate Limiting**: Implement for production to prevent abuse

## 📊 Performance Metrics

**Data Pipeline:**
- OWID download: ~5-10 seconds
- State generation: <1 second
- ML training (15 models): ~2 seconds
- Total initialization: ~15 seconds

**Dashboard:**
- Initial load: ~2-3 seconds
- Page navigation: <1 second
- AI query response: 2-5 seconds (depends on Claude API)

## 🧪 Testing Strategy

Current:
- `run_tests.py` - End-to-end pipeline test
- Manual verification of outputs

Production:
- Unit tests for each module (pytest)
- Integration tests for data flow
- UI tests (Selenium/Playwright)
- Load tests for concurrent users

---

**Architecture Version**: 1.0  
**Last Updated**: Built for MoSPI Portfolio Project  
**Maintainability**: Modular design allows easy updates to any layer
