import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os

# Add the current directory to Python path to import our modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import page modules with error handling
try:
    from pages import (
        home, login, stories, upload, calls, 
        autobiography, settings, dashboard, 
        historical_figures, maps_timeline, community
    )
    from utils.auth import check_authentication
    from utils.database import init_database
    from utils.config import APP_CONFIG
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

# Configure the Streamlit page
st.set_page_config(
    page_title="Cultural Storyteller",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database on first run
init_database()

# Load custom CSS for dark gradient theme
def load_css():
    st.markdown("""
    <style>
    /* Dark gradient theme */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%);
        min-height: 100vh;
    }
    
    /* Custom sidebar */
    .css-1d391kg {
        background: linear-gradient(135deg, #0f1419 0%, #1a252f 100%);
    }
    
    /* Navigation styling */
    .nav-container {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Card styling */
    .story-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
    }
    
    .story-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        color: white;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        z-index: 1000;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .story-card {
            margin: 5px 0;
            padding: 15px;
        }
        
        .main-header h1 {
            font-size: 1.5rem;
        }
    }
    
    /* Avatar container */
    .avatar-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 300px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        margin: 20px 0;
    }
    
    /* Voice control panel */
    .voice-panel {
        background: rgba(0, 0, 0, 0.3);
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def show_splash_screen():
    """Display splash screen with branding"""
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1 style="font-size: 3rem; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.8);">
            📚 Cultural Storyteller
        </h1>
        <p style="font-size: 1.2rem; color: #cccccc; margin-top: 20px;">
            Preserving Heritage Through Digital Stories
        </p>
        <div style="margin-top: 40px;">
            <h3 style="color: #ffd700; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">
                Powered by gfd Groups
            </h3>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Enter Platform", key="splash_enter"):
        st.session_state.show_splash = False
        st.rerun()

def main():
    """Main application function"""
    load_css()
    
    # Initialize session state
    if 'show_splash' not in st.session_state:
        st.session_state.show_splash = True
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user_type' not in st.session_state:
        st.session_state.user_type = None
    
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None
    
    # Show splash screen on first visit
    if st.session_state.show_splash:
        show_splash_screen()
        return
    
    # Authentication check
    if not st.session_state.authenticated:
        login.show_login_page()
        return
    
    # Main navigation
    with st.container():
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        
        # Navigation menu
        pages = {
            "🏠 Home": "home",
            "📖 Stories": "stories", 
            "📤 Upload": "upload",
            "📞 Calls": "calls",
            "📝 Autobiography": "autobiography",
            "🏛️ Historical Figures": "historical",
            "🗺️ Maps & Timeline": "maps",
            "👥 Community": "community",
            "📊 Dashboard": "dashboard",
            "⚙️ Settings": "settings"
        }
        
        selected = option_menu(
            menu_title=None,
            options=list(pages.keys()),
            icons=None,
            menu_icon=None,
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"background-color": "transparent"},
                "icon": {"color": "white"},
                "nav-link": {
                    "color": "white",
                    "--hover-color": "#667eea",
                    "background-color": "transparent",
                    "border-radius": "10px"
                },
                "nav-link-selected": {
                    "background-color": "#667eea",
                    "color": "white"
                }
            }
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Route to selected page
    page = pages[selected]
    
    if page == "home":
        home.show_home_page()
    elif page == "stories":
        stories.show_stories_page()
    elif page == "upload":
        upload.show_upload_page()
    elif page == "calls":
        calls.show_calls_page()
    elif page == "autobiography":
        autobiography.show_autobiography_page()
    elif page == "historical":
        historical_figures.show_historical_figures_page()
    elif page == "maps":
        maps_timeline.show_maps_timeline_page()
    elif page == "community":
        community.show_community_page()
    elif page == "dashboard":
        dashboard.show_dashboard_page()
    elif page == "settings":
        settings.show_settings_page()
    
    # Footer
    st.markdown("""
    <div class="footer">
        Powered by gfd Groups | Cultural Storyteller Platform © 2025
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()