# AgriPulse AI - Docker Architecture Diagrams

Visual reference for understanding the Docker deployment architecture.

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Internet / Users                         │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ HTTP/HTTPS
                               │ Port 8501
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                        Docker Host Server                        │
│                                                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              AgriPulse AI Container                      │   │
│  │                                                           │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │         Streamlit Web Server                     │   │   │
│  │  │         (Port 8501)                              │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                        ↓                                 │   │
│  │  ┌─────────────────────────────────────────────────┐   │   │
│  │  │      Multi-Agent System (Google ADK)            │   │   │
│  │  │                                                  │   │   │
│  │  │  ┌──────────────┐  ┌──────────────┐           │   │   │
│  │  │  │ Coordinator  │  │   Weather    │           │   │   │
│  │  │  │    Agent     │→ │    Agent     │           │   │   │
│  │  │  └──────────────┘  └──────────────┘           │   │   │
│  │  │         ↓                  ↓                    │   │   │
│  │  │  ┌──────────────┐  ┌──────────────┐           │   │   │
│  │  │  │    Yield     │  │  Discovery   │           │   │   │
│  │  │  │    Agent     │  │    Tools     │           │   │   │
│  │  │  └──────────────┘  └──────────────┘           │   │   │
│  │  └─────────────────────────────────────────────────┘   │   │
│  │                                                           │   │
│  │  Mounted Volumes:                                        │   │
│  │  ├── /app/secrets (Snowflake Private Key)              │   │
│  │  └── /app/logs (Application Logs)                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                   │
└───────────────────────┬───────────────────┬─────────────────────┘
                        │                   │
                        ↓                   ↓
        ┌───────────────────────┐  ┌──────────────────┐
        │   Google AI API       │  │  Snowflake DB    │
        │   (Gemini Models)     │  │  (ML Forecasts)  │
        └───────────────────────┘  └──────────────────┘
```

## 🐳 Docker Container Architecture

### Multi-Stage Build Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 1: BUILDER                              │
├─────────────────────────────────────────────────────────────────┤
│  Base Image: python:3.13-slim                                    │
│                                                                   │
│  1. Install build dependencies                                   │
│     ├── build-essential                                          │
│     ├── curl                                                     │
│     └── git                                                      │
│                                                                   │
│  2. Install uv (fast Python package installer)                   │
│                                                                   │
│  3. Create virtual environment (/opt/venv)                       │
│                                                                   │
│  4. Install Python dependencies                                  │
│     ├── google-adk                                               │
│     ├── streamlit                                                │
│     ├── snowflake                                                │
│     └── other packages from pyproject.toml                       │
│                                                                   │
│  Size: ~2-3GB (temporary)                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    Copy virtual environment
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    STAGE 2: RUNTIME                              │
├─────────────────────────────────────────────────────────────────┤
│  Base Image: python:3.13-slim                                    │
│                                                                   │
│  1. Copy virtual environment from builder                        │
│     └── /opt/venv → /opt/venv                                    │
│                                                                   │
│  2. Copy application code                                        │
│     ├── adk_app/                                                 │
│     ├── main.py                                                  │
│     └── pyproject.toml                                           │
│                                                                   │
│  3. Create non-root user (agripulse:1000)                        │
│                                                                   │
│  4. Configure health checks                                      │
│                                                                   │
│  5. Set environment variables                                    │
│                                                                   │
│  Final Size: ~1-2GB (60% smaller!)                               │
└─────────────────────────────────────────────────────────────────┘
```

### Runtime Container Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                  AgriPulse Container                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  /opt/venv/                    ← Virtual Environment             │
│  ├── bin/                                                        │
│  │   ├── python                                                  │
│  │   ├── streamlit                                               │
│  │   └── ...                                                     │
│  └── lib/python3.13/site-packages/                              │
│      ├── google/                                                 │
│      ├── streamlit/                                              │
│      ├── snowflake/                                              │
│      └── ...                                                     │
│                                                                   │
│  /app/                         ← Application Code                │
│  ├── adk_app/                                                    │
│  │   ├── agents/                                                 │
│  │   ├── tools/                                                  │
│  │   └── core/                                                   │
│  ├── main.py                                                     │
│  ├── pyproject.toml                                              │
│  └── .streamlit/config.toml                                      │
│                                                                   │
│  /app/secrets/                 ← Mounted Volume (Read-Only)      │
│  └── snowflake_key.pem                                           │
│                                                                   │
│  /app/logs/                    ← Mounted Volume (Read-Write)     │
│  └── *.log                                                       │
│                                                                   │
│  User: agripulse (UID 1000)   ← Non-root execution              │
│  Port: 8501                    ← Exposed to host                 │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 🌐 Network Architecture

