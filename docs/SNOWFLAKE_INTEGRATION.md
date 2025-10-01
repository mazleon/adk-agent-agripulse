# Snowflake Database Integration Guide

## Overview

AgriPulse AI now integrates with Snowflake database to provide real ML-powered yield forecasts. This integration allows the yield prediction agent to access actual forecast data from your Snowflake ML database.

## Architecture

```
Yield Agent
    ↓
YieldToolset (combines both sources)
    ├─→ Snowflake Tools (Primary)
    │   ├─ get_yield_forecast_from_db
    │   ├─ get_latest_yield_forecasts
    │   └─ get_yield_forecast_summary
    └─→ Calculated Tools (Fallback)
        ├─ predict_yield
        └─ analyze_soil_conditions
    ↓
SnowflakeConnectionManager
    ↓
Snowflake Database
    └─ DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS
```

## Setup

### 1. Database Credentials

The private key file `database_connection_config.pem` is already in your project root. This file contains the RSA private key for authenticating with Snowflake.

### 2. Environment Variables

Add these to your `.env` file (already configured with defaults):

```bash
SNOWFLAKE_USER=ML_SRV_USER
SNOWFLAKE_ACCOUNT=ae18467.eu-west-2.aws
SNOWFLAKE_ROLE=ML_SRV_RO_ROLE
SNOWFLAKE_WAREHOUSE=DEV_DATA_ML_WH
SNOWFLAKE_DATABASE=DEV_DATA_ML_DB
SNOWFLAKE_SCHEMA=DATA_ML_SCHEMA
```

### 3. Dependencies

Snowflake connector is already installed:
```bash
snowflake-connector-python==3.17.4
```

## Components

### 1. Connection Manager (`adk_app/core/database.py`)

**SnowflakeConnectionManager** - Handles all database operations:
- Connection lifecycle management
- Automatic connection pooling
- Context manager support
- Error handling and logging
- Automatic cleanup on session end

**Key Features:**
- ✅ Singleton pattern for connection reuse
- ✅ Context manager for safe connection handling
- ✅ Automatic connection cleanup
- ✅ Query execution with parameter binding
- ✅ Connection testing utilities

### 2. Snowflake Tools (`adk_app/tools/snowflake_yield_tools.py`)

**Available Tools:**

#### `get_yield_forecast_from_db()`
Fetch yield forecasts with optional filters:
```python
get_yield_forecast_from_db(
    crop_type="wheat",      # Optional
    location="London",      # Optional
    forecast_date="2025-10-01",  # Optional
    limit=10                # Default: 10
)
```

**Returns:**
```json
{
    "status": "success",
    "count": 5,
    "forecasts": [
        {
            "crop_type": "wheat",
            "location": "London",
            "predicted_yield": 4.2,
            "forecast_date": "2025-09-28",
            ...
        }
    ],
    "source": "Snowflake Database"
}
```

#### `get_latest_yield_forecasts()`
Get most recent forecasts:
```python
get_latest_yield_forecasts(limit=5)
```

#### `get_yield_forecast_summary()`
Get aggregated statistics:
```python
get_yield_forecast_summary(
    crop_type="wheat",  # Optional
    location="London"   # Optional
)
```

**Returns:**
```json
{
    "status": "success",
    "summary": [
        {
            "crop_type": "wheat",
            "location": "London",
            "forecast_count": 15,
            "avg_predicted_yield": 4.1,
            "min_predicted_yield": 3.5,
            "max_predicted_yield": 4.8
        }
    ]
}
```

#### `test_database_connection()`
Test Snowflake connectivity:
```python
test_database_connection()
```

### 3. Updated Yield Agent

The yield agent now prioritizes database forecasts:

**Tool Priority:**
1. **First**: Try database tools for real ML forecasts
2. **Fallback**: Use calculated predictions if database unavailable

**Example Query:**
```
User: "What yield can I expect for wheat?"

Agent: 
1. Calls get_yield_forecast_from_db(crop_type="wheat")
2. Returns ML-based forecast from Snowflake
3. Provides agricultural recommendations
```

## Usage Examples

### Test Database Connection

```bash
uv run python -c "
from adk_app.tools.snowflake_yield_tools import test_database_connection
result = test_database_connection()
print(result)
"
```

### Query Yield Forecasts

