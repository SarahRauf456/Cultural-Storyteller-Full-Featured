import streamlit as st
import hashlib
from utils.database import create_user, verify_user, get_user_by_username

def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def show_login_page():
    """Display login/registration page"""
    st.markdown("""
    <div class="main-header">
        <h1>Welcome to Cultural Storyteller</h1>
        <p>Choose your journey in preserving cultural heritage</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for login options
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="story-card">
            <h3 style="color: white; text-align: center;">📖 Storyteller Login</h3>
            <p style="color: #cccccc; text-align: center;">Share your cultural stories and heritage</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("storyteller_login"):
            st.subheader("Storyteller Access")
            username = st.text_input("Username", key="st_user")
            password = st.text_input("Password", type="password", key="st_pass")
            
            col_login, col_register = st.columns(2)
            
            with col_login:
                login_clicked = st.form_submit_button("🔐 Login", use_container_width=True)
            
            with col_register:
                register_clicked = st.form_submit_button("📝 Register", use_container_width=True)
            
            if login_clicked:
                if verify_user(username, hash_password(password), "storyteller"):
                    st.session_state.authenticated = True
                    st.session_state.user_type = "storyteller"
                    st.session_state.current_user = get_user_by_username(username)
                    st.success("✅ Welcome back, Storyteller!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            
            if register_clicked:
                if username and password:
                    if len(password) < 6:
                        st.error("Password must be at least 6 characters long")
                    elif create_user(username, hash_password(password), "storyteller"):
                        st.success("✅ Storyteller account created! Please login.")
                    else:
                        st.error("❌ Username already exists")
                else:
                    st.error("❌ Please fill all fields")
    
    with col2:
        st.markdown("""
        <div class="story-card">
            <h3 style="color: white; text-align: center;">👥 Audience Login</h3>
            <p style="color: #cccccc; text-align: center;">Explore and enjoy cultural stories</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("audience_login"):
            st.subheader("Audience Access")
            username = st.text_input("Username", key="aud_user")
            password = st.text_input("Password", type="password", key="aud_pass")
            
            col_login, col_register = st.columns(2)
            
            with col_login:
                login_clicked = st.form_submit_button("🔐 Login", use_container_width=True)
            
            with col_register:
                register_clicked = st.form_submit_button("📝 Register", use_container_width=True)
            
            if login_clicked:
                if verify_user(username, hash_password(password), "audience"):
                    st.session_state.authenticated = True
                    st.session_state.user_type = "audience"
                    st.session_state.current_user = get_user_by_username(username)
                    st.success("✅ Welcome back, Audience member!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            
            if register_clicked:
                if username and password:
                    if len(password) < 6:
                        st.error("Password must be at least 6 characters long")
                    elif create_user(username, hash_password(password), "audience"):
                        st.success("✅ Audience account created! Please login.")
                    else:
                        st.error("❌ Username already exists")
                else:
                    st.error("❌ Please fill all fields")
    
    # Guest access option
    st.markdown("---")
    col_guest = st.columns([1, 2, 1])
    with col_guest[1]:
        if st.button("🎭 Continue as Guest (Limited Access)", use_container_width=True):
            st.session_state.authenticated = True
            st.session_state.user_type = "guest"
            st.session_state.current_user = {"username": "Guest", "user_type": "guest"}
            st.rerun()