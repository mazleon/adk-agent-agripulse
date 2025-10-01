# AgriPulse AI - Agricultural Intelligence Assistant

An AI-powered agricultural assistant built with Google's Agent Development Kit (ADK), providing weather information and ML-powered crop yield predictions from Snowflake database.

## Features

- 🌤️ **Weather Agent**: Real-time weather data and forecasts for agricultural planning
- 🌾 **Yield Prediction Agent**: ML-powered crop yield forecasts from Snowflake database
- 🔍 **Discovery Tools**: Explore available crop types, districts, and forecast years
- 🤖 **Coordinator Agent**: Intelligent query routing to specialized agents
- 📊 **Snowflake Integration**: Real-time access to 645+ yield forecasts across 73 districts
- 📚 **Professional Architecture**: Well-structured, maintainable codebase following ADK best practices

## 📚 Documentation

**Complete documentation is available in the [`docs/`](docs/) folder:**

- [Documentation Index](docs/README.md) - Complete documentation overview
- [Snowflake Integration Guide](docs/SNOWFLAKE_INTEGRATION.md) - Database setup and usage
- [PEM Configuration Guide](docs/PEM_CONFIG_GUIDE.md) - Dynamic credential configuration
- [Discovery Tools](docs/DISCOVERY_TOOLS.md) - Explore available data
- [Response Format Guide](docs/RESPONSE_FORMAT.md) - Standard output format
- [Quick Start Guide](QUICKSTART.md) - Get started quickly

## Project Structure

```
agripulse-adk-agent/
├── adk_app/                    # Main application package
│   ├── config/                 # Configuration files (YAML)
│   ├── core/                   # Core utilities (settings, memory, callbacks, database)
│   ├── tools/                  # ADK tools and toolsets
│   │   ├── snowflake_yield_tools.py  # Snowflake database tools
│   │   └── toolsets/          # Organized tool collections
│   ├── agents/                 # Agent definitions
│   │   ├── weather/           # Weather agent
│   │   ├── yield_agent/       # Yield prediction agent (Snowflake-powered)
│   │   └── multi/             # Multi-agent orchestration
│   ├── runners/               # Agent runners
│   └── sessions/              # Session management
├── docs/                       # Complete documentation
│   ├── README.md              # Documentation index
│   ├── SNOWFLAKE_INTEGRATION.md  # Snowflake setup guide
│   └── ...                    # Additional guides
├── scripts/                    # Utility scripts
│   ├── test_snowflake.py      # Test database connection
│   ├── test_discovery_tools.py # Test discovery features
│   └── discover_schema.py     # Database schema discovery
├── tests/                      # Test files
├── .env                       # Environment variables (not in git)
├── .env.example              # Example environment file
├── database_connection_config.pem  # Snowflake private key (not in git)
└── pyproject.toml            # Project dependencies
```

## Installation

1. **Clone the repository**
   ```bash
   cd agripulse-adk-agent
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add:
   # - GOOGLE_API_KEY (required)
   # - Snowflake credentials (for yield predictions)
   # - SNOWFLAKE_PRIVATE_KEY_FILE path
   ```

3. **Install dependencies**
   ```bash
   uv sync
   ```

## Usage

### 🌐 Streamlit Web Interface (Recommended)

**Beautiful web UI with dark/light mode support:**
```bash
streamlit run main.py
```

Then open your browser to `http://localhost:8501`

See [Streamlit App Guide](STREAMLIT_APP.md) for details.

### 🖥️ Command Line Interface

**Weather Agent:**
```bash
uv run adk run adk_app/agents/weather
```

**Yield Agent:**
```bash
uv run adk run adk_app/agents/yield_agent
```

**Coordinator Agent:**
```bash
uv run adk run adk_app/agents/multi
```

### Example Queries

**Weather Queries:**
- "What's the weather in London?"
- "Will it rain in Paris tomorrow?"
- "Weather forecast for New York on 2025-10-05"

**Yield Queries:**
- "What's the yield forecast for HYV Aman in Dhaka for 2025?"
- "Show me the latest yield forecasts"
- "What crop types are available for forecast?"
- "What districts are covered?"
- "Get yield forecast summary for Aman crop"

**General Queries (via Coordinator):**
- "Hello, what can you help me with?"
- "What's the weather in Tokyo and what yield can I expect for rice?"

## Configuration

### Models (`adk_app/config/models.yaml`)
Configure which Gemini models to use for each agent.

### Runtime (`adk_app/config/runtime.yaml`)
Configure development UI, logging, and session management.

### Agent Configs (`adk_app/config/agent-configs/`)
Declarative configurations for individual agents.

## Development

### Project Philosophy

This project follows ADK best practices:
- **Separation of Concerns**: Tools, agents, and runners are clearly separated
- **Configuration-Driven**: YAML configs for easy customization
- **Modular Design**: Easy to add new agents and tools
- **Production-Ready**: Structured for deployment to Cloud Run or Agent Engine

### Adding a New Tool

1. Create tool function in `adk_app/tools/`
2. Add to appropriate toolset in `adk_app/tools/toolsets/`
3. Tool is automatically available to agents