```bash
uv run python -c "
from adk_app.tools.snowflake_yield_tools import get_yield_forecast_from_db
result = get_yield_forecast_from_db(crop_type='wheat', limit=5)
print(result)
"
```

### Use with Agent

```bash
uv run adk run adk_app/agents/yield_agent
```

Then ask:
- "Show me the latest yield forecasts"
- "What's the yield forecast for wheat?"
- "Get yield forecast summary for corn"

## Connection Lifecycle

### Automatic Management

The connection manager automatically handles:

1. **Connection Creation**: On first use
2. **Connection Reuse**: Singleton pattern
3. **Connection Cleanup**: On session end or error

### Manual Management

```python
from adk_app.core.database import get_snowflake_manager

# Get manager
manager = get_snowflake_manager()

# Use context manager (recommended)
with manager.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM table")
    results = cursor.fetchall()

# Connection automatically cleaned up
```

### Cleanup on Exit

```python
from adk_app.core.database import close_snowflake_connections

# Close all connections
close_snowflake_connections()
```

## Error Handling

The integration includes comprehensive error handling:

### Configuration Errors
```json
{
    "status": "error",
    "error_type": "configuration_error",
    "error_message": "Private key file not found",
    "suggestion": "Ensure database_connection_config.pem exists"
}
```

### Database Errors
```json
{
    "status": "error",
    "error_type": "database_error",
    "error_message": "Failed to fetch yield forecasts",
    "suggestion": "Check database connection and credentials"
}
```

### Graceful Fallback

If database is unavailable, the agent automatically falls back to calculated predictions.

## Security Best Practices

✅ **Private Key Security**
- PEM file stored locally (not in git)
- Read-only database role (`ML_SRV_RO_ROLE`)
- No write permissions

✅ **Connection Security**
- Private key authentication (no passwords)
- Encrypted connections
- Automatic connection cleanup

✅ **Query Safety**
- Parameterized queries (prevents SQL injection)
- Read-only operations
- Limited result sets

## Database Schema

**Table**: `DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS`

**Expected Columns** (adjust based on your actual schema):
- `crop_type` - Type of crop
- `location` - Geographic location
- `predicted_yield` - ML-predicted yield value
- `forecast_date` - Date of forecast
- `created_at` - Timestamp of record creation
- Additional ML model metadata

## Monitoring & Logging

All database operations are logged:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

**Log Examples:**
```
INFO - Connecting to Snowflake account: ae18467.eu-west-2.aws
INFO - Successfully connected to Snowflake
INFO - Executing yield forecast query with filters: crop=wheat
INFO - Snowflake connection closed
```

## Troubleshooting

### Connection Fails

**Check:**
1. PEM file exists: `ls database_connection_config.pem`
2. Environment variables set in `.env`
3. Network connectivity to Snowflake
4. Snowflake account/role permissions

**Test:**
```python
from adk_app.tools.snowflake_yield_tools import test_database_connection
print(test_database_connection())
```

### No Data Returned

**Check:**
1. Table exists and has data
2. Filters are not too restrictive
3. Role has SELECT permissions
4. Schema/database names are correct

### PEM File Not Found

**Solution:**
Ensure `database_connection_config.pem` is in project root:
```bash
ls /Users/saniyasultanatuba/Downloads/Python-dev/llm/agripulse-ai-agent/agripulse-adk-agent/database_connection_config.pem
```

## Performance Optimization

### Connection Pooling
- Single connection reused across queries
- Lazy connection initialization
- Automatic cleanup prevents connection leaks

### Query Optimization
- Parameterized queries
- Result limiting (default: 10 records)
- Efficient filtering at database level

### Caching (Future Enhancement)
Consider adding caching for frequently accessed forecasts:
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_forecast(crop_type, location):
    return get_yield_forecast_from_db(crop_type, location)
```

## Next Steps

1. ✅ **Test Connection**: Run `test_database_connection()`
2. ✅ **Query Data**: Try `get_latest_yield_forecasts()`
3. ✅ **Use Agent**: Ask yield agent for forecasts
4. 📊 **Monitor**: Check logs for database activity
5. 🔧 **Optimize**: Add caching if needed

---

**Your Snowflake integration is ready!** The yield agent now has access to real ML-powered forecasts from your database. 🎉