### Production Deployment

```
┌─────────────────────────────────────────────────────────────────┐
│                         Docker Host                              │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           agripulse-network (Bridge)                    │    │
│  │                                                          │    │
│  │  ┌──────────────────────────────────────────────────┐ │    │
│  │  │  agripulse-app                                    │ │    │
│  │  │  IP: 172.18.0.2                                   │ │    │
│  │  │  Port: 8501                                       │ │    │
│  │  └──────────────────────────────────────────────────┘ │    │
│  │                                                          │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↑                                     │
│                            │                                     │
│                    Port Mapping                                  │
│                    Host:8501 → Container:8501                    │
│                                                                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ↓
                    External Access
                    http://localhost:8501
```

### With Monitoring Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                         Docker Host                              │
│                                                                   │
│  ┌────────────────────────────────────────────────────────┐    │
│  │           agripulse-network (Bridge)                    │    │
│  │                                                          │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │    │
│  │  │ agripulse-app│  │  prometheus  │  │   grafana   │ │    │
│  │  │   :8501      │←─│    :9090     │←─│    :3000    │ │    │
│  │  └──────────────┘  └──────────────┘  └─────────────┘ │    │
│  │         ↑                  ↑                           │    │
│  │         │                  │                           │    │
│  │  ┌──────────────┐  ┌──────────────┐                  │    │
│  │  │   cadvisor   │  │node-exporter │                  │    │
│  │  │    :8080     │  │    :9100     │                  │    │
│  │  └──────────────┘  └──────────────┘                  │    │
│  │                                                          │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                   │
│  Port Mappings:                                                  │
│  ├── 8501 → AgriPulse App                                       │
│  ├── 9090 → Prometheus                                          │
│  ├── 3000 → Grafana                                             │
│  ├── 8080 → cAdvisor                                            │
│  └── 9100 → Node Exporter                                       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 Data Flow Architecture

### User Request Flow

```
1. User Browser
   │
   │ HTTP Request
   ↓
2. Docker Host (Port 8501)
   │
   │ Port Mapping
   ↓
3. AgriPulse Container
   │
   │ Streamlit Server
   ↓
4. Coordinator Agent
   │
   ├─→ Weather Query?
   │   │
   │   ↓
   │   Weather Agent
   │   │
   │   │ API Call
   │   ↓
   │   OpenWeather API
   │   │
   │   │ Weather Data
   │   ↓
   │   Format Response
   │
   └─→ Yield Query?
       │
       ↓
       Yield Agent
       │
       ├─→ get_yield_forecast_from_db()
       │   │
       │   │ SQL Query
       │   ↓
       │   Snowflake Database
       │   │
       │   │ Forecast Data
       │   ↓
       │   Format Results
       │
       └─→ get_crop_practice_data()
           │
           │ SQL Query
           ↓
           Snowflake Database
           │
           │ Practice Data
           ↓
           Combine & Format
           │
           ↓
5. Streamlit UI
   │
   │ Render Response
   ↓
6. User Browser
```

## 🔄 Deployment Workflow

### Build and Deploy Process

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT WORKFLOW                           │
└─────────────────────────────────────────────────────────────────┘

1. PREPARATION
   ├── Configure .env file
   ├── Add Snowflake private key
   └── Review configuration

2. BUILD PHASE
   │
   ├── ./build.sh
   │   │
   │   ├── Validate prerequisites
   │   │   ├── Docker installed?
   │   │   ├── Dockerfile exists?
   │   │   └── pyproject.toml exists?
   │   │
   │   ├── Execute multi-stage build
   │   │   ├── Stage 1: Install dependencies
   │   │   └── Stage 2: Create runtime image
   │   │
   │   └── Tag image: agripulse-ai:latest
   │
   └── Build complete ✓

