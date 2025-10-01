# 🌾 AgriPulse AI - Streamlit Web Application

## 🎯 Overview

Modern, beautiful web interface for AgriPulse AI with full dark/light mode support. Built with Streamlit for an intuitive chat-based experience.

---

## ✨ Features

### **🎨 Modern UI**
- ✅ Beautiful gradient header
- ✅ Clean, professional design
- ✅ Responsive layout
- ✅ Smooth animations and transitions

### **🌓 Theme Support**
- ✅ Automatic dark/light mode adaptation
- ✅ CSS variables for theme compatibility
- ✅ Consistent colors across themes

### **💬 Chat Interface**
- ✅ Real-time chat with AI agents
- ✅ Message history
- ✅ Typing indicators
- ✅ Error handling

### **🎛️ Interactive Features**
- ✅ Example query buttons
- ✅ Clear chat history
- ✅ Session statistics
- ✅ Database coverage info
- ✅ Quick links to documentation

### **🤖 Agent Integration**
- ✅ Multi-agent coordinator
- ✅ Weather agent
- ✅ Yield prediction agent
- ✅ Discovery tools

---

## 🚀 Quick Start

### **1. Install Dependencies**

```bash
# Install Streamlit and required packages
uv sync
```

This will install:
- `streamlit>=1.39.0`
- `streamlit-chat>=0.1.1`
- All other project dependencies

### **2. Configure Environment**

Ensure your `.env` file is configured:
```bash
# Copy example if needed
cp .env.example .env

# Edit with your credentials
nano .env
```

Required variables:
- `GOOGLE_API_KEY` - Your Google AI API key
- Snowflake credentials (for yield predictions)

### **3. Run the Application**

```bash
# Run Streamlit app
streamlit run main.py
```

Or with custom port:
```bash
streamlit run main.py --server.port 8501
```

### **4. Access the App**

Open your browser and navigate to:
```
http://localhost:8501
```

---

## 🎨 UI Components

### **Header**
- Gradient background (purple to blue)
- App title and description
- Technology badges

### **Sidebar**
- **Controls**: Clear chat history
- **Agent Info**: Available agents
- **Statistics**: Message count, query count
- **Database Coverage**: Forecasts, districts, years
- **Quick Links**: Documentation links

### **Main Chat Area**
- **Welcome Message**: Displayed when chat is empty
- **Chat Messages**: User and assistant messages
- **Chat Input**: Type your questions here
- **Loading Indicator**: Shows while agent is thinking

### **Example Queries Panel**
- **Weather Queries**: Weather-related examples
- **Yield Predictions**: Crop forecast examples
- **General**: Mixed queries

---

## 🌓 Dark/Light Mode

The app automatically adapts to Streamlit's theme settings:

### **Light Mode**
- Clean, bright interface
- High contrast for readability
- Professional appearance

### **Dark Mode**
- Easy on the eyes
- Reduced eye strain
- Modern aesthetic

### **Change Theme**
1. Click the ⋮ menu (top right)
2. Select "Settings"
3. Choose "Light" or "Dark" theme

---

## 💡 Example Queries

### **Weather Queries**
```
What's the weather in Dhaka?
Will it rain in London tomorrow?
Weather forecast for New York
```

### **Yield Predictions**
```
What crop types are available?
Show me the latest yield forecasts
What's the yield forecast for HYV Aman in Dhaka for 2025?
What districts are covered?
```

### **General Queries**
```
What can you help me with?
Show me weather and yield forecasts for Dhaka
```

---

## 🔧 Configuration