### Adding a New Agent

1. Create agent directory in `adk_app/agents/`
2. Add `persona.md` with instructions
3. Create `agent.py` with agent definition
4. Export in `adk_app/agents/__init__.py`

## Data Sources

### Weather API
Uses Open-Meteo (free, no API key required):
- Current weather conditions
- 7-day forecasts
- Global coverage

### Yield Predictions - Snowflake Database
Real ML-powered forecasts from Snowflake:
- **645 yield forecasts** from ML models
- **2 crop varieties**: Aman rice types
- **73 districts** across Bangladesh
- **5 years** of forecast data (2024-2028)
- **Confidence intervals** for all predictions
- **Ensemble ML models** for accuracy

See [Snowflake Integration Guide](docs/SNOWFLAKE_INTEGRATION.md) for setup.

## Testing

### Unit Tests
```bash
uv run pytest tests/
```

### Integration Tests
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

## Deployment

### Cloud Run
See `deploy/cloudrun/` for containerization.

### Agent Engine
See `deploy/agent_engine/` for Vertex AI Agent Engine deployment.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI API key for Gemini | Yes |
| `SNOWFLAKE_USER` | Snowflake username | Yes (for yield predictions) |
| `SNOWFLAKE_ACCOUNT` | Snowflake account identifier | Yes (for yield predictions) |
| `SNOWFLAKE_ROLE` | Snowflake role name | Yes (for yield predictions) |
| `SNOWFLAKE_WAREHOUSE` | Snowflake warehouse name | Yes (for yield predictions) |
| `SNOWFLAKE_DATABASE` | Snowflake database name | Yes (for yield predictions) |
| `SNOWFLAKE_SCHEMA` | Snowflake schema name | Yes (for yield predictions) |
| `SNOWFLAKE_PRIVATE_KEY_FILE` | Path to PEM file | Yes (for yield predictions) |
| `GOOGLE_CLOUD_PROJECT` | GCP project ID (for Vertex AI) | No |
| `ENVIRONMENT` | Environment (development/production) | No |
| `DEV_UI_PORT` | Port for development UI | No |

See [PEM Configuration Guide](docs/PEM_CONFIG_GUIDE.md) for details on configuring the private key file.

## Architecture

### Agent Flow

```
User Query
    ↓
Coordinator Agent
    ↓
├─→ Weather Agent → Weather Tools → Open-Meteo API
└─→ Yield Agent → Snowflake Tools → Snowflake Database (ML Forecasts)
    ↓
Response to User (Standard Format)
```

### Snowflake Integration

```
Yield Agent
    ↓
YieldToolset
    ├─→ get_yield_forecast_from_db (filtered queries)
    ├─→ get_latest_yield_forecasts (recent forecasts)
    ├─→ get_yield_forecast_summary (aggregated stats)
    ├─→ get_available_crop_types (discovery)
    ├─→ get_available_districts (discovery)
    └─→ get_available_forecast_years (discovery)
    ↓
SnowflakeConnectionManager
    ↓
Snowflake Database (DEV_DATA_ML_DB.DATA_ML_SCHEMA.STG_ML_YIELD_FORECASTS)
```

### Key Components

- **Settings**: Centralized configuration management
- **Memory**: Session state management
- **Callbacks**: Observability and logging
- **Toolsets**: Organized tool collections
- **Agents**: Specialized AI agents with personas

## License

Apache 2.0

## Contributing

Contributions welcome! Please follow the existing code structure and add tests for new features.

## Quick Start

### **Web Interface (Recommended)**
1. **Install dependencies**: `uv sync`
2. **Configure environment**: Copy `.env.example` to `.env` and add credentials
3. **Run Streamlit app**: `streamlit run main.py`
4. **Open browser**: Navigate to `http://localhost:8501`
5. **Start chatting**: Ask "What crop types are available for forecast?"

### **Command Line**
1. **Install dependencies**: `uv sync`
2. **Configure environment**: Copy `.env.example` to `.env` and add credentials
3. **Test connection**: `uv run python scripts/test_snowflake.py`
4. **Run agent**: `uv run adk run adk_app/agents/yield_agent`

See [Quick Start Guide](QUICKSTART.md) and [Streamlit App Guide](STREAMLIT_APP.md) for detailed instructions.

## Documentation

📚 **All documentation is in the [`docs/`](docs/) folder**

- [Documentation Index](docs/README.md)
- [Snowflake Integration](docs/SNOWFLAKE_INTEGRATION.md)
- [PEM Configuration](docs/PEM_CONFIG_GUIDE.md)
- [Discovery Tools](docs/DISCOVERY_TOOLS.md)
- [Response Format](docs/RESPONSE_FORMAT.md)

## Support

For issues or questions:
1. Check the [documentation](docs/README.md)
2. Review [troubleshooting guides](docs/SNOWFLAKE_INTEGRATION.md#troubleshooting)
3. Open a GitHub issue

---

Built with ❤️ using Google's Agent Development Kit (ADK) and Snowflake
