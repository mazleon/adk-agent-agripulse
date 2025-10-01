# Crop Best Practices Implementation

## Overview
Implemented crop best practices feature that provides standard cultivation guidelines from Snowflake database table `DEV_DATA_ML_DB.DATA_ML_SCHEMA.VW_STG_CROP_PRACTICE`.

## Features Implemented

### 1. New Tools Created (`crop_practice_tools.py`)

#### `get_crop_best_practices(crop_type, season)`
Retrieves comprehensive best practice information including:
- Plant height and width specifications
- Grain yield range (min/max kg per hectare)
- Planting density recommendations
- Fertilizer requirements (N, P, K)
- Irrigation frequency
- Harvest timing
- Pest management notes
- Soil type recommendations

**Parameters:**
- `crop_type` (REQUIRED): e.g., "Rice", "Aman", "Wheat", "Maize"
- `season` (REQUIRED): e.g., "Kharif", "Rabi", "Summer", "Winter", "Monsoon"

**Example Usage:**
```python
get_crop_best_practices(crop_type="Rice", season="Kharif")
get_crop_best_practices(crop_type="Aman", season="Kharif")
```

#### `get_available_crop_practice_types()`
Lists all available crop types and seasons in the database.

**Returns:**
- List of available crops
- List of available seasons
- All crop-season combinations with practice counts

#### `get_crop_practice_summary(crop_type)`
Provides aggregated summary of practices across all seasons for a specific crop.

### 2. Integration with Yield Agent

Updated `YieldToolset` to include the new crop practice tools:
- Added imports for crop practice tools
- Registered all three new tools with the yield agent

### 3. Enhanced Agent Instructions

Updated `yield_agent/persona.md` with:

#### New Responsibility Section
Added "Crop Best Practices & Standards" as a core responsibility

#### Tool Priority Guidelines
Added clear priority for when to use crop practice tools:
- Standard practices queries
- Plant specifications
- Yield ranges
- Fertilizer recommendations
- Irrigation schedules

#### Handling Best Practice Queries
Detailed workflow for:
1. Identifying required information (crop type + season)
2. Asking clarifying questions when information is missing
3. Formatting responses with comprehensive practice details

#### Enhanced Response Format
Updated yield forecast format to include BOTH:
- Standard best practice yield ranges
- Historical ML-based predictions

**New Format:**
```
Here is the yield forecast for [CROP] in [DISTRICT] for [YEAR]:

* From our standard best practice:
  - Expected Yield Range: X to Y kg/ha (A to B tons/ha)
  - Based on: [SEASON] season cultivation standards

* From our historical analysis:
  - Predicted Yield: X.XX tons per hectare
  - Confidence Interval: X.XX to X.XX tons per hectare
```

#### Example Interactions
Added two comprehensive examples:
1. "What are the best practices for Aman rice?"
2. "Tell me about rice cultivation standards for Kharif season"

## Database Schema

**Table:** `DEV_DATA_ML_DB.DATA_ML_SCHEMA.VW_STG_CROP_PRACTICE`

**Columns:**
- `CROP_TYPE`: Type of crop
- `SEASON`: Growing season
- `PLANT_HEIGHT_CM`: Expected plant height
- `PLANT_WIDTH_CM`: Expected plant width
- `GRAIN_YIELD_MIN_KG_HA`: Minimum expected yield
- `GRAIN_YIELD_MAX_KG_HA`: Maximum expected yield
- `PLANTING_DENSITY_PLANTS_M2`: Recommended planting density
- `FERTILIZER_N_KG_HA`: Nitrogen requirement
- `FERTILIZER_P_KG_HA`: Phosphorus requirement
- `FERTILIZER_K_KG_HA`: Potassium requirement
- `IRRIGATION_FREQUENCY_DAYS`: Irrigation schedule
- `PEST_MANAGEMENT_NOTES`: Pest control guidelines
- `HARVEST_TIME_DAYS`: Days to harvest
- `SOIL_TYPE_RECOMMENDED`: Optimal soil type
- `ADDITIONAL_NOTES`: Extra information

## User Interaction Flow

### Scenario 1: User asks about best practices
```
User: "What are the best practices for rice?"

Agent: 
1. Identifies missing information (season)
2. Asks: "Which season are you planning for?"
3. User provides season
4. Calls get_crop_best_practices(crop_type="Rice", season="Kharif")
5. Presents comprehensive best practice information
```

### Scenario 2: User asks for yield forecast
```
User: "What's the yield forecast for Aman in Dhaka for 2025?"

Agent:
1. Calls get_crop_best_practices(crop_type="Aman", season="Kharif")
   - Gets standard yield range
2. Calls get_yield_forecast_from_db(...)
   - Gets ML prediction
3. Presents BOTH in formatted response:
   - Best practice range: 3,500-5,000 kg/ha
   - Historical prediction: 2,570 kg/ha with confidence interval
4. Explains any discrepancy between the two
```

### Scenario 3: Discovery
```
User: "What crops have best practice information?"

Agent:
1. Calls get_available_crop_practice_types()
2. Shows all available crops and seasons
3. Invites user to ask about specific combinations
```

## Benefits

1. **Comprehensive Information**: Users get both standard guidelines AND data-driven predictions
2. **Actionable Advice**: Specific recommendations for fertilizers, irrigation, spacing
3. **Context**: Comparison between best practice and actual predictions helps identify issues
4. **Discovery**: Easy exploration of available information
5. **Conversational**: Agent asks clarifying questions when needed

## Testing

To test the implementation:

1. **Start Streamlit app:**
   ```bash
   streamlit run main.py
   ```

2. **Test queries:**
   - "What are the best practices for rice in Kharif season?"
   - "Tell me about Aman rice cultivation standards"
   - "What crops have best practice information?"
   - "Show me yield forecast for Aman in Dhaka for 2025" (should include both best practice and historical data)

## Files Modified

1. **Created:**
   - `adk_app/tools/crop_practice_tools.py` - New tool implementations

2. **Modified:**
   - `adk_app/tools/toolsets/yield_toolset.py` - Added crop practice tools
   - `adk_app/agents/yield_agent/persona.md` - Enhanced instructions and examples

## Next Steps

1. Populate the `VW_STG_CROP_PRACTICE` table with actual data
2. Test with real database queries
3. Add more example interactions to the persona
4. Consider adding visualization for yield comparisons
5. Implement seasonal recommendations based on current date
