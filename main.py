"""
AgriPulse AI - Streamlit Web Application
Modern chatbot interface for agricultural intelligence assistant
"""
import streamlit as st
import asyncio
from pathlib import Path
import sys
from datetime import datetime
from typing import List, Dict, Any
import os

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from adk_app.agents import coordinator_agent
from google.adk.runners import InMemoryRunner
from google.genai import types


# Page configuration
st.set_page_config(
    page_title="AgriPulse AI - Agricultural Intelligence Assistant",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/agripulse-ai',
        'Report a bug': "https://github.com/yourusername/agripulse-ai/issues",
        'About': "# AgriPulse AI\nYour intelligent agricultural assistant powered by Google ADK and Snowflake"
    }
)

# Custom CSS for modern UI with dark/light mode support
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Chat message styling */
    .stChatMessage {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    
    /* User message - adapts to theme */
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Assistant message - adapts to theme */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: var(--secondary-background-color);
        border-left: 4px solid #667eea;
    }
    
    /* Header styling */
    .app-header {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        text-align: center;
    }
    
    /* Sidebar styling */
    .sidebar-content {
        padding: 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    /* Info boxes */
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        background-color: var(--secondary-background-color);
    }
    
    /* Stats cards */
    .stat-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
    }
    
    /* Agent selector */
    .agent-selector {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: var(--secondary-background-color);
        margin-bottom: 1rem;
    }
    
    /* Example queries */
    .example-query {
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .example-query:hover {
        transform: translateX(5px);
        border-color: #667eea;
    }
    
    /* Loading animation */
    .loading-dots {
        display: inline-block;
    }
    
    .loading-dots::after {
        content: '...';
        animation: dots 1.5s steps(4, end) infinite;
    }
    
    @keyframes dots {
        0%, 20% { content: '.'; }
        40% { content: '..'; }
        60%, 100% { content: '...'; }
    }
    
    /* Forecast card */
    .forecast-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        margin: 1rem 0;
    }
    
    /* Success/Error messages */
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .error-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "agent_runner" not in st.session_state:
        st.session_state.agent_runner = None
    
    if "user_id" not in st.session_state:
        st.session_state.user_id = "user_001"
    
    if "session_id" not in st.session_state:
        import uuid
        st.session_state.session_id = str(uuid.uuid4())
    
    if "conversation_count" not in st.session_state:
        st.session_state.conversation_count = 0
    
    if "selected_agent" not in st.session_state:
        st.session_state.selected_agent = "Multi-Agent Coordinator"
    
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    if "pending_query" not in st.session_state:
        st.session_state.pending_query = None
    
    if "session_created" not in st.session_state:
        st.session_state.session_created = False


def get_agent_runner():
    """Get or create agent runner"""
    if st.session_state.agent_runner is None:
        st.session_state.agent_runner = InMemoryRunner(agent=coordinator_agent)
        st.session_state.session_created = True
    
    return st.session_state.agent_runner


async def get_agent_response(user_message: str, retry_count: int = 0) -> str:
    """Get response from agent"""
    try:
        runner = get_agent_runner()
        response_text = ""
        
        user_id = st.session_state.user_id
        session_id = st.session_state.session_id
        
        # First, ensure the session exists by creating it if needed
        try:
            # Try to create/get the session
            session = runner.session_service.create_session(
                app_name="agripulse_ai",
                user_id=user_id,
                session_id=session_id
            )
        except Exception as session_error:
            # Session might already exist, that's okay
            pass
        
        # Create content object for the message
        new_message = types.Content(
            role="user",
            parts=[types.Part(text=user_message)]
        )
        
        # Run agent with proper parameters
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            # Extract content from event
            if hasattr(event, 'content') and event.content:
                content = event.content
                # Handle different content types
                if isinstance(content, str):
                    response_text += content
                elif hasattr(content, 'parts'):
                    for part in content.parts:
                        if hasattr(part, 'text'):
                            response_text += part.text
                elif hasattr(content, 'text'):
                    response_text += str(content.text)
                else:
                    response_text += str(content)
            elif hasattr(event, 'text') and event.text:
                response_text += str(event.text)
            elif hasattr(event, 'message') and event.message:
                response_text += str(event.message)
        
        return response_text if response_text else "I apologize, but I couldn't generate a response. Please try again."
    
    except ValueError as e:
        if "Session not found" in str(e) and retry_count == 0:
            # Session expired, create new one and retry
            import uuid
            st.session_state.session_id = str(uuid.uuid4())
            # Don't reset the runner, just use new session ID
            return await get_agent_response(user_message, retry_count=1)
        else:
            return f"❌ **Session Error:** {str(e)}\n\nPlease refresh the page to start a new session."
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        # Only show first 500 chars of traceback to avoid overwhelming the UI
        short_trace = error_details[:500] + "..." if len(error_details) > 500 else error_details
        return f"❌ **Error:** {str(e)}\n\n```\n{short_trace}\n```"


