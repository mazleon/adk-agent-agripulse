# Dashboard Agent

The **Dashboard Agent** is a specialized AI agent for AgriPulse that provides intelligent database querying and analytics capabilities through natural language interactions.

## Overview

The Dashboard Agent converts natural language questions into SQL queries, executes them safely against the Snowflake database, and presents results in a clear, actionable format.

## Features

- 🔍 **Natural Language to SQL**: Convert plain English questions to SQL queries
- 📊 **Data Exploration**: Discover available tables, columns, and data
- 🔒 **Read-Only Security**: Only SELECT queries allowed, no data modification
- 📈 **Analytics**: Get insights, summaries, and statistics
- 🎯 **Intelligent Inference**: Automatically determines which table to query
- ✨ **User-Friendly**: Clear, structured data presentation

## Quick Start

### Run the Agent

```bash
# Start the dashboard agent
uv run adk run adk_app/agents/dashboard_agent
```

### Example Queries

**Explore the database**:
```
"What tables are available?"
"Show me the database schema"
"Give me a summary of the yield forecasts table"
```

**Query yield forecasts**:
```
"Show me yield forecasts for Dhaka district"
"What are the predicted yields for Aman crop in 2025?"
"List all forecasts with yield above 3 tons per hectare"
"Show me the top 5 highest predicted yields"
```

**Query crop practices**:
```
"Show me rice varieties for Aman season"
"What varieties have yield above 6 tons per hectare?"
"List varieties resistant to blast disease"
```

## Available Tools

### 1. get_database_schema()
Get information about available tables and their structure.

**Use when**:
- User asks "What tables are available?"
- User wants to understand the database structure
- Starting data exploration

### 2. generate_and_execute_query(user_query, table_name, limit)
Convert natural language to SQL and execute the query.

**Parameters**:
- `user_query` (required): Natural language question
- `table_name` (optional): Specific table to query
- `limit` (optional): Max records (default: 50, max: 100)

**Use when**:
- User asks a specific data question
- User wants to see database records
- User needs filtered or sorted data

### 3. get_table_summary(table_name)
Get statistical summary of a table.

**Parameters**:
- `table_name` (required): Table to summarize

**Use when**:
- User asks for table statistics
- User wants data coverage information
- User asks "How much data is there?"

## Database Tables

### STG_ML_YIELD_FORECASTS
ML-based yield forecasts for crops and districts.

**Key Columns**:
- `DISTRICT_NAME`: District/location
- `CROP_TYPE`: Crop variety
- `FORECAST_YEAR`: Year of forecast
- `PREDICTED_YIELD`: ML-predicted yield (tons/hectare)
- `CONFIDENCE_LOWER/UPPER`: Confidence bounds
- `MODEL_USED`: ML model name
- `PREDICTION_DATE`: When prediction was made

### VW_STG_CROP_PRACTICE
Crop cultivation best practices and variety information.

**Key Columns**:
- `CROP_TYPE`: Crop type (rice, wheat, maize)
- `VARIETY`: Specific variety name
- `GRAIN_YIELD_FROM_T_HA/TO_T_HA`: Expected yield range
- `SEASON`: Growing season
- `RESISTANT_TO`: Disease/pest resistance
- `SUITABLE_FOR`: Suitable conditions

## Security

✅ **Read-Only Operations**
- Only SELECT queries allowed
- No INSERT, UPDATE, DELETE, or DDL
- Automatic query validation

✅ **SQL Injection Prevention**
- Parameterized queries
- Input sanitization
- Query pattern validation

✅ **Resource Protection**
- Result limits (max 100 records)
- Connection pooling
- Automatic cleanup

## Architecture

```
dashboard_agent/
├── agent.py          # Agent definition
├── persona.md        # Agent instructions and behavior
└── README.md         # This file

tools/
├── dashboard_tools.py              # Core tools implementation
└── toolsets/
    └── dashboard_toolset.py        # Tool wrapper
```

## Testing

Run the test suite:

```bash
# Run dashboard agent tests
uv run python tests/test_dashboard_agent.py
```

Tests cover:
- Schema retrieval
- Table name inference
- Query validation
- SQL generation
- Table summaries
- Query execution

## Example Interactions

### Data Exploration
```
User: What kind of data can I query?

Agent: Let me show you what's available in our agricultural database.

📋 Available Database Tables

1. STG_ML_YIELD_FORECASTS - ML Yield Predictions
   Contains 645 records of ML-based yield forecasts
   - Districts: Dhaka, Bagerhat, Chittagong, and more
   - Crops: Aman, Aus, Boro varieties
   - Years: 2024-2028

2. VW_STG_CROP_PRACTICE - Crop Cultivation Practices
   Contains variety information and best practices
   - Crop types: Rice, wheat, maize
   - Seasons: Aman, Boro, Aus, Rabi, Kharif

What would you like to explore first?
```

### Specific Query
```
User: Show me yield forecasts for Dhaka in 2025

Agent: Let me retrieve the yield forecasts for Dhaka district in 2025.

📊 Yield Forecasts for Dhaka - 2025 (3 records found)

1. High Yielding Variety (HYV) Aman
   - Predicted Yield: 2.85 tons/hectare
   - Confidence Range: 2.60 - 3.10 tons/hectare
   - Model: Ensemble

2. Aman (Broadcast)
   - Predicted Yield: 2.45 tons/hectare
   - Confidence Range: 2.20 - 2.70 tons/hectare
   - Model: Ensemble

3. Local Transplanted (L.T) Aman
   - Predicted Yield: 2.30 tons/hectare
   - Confidence Range: 2.05 - 2.55 tons/hectare
   - Model: Ensemble

Key Insights:
- HYV Aman shows the highest predicted yield
- All forecasts use the Ensemble ML model
- Confidence intervals indicate reliable predictions

Would you like to see forecasts for other districts?
```

## Integration

The dashboard agent can be integrated with other agents in a multi-agent system:

```python
from adk_app.agents.dashboard_agent.agent import dashboard_agent
from adk_app.agents.yield_agent.agent import yield_agent
from adk_app.agents.weather.agent import weather_agent

# Use in coordinator
coordinator = Agent(
    name="coordinator",
    agents=[weather_agent, yield_agent, dashboard_agent]
)
```

## Limitations

- **Read-only**: Cannot modify data (by design)
- **Query complexity**: Simple pattern-based SQL generation
- **Result limits**: Maximum 100 records per query
- **Table coverage**: Only configured tables accessible

## Future Enhancements

- Advanced SQL generation using LLM
- Data visualization capabilities
- Query caching for performance
- Export functionality (CSV, JSON)
- Saved query templates
- Real-time data streaming

## Support

For issues or questions:
1. Check the comprehensive documentation in `docs/DASHBOARD_AGENT_COMPLETE.md`
2. Review test cases in `tests/test_dashboard_agent.py`
3. Examine the persona in `persona.md` for behavior details

## License

Part of the AgriPulse AI project.
