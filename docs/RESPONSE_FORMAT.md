# 📋 Yield Forecast Response Format

## 🎯 Standard Response Format

All yield forecast responses **MUST** follow this exact format:

---

## 📝 Format Template

```
Here is the yield forecast for [CROP_TYPE] rice in [DISTRICT] for [YEAR]:

* From our standard best practice:
  - Predicted Yield: Will be implemented later

* From our historical analysis:
  - Predicted Yield: [X.XX] tons per hectare
  - Confidence Interval: [X.XX] to [X.XX] tons per hectare
```

---

## ✨ Format Rules

### **1. Opening Line**
```
Here is the yield forecast for [CROP_TYPE] rice in [DISTRICT] for [YEAR]:
```

**Rules:**
- ✅ Always start with "Here is the yield forecast for"
- ✅ Include the full crop type name from database
- ✅ Add "rice" after the crop type for clarity
- ✅ Include district name
- ✅ Include forecast year
- ✅ End with colon (:)

**Examples:**
- ✅ "Here is the yield forecast for (Broadcast+L.T + HYV) Aman rice in Mymensingh for 2026:"
- ✅ "Here is the yield forecast for High Yielding Variety (HYV) Aman rice in Dhaka for 2025:"
- ❌ "Forecast for Aman in Dhaka:" (too short, missing details)

### **2. Standard Best Practice Section**
```
* From our standard best practice:
  - Predicted Yield: Will be implemented later
```

**Rules:**
- ✅ Always include this section
- ✅ Use exact text: "From our standard best practice:"
- ✅ Always show: "Predicted Yield: Will be implemented later"
- ✅ Use bullet point with asterisk (*)
- ✅ Indent sub-items with 2 spaces and dash (-)

### **3. Historical Analysis Section**
```
* From our historical analysis:
  - Predicted Yield: [X.XX] tons per hectare
  - Confidence Interval: [X.XX] to [X.XX] tons per hectare
```

**Rules:**
- ✅ Always include this section
- ✅ Use exact text: "From our historical analysis:"
- ✅ Show actual predicted yield from database
- ✅ Show confidence interval (CONFIDENCE_LOWER to CONFIDENCE_UPPER)
- ✅ Format numbers to 2 decimal places
- ✅ Always include "tons per hectare" unit
- ✅ Use bullet point with asterisk (*)
- ✅ Indent sub-items with 2 spaces and dash (-)

---

## 📊 Complete Examples

### **Example 1: Single Forecast**

```
Here is the yield forecast for (Broadcast+L.T + HYV) Aman rice in Mymensingh for 2026:

* From our standard best practice:
  - Predicted Yield: Will be implemented later

* From our historical analysis:
  - Predicted Yield: 2.57 tons per hectare
  - Confidence Interval: 2.45 to 2.69 tons per hectare
```

### **Example 2: Another Single Forecast**

```
Here is the yield forecast for High Yielding Variety (HYV) Aman rice in Dhaka for 2025:

* From our standard best practice:
  - Predicted Yield: Will be implemented later

* From our historical analysis:
  - Predicted Yield: 2.50 tons per hectare
  - Confidence Interval: 2.45 to 2.55 tons per hectare
```

### **Example 3: Multiple Forecasts**

```
**Latest ML Yield Forecasts:**

1. Here is the yield forecast for (Broadcast+L.T + HYV) Aman rice in Bagerhat for 2028:
   * From our standard best practice:
     - Predicted Yield: Will be implemented later
   * From our historical analysis:
     - Predicted Yield: 2.34 tons per hectare
     - Confidence Interval: 2.11 to 2.57 tons per hectare

2. Here is the yield forecast for High Yielding Variety (HYV) Aman rice in Bagerhat for 2028:
   * From our standard best practice:
     - Predicted Yield: Will be implemented later
   * From our historical analysis:
     - Predicted Yield: 2.62 tons per hectare
     - Confidence Interval: 2.37 to 2.87 tons per hectare

3. Here is the yield forecast for (Broadcast+L.T + HYV) Aman rice in Bandarban for 2028:
   * From our standard best practice:
     - Predicted Yield: Will be implemented later
   * From our historical analysis:
     - Predicted Yield: 2.67 tons per hectare
     - Confidence Interval: 2.41 to 2.93 tons per hectare
```

---

## 🔧 Implementation Guide

### **Step 1: Get Data from Database**

```python
result = get_yield_forecast_from_db(
    yield_variety="High Yielding Variety (HYV) Aman",
    district="Dhaka",
    forecast_year=2025
)

forecast = result['forecasts'][0]
```

