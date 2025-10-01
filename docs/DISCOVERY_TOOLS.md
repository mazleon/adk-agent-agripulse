# 🔍 Discovery Tools - Feature Documentation

## ✨ New Features Added

Your yield agent now has **discovery tools** that allow users to explore what data is available in the database before making specific queries!

---

## 🎯 What's New

### **3 New Discovery Tools**

1. ✅ **`get_available_crop_types()`** - Show all crop types/varieties
2. ✅ **`get_available_districts()`** - Show all districts with data
3. ✅ **`get_available_forecast_years()`** - Show all available years

---

## 📊 Available Data Summary

### **Crop Types: 2 Main Varieties**
- **(Broadcast+L.T + HYV) Aman** - 325 forecasts
- **High Yielding Variety (HYV) Aman** - 320 forecasts

**Main Categories:**
- Aman
- HYV (High Yielding Variety)
- Broadcast

### **Districts: 73 Districts Across Bangladesh**
Including:
- Bagerhat, Bandarban, Barguna, Barishal, Bhola
- Bogura, Brahmanbaria, Chandpur, Chattogram
- Dhaka, Dinajpur, Faridpur, Gazipur
- Khulna, Mymensingh, Rajshahi, Rangpur, Sylhet
- And 55+ more districts!

### **Forecast Years: 5 Years**
- 2024 (129 forecasts)
- 2025 (129 forecasts)
- 2026 (129 forecasts)
- 2027 (129 forecasts)
- 2028 (129 forecasts)

---

## 🚀 How to Use

### **Run the Yield Agent**

```bash
cd /Users/saniyasultanatuba/Downloads/Python-dev/llm/agripulse-ai-agent/agripulse-adk-agent

uv run adk run adk_app/agents/yield_agent
```

### **Example User Queries**

#### 1. **Discover Crop Types**
```
User: What crop types are available for forecast?
User: What yield varieties can I get forecasts for?
User: Show me all crop types
```

**Agent Response:**
```
Available Crop Types for Yield Forecasting:

Main Categories:
- Aman (multiple varieties)
- HYV (High Yielding Variety)
- Broadcast

Detailed Varieties (Total: 2):
1. (Broadcast+L.T + HYV) Aman - 325 forecasts
2. High Yielding Variety (HYV) Aman - 320 forecasts

You can ask for forecasts using any of these crop types!
```

#### 2. **Discover Districts**
```
User: What districts are covered?
User: Which locations have forecast data?
User: Show me all available districts
```

**Agent Response:**
```
Available Districts (Total: 73):

1. Bagerhat - 10 forecasts
2. Bandarban - 10 forecasts
3. Barguna - 10 forecasts
4. Dhaka - 10 forecasts
5. Khulna - 10 forecasts
... and 68 more districts!

You can get forecasts for any of these districts.
```

#### 3. **Discover Years**
```
User: What years are available for forecasts?
User: Which years have forecast data?
User: Show me available forecast years
```

**Agent Response:**
```
Available Forecast Years (Total: 5):

- 2028: 129 forecasts
- 2027: 129 forecasts
- 2026: 129 forecasts
- 2025: 129 forecasts
- 2024: 129 forecasts

You can get forecasts for any of these years!
```

---

## 🎓 Complete Workflow Example

### **Scenario: User doesn't know what to ask**

```
User: I want yield forecasts but don't know what's available

Agent: I can help you explore our forecast database! Let me show you what's available.

[Calls get_available_crop_types]

We have forecasts for these crop types:
- (Broadcast+L.T + HYV) Aman
- High Yielding Variety (HYV) Aman

[Calls get_available_districts]

And we cover 73 districts across Bangladesh, including:
- Bagerhat, Dhaka, Khulna, Rajshahi, Sylhet, and many more

[Calls get_available_forecast_years]

Forecasts are available for years 2024-2028.

What would you like to know? For example:
- "Show me Aman forecasts for Bagerhat in 2024"
- "What's the yield forecast for HYV Aman in Dhaka?"

User: Show me Aman forecasts for Bagerhat in 2024

Agent: [Calls get_yield_forecast_from_db with filters]

Here are the Aman forecasts for Bagerhat in 2024:
- Predicted Yield: 2.34 tons/hectare
- Confidence Range: 2.11 - 2.57 tons/hectare
- Model: Ensemble
```

---

## 🔧 Technical Implementation

