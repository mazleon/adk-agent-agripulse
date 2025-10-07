# AgriPulse AI - Deployment Checklist

Complete checklist for deploying AgriPulse AI to production using Docker.

## 📋 Pre-Deployment Checklist

### ✅ Infrastructure Requirements

- [ ] Docker installed (version 20.10+)
- [ ] Docker Compose installed (version 2.0+)
- [ ] Minimum 2GB RAM available
- [ ] Minimum 2 CPU cores
- [ ] 5GB disk space available
- [ ] Port 8501 available (or custom port configured)
- [ ] Network access to:
  - [ ] Google AI API (generativelanguage.googleapis.com)
  - [ ] Snowflake database (*.snowflakecomputing.com)

### ✅ Credentials and Secrets

- [ ] Google API Key obtained
  - [ ] API key has access to Gemini models
  - [ ] API key tested and working
  
- [ ] Snowflake credentials ready
  - [ ] Username
  - [ ] Account identifier
  - [ ] Role name
  - [ ] Warehouse name
  - [ ] Database name (DEV_DATA_ML_DB)
  - [ ] Schema name (DATA_ML_SCHEMA)
  
- [ ] Snowflake private key file
  - [ ] RSA private key in PEM format
  - [ ] Key file has correct permissions (600)
  - [ ] Key matches public key in Snowflake

### ✅ Configuration Files

- [ ] `.env` file created from `.env.docker` template
- [ ] All required environment variables set
- [ ] No placeholder values remaining
- [ ] Secrets directory created (`deployment/secrets/`)
- [ ] Snowflake key copied to `deployment/secrets/snowflake_key.pem`

### ✅ Code and Dependencies

- [ ] Latest code pulled from repository
- [ ] `pyproject.toml` present and up-to-date
- [ ] `uv.lock` file present (if using uv)
- [ ] All application files present in project root

## 🚀 Deployment Steps

### Step 1: Prepare Environment

```bash
# Navigate to deployment directory
cd deployment

# Create environment file
cp .env.docker .env

# Edit with your credentials
nano .env  # or notepad .env on Windows
```

**Verify:**
- [ ] All `your_*` placeholders replaced
- [ ] No syntax errors in .env file
- [ ] File saved properly

### Step 2: Set Up Secrets

```bash
# Create secrets directory
mkdir -p secrets

# Copy Snowflake private key
cp /path/to/your/key.pem secrets/snowflake_key.pem

# Set permissions (Linux/Mac)
chmod 600 secrets/snowflake_key.pem
```

**Verify:**
- [ ] Key file exists at `deployment/secrets/snowflake_key.pem`
- [ ] Key file is readable
- [ ] Key file has correct format (PEM)

### Step 3: Build Docker Image

**Linux/Mac:**
```bash
chmod +x build.sh
./build.sh
```

**Windows:**
```cmd
build.bat
```

**Verify:**
- [ ] Build completed without errors
- [ ] Image `agripulse-ai:latest` created
- [ ] Image size reasonable (~1-2GB)

### Step 4: Test Configuration

```bash
# Validate docker-compose configuration
docker-compose config

# Check for errors
echo $?  # Should be 0
```

**Verify:**
- [ ] No YAML syntax errors
- [ ] All environment variables resolved
- [ ] Volumes and networks configured correctly

### Step 5: Deploy Application

**Linux/Mac:**
```bash
chmod +x deploy.sh
./deploy.sh up
```

**Windows:**
```cmd
deploy.bat up
```

**Verify:**
- [ ] Container started successfully
- [ ] No error messages in output
- [ ] Container shows as "healthy" after 40 seconds

### Step 6: Verify Deployment

```bash
# Check container status
docker-compose ps

# Check logs
docker-compose logs agripulse-app

# Test health endpoint
curl http://localhost:8501/_stcore/health
```

**Verify:**
- [ ] Container status is "Up" and "healthy"
- [ ] No error messages in logs
- [ ] Health endpoint returns 200 OK
- [ ] Application accessible at http://localhost:8501

### Step 7: Functional Testing

**Test Cases:**

1. **Application Access**
   - [ ] Open http://localhost:8501 in browser
   - [ ] Page loads without errors
   - [ ] UI displays correctly

2. **Weather Agent**
   - [ ] Ask: "What's the weather in London?"
   - [ ] Receives weather data
   - [ ] No API errors

3. **Yield Agent**
   - [ ] Ask: "What crop types are available?"
   - [ ] Receives crop type list
   - [ ] Database connection working

