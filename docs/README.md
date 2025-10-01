# 📚 AgriPulse AI Documentation

Welcome to the AgriPulse AI Agent Development Kit documentation!

---

## 📖 Documentation Index

### **Getting Started**
- [Main README](../README.md) - Project overview and quick start
- [Quick Start Guide](../QUICKSTART.md) - Get up and running quickly

### **Snowflake Integration**
- [Snowflake Integration Guide](SNOWFLAKE_INTEGRATION.md) - Complete integration documentation
- [Snowflake Implementation Summary](SNOWFLAKE_COMPLETE.md) - Implementation overview
- [PEM Configuration Guide](PEM_CONFIG_GUIDE.md) - Dynamic PEM file configuration

### **Features & Fixes**
- [Discovery Tools](DISCOVERY_TOOLS.md) - Crop types, districts, and years discovery
- [Feature Complete Summary](FEATURE_COMPLETE.md) - All implemented features
- [Query Logic Fix](QUERY_FIX.md) - Query issue resolution
- [Fixed Issues](FIXED_ISSUES.md) - Issues resolved during development

### **Response Formatting**
- [Response Format Guide](RESPONSE_FORMAT.md) - Standard yield forecast format
- [Format Implementation](FORMAT_IMPLEMENTATION.md) - Format implementation details

---

## 🗂️ Documentation Structure

```
docs/
├── README.md                      # This file - Documentation index
├── SNOWFLAKE_INTEGRATION.md       # Complete Snowflake integration guide
├── SNOWFLAKE_COMPLETE.md          # Implementation summary
├── PEM_CONFIG_GUIDE.md            # PEM file configuration
├── DISCOVERY_TOOLS.md             # Discovery tools documentation
├── FEATURE_COMPLETE.md            # All features summary
├── QUERY_FIX.md                   # Query logic fix documentation
├── FIXED_ISSUES.md                # Issues and resolutions
├── RESPONSE_FORMAT.md             # Response format guide
└── FORMAT_IMPLEMENTATION.md       # Format implementation
```

---

## 🚀 Quick Links