### **Page Configuration**
```python
st.set_page_config(
    page_title="AgriPulse AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### **Custom CSS**
The app uses custom CSS for:
- Chat message styling
- Button animations
- Card layouts
- Theme-adaptive colors

All CSS uses CSS variables for automatic theme adaptation:
- `var(--secondary-background-color)`
- `var(--border-color)`
- `var(--text-color)`

---

## 📊 Session State

The app maintains session state for:
- **messages**: Chat history
- **agent_runner**: ADK agent runner instance
- **conversation_count**: Number of queries
- **selected_agent**: Currently selected agent
- **theme**: Current theme preference

---

## 🎯 Key Functions

### **`initialize_session_state()`**
Initializes all session state variables

### **`get_agent_runner()`**
Creates or retrieves the ADK agent runner

### **`get_agent_response(user_message)`**
Async function to get response from agent

### **`display_header()`**
Renders the app header

### **`display_sidebar()`**
Renders sidebar with controls and info

### **`display_example_queries()`**
Shows example query buttons

### **`display_chat_interface()`**
Main chat interface

### **`display_welcome_message()`**
Welcome screen when chat is empty

---

## 🐛 Troubleshooting

### **App Won't Start**
```bash
# Check if Streamlit is installed
streamlit --version

# Reinstall if needed
uv sync
```

### **Agent Not Responding**
- Check `.env` file has `GOOGLE_API_KEY`
- Verify Snowflake credentials
- Check network connection

### **Theme Issues**
- Clear browser cache
- Restart Streamlit app
- Check Streamlit settings

### **Import Errors**
```bash
# Ensure all dependencies are installed
uv sync

# Check Python version
python --version  # Should be 3.13+
```

---

## 🚀 Advanced Usage

### **Custom Port**
```bash
streamlit run main.py --server.port 8080
```

### **External Access**
```bash
streamlit run main.py --server.address 0.0.0.0
```

### **Development Mode**
```bash
streamlit run main.py --server.runOnSave true
```

### **Production Deployment**
```bash
# With custom config
streamlit run main.py --server.headless true --server.port 8501
```

---

## 📱 Responsive Design

The app is fully responsive:
- **Desktop**: Wide layout with sidebar
- **Tablet**: Collapsible sidebar
- **Mobile**: Stacked layout, hamburger menu

---

## 🎨 Customization

### **Change Colors**
Edit the CSS gradient in `main.py`:
```python
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### **Add New Example Queries**
Update the `examples` dictionary in `display_example_queries()`:
```python
examples = {
    "Your Category": [
        "Your example query 1",
        "Your example query 2"
    ]
}
```

### **Modify Layout**
Change column ratios in `main()`:
```python
col1, col2 = st.columns([3, 1])  # Adjust ratio
```

---

## 📈 Performance

### **Optimization Tips**
- ✅ Agent runner is cached in session state
- ✅ Messages stored efficiently
- ✅ Minimal re-renders
- ✅ Async agent calls

### **Resource Usage**
- **Memory**: ~100-200 MB
- **CPU**: Low (spikes during agent calls)
- **Network**: Only for API calls

---

## 🔒 Security

### **Best Practices**
- ✅ API keys in `.env` file (not in code)
- ✅ `.env` file in `.gitignore`
- ✅ No sensitive data in session state
- ✅ Secure Snowflake connection

### **Production Considerations**
- Use environment variables
- Enable HTTPS
- Add authentication if needed
- Rate limit API calls

---

## 📚 Documentation

- [Main README](README.md)
- [Snowflake Integration](docs/SNOWFLAKE_INTEGRATION.md)
- [Discovery Tools](docs/DISCOVERY_TOOLS.md)
- [Response Format](docs/RESPONSE_FORMAT.md)

---

## 🎉 Features Checklist

- [x] Modern, beautiful UI
- [x] Dark/light mode support
- [x] Chat interface
- [x] Example queries
- [x] Session statistics
- [x] Database info display
- [x] Error handling
- [x] Loading indicators
- [x] Responsive design
- [x] Agent integration
- [x] Documentation links

---

## 🚀 Start Using

```bash
# 1. Install dependencies
uv sync

# 2. Configure environment
cp .env.example .env
# Edit .env with your credentials

# 3. Run the app
streamlit run main.py

# 4. Open browser
# Navigate to http://localhost:8501
```

---

**Your beautiful AgriPulse AI web interface is ready!** 🌾✨

Start chatting with your intelligent agricultural assistant now!
