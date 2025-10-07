# AgriPulse AI - Deployment Files Index

Quick reference guide to all deployment files and their purposes.

## 🚀 Getting Started

**New to Docker deployment?** Start here:
1. Read [`QUICKSTART.md`](QUICKSTART.md) - 5-minute setup guide
2. Follow [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md) - Step-by-step checklist
3. Reference [`README.md`](README.md) - Complete documentation

## 📁 File Directory

### 🔧 Core Configuration Files

| File | Purpose | When to Use |
|------|---------|-------------|
| **Dockerfile** | Multi-stage Docker image definition | Building the container image |
| **.dockerignore** | Excludes files from build context | Optimizing build performance |
| **docker-compose.yml** | Production orchestration | Deploying to production |
| **docker-compose.dev.yml** | Development orchestration | Local development |
| **docker-compose.monitoring.yml** | Monitoring stack | Setting up observability |
| **streamlit_config.toml** | Streamlit server configuration | Customizing UI behavior |
| **.env.docker** | Environment variable template | Initial setup |

### 🤖 Automation Scripts

| Script | Platform | Purpose |
|--------|----------|---------|
| **build.sh** | Linux/Mac | Build Docker image |
| **build.bat** | Windows | Build Docker image |
| **deploy.sh** | Linux/Mac | Deploy and manage application |
| **deploy.bat** | Windows | Deploy and manage application |
| **healthcheck.py** | All | Health monitoring and diagnostics |

### 📚 Documentation

| Document | Audience | Content |
|----------|----------|---------|
| **QUICKSTART.md** | Beginners | 5-minute quick start |
| **README.md** | All users | Complete deployment guide |
| **DEPLOYMENT_CHECKLIST.md** | DevOps | Pre-deployment checklist |
| **DEPLOYMENT_SUMMARY.md** | Technical | Architecture overview |
| **INDEX.md** | All users | This file |

### 📊 Monitoring Configuration

| File | Purpose |
|------|---------|
| **monitoring/prometheus.yml** | Prometheus scrape configuration |
| **monitoring/grafana/datasources/prometheus.yml** | Grafana datasource setup |
| **monitoring/grafana/dashboards/dashboard.yml** | Dashboard provisioning |

### 🔒 Runtime Files (Not in Git)