3. DEPLOYMENT PHASE
   │
   ├── ./deploy.sh up
   │   │
   │   ├── Validate configuration
   │   │   ├── .env file exists?
   │   │   ├── Required variables set?
   │   │   ├── Secrets directory exists?
   │   │   └── Snowflake key present?
   │   │
   │   ├── Start services
   │   │   ├── Create network
   │   │   ├── Mount volumes
   │   │   ├── Start container
   │   │   └── Wait for health check
   │   │
   │   └── Verify deployment
   │       ├── Container running?
   │       ├── Health check passing?
   │       └── Application accessible?
   │
   └── Deployment complete ✓

4. VERIFICATION
   │
   ├── Access http://localhost:8501
   ├── Test weather queries
   ├── Test yield predictions
   └── Check logs
   
5. MONITORING (Optional)
   │
   ├── docker-compose -f docker-compose.monitoring.yml up -d
   │   │
   │   ├── Start Prometheus
   │   ├── Start Grafana
   │   ├── Start cAdvisor
   │   └── Start Node Exporter
   │
   └── Access dashboards
       ├── Prometheus: http://localhost:9090
       ├── Grafana: http://localhost:3000
       └── cAdvisor: http://localhost:8080
```

## 🔒 Security Architecture

### Security Layers

```
┌─────────────────────────────────────────────────────────────────┐
│                      SECURITY LAYERS                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Layer 1: Network Isolation                                      │
│  ├── Custom Docker bridge network                                │
│  ├── No direct internet access from container                    │
│  └── Only exposed ports accessible                               │
│                                                                   │
│  Layer 2: Container Security                                     │
│  ├── Non-root user execution (UID 1000)                          │
│  ├── Minimal base image (python:3.13-slim)                       │
│  ├── No privileged mode                                          │
│  └── Resource limits enforced                                    │
│                                                                   │
│  Layer 3: Secrets Management                                     │
│  ├── Private keys in mounted volumes                             │
│  ├── Environment variables for config                            │
│  ├── No secrets in image layers                                  │
│  └── Read-only secret mounts                                     │
│                                                                   │
│  Layer 4: Access Control                                         │
│  ├── File permissions enforced                                   │
│  ├── User isolation                                              │
│  └── Volume mount restrictions                                   │
│                                                                   │
│  Layer 5: Application Security                                   │
│  ├── CORS protection                                             │
│  ├── XSRF protection                                             │
│  ├── Input validation                                            │
│  └── Error handling                                              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 📈 Monitoring Architecture

### Metrics Collection Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    MONITORING STACK                              │
└─────────────────────────────────────────────────────────────────┘

AgriPulse Container
├── Health Endpoint (:8501/_stcore/health)
│   └─→ Prometheus scrapes every 30s
│
├── Container Metrics
│   └─→ cAdvisor collects
│       ├── CPU usage
│       ├── Memory usage
│       ├── Network I/O
│       └── Disk I/O
│
└── System Metrics
    └─→ Node Exporter collects
        ├── CPU stats
        ├── Memory stats
        ├── Disk stats
        └── Network stats

All metrics → Prometheus (Time-series DB)
                    ↓
              Grafana (Visualization)
                    ↓
              Dashboards & Alerts
```

## 🔄 Update and Maintenance Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    UPDATE WORKFLOW                               │
└─────────────────────────────────────────────────────────────────┘

1. Code Update
   ├── git pull
   └── Review changes

2. Rebuild Image
   ├── ./build.sh --no-cache
   └── New image created

3. Zero-Downtime Update (Optional)
   ├── Scale up new version
   │   └── docker-compose up -d --scale agripulse-app=2
   ├── Verify new container healthy
   └── Remove old container

4. Standard Update
   ├── ./deploy.sh down
   ├── ./deploy.sh up
   └── Verify deployment

5. Rollback (if needed)
   ├── docker tag agripulse-ai:previous agripulse-ai:latest
   ├── ./deploy.sh down
   └── ./deploy.sh up
```

---

## 📝 Legend

```
┌─────┐
│ Box │  = Component/Container
└─────┘

  ↓     = Data/Control flow

  →     = Connection/Relationship

  ├──   = Branch/Option

  :8501 = Port number

  ✓     = Completed/Success
```

---

**Version:** 1.0.0  
**Last Updated:** 2025-10-07  
**For:** AgriPulse AI Docker Deployment