4. **Combined Query**
   - [ ] Ask: "What's the yield forecast for HYV Aman in Dhaka for 2025?"
   - [ ] Receives both forecast and practice data
   - [ ] Data formatted correctly

## 🔍 Post-Deployment Verification

### Performance Checks

```bash
# Check resource usage
docker stats agripulse-app

# Monitor for 5 minutes
# Verify:
```
- [ ] CPU usage < 50% (idle)
- [ ] Memory usage < 1GB (idle)
- [ ] No memory leaks observed

### Security Checks

- [ ] Container running as non-root user
- [ ] Secrets not exposed in logs
- [ ] Environment variables not in image layers
- [ ] No sensitive data in container inspect output

### Logging Checks

```bash
# Check log directory
ls -la logs/

# View recent logs
docker-compose logs --tail=100 agripulse-app
```

**Verify:**
- [ ] Logs being written to `deployment/logs/`
- [ ] Log level appropriate (INFO for production)
- [ ] No error or warning messages
- [ ] Timestamps correct

## 🔄 Maintenance Tasks

### Daily

- [ ] Check application health
  ```bash
  curl http://localhost:8501/_stcore/health
  ```

- [ ] Review logs for errors
  ```bash
  docker-compose logs --tail=100 | grep ERROR
  ```

### Weekly

- [ ] Check disk space
  ```bash
  df -h
  docker system df
  ```

- [ ] Review resource usage
  ```bash
  docker stats agripulse-app --no-stream
  ```

- [ ] Rotate logs if needed
  ```bash
  # Archive old logs
  tar -czf logs-$(date +%Y%m%d).tar.gz logs/
  ```

### Monthly

- [ ] Update base images
  ```bash
  docker pull python:3.13-slim
  ./build.sh --no-cache
  ```

- [ ] Review and update dependencies
  ```bash
  # Check for updates in pyproject.toml
  ```

- [ ] Backup configuration
  ```bash
  tar -czf backup-$(date +%Y%m%d).tar.gz .env secrets/
  ```

## 🚨 Rollback Procedure

If deployment fails or issues occur:

### Quick Rollback

```bash
# Stop current deployment
./deploy.sh down

# Restore previous image
docker tag agripulse-ai:previous agripulse-ai:latest

# Redeploy
./deploy.sh up
```

### Full Rollback

```bash
# Stop services
./deploy.sh down

# Remove current image
docker rmi agripulse-ai:latest

# Restore from backup
docker load < agripulse-ai-backup.tar

# Restore configuration
tar -xzf backup-YYYYMMDD.tar.gz

# Redeploy
./deploy.sh up
```

## 📊 Monitoring Setup

### Health Monitoring

Add to your monitoring system:

```yaml
# Prometheus scrape config
- job_name: 'agripulse'
  static_configs:
    - targets: ['localhost:8501']
  metrics_path: '/_stcore/health'
```

### Alerting Rules

Set up alerts for:
- [ ] Container down
- [ ] Health check failing
- [ ] High memory usage (>80%)
- [ ] High CPU usage (>80%)
- [ ] Disk space low (<10%)

## 🔐 Security Hardening

### Production Security Checklist

- [ ] Use Docker secrets instead of environment variables
- [ ] Enable TLS/SSL with reverse proxy (nginx/traefik)
- [ ] Implement rate limiting
- [ ] Set up firewall rules
- [ ] Enable audit logging
- [ ] Regular security scans
  ```bash
  docker scan agripulse-ai:latest
  ```

### Network Security

- [ ] Use internal Docker network
- [ ] Expose only necessary ports
- [ ] Implement reverse proxy
- [ ] Enable CORS restrictions
- [ ] Set up VPN for admin access

## 📝 Documentation

### Required Documentation

- [ ] Deployment architecture diagram
- [ ] Network topology diagram
- [ ] Incident response procedures
- [ ] Contact information for support
- [ ] API key rotation procedures
- [ ] Backup and recovery procedures

## ✅ Sign-Off

### Deployment Approval

- [ ] All checklist items completed
- [ ] Functional tests passed
- [ ] Performance verified
- [ ] Security checks passed
- [ ] Documentation updated
- [ ] Team notified

**Deployed By:** ___________________  
**Date:** ___________________  
**Version:** ___________________  
**Environment:** ___________________  

### Stakeholder Approval

- [ ] Technical Lead: ___________________
- [ ] DevOps Lead: ___________________
- [ ] Security Team: ___________________
- [ ] Product Owner: ___________________

---

**Next Review Date:** ___________________  
**Monitoring Dashboard:** ___________________  
**Incident Response Contact:** ___________________