### **Tool Functions**

#### 1. `get_available_crop_types()`

**Query:**
```sql
SELECT DISTINCT 
    CROP_TYPE,
    COUNT(*) as forecast_count
FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS
GROUP BY CROP_TYPE
ORDER BY forecast_count DESC, CROP_TYPE
```

**Returns:**
```json
{
    "status": "success",
    "total_varieties": 2,
    "crop_types": [
        {
            "crop_type": "(Broadcast+L.T + HYV) Aman",
            "forecast_count": 325
        },
        {
            "crop_type": "High Yielding Variety (HYV) Aman",
            "forecast_count": 320
        }
    ],
    "main_categories": ["Aman", "Broadcast", "HYV (High Yielding Variety)"],
    "source": "Snowflake ML Database"
}
```

#### 2. `get_available_districts()`

**Query:**
```sql
SELECT DISTINCT 
    DISTRICT_NAME,
    COUNT(*) as forecast_count
FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS
GROUP BY DISTRICT_NAME
ORDER BY DISTRICT_NAME
```

**Returns:**
```json
{
    "status": "success",
    "total_districts": 73,
    "districts": [
        {"district_name": "Bagerhat", "forecast_count": 10},
        {"district_name": "Dhaka", "forecast_count": 10},
        ...
    ],
    "source": "Snowflake ML Database"
}
```

#### 3. `get_available_forecast_years()`

**Query:**
```sql
SELECT DISTINCT 
    FORECAST_YEAR,
    COUNT(*) as forecast_count
FROM DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS
GROUP BY FORECAST_YEAR
ORDER BY FORECAST_YEAR DESC
```

**Returns:**
```json
{
    "status": "success",
    "total_years": 5,
    "years": [
        {"forecast_year": 2028, "forecast_count": 129},
        {"forecast_year": 2027, "forecast_count": 129},
        ...
    ],
    "source": "Snowflake ML Database"
}
```

---

## 🧪 Testing

### **Test Discovery Tools**

```bash
uv run python scripts/test_discovery_tools.py
```

**Expected Output:**
```
✅ Found 2 crop varieties
✅ Found 73 districts
✅ Found 5 forecast years
```

### **Test with Agent**

```bash
uv run adk run adk_app/agents/yield_agent
```

**Test Queries:**
1. "What crop types are available?"
2. "What districts are covered?"
3. "What years have forecasts?"
4. "Show me all available data"

---

## 📁 Files Modified

### **New Functions Added**
- `adk_app/tools/snowflake_yield_tools.py`
  - `get_available_crop_types()`
  - `get_available_districts()`
  - `get_available_forecast_years()`

### **Updated Files**
- `adk_app/tools/toolsets/yield_toolset.py` - Added 3 new tools
- `adk_app/agents/yield_agent/persona.md` - Added discovery tool guidance
- `scripts/test_discovery_tools.py` - New test script

---

## 🎯 Use Cases

### **1. First-Time Users**
Users who don't know what data is available can explore:
```
"What crop types can I get forecasts for?"
"What districts are covered?"
```

### **2. Data Exploration**
Users can browse available options before making specific queries:
```
"Show me all available crop varieties"
"List all districts with forecast data"
```

### **3. Planning Queries**
Users can check what years are available:
```
"What years have forecast data?"
"Can I get forecasts for 2025?"
```

### **4. Guided Discovery**
Agent can proactively help users:
```
User: "I want yield forecasts"
Agent: "Let me show you what's available..."
[Shows crop types, districts, and years]
```

---

## ✅ Benefits

1. ✅ **User-Friendly** - Users don't need to guess what data exists
2. ✅ **Reduces Errors** - Users can see valid options before querying
3. ✅ **Improves UX** - Guided discovery of available data
4. ✅ **Transparent** - Shows exactly what's in the database
5. ✅ **Helpful** - Agent can suggest valid queries based on available data

---

## 🎉 Summary

Your yield agent now has **discovery tools** that make it easy for users to:

✅ **Explore** what crop types are available  
✅ **Discover** which districts have data  
✅ **Check** what forecast years exist  
✅ **Make informed queries** based on available data  

**Start using it:**
```bash
uv run adk run adk_app/agents/yield_agent
```

Then ask: **"What crop types are available for forecast?"**

Your users can now easily discover what data is available before making specific forecast requests! 🌾📊
