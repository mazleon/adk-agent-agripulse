# AgriPulse AI - Docker Quick Start Guide

Get AgriPulse AI running in Docker in under 5 minutes!

## 🚀 Quick Start (3 Steps)

### Step 1: Configure Environment (2 minutes)

```bash
cd deployment

# Copy environment template
cp .env.docker .env

# Edit with your credentials
# Windows: notepad .env
# Linux/Mac: nano .env
```

**Required values to update:**
- `GOOGLE_API_KEY` - Your Google API key
- `SNOWFLAKE_USER` - Your Snowflake username
- `SNOWFLAKE_ACCOUNT` - Your Snowflake account ID
- `SNOWFLAKE_ROLE` - Your Snowflake role
- `SNOWFLAKE_WAREHOUSE` - Your Snowflake warehouse

### Step 2: Add Snowflake Key (1 minute)

```bash
# Create secrets directory
mkdir secrets

# Copy your Snowflake private key
# Windows:
copy C:\path\to\your\key.pem secrets\snowflake_key.pem

# Linux/Mac:
cp /path/to/your/key.pem secrets/snowflake_key.pem
```

### Step 3: Deploy (2 minutes)

**Windows:**
```cmd
build.bat
deploy.bat up
```

**Linux/Mac:**
```bash
chmod +x build.sh deploy.sh
./build.sh
./deploy.sh up
```

**Done!** Open http://localhost:8501

---

## 📖 Detailed Instructions

### Prerequisites

**Required:**
- Docker Desktop installed
- Google API Key
- Snowflake database credentials
- Snowflake RSA private key

**Check Docker:**
```bash
docker --version
docker-compose --version
```

### Configuration Details

#### 1. Environment Variables

Edit `deployment/.env`:

```bash
# Google API
GOOGLE_API_KEY=AIzaSyC...your_actual_key_here

# Snowflake
SNOWFLAKE_USER=your_username
SNOWFLAKE_ACCOUNT=xy12345.us-east-1
SNOWFLAKE_ROLE=ACCOUNTADMIN
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=DEV_DATA_ML_DB
SNOWFLAKE_SCHEMA=DATA_ML_SCHEMA
```

#### 2. Snowflake Private Key

Your key should look like:
```
-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC...
...
-----END PRIVATE KEY-----
```

Place it at: `deployment/secrets/snowflake_key.pem`

### Build Options

**Standard build:**
```bash
./build.sh
```

**With specific tag:**
```bash
./build.sh -t v1.0.0
```

**Without cache (clean build):**
```bash
./build.sh --no-cache
```

### Deployment Options

**Production mode:**
```bash
./deploy.sh up
```

**Development mode (with hot-reload):**
```bash
./deploy.sh -d up
```

**Custom port:**
```bash
# Edit .env
APP_PORT=8080

# Deploy
./deploy.sh up
```

---

## 🔍 Verification

### 1. Check Container Status

```bash
docker-compose ps
```

Expected output:
```
NAME                COMMAND             STATUS          PORTS
agripulse-app       streamlit run...    Up (healthy)    0.0.0.0:8501->8501/tcp
```

### 2. Check Logs

```bash
./deploy.sh logs
```

Look for:
- ✅ "You can now view your Streamlit app in your browser"
- ✅ "Network URL: http://0.0.0.0:8501"
- ❌ No ERROR messages

### 3. Test Application

**Open browser:**
```
http://localhost:8501
```

**Test queries:**
1. "What's the weather in London?"
2. "What crop types are available?"
3. "Show me yield forecasts for Dhaka"

---

## 🛠️ Common Commands

### Management

```bash
# Start services
./deploy.sh up

# Stop services
./deploy.sh down

# Restart services
./deploy.sh restart

# View logs
./deploy.sh logs

# Check status
./deploy.sh status
```

### Debugging

```bash
# Access container shell
docker exec -it agripulse-app bash

# View real-time logs
docker logs agripulse-app -f

# Check resource usage
docker stats agripulse-app

# Inspect configuration
docker-compose config
```

### Updates

```bash
# Rebuild and restart
./deploy.sh build

# Or manually
./build.sh --no-cache
./deploy.sh down
./deploy.sh up
```

---

## ❌ Troubleshooting

### Issue: Container won't start

**Check logs:**
```bash
docker-compose logs agripulse-app
```

**Common causes:**
- Missing environment variables
- Invalid Snowflake credentials
- Port 8501 already in use
- Missing private key file

