import streamlit as st
from utils.database import get_all_stories, search_stories
import time

def show_stories_page():
    """Display stories page with search and filtering"""
    st.markdown('<div class="main-header"><h1>📖 Cultural Stories Library</h1></div>', unsafe_allow_html=True)
    
    # Search and filter section
    show_search_filters()
    
    # Stories grid
    show_stories_grid()

def show_search_filters():
    """Display search and filter options"""
    st.markdown("### 🔍 Discover Stories")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search_query = st.text_input("🔍 Search stories...", placeholder="Enter keywords")
    
    with col2:
        regions = ["All Regions", "North India", "South India", "East India", "West India", "Central India"]
        selected_region = st.selectbox("📍 Region", regions)
    
    with col3:
        categories = ["All Categories", "Historical", "Mythological", "Folk Tales", "Wisdom", "Heroic", "Romance"]
        selected_category = st.selectbox("🏷️ Category", categories)
    
    with col4:
        languages = ["All Languages", "Hindi", "English", "Tamil", "Bengali", "Telugu", "Marathi"]
        selected_language = st.selectbox("🗣️ Language", languages)
    
    # Apply filters button
    if st.button("🎯 Apply Filters", use_container_width=True):
        st.success(f"Filters applied! Found stories matching your criteria.")

def show_stories_grid():
    """Display stories in a grid layout"""
    st.markdown("### 📚 Featured Stories")
    
    # Mock stories data
    stories = [
        {
            "title": "The Wisdom of Akbar and Birbal",
            "author": "RajasthanTeller",
            "description": "Discover the legendary wit and wisdom of Emperor Akbar's court advisor Birbal through these timeless tales.",
            "category": "Historical",
            "region": "North India",
            "language": "Hindi",
            "views": 1234,
            "likes": 89,
            "duration": "15 min",
            "avatar": "🤴",
            "voice_available": True,
            "video_available": True
        },
        {
            "title": "Tales of Tenali Rama's Wit",
            "author": "SouthernSage", 
            "description": "Experience the clever and humorous stories of Tenali Rama, the witty courtier of Krishnadevaraya.",
            "category": "Wisdom",
            "region": "South India",
            "language": "Telugu",
            "views": 987,
            "likes": 67,
            "duration": "12 min",
            "avatar": "🧙‍♂️",
            "voice_available": True,
            "video_available": True
        },
        {
            "title": "The Brave Queen Lakshmibai",
            "author": "WarriorStories",
            "description": "The inspiring tale of Rani Lakshmibai's courage and sacrifice for her motherland.",
            "category": "Heroic",
            "region": "Central India", 
            "language": "Hindi",
            "views": 2156,
            "likes": 143,
            "duration": "20 min",
            "avatar": "👑",
            "voice_available": True,
            "video_available": True
        },
        {
            "title": "The Merchant and the Magic Lamp",
            "author": "FolkTalesMaster",
            "description": "A mystical folk tale from the streets of old Delhi about kindness and magic.",
            "category": "Folk Tales",
            "region": "North India",
            "language": "English",
            "views": 756,
            "likes": 45,
            "duration": "8 min",
            "avatar": "🪔",
            "voice_available": True,
            "video_available": False
        },
        {
            "title": "Panchatantra: The Lion and the Mouse",
            "author": "WisdomKeeper",
            "description": "Classic moral story teaching the value of kindness regardless of size or status.",
            "category": "Wisdom",
            "region": "All India",
            "language": "English",
            "views": 1876,
            "likes": 98,
            "duration": "6 min",
            "avatar": "🦁",
            "voice_available": True,
            "video_available": True
        },
        {
            "title": "The Dancing Peacock of Rajasthan",
            "author": "DesertChronicles",
            "description": "A beautiful tale of art, nature, and tradition from the royal courts of Rajasthan.",
            "category": "Folk Tales",
            "region": "West India",
            "language": "Hindi",
            "views": 543,
            "likes": 34,
            "duration": "10 min",
            "avatar": "🦚",
            "voice_available": True,
            "video_available": True
        }
    ]
    
    # Display stories in rows of 2
    for i in range(0, len(stories), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            if i < len(stories):
                display_story_card(stories[i])
        
        with col2:
            if i + 1 < len(stories):
                display_story_card(stories[i + 1])

def display_story_card(story):
    """Display individual story card"""
    st.markdown(f"""
    <div class="story-card">
        <div style="display: flex; align-items: center; margin-bottom: 15px;">
            <span style="font-size: 2rem; margin-right: 15px;">{story['avatar']}</span>
            <div>
                <h3 style="color: white; margin: 0; margin-bottom: 5px;">{story['title']}</h3>
                <p style="color: #cccccc; margin: 0; font-size: 0.9rem;">by {story['author']}</p>
            </div>
        </div>
        
        <p style="color: #cccccc; line-height: 1.6; margin-bottom: 15px;">
            {story['description']}
        </p>
        
        <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 15px;">
            <span style="background: rgba(255,255,255,0.2); padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; color: white;">
                🏷️ {story['category']}
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; color: white;">
                📍 {story['region']}
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; color: white;">
                🗣️ {story['language']}
            </span>
            <span style="background: rgba(255,255,255,0.2); padding: 4px 8px; border-radius: 12px; font-size: 0.8rem; color: white;">
                ⏱️ {story['duration']}
            </span>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; color: #cccccc; font-size: 0.9rem;">
            <span>👁️ {story['views']} views</span>
            <span>❤️ {story['likes']} likes</span>
            <div style="display: flex; gap: 5px;">
                {"🎵" if story['voice_available'] else "🔇"}
                {"📹" if story['video_available'] else "📷"}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"📖 Read", key=f"read_{story['title']}", use_container_width=True):
            show_story_viewer(story)
    
    with col2:
        if st.button(f"🎵 Listen", key=f"listen_{story['title']}", use_container_width=True):
            play_story_audio(story)
    
    with col3:
        if st.button(f"💬 Discuss", key=f"discuss_{story['title']}", use_container_width=True):
            show_story_comments(story)

def show_story_viewer(story):
    """Display full story content"""
    st.markdown(f"### 📖 {story['title']}")
    
    # Story content (mock)
    story_content = f"""
    **{story['title']}**
    *by {story['author']}*
    
    {story['description']}
    
    Once upon a time, in the grand courts of ancient India, there lived remarkable individuals whose wisdom and wit have echoed through the centuries. This is their story...
    
    [Story content would continue here with full narrative, formatted beautifully with proper paragraphs, dialogue, and cultural context]
    
    The moral of this tale teaches us valuable lessons about {story['category'].lower()} that remain relevant in our modern world.
    
    ---
    *This story has been preserved and shared through the Cultural Storyteller platform to keep our heritage alive.*
    """
    
    st.markdown(story_content)
    
    # Voice narration controls
    show_voice_controls(story)

def play_story_audio(story):
    """Play story with voice narration"""
    st.markdown(f"### 🎵 Listening to: {story['title']}")
    
    # Voice personality selection
    st.markdown("#### Choose Your Narrator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🧙‍♂️ Wise Elder", use_container_width=True):
            st.info("Playing with Wise Elder voice (Deep, slow, thoughtful)")
            show_audio_player("wise_elder")
    
    with col2:
        if st.button("👑 Royal Narrator", use_container_width=True):
            st.info("Playing with Royal Narrator voice (Dignified, clear, authoritative)")
            show_audio_player("royal")
    
    with col3:
        if st.button("🎭 Dramatic Storyteller", use_container_width=True):
            st.info("Playing with Dramatic Storyteller voice (Expressive, varied, engaging)")
            show_audio_player("dramatic")

def show_audio_player(voice_type):
    """Display audio player controls"""
    st.markdown("""
    <div class="voice-panel">
        <div style="text-align: center; padding: 20px;">
            <div style="font-size: 3rem; margin-bottom: 10px;">🎵</div>
            <p style="color: white; margin-bottom: 15px;">Audio Player</p>
            <div style="background: rgba(255,255,255,0.1); height: 40px; border-radius: 20px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                <span style="color: #4CAF50;">● Playing...</span>
            </div>
            <div style="display: flex; justify-content: center; gap: 15px;">
                <button style="background: none; border: none; color: white; font-size: 1.5rem;">⏮️</button>
                <button style="background: none; border: none; color: white; font-size: 2rem;">⏸️</button>
                <button style="background: none; border: none; color: white; font-size: 1.5rem;">⏭️</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress simulation
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.1)
        progress.progress(i + 1)
        if i == 20:  # Simulate stopping early
            break
    
    st.success("Audio preview completed! Full audio available for registered users.")

def show_voice_controls(story):
    """Display voice narration controls"""
    st.markdown("#### 🎵 Voice Narration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        voice_personalities = ["Wise Elder", "Royal Narrator", "Dramatic Storyteller", "Gentle Grandmother", "Heroic Warrior"]
        selected_voice = st.selectbox("Choose Narrator Voice", voice_personalities)
    
    with col2:
        speech_speed = st.slider("Speech Speed", 0.5, 2.0, 1.0, 0.1)
    
    if st.button("🎵 Play Narration", use_container_width=True):
        st.success(f"Playing story with {selected_voice} voice at {speech_speed}x speed")
        show_audio_player(selected_voice.lower().replace(" ", "_"))

def show_story_comments(story):
    """Display story comments and discussion"""
    st.markdown(f"### 💬 Discussion: {story['title']}")
    
    # Mock comments
    comments = [
        {
            "author": "CultureLover",
            "text": "Beautiful retelling of this classic tale! The voice narration was perfect.",
            "likes": 12,
            "time": "2 hours ago"
        },
        {
            "author": "HistoryBuff",
            "text": "I love how this story preserves the original cultural context. Thank you for sharing!",
            "likes": 8,
            "time": "5 hours ago"
        },
        {
            "author": "YoungLearner",
            "text": "My grandmother used to tell me this story. This brought back beautiful memories. ❤️",
            "likes": 15,
            "time": "1 day ago"
        }
    ]
    
    # Display comments
    for comment in comments:
        st.markdown(f"""
        <div class="story-card">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <strong style="color: white;">{comment['author']}</strong>
                <span style="color: #cccccc; font-size: 0.9rem;">{comment['time']}</span>
            </div>
            <p style="color: #cccccc; margin-bottom: 10px;">{comment['text']}</p>
            <div style="color: #cccccc; font-size: 0.9rem;">❤️ {comment['likes']} likes</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Add comment section (for registered users)
    if st.session_state.get('user_type') != 'guest':
        st.markdown("#### Add Your Comment")
        
        comment_text = st.text_area("Share your thoughts...", placeholder="What did you think of this story?")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            comment_type = st.radio("Comment Type", ["💬 Text", "🎵 Voice Note"], horizontal=True)
        
        with col2:
            if st.button("💬 Post Comment", use_container_width=True):
                if comment_text:
                    st.success("Comment posted successfully!")
                    st.rerun()
                else:
                    st.error("Please write a comment first!")
    else:
        st.info("👥 Register to join the discussion!")