def display_header():
    """Display application header"""
    st.markdown("""
    <div class="app-header">
        <h1>🌾 AgriPulse AI</h1>
        <p>Your Intelligent Agricultural Assistant</p>
        <p style="font-size: 0.9rem; opacity: 0.9;">
            Powered by Google ADK & Snowflake ML Forecasts
        </p>
    </div>
    """, unsafe_allow_html=True)


def display_sidebar():
    """Display sidebar with controls and information"""
    with st.sidebar:
        st.markdown("### 🎛️ Controls")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.conversation_count = 0
            # Reset agent runner and create new session
            st.session_state.agent_runner = None
            st.session_state.session_created = False
            import uuid
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()
        
        st.markdown("---")
        
        # Agent information
        st.markdown("### 🤖 Available Agents")
        st.markdown("""
        <div class="info-box">
            <strong>🌤️ Weather Agent</strong><br>
            Real-time weather data and forecasts
        </div>
        <div class="info-box">
            <strong>🌾 Yield Agent</strong><br>
            ML-powered crop yield predictions
        </div>
        <div class="info-box">
            <strong>🔍 Discovery Tools</strong><br>
            Explore available data
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Statistics
        st.markdown("### 📊 Session Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Messages", len(st.session_state.messages))
        with col2:
            st.metric("Queries", st.session_state.conversation_count)
        
        st.markdown("---")
        
        # Database info
        st.markdown("### 📈 Database Coverage")
        st.markdown("""
        <div class="stat-card">
            <h3>645</h3>
            <p>Yield Forecasts</p>
        </div>
        <div class="stat-card">
            <h3>73</h3>
            <p>Districts</p>
        </div>
        <div class="stat-card">
            <h3>5</h3>
            <p>Years (2024-2028)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Quick links
        st.markdown("### 🔗 Quick Links")
        st.markdown("""
        - [📚 Documentation](docs/README.md)
        - [🔧 Setup Guide](docs/SNOWFLAKE_INTEGRATION.md)
        - [🔍 Discovery Tools](docs/DISCOVERY_TOOLS.md)
        """)


def display_example_queries():
    """Display example queries"""
    st.markdown("### 💡 Example Queries")
    
    examples = {
        "Weather": [
            "What's the weather in Dhaka?",
            "Will it rain in London tomorrow?",
            "Weather forecast for New York"
        ],
        "Yield Predictions": [
            "What crop types are available?",
            "Show me the latest yield forecasts",
            "What's the yield forecast for HYV Aman in Dhaka for 2025?",
            "What districts are covered?"
        ],
        "General": [
            "What can you help me with?",
            "Show me weather and yield forecasts for Dhaka"
        ]
    }
    
    for category, queries in examples.items():
        with st.expander(f"📌 {category}", expanded=False):
            for query in queries:
                if st.button(query, key=f"example_{query}", use_container_width=True):
                    # Set a flag to process this query
                    st.session_state.pending_query = query
                    st.rerun()


def display_chat_interface():
    """Display main chat interface"""
    # Check if there's a pending query from example buttons
    if st.session_state.pending_query:
        prompt = st.session_state.pending_query
        st.session_state.pending_query = None
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.conversation_count += 1
        
        # Get and display assistant response
        with st.spinner("Thinking..."):
            response = asyncio.run(get_agent_response(prompt))
            st.session_state.messages.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me about weather or crop yield predictions..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.conversation_count += 1
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = asyncio.run(get_agent_response(prompt))
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})


def display_welcome_message():
    """Display welcome message when chat is empty"""
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1rem;">
            <h2>👋 Welcome to AgriPulse AI!</h2>
            <p style="font-size: 1.1rem; color: #666; margin: 1rem 0;">
                I'm your intelligent agricultural assistant. I can help you with:
            </p>
            <div style="display: flex; justify-content: center; gap: 2rem; margin: 2rem 0; flex-wrap: wrap;">
                <div class="forecast-card" style="flex: 1; min-width: 250px;">
                    <h3>🌤️ Weather Information</h3>
                    <p>Real-time weather data and forecasts for agricultural planning</p>
                </div>
                <div class="forecast-card" style="flex: 1; min-width: 250px;">
                    <h3>🌾 Yield Predictions</h3>
                    <p>ML-powered crop yield forecasts from Snowflake database</p>
                </div>
                <div class="forecast-card" style="flex: 1; min-width: 250px;">
                    <h3>🔍 Data Discovery</h3>
                    <p>Explore available crop types, districts, and forecast years</p>
                </div>
            </div>
            <p style="font-size: 1rem; color: #888;">
                💬 Start by typing a question below or try one of the example queries from the sidebar!
            </p>
        </div>
        """, unsafe_allow_html=True)


def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Display header
    display_header()
    
    # Create layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display welcome message or chat
        if len(st.session_state.messages) == 0:
            display_welcome_message()
        
        # Chat interface
        display_chat_interface()
    
    with col2:
        # Example queries
        display_example_queries()
    
    # Sidebar
    display_sidebar()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; padding: 1rem;">
        <p>Built with ❤️ using Google's Agent Development Kit (ADK) and Snowflake</p>
        <p style="font-size: 0.9rem;">
            🌾 AgriPulse AI | Version 1.0.0 | 
            <a href="docs/README.md" style="color: #667eea;">Documentation</a>
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
