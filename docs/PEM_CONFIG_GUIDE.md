# 🔐 Dynamic PEM File Configuration Guide

## ✅ Feature Implemented

You can now configure the Snowflake private key (PEM) file path dynamically using the `.env` file!

---

## 🎯 How to Configure

### **1. Add to Your `.env` File**

Open your `.env` file and add:

```bash
SNOWFLAKE_PRIVATE_KEY_FILE=database_connection_config.pem
```

---

## 📝 Configuration Options

### **Option 1: Relative Path (Recommended)**

```bash
# Relative to project root
SNOWFLAKE_PRIVATE_KEY_FILE=database_connection_config.pem
```

### **Option 2: Relative Path with Directory**

```bash
# In a subdirectory
SNOWFLAKE_PRIVATE_KEY_FILE=./config/database_connection_config.pem
```

### **Option 3: Absolute Path**

```bash
# Full absolute path
SNOWFLAKE_PRIVATE_KEY_FILE=/Users/yourname/keys/snowflake_key.pem
```

### **Option 4: Home Directory Path**

```bash
# Using ~ for home directory
SNOWFLAKE_PRIVATE_KEY_FILE=~/.ssh/snowflake_key.pem
```

### **Option 5: Different Environments**

```bash
# Development
SNOWFLAKE_PRIVATE_KEY_FILE=./keys/dev_snowflake.pem

# Production
SNOWFLAKE_PRIVATE_KEY_FILE=/secure/path/prod_snowflake.pem
```

---

## 🔧 How It Works

### **Path Resolution Logic**

1. **Reads from `.env`**: Gets `SNOWFLAKE_PRIVATE_KEY_FILE` value
2. **Expands User Path**: Converts `~` to actual home directory
3. **Resolves Relative Paths**: Makes relative paths relative to project root
4. **Falls Back to Default**: Uses `database_connection_config.pem` if not set

### **Code Implementation**

```python
# In adk_app/core/database.py

pem_file_path = os.getenv("SNOWFLAKE_PRIVATE_KEY_FILE")

if not pem_file_path:
    # Fallback to default
    pem_file_path = "database_connection_config.pem"
else:
    # Expand ~ to home directory
    pem_file_path = os.path.expanduser(pem_file_path)
    
    # Make relative paths relative to project root
    if not os.path.isabs(pem_file_path):
        pem_file_path = project_root / pem_file_path
```

---

## 📊 Examples

### **Example 1: Default Setup**

**`.env` file:**
```bash
SNOWFLAKE_PRIVATE_KEY_FILE=database_connection_config.pem
```

**Result:**
- Looks for: `/path/to/project/database_connection_config.pem`

---

### **Example 2: Keys in Subdirectory**

**`.env` file:**
```bash
SNOWFLAKE_PRIVATE_KEY_FILE=config/keys/snowflake.pem
```

**Result:**
- Looks for: `/path/to/project/config/keys/snowflake.pem`

---

### **Example 3: Absolute Path**

**`.env` file:**
```bash
SNOWFLAKE_PRIVATE_KEY_FILE=/Users/saniyasultanatuba/.ssh/snowflake_key.pem
```

**Result:**
- Looks for: `/Users/saniyasultanatuba/.ssh/snowflake_key.pem`

---

### **Example 4: Home Directory**

**`.env` file:**
```bash
SNOWFLAKE_PRIVATE_KEY_FILE=~/.ssh/snowflake_key.pem
```

**Result:**
- Expands to: `/Users/saniyasultanatuba/.ssh/snowflake_key.pem`

---

### **Example 5: Not Set (Fallback)**

**`.env` file:**
```bash
# SNOWFLAKE_PRIVATE_KEY_FILE not set
```

**Result:**
- Uses default: `/path/to/project/database_connection_config.pem`
- Logs warning: "SNOWFLAKE_PRIVATE_KEY_FILE not set in .env, using default"

---

## 🚀 Setup Instructions

### **Step 1: Update Your `.env` File**

```bash
# Copy from example
cp .env.example .env

# Edit .env and add your PEM file path
nano .env
```

Add this line:
```bash
SNOWFLAKE_PRIVATE_KEY_FILE=database_connection_config.pem
```

### **Step 2: Place Your PEM File**

**Option A: Project Root (Default)**
```bash
# Place file in project root
/path/to/project/database_connection_config.pem
```

**Option B: Custom Location**
```bash
# Place file anywhere and update .env
SNOWFLAKE_PRIVATE_KEY_FILE=/custom/path/to/your_key.pem
```

### **Step 3: Test the Connection**

```bash
# Test database connection
uv run python scripts/test_snowflake.py
```

**Expected Output:**
```
INFO - Using PEM file: /path/to/your/database_connection_config.pem
✅ Connection successful!
```

---

## 🔒 Security Best Practices

### **1. Never Commit PEM Files**

The `.gitignore` already includes:
```
*.pem
database_connection_config.pem
*.key
*.p8
```

### **2. Use Environment-Specific Files**

