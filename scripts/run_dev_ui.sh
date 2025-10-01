#!/bin/bash
# Run AgriPulse AI Development UI

echo "🌾 Starting AgriPulse AI Development UI..."

# Activate virtual environment if using uv
if command -v uv &> /dev/null; then
    uv run python -m adk_app.runners.dev_ui
else
    python -m adk_app.runners.dev_ui
fi