### **Step 2: Extract Values**

```python
crop_type = forecast['crop_type']           # "High Yielding Variety (HYV) Aman"
district = forecast['district_name']        # "Dhaka"
year = forecast['forecast_year']            # 2025
predicted = forecast['predicted_yield']     # 2.50
conf_lower = forecast['confidence_lower']   # 2.45
conf_upper = forecast['confidence_upper']   # 2.55
```

### **Step 3: Format Response**

```python
response = f"""Here is the yield forecast for {crop_type} rice in {district} for {year}:

* From our standard best practice:
  - Predicted Yield: Will be implemented later

* From our historical analysis:
  - Predicted Yield: {predicted:.2f} tons per hectare
  - Confidence Interval: {conf_lower:.2f} to {conf_upper:.2f} tons per hectare"""
```

---

## ✅ Checklist

Before presenting a yield forecast, verify:

- [ ] Includes opening line with full crop type, district, and year
- [ ] Adds "rice" after crop type name
- [ ] Includes "From our standard best practice" section
- [ ] Shows "Will be implemented later" for standard best practice
- [ ] Includes "From our historical analysis" section
- [ ] Shows actual predicted yield from database
- [ ] Shows confidence interval with lower and upper bounds
- [ ] Numbers formatted to 2 decimal places
- [ ] Includes "tons per hectare" unit
- [ ] Uses correct bullet points and indentation
- [ ] Ends with colon after opening line

---

## ❌ Common Mistakes to Avoid

### **Mistake 1: Missing "rice"**
```
❌ "Here is the yield forecast for HYV Aman in Dhaka for 2025:"
✅ "Here is the yield forecast for High Yielding Variety (HYV) Aman rice in Dhaka for 2025:"
```

### **Mistake 2: Wrong Standard Best Practice Text**
```
❌ "- Predicted Yield: Coming soon"
❌ "- Predicted Yield: Not available"
✅ "- Predicted Yield: Will be implemented later"
```

### **Mistake 3: Missing Confidence Interval**
```
❌ "- Predicted Yield: 2.50 tons per hectare"
✅ "- Predicted Yield: 2.50 tons per hectare
    - Confidence Interval: 2.45 to 2.55 tons per hectare"
```

### **Mistake 4: Wrong Number Format**
```
❌ "- Predicted Yield: 2.5 tons per hectare"        (1 decimal)
❌ "- Predicted Yield: 2.501234 tons per hectare"   (too many decimals)
✅ "- Predicted Yield: 2.50 tons per hectare"       (2 decimals)
```

### **Mistake 5: Missing Sections**
```
❌ Only showing historical analysis (missing standard best practice)
❌ Only showing standard best practice (missing historical analysis)
✅ Always show BOTH sections
```

---

## 📚 Additional Information (Optional)

After the main forecast, you can optionally add:

```
**Additional Information:**
- Model Used: Ensemble
- Prediction Date: 2025-08-24
- Source: Snowflake ML Database

**Factors Affecting Yield:**
- Soil quality and fertility
- Weather conditions during growing season
- Irrigation availability
- Pest and disease management
```

---

## 🎯 Summary

**The format has TWO required sections:**

1. **Standard Best Practice** → Always shows "Will be implemented later"
2. **Historical Analysis** → Shows actual data from database

**Always include:**
- Full crop type name + "rice"
- District name
- Forecast year
- Predicted yield (2 decimals)
- Confidence interval (2 decimals)
- Proper bullet points and indentation

**This format ensures:**
- ✅ Consistency across all responses
- ✅ Clear separation of future vs current capabilities
- ✅ Professional presentation
- ✅ Easy to read and understand
- ✅ Includes confidence intervals for transparency

---

## 🚀 Quick Reference

**Copy this template for every forecast:**

```
Here is the yield forecast for [CROP_TYPE] rice in [DISTRICT] for [YEAR]:

* From our standard best practice:
  - Predicted Yield: Will be implemented later

* From our historical analysis:
  - Predicted Yield: [X.XX] tons per hectare
  - Confidence Interval: [X.XX] to [X.XX] tons per hectare
```

**Replace:**
- `[CROP_TYPE]` → Full variety name from database
- `[DISTRICT]` → District name
- `[YEAR]` → Forecast year
- `[X.XX]` → Actual values from database (2 decimal places)

---

**This format is now implemented in the yield agent persona and will be used for all yield forecast responses!** 🌾✨