### **Setup & Configuration**
1. [Snowflake Setup](SNOWFLAKE_INTEGRATION.md#setup)
2. [PEM File Configuration](PEM_CONFIG_GUIDE.md#how-to-configure)
3. [Environment Variables](../README.md#environment-setup)

### **Using the Agent**
1. [Yield Predictions](RESPONSE_FORMAT.md#format-template)
2. [Discovery Tools](DISCOVERY_TOOLS.md#how-to-use)
3. [Query Examples](QUERY_FIX.md#testing)

### **Troubleshooting**
1. [Common Issues](FIXED_ISSUES.md#issues-resolved)
2. [Query Problems](QUERY_FIX.md#root-cause-analysis)
3. [Connection Issues](SNOWFLAKE_INTEGRATION.md#troubleshooting)

---

## 📊 Feature Overview

### **Snowflake Database Integration**
- ✅ Connection manager with lifecycle management
- ✅ Private key authentication
- ✅ Automatic connection cleanup
- ✅ Query execution with parameterized queries
- ✅ Error handling and logging

### **Yield Prediction Tools**
- ✅ Get yield forecasts with filters
- ✅ Get latest forecasts
- ✅ Get forecast summaries
- ✅ Discovery tools (crop types, districts, years)
- ✅ Standard response format

### **Database Coverage**
- ✅ 645 yield forecasts
- ✅ 2 crop varieties (Aman types)
- ✅ 73 districts across Bangladesh
- ✅ 5 years of forecast data (2024-2028)

---

## 🔧 Technical Documentation

### **Architecture**
```
Yield Agent
    ↓
YieldToolset
    ├─→ Snowflake Tools (Primary)
    │   ├─ get_yield_forecast_from_db
    │   ├─ get_latest_yield_forecasts
    │   ├─ get_yield_forecast_summary
    │   ├─ get_available_crop_types
    │   ├─ get_available_districts
    │   └─ get_available_forecast_years
    └─→ Calculated Tools (Fallback)
        ├─ predict_yield
        └─ analyze_soil_conditions
    ↓
SnowflakeConnectionManager
    ↓
Snowflake Database
```

### **Database Schema**
- **Table**: `DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS`
- **Columns**: ID, DISTRICT_NAME, CROP_TYPE, FORECAST_YEAR, PREDICTED_YIELD, CONFIDENCE_LOWER, CONFIDENCE_UPPER, MODEL_USED, PREDICTION_DATE

---

## 📝 Response Format

All yield forecasts follow this standard format:

```
Here is the yield forecast for [CROP_TYPE] rice in [DISTRICT] for [YEAR]:

* From our standard best practice:
  - Predicted Yield: Will be implemented later

* From our historical analysis:
  - Predicted Yield: [X.XX] tons per hectare
  - Confidence Interval: [X.XX] to [X.XX] tons per hectare
```

See [Response Format Guide](RESPONSE_FORMAT.md) for details.

---

## 🧪 Testing

### **Test Scripts**
```bash
# Test Snowflake connection
uv run python scripts/test_snowflake.py

# Test discovery tools
uv run python scripts/test_discovery_tools.py

# Test correct query behavior
uv run python scripts/test_correct_query.py

# Discover database schema
uv run python scripts/discover_schema.py
```

### **Run Agents**
```bash
# Yield agent
uv run adk run adk_app/agents/yield_agent

# Multi-agent coordinator
uv run adk run adk_app/agents/multi

# Web interface
uv run adk web
```

---

## 🔐 Security

### **PEM File Security**
- ✅ PEM files excluded from git (`.gitignore`)
- ✅ Dynamic path configuration via `.env`
- ✅ Support for secure locations (`~/.ssh/`, `/etc/secrets/`)
- ✅ Read-only database role

### **Best Practices**
- Never commit PEM files
- Use environment-specific credentials
- Set proper file permissions (`chmod 600`)
- Store in secure locations

---

## 📚 Additional Resources

### **Project Files**
- [README.md](../README.md) - Main project documentation
- [QUICKSTART.md](../QUICKSTART.md) - Quick start guide
- [.env.example](../.env.example) - Environment configuration template

### **Code Structure**
- `adk_app/core/database.py` - Connection manager
- `adk_app/tools/snowflake_yield_tools.py` - Database tools
- `adk_app/agents/yield_agent/` - Yield prediction agent
- `scripts/` - Test and utility scripts

---

## 🎯 Common Tasks

### **1. Set Up Snowflake Connection**
1. Copy `.env.example` to `.env`
2. Add your Snowflake credentials
3. Set `SNOWFLAKE_PRIVATE_KEY_FILE` path
4. Test: `uv run python scripts/test_snowflake.py`

### **2. Query Yield Forecasts**
```bash
uv run adk run adk_app/agents/yield_agent
```
Ask: "What's the yield forecast for HYV Aman in Dhaka for 2025?"

### **3. Discover Available Data**
```bash
uv run adk run adk_app/agents/yield_agent
```
Ask: "What crop types are available?"

### **4. Troubleshoot Issues**
- Check [Fixed Issues](FIXED_ISSUES.md)
- Check [Query Fix](QUERY_FIX.md)
- Check [Snowflake Integration](SNOWFLAKE_INTEGRATION.md#troubleshooting)

---

## 🆘 Support

### **Documentation Issues**
If you find any issues with the documentation:
1. Check the specific guide for your topic
2. Review troubleshooting sections
3. Check test scripts for examples

### **Technical Issues**
1. Review error messages in logs
2. Check [Fixed Issues](FIXED_ISSUES.md) for similar problems
3. Verify configuration in `.env` file
4. Test connection: `uv run python scripts/test_snowflake.py`

---

## 📈 Version History

### **Latest Updates**
- ✅ Dynamic PEM file configuration
- ✅ Discovery tools (crop types, districts, years)
- ✅ Standard response format
- ✅ Query logic fixes
- ✅ Comprehensive documentation

---

## 🎉 Quick Start

**Get started in 3 steps:**

1. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

2. **Test Connection**
   ```bash
   uv run python scripts/test_snowflake.py
   ```

3. **Run Agent**
   ```bash
   uv run adk run adk_app/agents/yield_agent
   ```

**That's it!** Your AgriPulse AI is ready to provide yield forecasts! 🌾✨

---

**For detailed information on any topic, click the links above or browse the documentation files in this folder.**