| File/Directory | Purpose | Created By |
|----------------|---------|------------|
| **.env** | Your actual configuration | You (from .env.docker) |
| **secrets/** | Sensitive files (keys, certs) | You |
| **secrets/snowflake_key.pem** | Snowflake private key | You |
| **logs/** | Application logs | Container |
| **.gitignore** | Prevents committing sensitive files | Included |

## 🎯 Common Tasks

### First-Time Setup

```bash
# 1. Read quick start
cat QUICKSTART.md

# 2. Configure environment
cp .env.docker .env
nano .env

# 3. Add secrets
mkdir secrets
cp /path/to/key.pem secrets/snowflake_key.pem

# 4. Build and deploy
./build.sh
./deploy.sh up
```

**Documentation:** [`QUICKSTART.md`](QUICKSTART.md)

### Building the Image

```bash
# Standard build
./build.sh

# With custom tag
./build.sh -t v1.0.0

# Without cache
./build.sh --no-cache
```

**Script:** `build.sh` (Linux/Mac) or `build.bat` (Windows)  
**Documentation:** [`README.md#build-commands`](README.md#build-commands)

### Deploying the Application

```bash
# Production deployment
./deploy.sh up

# Development deployment
./deploy.sh -d up

# Stop services
./deploy.sh down

# View logs
./deploy.sh logs
```

**Script:** `deploy.sh` (Linux/Mac) or `deploy.bat` (Windows)  
**Configuration:** `docker-compose.yml` or `docker-compose.dev.yml`  
**Documentation:** [`README.md#deployment-options`](README.md#deployment-options)

### Health Monitoring

```bash
# Quick health check
curl http://localhost:8501/_stcore/health

# Comprehensive check
docker exec agripulse-app python deployment/healthcheck.py

# JSON output
docker exec agripulse-app python deployment/healthcheck.py --json
```

**Script:** `healthcheck.py`  
**Documentation:** [`README.md#health-checks`](README.md#health-checks)

### Setting Up Monitoring

```bash
# Deploy monitoring stack
docker-compose -f docker-compose.monitoring.yml up -d

# Access dashboards
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000
# cAdvisor: http://localhost:8080
```

**Configuration:** `docker-compose.monitoring.yml`  
**Prometheus Config:** `monitoring/prometheus.yml`  
**Documentation:** [`README.md#monitoring`](README.md#monitoring)

### Troubleshooting

```bash
# View logs
./deploy.sh logs

# Check container status
docker-compose ps

# Access container shell
docker exec -it agripulse-app bash

# Check resource usage
docker stats agripulse-app
```

**Documentation:** [`README.md#troubleshooting`](README.md#troubleshooting)

## 📖 Documentation Guide

### For Different Roles

**Developers:**
1. Start with [`QUICKSTART.md`](QUICKSTART.md)
2. Use [`docker-compose.dev.yml`](docker-compose.dev.yml) for local development
3. Reference [`README.md`](README.md) for detailed commands

**DevOps Engineers:**
1. Review [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md)
2. Study [`DEPLOYMENT_SUMMARY.md`](DEPLOYMENT_SUMMARY.md) for architecture
3. Use [`docker-compose.yml`](docker-compose.yml) for production
4. Set up monitoring with [`docker-compose.monitoring.yml`](docker-compose.monitoring.yml)

**System Administrators:**
1. Follow [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md)
2. Configure monitoring from [`docker-compose.monitoring.yml`](docker-compose.monitoring.yml)
3. Set up health checks using [`healthcheck.py`](healthcheck.py)
4. Reference [`README.md#production-best-practices`](README.md#production-best-practices)

**Managers/Stakeholders:**
1. Read [`DEPLOYMENT_SUMMARY.md`](DEPLOYMENT_SUMMARY.md) for overview
2. Review [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md) for sign-off

## 🔍 Quick Reference

### Environment Variables

**File:** `.env` (create from `.env.docker`)

**Required:**
- `GOOGLE_API_KEY`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_ROLE`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`

**Optional:**
- `APP_PORT` (default: 8501)
- `ENVIRONMENT` (default: production)
- `LOG_LEVEL` (default: INFO)

### Ports

| Service | Port | Purpose |
|---------|------|---------|
| AgriPulse App | 8501 | Main application |
| Prometheus | 9090 | Metrics collection |
| Grafana | 3000 | Visualization |
| cAdvisor | 8080 | Container metrics |
| Node Exporter | 9100 | System metrics |

### Commands Cheat Sheet

```bash
# Build
./build.sh [-t TAG] [--no-cache]

# Deploy
./deploy.sh [up|down|restart|logs|status|build] [-d]

# Health Check
docker exec agripulse-app python deployment/healthcheck.py

# Logs
docker-compose logs -f [agripulse-app]

# Shell Access
docker exec -it agripulse-app bash

# Resource Usage
docker stats agripulse-app
```

## 🎓 Learning Path

### Beginner

1. **Setup** → [`QUICKSTART.md`](QUICKSTART.md)
2. **Deploy** → Follow the 3-step guide
3. **Verify** → Check http://localhost:8501
4. **Test** → Try example queries

### Intermediate

1. **Configuration** → Customize `.env` and `streamlit_config.toml`
2. **Development** → Use `docker-compose.dev.yml`
3. **Monitoring** → Deploy monitoring stack
4. **Troubleshooting** → Use health checks and logs

### Advanced

1. **Architecture** → Study [`DEPLOYMENT_SUMMARY.md`](DEPLOYMENT_SUMMARY.md)
2. **Security** → Implement production hardening
3. **Scaling** → Configure resource limits
4. **Automation** → Set up CI/CD pipelines

## 🔗 External Resources

### Docker
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/compose-file/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

### Streamlit
- [Streamlit Docs](https://docs.streamlit.io/)
- [Streamlit Deployment](https://docs.streamlit.io/knowledge-base/tutorials/deploy)

### Monitoring
- [Prometheus Docs](https://prometheus.io/docs/)
- [Grafana Docs](https://grafana.com/docs/)

## 📞 Getting Help

### Documentation Priority

1. **Quick Issue?** → [`README.md#troubleshooting`](README.md#troubleshooting)
2. **Setup Help?** → [`QUICKSTART.md`](QUICKSTART.md)
3. **Pre-deployment?** → [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md)
4. **Architecture Questions?** → [`DEPLOYMENT_SUMMARY.md`](DEPLOYMENT_SUMMARY.md)

### Debug Steps

1. Check logs: `./deploy.sh logs`
2. Run health check: `docker exec agripulse-app python deployment/healthcheck.py`
3. Verify configuration: `docker-compose config`
4. Check container status: `docker-compose ps`
5. Review documentation: [`README.md`](README.md)

## 📝 File Modification Guide

### When to Edit

| File | Edit When | Don't Edit If |
|------|-----------|---------------|
| `.env` | Always (your config) | Using template |
| `docker-compose.yml` | Changing resources/ports | First deployment |
| `streamlit_config.toml` | Customizing UI | Using defaults |
| `Dockerfile` | Changing dependencies | Standard setup |
| Scripts (.sh/.bat) | Adding automation | Scripts work |

### Safe to Customize

✅ `.env` - Your configuration
✅ `streamlit_config.toml` - UI settings
✅ `docker-compose.yml` - Resource limits, ports
✅ `monitoring/prometheus.yml` - Scrape intervals

### Avoid Modifying

⚠️ `Dockerfile` - Unless you know Docker well
⚠️ `.dockerignore` - Optimized for this project
⚠️ Build scripts - Unless fixing bugs
⚠️ `healthcheck.py` - Core functionality

## ✅ Verification Checklist

After deployment, verify:

- [ ] Container is running: `docker-compose ps`
- [ ] Health check passes: `curl http://localhost:8501/_stcore/health`
- [ ] Application accessible: http://localhost:8501
- [ ] No errors in logs: `./deploy.sh logs`
- [ ] Database connected: Test a yield query
- [ ] API working: Test a weather query

## 🎯 Next Steps

**After successful deployment:**

1. **Test thoroughly** - All features and agents
2. **Set up monitoring** - Deploy monitoring stack
3. **Configure backups** - Environment and secrets
4. **Production hardening** - HTTPS, firewall, etc.
5. **Document procedures** - Custom runbooks

**Recommended reading order:**
1. [`QUICKSTART.md`](QUICKSTART.md) - Get started
2. [`DEPLOYMENT_CHECKLIST.md`](DEPLOYMENT_CHECKLIST.md) - Follow checklist
3. [`README.md`](README.md) - Deep dive
4. [`DEPLOYMENT_SUMMARY.md`](DEPLOYMENT_SUMMARY.md) - Understand architecture

---

**Need help?** Start with [`QUICKSTART.md`](QUICKSTART.md) or [`README.md#troubleshooting`](README.md#troubleshooting)

**Version:** 1.0.0  
**Last Updated:** 2025-10-07
