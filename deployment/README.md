# AgriPulse AI - Docker Deployment Guide

Complete guide for deploying AgriPulse AI using Docker and Docker Compose.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Deployment Options](#deployment-options)
- [Management](#management)
- [Troubleshooting](#troubleshooting)
- [Production Best Practices](#production-best-practices)

## 🔧 Prerequisites

### Required Software

- **Docker**: Version 20.10 or higher
  ```bash
  docker --version
  ```

- **Docker Compose**: Version 2.0 or higher
  ```bash
  docker-compose --version
  ```

### Required Credentials

1. **Google API Key**: For Gemini AI models
2. **Snowflake Credentials**: Database access credentials
3. **Snowflake Private Key**: RSA private key for authentication

## 🚀 Quick Start

### 1. Prepare Configuration

```bash
cd deployment

# Copy environment template
cp .env.docker .env

# Edit configuration
nano .env  # or use your preferred editor
```

### 2. Set Up Secrets

```bash
# Create secrets directory
mkdir -p secrets

# Copy your Snowflake private key
cp /path/to/your/snowflake_key.pem secrets/snowflake_key.pem

# Set proper permissions
chmod 600 secrets/snowflake_key.pem
```

### 3. Deploy Application

```bash
# Make scripts executable
chmod +x build.sh deploy.sh

# Build Docker image
./build.sh

# Deploy with docker-compose
./deploy.sh up
```

### 4. Access Application

Open your browser and navigate to:
```
http://localhost:8501
```

## ⚙️ Configuration

### Environment Variables

Edit `deployment/.env` file:

```bash
# Application
APP_PORT=8501
ENVIRONMENT=production
LOG_LEVEL=INFO

# Google API
GOOGLE_API_KEY=your_actual_api_key_here

# Snowflake Database
SNOWFLAKE_USER=your_username
SNOWFLAKE_ACCOUNT=your_account_id
SNOWFLAKE_ROLE=your_role
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=DEV_DATA_ML_DB
SNOWFLAKE_SCHEMA=DATA_ML_SCHEMA
```

### Streamlit Configuration

Customize `deployment/streamlit_config.toml` for:
- Server settings
- Theme customization
- Performance tuning
- Security options

## 🎯 Deployment Options

### Production Deployment

```bash
# Build and deploy
./deploy.sh up

# Or manually with docker-compose
docker-compose -f docker-compose.yml --env-file .env up -d
```

### Development Deployment

```bash
# Use development configuration
./deploy.sh -d up

# Or manually
docker-compose -f docker-compose.dev.yml up -d
```

Development mode features:
- Hot-reload on code changes
- Debug logging enabled
- Source code mounted as volume
- No build caching

### Custom Port

```bash
# Change port in .env
APP_PORT=8080

# Restart services
./deploy.sh restart
```

## 🛠️ Management

### Build Commands

```bash
# Build with default settings
./build.sh

# Build with specific tag
./build.sh -t v1.0.0

# Build without cache
./build.sh --no-cache

# Build for specific platform
./build.sh -p linux/amd64
```

### Deployment Commands

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

# Rebuild and start
./deploy.sh build
```

### Docker Compose Commands

```bash
# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f agripulse-app

# Restart specific service
docker-compose restart agripulse-app

# Scale services (if needed)
docker-compose up -d --scale agripulse-app=3

# Remove volumes
docker-compose down -v
```

### Container Management

```bash
# Access container shell
docker exec -it agripulse-app bash

# View container logs
docker logs agripulse-app -f

# Inspect container
docker inspect agripulse-app

# View resource usage
docker stats agripulse-app

# Copy files from container
docker cp agripulse-app:/app/logs ./local-logs
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Container Won't Start

```bash
# Check logs
docker-compose logs agripulse-app

# Check container status
docker-compose ps

# Verify environment variables
docker-compose config
```

#### 2. Database Connection Failed

```bash
# Verify Snowflake credentials in .env
cat .env | grep SNOWFLAKE

# Check if private key exists
ls -la secrets/snowflake_key.pem

# Test from container
docker exec -it agripulse-app python -c "from adk_app.core.database import get_snowflake_manager; get_snowflake_manager().test_connection()"
```

#### 3. Port Already in Use

```bash
# Find process using port
lsof -i :8501  # Linux/Mac
netstat -ano | findstr :8501  # Windows

# Change port in .env
APP_PORT=8502

# Restart
./deploy.sh restart
```

#### 4. Permission Denied Errors

```bash
# Fix secrets permissions
chmod 600 secrets/snowflake_key.pem

# Fix script permissions
chmod +x build.sh deploy.sh

# Fix log directory permissions
chmod 755 logs/
```

#### 5. Out of Memory

```bash
# Check resource usage
docker stats

# Increase memory limit in docker-compose.yml
# Edit deploy.resources.limits.memory

# Restart with new limits
./deploy.sh restart
```

### Health Checks

```bash
# Check application health
curl http://localhost:8501/_stcore/health

# Check container health
docker inspect --format='{{.State.Health.Status}}' agripulse-app

# View health check logs
docker inspect --format='{{range .State.Health.Log}}{{.Output}}{{end}}' agripulse-app
```

### Debug Mode

```bash
# Enable debug logging
# Edit .env
LOG_LEVEL=DEBUG

# Restart services
./deploy.sh restart

# View detailed logs
./deploy.sh logs
```

## 🔒 Production Best Practices

### Security

1. **Use Secrets Management**
   ```bash
   # Use Docker secrets instead of environment variables
   echo "your_api_key" | docker secret create google_api_key -
   ```

2. **Restrict Network Access**
   ```yaml
   # In docker-compose.yml
   networks:
     agripulse-network:
       driver: bridge
       internal: true  # No external access
   ```

3. **Use Non-Root User**
   - Already configured in Dockerfile
   - Container runs as user `agripulse` (UID 1000)

4. **Scan Images for Vulnerabilities**
   ```bash
   docker scan agripulse-ai:latest
   ```

### Performance

1. **Resource Limits**
   ```yaml
   # Adjust in docker-compose.yml
   deploy:
     resources:
       limits:
         cpus: '4.0'
         memory: 4G
   ```

2. **Enable Caching**
   ```bash
   # Use BuildKit for better caching
   DOCKER_BUILDKIT=1 ./build.sh
   ```

3. **Multi-Stage Build**
   - Already implemented in Dockerfile
   - Reduces final image size by ~60%

### Monitoring

1. **Container Logs**
   ```bash
   # Centralized logging
   docker-compose logs -f > app.log
   ```

2. **Health Monitoring**
   ```bash
   # Set up monitoring with Prometheus/Grafana
   # Health endpoint: http://localhost:8501/_stcore/health
   ```

3. **Resource Monitoring**
   ```bash
   # Real-time stats
   docker stats agripulse-app
   ```

### Backup and Recovery

1. **Backup Configuration**
   ```bash
   # Backup environment and secrets
   tar -czf backup-$(date +%Y%m%d).tar.gz .env secrets/
   ```

2. **Volume Backup**
   ```bash
   # Backup logs
   docker run --rm -v agripulse-logs:/data -v $(pwd):/backup \
     alpine tar -czf /backup/logs-backup.tar.gz /data
   ```

### Updates and Maintenance

1. **Update Application**
   ```bash
   # Pull latest code
   git pull

   # Rebuild image
   ./build.sh -t v1.1.0

   # Deploy new version
   docker-compose up -d --no-deps agripulse-app
   ```

2. **Zero-Downtime Updates**
   ```bash
   # Scale up new version
   docker-compose up -d --scale agripulse-app=2

   # Remove old container
   docker stop old_container_id
   ```

## 📊 Architecture

### Container Structure

```
agripulse-app
├── Application Code (/app)
├── Virtual Environment (/opt/venv)
├── Secrets (/app/secrets) - mounted volume
├── Logs (/app/logs) - mounted volume
└── Config (/app/.streamlit)
```

### Network Architecture

```
Internet
    ↓
Port 8501
    ↓
Docker Bridge Network (agripulse-network)
    ↓
AgriPulse Container
    ↓
External Services (Google AI, Snowflake)
```

### Data Flow

```
User Request → Streamlit UI → Coordinator Agent
                                    ↓
                        ┌───────────┴───────────┐
                        ↓                       ↓
                Weather Agent            Yield Agent
                        ↓                       ↓
                OpenWeather API         Snowflake DB
```

## 🔗 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Streamlit Deployment Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy)
- [Google ADK Documentation](https://github.com/google/adk)

## 📝 File Structure

```
deployment/
├── Dockerfile                  # Multi-stage production Dockerfile
├── .dockerignore              # Build context optimization
├── docker-compose.yml         # Production orchestration
├── docker-compose.dev.yml     # Development orchestration
├── streamlit_config.toml      # Streamlit configuration
├── .env.docker                # Environment template
├── .env                       # Your actual configuration (gitignored)
├── build.sh                   # Build automation script
├── deploy.sh                  # Deployment automation script
├── README.md                  # This file
├── secrets/                   # Sensitive files (gitignored)
│   └── snowflake_key.pem     # Snowflake private key
└── logs/                      # Application logs (gitignored)
```

## 🆘 Support

For issues and questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review container logs: `./deploy.sh logs`
3. Check application documentation in `/docs`
4. Open an issue on GitHub

---

**Version**: 1.0.0  
**Last Updated**: 2025-10-07  
**Maintained By**: AgriPulse AI Team
