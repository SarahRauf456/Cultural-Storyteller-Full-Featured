import streamlit as st
from utils.database import get_recent_stories, get_user_stats
import plotly.express as px
import plotly.graph_objects as go

def show_home_page():
    """Display the home page with user-specific dashboard"""
    st.markdown('<div class="main-header"><h1>🏠 Cultural Storyteller Hub</h1></div>', unsafe_allow_html=True)
    
    user_type = st.session_state.get('user_type', 'guest')
    current_user = st.session_state.get('current_user', {})
    
    # Welcome message
    st.markdown(f"""
    <div class="story-card">
        <h2 style="color: white;">Welcome back, {current_user.get('username', 'Guest')}! 👋</h2>
        <p style="color: #cccccc;">You're logged in as a <strong>{user_type.title()}</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # User type specific dashboard
    if user_type == "storyteller":
        show_storyteller_dashboard()
    elif user_type == "audience":
        show_audience_dashboard()
    else:
        show_guest_dashboard()
    
    # Recent stories section
    show_recent_stories()
    
    # Platform statistics
    show_platform_stats()

def show_storyteller_dashboard():
    """Dashboard for storytellers"""
    st.markdown("### 📖 Your Storyteller Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Mock user stats (in real app, fetch from database)
    with col1:
        st.markdown("""
        <div class="story-card" style="text-align: center;">
            <h3 style="color: #4CAF50;">12</h3>
            <p style="color: #cccccc;">Stories Published</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="story-card" style="text-align: center;">
            <h3 style="color: #2196F3;">3,456</h3>
            <p style="color: #cccccc;">Total Views</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="story-card" style="text-align: center;">
            <h3 style="color: #FF9800;">234</h3>
            <p style="color: #cccccc;">Followers</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="story-card" style="text-align: center;">
            <h3 style="color: #9C27B0;">15</h3>
            <p style="color: #cccccc;">Badges Earned</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Create New Story", use_container_width=True):
            st.switch_page("pages/upload.py")
    
    with col2:
        if st.button("📞 Start Voice Call", use_container_width=True):
            st.switch_page("pages/calls.py")
    
    with col3:
        if st.button("📖 Write Autobiography", use_container_width=True):
            st.switch_page("pages/autobiography.py")

def show_audience_dashboard():
    """Dashboard for audience members"""
    st.markdown("### 👥 Your Audience Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="story-card" style="text-align: center;">
            <h3 style="color: #4CAF50;">45</h3>
            <p style="color: #cccccc;">Stories Read</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="story-card" style="text-align: center;">
            <h3 style="color: #2196F3;">8</h3>
            <p style="color: #cccccc;">Following</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="story-card" style="text-align: center;">
            <h3 style="color: #FF9800;">23</h3>
            <p style="color: #cccccc;">Comments Made</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="story-card" style="text-align: center;">
            <h3 style="color: #9C27B0;">12</h3>
            <p style="color: #cccccc;">Stories Saved</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick actions
    st.markdown("### 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📚 Browse Stories", use_container_width=True):
            st.switch_page("pages/stories.py")
    
    with col2:
        if st.button("🏛️ Historical Figures", use_container_width=True):
            st.switch_page("pages/historical_figures.py")
    
    with col3:
        if st.button("🗺️ Explore Timeline", use_container_width=True):
            st.switch_page("pages/maps_timeline.py")

def show_guest_dashboard():
    """Dashboard for guest users"""
    st.markdown("### 🎭 Guest Experience")
    
    st.markdown("""
    <div class="story-card">
        <h3 style="color: white;">Limited Access Mode</h3>
        <p style="color: #cccccc;">As a guest, you can browse stories and historical figures, but cannot create content or participate in calls.</p>
        <p style="color: #ffd700;">💡 Register for full access to all features!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📚 Browse Stories", use_container_width=True):
            st.switch_page("pages/stories.py")
    
    with col2:
        if st.button("🏛️ Historical Figures", use_container_width=True):
            st.switch_page("pages/historical_figures.py")

def show_recent_stories():
    """Display recent stories"""
    st.markdown("### 📰 Recent Stories")
    
    # Mock recent stories data
    recent_stories = [
        {
            "title": "The Legend of Akbar and Birbal",
            "author": "RajasthanTeller",
            "views": 1234,
            "category": "Historical",
            "region": "North India"
        },
        {
            "title": "Tales of Tenali Rama's Wit",
            "author": "SouthernSage",
            "views": 987,
            "category": "Wisdom",
            "region": "South India"
        },
        {
            "title": "The Brave Princess of Jhansi",
            "author": "WarriorStories",
            "views": 2156,
            "category": "Heroic",
            "region": "Central India"
        }
    ]
    
    for story in recent_stories:
        with st.container():
            st.markdown(f"""
            <div class="story-card">
                <h4 style="color: white; margin-bottom: 10px;">{story['title']}</h4>
                <div style="display: flex; justify-content: space-between; color: #cccccc; font-size: 0.9rem;">
                    <span>👤 {story['author']}</span>
                    <span>👁️ {story['views']} views</span>
                    <span>📍 {story['region']}</span>
                    <span>🏷️ {story['category']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show_platform_stats():
    """Display platform statistics with charts"""
    st.markdown("### 📊 Platform Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Stories by region chart
        regions = ['North India', 'South India', 'East India', 'West India', 'Central India']
        story_counts = [45, 38, 25, 32, 28]
        
        fig = px.pie(
            values=story_counts,
            names=regions,
            title="Stories by Region",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # User activity over time
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        storytellers = [20, 35, 42, 55, 68, 78]
        audience = [150, 220, 280, 340, 420, 480]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=months, y=storytellers, name='Storytellers', line=dict(color='#667eea')))
        fig.add_trace(go.Scatter(x=months, y=audience, name='Audience', line=dict(color='#764ba2')))
        
        fig.update_layout(
            title='User Growth Over Time',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            xaxis=dict(gridcolor='rgba(255,255,255,0.1)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
        )
        st.plotly_chart(fig, use_container_width=True)