### Issue: "Permission denied" on private key

**Linux/Mac:**
```bash
chmod 600 deployment/secrets/snowflake_key.pem
```

**Windows:**
```cmd
icacls deployment\secrets\snowflake_key.pem /inheritance:r /grant:r "%USERNAME%:R"
```

### Issue: Database connection failed

**Verify credentials:**
```bash
# Check if key file exists
ls -la deployment/secrets/snowflake_key.pem

# Test from container
docker exec -it agripulse-app python -c "from adk_app.core.database import get_snowflake_manager; print(get_snowflake_manager().test_connection())"
```

### Issue: Port already in use

**Find what's using the port:**
```bash
# Linux/Mac
lsof -i :8501

# Windows
netstat -ano | findstr :8501
```

**Use different port:**
```bash
# Edit .env
APP_PORT=8502

# Restart
./deploy.sh restart
```

### Issue: Build fails

**Clear Docker cache:**
```bash
docker system prune -a
./build.sh --no-cache
```

**Check disk space:**
```bash
docker system df
df -h  # Linux/Mac
```

---

## 🔄 Updating

### Update Application Code

```bash
# Pull latest code
git pull

# Rebuild
./build.sh --no-cache

# Redeploy
./deploy.sh down
./deploy.sh up
```

### Update Dependencies

```bash
# Edit pyproject.toml
# Then rebuild
./build.sh --no-cache
./deploy.sh build
```

---

## 🔒 Security Notes

### Production Deployment

1. **Use strong secrets:**
   - Don't commit `.env` to git
   - Use Docker secrets for sensitive data
   - Rotate API keys regularly

2. **Network security:**
   - Use reverse proxy (nginx/traefik)
   - Enable HTTPS/TLS
   - Restrict network access

3. **Container security:**
   - Runs as non-root user (already configured)
   - Scan images: `docker scan agripulse-ai:latest`
   - Keep base images updated

### Environment Files

**Never commit these files:**
- `deployment/.env`
- `deployment/secrets/*`
- `deployment/logs/*`

These are already in `.gitignore`

---

## 📊 Resource Requirements

### Minimum

- **CPU:** 1 core
- **RAM:** 1GB
- **Disk:** 3GB

### Recommended

- **CPU:** 2 cores
- **RAM:** 2GB
- **Disk:** 5GB

### Adjust Limits

Edit `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      cpus: '4.0'
      memory: 4G
```

---

## 🆘 Getting Help

### Check Documentation

1. Full deployment guide: `deployment/README.md`
2. Deployment checklist: `deployment/DEPLOYMENT_CHECKLIST.md`
3. Main README: `../README.md`

### Logs and Diagnostics

```bash
# Application logs
./deploy.sh logs

# Container details
docker inspect agripulse-app

# Health check
curl http://localhost:8501/_stcore/health

# Resource usage
docker stats agripulse-app
```

### Common Log Messages

**✅ Success:**
```
You can now view your Streamlit app in your browser.
Network URL: http://0.0.0.0:8501
```

**⚠️ Warning (usually safe):**
```
SNOWFLAKE_PRIVATE_KEY_FILE not set in .env, using default
```

**❌ Error (needs fixing):**
```
Failed to connect to Snowflake
Invalid API key
Permission denied
```

---

## 🎯 Next Steps

After successful deployment:

1. **Test all features:**
   - Weather queries
   - Yield predictions
   - Crop practice data

2. **Set up monitoring:**
   - Health checks
   - Log aggregation
   - Resource monitoring

3. **Configure backups:**
   - Environment files
   - Application logs
   - Database credentials

4. **Production hardening:**
   - Enable HTTPS
   - Set up reverse proxy
   - Configure firewall

---

## 📝 Quick Reference

### File Locations

```
deployment/
├── .env                    # Your configuration
├── secrets/
│   └── snowflake_key.pem  # Your private key
├── logs/                   # Application logs
├── build.sh/bat            # Build script
├── deploy.sh/bat           # Deployment script
└── docker-compose.yml      # Orchestration config
```

### URLs

- **Application:** http://localhost:8501
- **Health Check:** http://localhost:8501/_stcore/health

### Key Commands

```bash
# Build
./build.sh

# Deploy
./deploy.sh up

# Stop
./deploy.sh down

# Logs
./deploy.sh logs

# Status
./deploy.sh status
```

---

**Version:** 1.0.0  
**Last Updated:** 2025-10-07  
**Support:** See deployment/README.md for detailed help
