# 🚀 Dashboard Agent - Quick Start Guide

## What is the Dashboard Agent?

The Dashboard Agent is an AI-powered database assistant that converts your natural language questions into SQL queries and retrieves data from the Snowflake agricultural database.

## Quick Start (3 Steps)

### 1. Run the Agent
```bash
uv run adk run adk_app/agents/dashboard_agent
```

### 2. Ask Questions
Start with:
```
"What tables are available?"
```

### 3. Explore Data
Try these queries:
```
"Show me yield forecasts for Dhaka district"
"What rice varieties are best for Aman season?"
"List all forecasts with yield above 3 tons per hectare"
```

## Common Queries

### 📊 Explore the Database
```
"What data is available?"
"Show me the database schema"
"Give me a summary of the yield forecasts table"
"How many records are in the database?"
```

### 🌾 Yield Forecasts
```
"Show yield forecasts for Dhaka in 2025"
"What are the top 5 highest predicted yields?"
"List all Aman crop forecasts"
"Show me forecasts with confidence above 90%"
"Compare yields across districts"
```

### 🌱 Crop Practices
```
"Show rice varieties for Aman season"
"What varieties yield above 6 tons per hectare?"
"List varieties resistant to blast disease"
"Show varieties released after 2000"
"What's the best variety for rainfed conditions?"
```

### 📈 Analytics
```
"What's the average yield by district?"
"Show yield trends over years"
"Which district has the highest yields?"
"Compare Aman and Boro varieties"
```

## Available Tables

### STG_ML_YIELD_FORECASTS
ML-based yield predictions (645 records)
- **Districts**: Dhaka, Bagerhat, Chittagong, Mymensingh, etc.
- **Crops**: Aman, Aus, Boro varieties
- **Years**: 2024-2028
- **Data**: Predicted yields, confidence intervals, ML models

### VW_STG_CROP_PRACTICE
Crop cultivation best practices
- **Crops**: Rice, wheat, maize
- **Seasons**: Aman, Boro, Aus, Rabi, Kharif
- **Data**: Varieties, yield potential, disease resistance

## Tips for Better Results

### ✅ Do This
- Be specific: "Show Dhaka forecasts for 2025"
- Use proper names: "Aman", "Dhaka", "rice"
- Ask for summaries: "Give me a summary of..."
- Request top results: "Show top 5..."

### ❌ Avoid This
- Too vague: "Show me data"
- Misspellings: "Daka" instead of "Dhaka"
- Complex joins: Agent handles simple queries best
- Data modification: Read-only access only

## Example Session

```
You: What tables are available?

Agent: 📋 Available Database Tables

1. STG_ML_YIELD_FORECASTS - ML Yield Predictions
   Contains 645 records of ML-based yield forecasts
   
2. VW_STG_CROP_PRACTICE - Crop Cultivation Practices
   Contains variety information and best practices

What would you like to explore?

---

You: Show me yield forecasts for Dhaka in 2025

Agent: 📊 Yield Forecasts for Dhaka - 2025 (3 records found)

1. High Yielding Variety (HYV) Aman
   - Predicted Yield: 2.85 tons/hectare
   - Confidence Range: 2.60 - 3.10 tons/hectare

2. Aman (Broadcast)
   - Predicted Yield: 2.45 tons/hectare
   - Confidence Range: 2.20 - 2.70 tons/hectare

3. Local Transplanted (L.T) Aman
   - Predicted Yield: 2.30 tons/hectare
   - Confidence Range: 2.05 - 2.55 tons/hectare

Key Insights:
- HYV Aman shows the highest predicted yield
- All forecasts use the Ensemble ML model

Would you like to see forecasts for other districts?
```

## Troubleshooting

### No Results Found?
- Check spelling of district/crop names
- Try broader search terms
- Ask "What districts are available?"

### Query Too Complex?
- Break it into simpler questions
- Ask for schema first
- Use specific filters

### Need Help?
- Ask "What can I query?"
- Request "Show me example queries"
- Check the schema with "What tables exist?"

## Testing

Run the test suite to verify everything works:
```bash
uv run python tests/test_dashboard_agent.py
```

## More Information

- **Full Documentation**: `docs/DASHBOARD_AGENT_COMPLETE.md`
- **Agent README**: `adk_app/agents/dashboard_agent/README.md`
- **Implementation Details**: `DASHBOARD_AGENT_IMPLEMENTATION.md`

## Security Note

🔒 The Dashboard Agent is **read-only**. It can only retrieve data, never modify it. All queries are validated for safety.

---

**Ready to explore your agricultural data?**

```bash
uv run adk run adk_app/agents/dashboard_agent
```

Then ask: **"What data is available?"**
