# AgriPulse AI - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### 1. Setup Environment

```bash
# Make sure you're in the project directory
cd agripulse-adk-agent

# Install dependencies
uv sync

# Copy environment file and add your API key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 2. Run Your First Agent

**Option A: Weather Agent (Recommended for testing)**
```bash
uv run adk run adk_app/agents/weather
```

Then try:
- "What's the weather in London?"
- "Will it rain in Paris tomorrow?"

**Option B: Coordinator Agent (Full system)**
```bash
uv run adk run adk_app/agents/multi
```

Then try:
- "Hello, what can you do?"
- "What's the weather in Tokyo?"
- "What yield can I expect from 10 hectares of wheat?"

### 3. Run Tests

```bash
# Run all tests
uv run pytest tests/

# Run specific test
uv run pytest tests/test_weather_agent.py -v
```

## 📁 Project Structure Overview

```
adk_app/
├── agents/          # AI Agents
│   ├── weather/     # Weather specialist
│   ├── yield_agent/ # Yield prediction specialist
│   └── multi/       # Coordinator (routes to specialists)
├── tools/           # Functions agents can call
│   ├── weather_tools.py
│   └── yield_tools.py
├── config/          # YAML configurations
└── core/            # Settings and utilities
```

## 🎯 Common Tasks

### Test Weather API
```bash
uv run python -c "from adk_app.tools.weather_tools import get_weather_report; print(get_weather_report('London'))"
```

### Test Yield Prediction
```bash
uv run python -c "from adk_app.tools.yield_tools import predict_yield; print(predict_yield('wheat', 10, 'London'))"
```

### Change Model Configuration
Edit `adk_app/config/models.yaml` to use different Gemini models or adjust parameters.

## 🐛 Troubleshooting

**Issue: "No module named 'adk_app'"**
- Make sure you're running commands from the project root directory
- Run `uv sync` to ensure all dependencies are installed

**Issue: "GOOGLE_API_KEY not found"**
- Check that `.env` file exists in project root
- Verify `GOOGLE_API_KEY=your_key_here` is set in `.env`

**Issue: Agent not responding**
- Check the log file: `tail -f /var/folders/.../agents_log/agent.latest.log`
- Verify your API key is valid
- Ensure you have internet connection for weather API

## 📚 Next Steps

1. **Customize Agents**: Edit persona files in `adk_app/agents/*/persona.md`
2. **Add New Tools**: Create functions in `adk_app/tools/`
3. **Configure Models**: Adjust settings in `adk_app/config/models.yaml`
4. **Deploy**: See `README.md` for deployment options

## 💡 Example Queries

### Weather Agent
- "What's the current weather in New York?"
- "Weather forecast for London on 2025-10-10"
- "Will it rain in Mumbai tomorrow?"
- "Temperature in Berlin"

### Yield Agent
- "Expected yield for 5 hectares of corn"
- "Should I plant wheat or rice?"
- "Analyze soil conditions in California"
- "Best crop for my 20 hectare field"

### Coordinator (handles both)
- "What's the weather and what should I plant?"
- "Check weather in Paris and predict wheat yield for 15 hectares"

---

**Need help?** Check the full [README.md](README.md) or open an issue.