```bash
# Development
SNOWFLAKE_PRIVATE_KEY_FILE=./keys/dev.pem

# Staging
SNOWFLAKE_PRIVATE_KEY_FILE=./keys/staging.pem

# Production
SNOWFLAKE_PRIVATE_KEY_FILE=/secure/prod.pem
```

### **3. Set Proper File Permissions**

```bash
# Make PEM file readable only by owner
chmod 600 database_connection_config.pem
```

### **4. Store in Secure Location**

```bash
# Good: User's SSH directory
SNOWFLAKE_PRIVATE_KEY_FILE=~/.ssh/snowflake_key.pem

# Good: Secure system directory
SNOWFLAKE_PRIVATE_KEY_FILE=/etc/secrets/snowflake_key.pem

# Bad: Public directory
SNOWFLAKE_PRIVATE_KEY_FILE=/tmp/key.pem  # ❌ Don't do this
```

---

## 🧪 Testing Different Configurations

### **Test 1: Default Configuration**

```bash
# Remove SNOWFLAKE_PRIVATE_KEY_FILE from .env
# Should use default: database_connection_config.pem

uv run python scripts/test_snowflake.py
```

### **Test 2: Custom Path**

```bash
# Add to .env:
# SNOWFLAKE_PRIVATE_KEY_FILE=custom_path/my_key.pem

uv run python scripts/test_snowflake.py
```

### **Test 3: Absolute Path**

```bash
# Add to .env:
# SNOWFLAKE_PRIVATE_KEY_FILE=/absolute/path/to/key.pem

uv run python scripts/test_snowflake.py
```

---

## 📋 Complete `.env` Example

```bash
# Google API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Snowflake Database Configuration
SNOWFLAKE_USER=ML_SRV_USER
SNOWFLAKE_ACCOUNT=ae18467.eu-west-2.aws
SNOWFLAKE_ROLE=ML_SRV_RO_ROLE
SNOWFLAKE_WAREHOUSE=DEV_DATA_ML_WH
SNOWFLAKE_DATABASE=DEV_DATA_ML_DB
SNOWFLAKE_SCHEMA=DATA_ML_SCHEMA

# Snowflake Private Key File Path
# Choose one of these options:
SNOWFLAKE_PRIVATE_KEY_FILE=database_connection_config.pem                    # Relative to project root
# SNOWFLAKE_PRIVATE_KEY_FILE=./config/snowflake_key.pem                     # In subdirectory
# SNOWFLAKE_PRIVATE_KEY_FILE=~/.ssh/snowflake_key.pem                       # In home directory
# SNOWFLAKE_PRIVATE_KEY_FILE=/absolute/path/to/snowflake_key.pem            # Absolute path

# Environment
ENVIRONMENT=development

# Runtime Configuration
DEV_UI_PORT=8080
LOG_LEVEL=INFO
```

---

## ✅ Benefits

### **1. Flexibility**
- ✅ Easy to change PEM file location
- ✅ Different files for different environments
- ✅ No code changes needed

### **2. Security**
- ✅ Keep PEM files outside project directory
- ✅ Use secure system locations
- ✅ Environment-specific credentials

### **3. Portability**
- ✅ Works on different machines
- ✅ Team members can use their own paths
- ✅ CI/CD friendly

### **4. Maintainability**
- ✅ Single place to update path
- ✅ Clear configuration
- ✅ Easy to debug

---

## 🐛 Troubleshooting

### **Issue: File Not Found**

**Error:**
```
FileNotFoundError: Private key file not found: /path/to/file.pem
```

**Solution:**
1. Check the path in `.env` is correct
2. Verify the file exists: `ls -la /path/to/file.pem`
3. Check file permissions: `ls -l /path/to/file.pem`

---

### **Issue: Using Default Path**

**Warning:**
```
SNOWFLAKE_PRIVATE_KEY_FILE not set in .env, using default
```

**Solution:**
1. Add `SNOWFLAKE_PRIVATE_KEY_FILE` to your `.env` file
2. Or place PEM file at default location: `database_connection_config.pem`

---

### **Issue: Relative Path Not Working**

**Problem:** File not found with relative path

**Solution:**
- Relative paths are relative to **project root**, not current directory
- Use absolute path if unsure: `SNOWFLAKE_PRIVATE_KEY_FILE=/full/path/to/file.pem`

---

## 📚 Summary

**You can now configure the PEM file path in three ways:**

1. **Environment Variable** (Recommended)
   ```bash
   SNOWFLAKE_PRIVATE_KEY_FILE=your_path_here.pem
   ```

2. **Default Location** (Fallback)
   - Place file at: `database_connection_config.pem` in project root

3. **Absolute Path** (Most Secure)
   ```bash
   SNOWFLAKE_PRIVATE_KEY_FILE=/secure/path/to/key.pem
   ```

**The system will:**
- ✅ Read from `.env` file
- ✅ Expand `~` to home directory
- ✅ Resolve relative paths to project root
- ✅ Fall back to default if not set
- ✅ Log which file is being used

**Start using it now!** Just add `SNOWFLAKE_PRIVATE_KEY_FILE` to your `.env` file! 🔐✨
