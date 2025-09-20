import streamlit as st
from utils.webrtc_utils import create_webrtc_connection
import time

def show_calls_page():
    """Display video and voice calls page with avatar support"""
    user_type = st.session_state.get('user_type', 'guest')
    
    if user_type == 'guest':
        st.warning("🚫 Video/Voice calls are only available for registered users. Please login to continue.")
        return
    
    st.markdown('<div class="main-header"><h1>📞 Cultural Stories Live Sessions</h1></div>', unsafe_allow_html=True)
    
    # Call type selection
    tab1, tab2, tab3, tab4 = st.tabs(["📞 Voice Calls", "📹 Video Calls", "🎭 Avatar Sessions", "📊 Room Management"])
    
    with tab1:
        show_voice_calls()
    
    with tab2:
        show_video_calls()
    
    with tab3:
        show_avatar_sessions()
    
    with tab4:
        show_room_management()

def show_voice_calls():
    """Voice calling interface"""
    st.markdown("### 🎤 Voice Storytelling Sessions")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🎭 Active Voice Rooms")
        
        # Mock active voice rooms
        voice_rooms = [
            {
                "name": "Akbar-Birbal Tales Circle",
                "host": "RajasthanTeller",
                "participants": 8,
                "max_participants": 12,
                "topic": "Wisdom Tales",
                "language": "Hindi",
                "duration": "45 min"
            },
            {
                "name": "Panchatantra Stories",
                "host": "WisdomKeeper",
                "participants": 5,
                "max_participants": 10,
                "topic": "Moral Stories",
                "language": "English",
                "duration": "30 min"
            },
            {
                "name": "Regional Folk Tales",
                "host": "FolkMaster",
                "participants": 12,
                "max_participants": 15,
                "topic": "Folk Tales",
                "language": "Multiple",
                "duration": "60 min"
            }
        ]
        
        for room in voice_rooms:
            st.markdown(f"""
            <div class="story-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="color: white; margin: 0;">{room['name']}</h4>
                        <p style="color: #cccccc; margin: 5px 0;">Host: {room['host']} | {room['topic']}</p>
                        <div style="display: flex; gap: 15px; font-size: 0.9rem; color: #aaaaaa;">
                            <span>👥 {room['participants']}/{room['max_participants']}</span>
                            <span>🗣️ {room['language']}</span>
                            <span>⏱️ {room['duration']}</span>
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #4CAF50; font-size: 2rem;">🎤</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_join, col_listen = st.columns(2)
            with col_join:
                if st.button(f"🎤 Join Room", key=f"join_voice_{room['name']}", use_container_width=True):
                    join_voice_room(room)
            
            with col_listen:
                if st.button(f"👂 Listen Only", key=f"listen_{room['name']}", use_container_width=True):
                    listen_to_room(room)
    
    with col2:
        st.markdown("#### 🎙️ Quick Actions")
        
        # Start new room
        st.markdown("""
        <div class="story-card" style="text-align: center;">
            <h4 style="color: white;">Start New Room</h4>
            <p style="color: #cccccc;">Create your storytelling session</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎤 Create Voice Room", use_container_width=True):
            show_create_room_form("voice")
        
        # Voice settings
        st.markdown("#### 🎛️ Voice Settings")
        
        microphone_test = st.button("🎤 Test Microphone", use_container_width=True)
        if microphone_test:
            show_microphone_test()
        
        voice_quality = st.selectbox("🎧 Voice Quality", ["High", "Standard", "Low Bandwidth"])
        noise_suppression = st.checkbox("🔇 Noise Suppression", value=True)
        echo_cancellation = st.checkbox("📢 Echo Cancellation", value=True)

def show_video_calls():
    """Video calling interface"""
    st.markdown("### 📹 Video Storytelling Sessions")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 📺 Active Video Rooms")
        
        # Mock active video rooms
        video_rooms = [
            {
                "name": "Historical Figures Showcase",
                "host": "HistoryMaster",
                "participants": 6,
                "max_participants": 8,
                "topic": "Live Historical Reenactment",
                "language": "English",
                "features": ["Screen Share", "Costumes", "Props"]
            },
            {
                "name": "Interactive Mythology",
                "host": "MythTeller",
                "participants": 10,
                "max_participants": 12,
                "topic": "Mythology with Visuals",
                "language": "Hindi",
                "features": ["Visual Effects", "Multiple Cameras"]
            }
        ]
        
        for room in video_rooms:
            st.markdown(f"""
            <div class="story-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="color: white; margin: 0;">{room['name']}</h4>
                        <p style="color: #cccccc; margin: 5px 0;">Host: {room['host']} | {room['topic']}</p>
                        <div style="display: flex; gap: 15px; font-size: 0.9rem; color: #aaaaaa; margin-bottom: 5px;">
                            <span>👥 {room['participants']}/{room['max_participants']}</span>
                            <span>🗣️ {room['language']}</span>
                        </div>
                        <div style="display: flex; gap: 10px;">
                            {' '.join([f'<span style="background: rgba(255,255,255,0.2); padding: 2px 6px; border-radius: 8px; font-size: 0.8rem;">{feature}</span>' for feature in room['features']])}
                        </div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #2196F3; font-size: 2rem;">📹</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_join, col_watch = st.columns(2)
            with col_join:
                if st.button(f"📹 Join Video", key=f"join_video_{room['name']}", use_container_width=True):
                    join_video_room(room)
            
            with col_watch:
                if st.button(f"👁️ Watch Only", key=f"watch_{room['name']}", use_container_width=True):
                    watch_room(room)
    
    with col2:
        st.markdown("#### 📹 Video Controls")
        
        # Camera test
        camera_test = st.button("📸 Test Camera", use_container_width=True)
        if camera_test:
            show_camera_test()
        
        # Video settings
        video_quality = st.selectbox("📺 Video Quality", ["HD 720p", "SD 480p", "Low 360p"])
        camera_source = st.selectbox("📷 Camera", ["Default Camera", "External Camera"])
        
        # Background options
        st.markdown("#### 🖼️ Background Options")
        background_type = st.radio("Background", [
            "🎭 Real Video",
            "🖼️ Custom Background", 
            "🌫️ Blur Background",
            "🎪 Virtual Backgrounds"
        ])
        
        if background_type == "🖼️ Custom Background":
            uploaded_bg = st.file_uploader("Upload Background", type=['jpg', 'png'])
        elif background_type == "🎪 Virtual Backgrounds":
            virtual_bg = st.selectbox("Choose Virtual BG", [
                "🏰 Palace Hall", "🌅 Sunset", "📚 Library", "🏛️ Temple", "🌳 Forest"
            ])

def show_avatar_sessions():
    """Avatar-based storytelling sessions"""
    st.markdown("### 🎭 Avatar Storytelling Sessions")
    
    st.info("💡 Use animated historical figure avatars for immersive storytelling experiences!")
    
    # Avatar selection
    st.markdown("#### 👑 Choose Your Avatar")
    
    col1, col2, col3, col4 = st.columns(4)
    
    avatars = [
        {"name": "Emperor Akbar", "emoji": "👑", "description": "Wise ruler of Mughal Empire", "voice": "Royal, Authoritative"},
        {"name": "Birbal", "emoji": "🧙‍♂️", "description": "Witty advisor and poet", "voice": "Clever, Humorous"},
        {"name": "Tenali Rama", "emoji": "🎭", "description": "Court jester with wisdom", "voice": "Sharp, Playful"},
        {"name": "Rani Lakshmibai", "emoji": "⚔️", "description": "Brave warrior queen", "voice": "Strong, Inspiring"}
    ]
    
    selected_avatar = None
    
    for i, avatar in enumerate(avatars):
        with [col1, col2, col3, col4][i]:
            st.markdown(f"""
            <div class="story-card" style="text-align: center; height: 250px;">
                <div style="font-size: 4rem; margin-bottom: 15px;">{avatar['emoji']}</div>
                <h4 style="color: white; margin-bottom: 10px;">{avatar['name']}</h4>
                <p style="color: #cccccc; font-size: 0.9rem; margin-bottom: 15px;">{avatar['description']}</p>
                <p style="color: #aaaaaa; font-size: 0.8rem;"><strong>Voice:</strong> {avatar['voice']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Select {avatar['name']}", key=f"select_{i}", use_container_width=True):
                selected_avatar = avatar
                st.success(f"✅ {avatar['name']} avatar selected!")
    
    if selected_avatar:
        show_avatar_customization(selected_avatar)
    
    # Active avatar sessions
    st.markdown("#### 🎪 Active Avatar Sessions")
    
    avatar_sessions = [
        {
            "title": "Court of Akbar - Live Session",
            "avatars": ["👑 Akbar", "🧙‍♂️ Birbal", "🎭 Courtiers"],
            "participants": 15,
            "topic": "Interactive Wisdom Tales",
            "duration": "Live Now"
        },
        {
            "title": "Tenali Rama's Puzzle Hour",
            "avatars": ["🎭 Tenali Rama", "👑 King", "👥 Court"],
            "participants": 8,
            "topic": "Logic Puzzles & Stories",
            "duration": "Starting in 10 min"
        }
    ]
    
    for session in avatar_sessions:
        st.markdown(f"""
        <div class="story-card">
            <h4 style="color: white; margin-bottom: 10px;">{session['title']}</h4>
            <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                {' '.join([f'<span style="background: rgba(255,255,255,0.2); padding: 4px 8px; border-radius: 12px; font-size: 0.9rem;">{avatar}</span>' for avatar in session['avatars']])}
            </div>
            <div style="display: flex; justify-content: space-between; color: #cccccc; font-size: 0.9rem;">
                <span>👥 {session['participants']} participants</span>
                <span>🎯 {session['topic']}</span>
                <span>⏰ {session['duration']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🎭 Join Avatar Session", key=f"join_avatar_{session['title']}", use_container_width=True):
            join_avatar_session(session)

def show_avatar_customization(avatar):
    """Show avatar customization options"""
    st.markdown(f"#### 🎨 Customize {avatar['name']} Avatar")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎭 Avatar Settings**")
        
        expression_style = st.selectbox("😊 Expression Style", [
            "Wise and Calm", "Animated and Lively", "Serious and Royal", "Playful and Humorous"
        ])
        
        gesture_frequency = st.slider("👐 Gesture Frequency", 0.1, 2.0, 1.0)
        eye_contact = st.checkbox("👁️ Maintain Eye Contact", value=True)
        
        voice_pitch = st.slider("🎵 Voice Pitch", 0.5, 2.0, 1.0)
        speaking_speed = st.slider("⏩ Speaking Speed", 0.5, 2.0, 1.0)
    
    with col2:
        st.markdown("**👗 Appearance**")
        
        outfit_style = st.selectbox("👘 Outfit", [
            "Traditional Royal", "Court Dress", "Battle Attire", "Casual Traditional"
        ])
        
        background_scene = st.selectbox("🏰 Background Scene", [
            "Royal Palace", "Court Room", "Garden", "Battlefield", "Library"
        ])
        
        lighting_mood = st.selectbox("💡 Lighting", [
            "Royal Golden", "Dramatic", "Soft Natural", "Mystical"
        ])
    
    # Avatar preview
    st.markdown(f"""
    <div class="avatar-container">
        <div style="text-align: center;">
            <h3 style="color: white;">{avatar['name']} Avatar Preview</h3>
            <div style="background: linear-gradient(45deg, #667eea, #764ba2); height: 200px; border-radius: 15px; display: flex; align-items: center; justify-content: center; color: white; font-size: 3rem;">
                {avatar['emoji']}
            </div>
            <p style="color: #cccccc; margin-top: 15px;">3D Avatar with Real-time Animation</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"🎭 Start Session with {avatar['name']}", use_container_width=True):
        st.success(f"🎭 Avatar session started with {avatar['name']}!")
        show_avatar_controls()

def show_avatar_controls():
    """Show avatar control interface during session"""
    st.markdown("#### 🎮 Avatar Control Panel")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🎭 Expressions**")
        if st.button("😊 Happy", use_container_width=True):
            st.info("Avatar expression changed to happy")
        if st.button("🤔 Thoughtful", use_container_width=True):
            st.info("Avatar expression changed to thoughtful")
        if st.button("😮 Surprised", use_container_width=True):
            st.info("Avatar expression changed to surprised")
    
    with col2:
        st.markdown("**👐 Gestures**")
        if st.button("👋 Wave", use_container_width=True):
            st.info("Avatar waved")
        if st.button("👏 Applaud", use_container_width=True):
            st.info("Avatar applauded")
        if st.button("🤲 Welcome", use_container_width=True):
            st.info("Avatar made welcoming gesture")
    
    with col3:
        st.markdown("**🎵 Voice Actions**")
        if st.button("🎤 Start Speaking", use_container_width=True):
            st.info("Avatar is now speaking with lip sync")
        if st.button("🤐 Stop Speaking", use_container_width=True):
            st.info("Avatar stopped speaking")
        if st.button("🎵 Change Tone", use_container_width=True):
            st.info("Voice tone adjusted")

def show_room_management():
    """Room management interface"""
    st.markdown("### 📊 Room Management")
    
    user_type = st.session_state.get('user_type')
    
    if user_type == 'storyteller':
        # Storyteller room management
        st.markdown("#### 🏠 Your Rooms")
        
        my_rooms = [
            {"name": "Weekly Folk Tales", "type": "Voice", "participants": 12, "status": "Active"},
            {"name": "Historical Reenactment", "type": "Video", "participants": 8, "status": "Scheduled"},
            {"name": "Avatar Story Hour", "type": "Avatar", "participants": 5, "status": "Ended"}
        ]
        
        for room in my_rooms:
            status_color = {"Active": "#4CAF50", "Scheduled": "#FF9800", "Ended": "#757575"}[room['status']]
            
            st.markdown(f"""
            <div class="story-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="color: white; margin: 0;">{room['name']}</h4>
                        <p style="color: #cccccc; margin: 5px 0;">Type: {room['type']} | Participants: {room['participants']}</p>
                    </div>
                    <div style="color: {status_color}; font-weight: bold;">{room['status']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("📊 Analytics", key=f"analytics_{room['name']}", use_container_width=True):
                    show_room_analytics(room)
            
            with col2:
                if st.button("⚙️ Settings", key=f"settings_{room['name']}", use_container_width=True):
                    show_room_settings(room)
            
            with col3:
                if room['status'] == 'Active':
                    if st.button("📞 Join", key=f"manage_join_{room['name']}", use_container_width=True):
                        st.success(f"Joined {room['name']}")
    
    # Create new room
    st.markdown("#### ➕ Create New Room")
    
    with st.form("create_room"):
        col1, col2 = st.columns(2)
        
        with col1:
            room_name = st.text_input("Room Name *")
            room_type = st.selectbox("Room Type *", ["Voice", "Video", "Avatar", "Mixed"])
            max_participants = st.number_input("Max Participants", 2, 50, 10)
        
        with col2:
            room_topic = st.text_input("Topic/Theme")
            room_language = st.selectbox("Primary Language", ["Hindi", "English", "Tamil", "Bengali", "Multiple"])
            is_public = st.checkbox("Public Room", value=True)
        
        room_description = st.text_area("Room Description")
        
        # Schedule options
        schedule_now = st.radio("Schedule", ["Start Now", "Schedule for Later"], horizontal=True)
        
        if schedule_now == "Schedule for Later":
            col1, col2 = st.columns(2)
            with col1:
                schedule_date = st.date_input("Date")
            with col2:
                schedule_time = st.time_input("Time")
        
        submitted = st.form_submit_button("🚀 Create Room", use_container_width=True)
        
        if submitted and room_name and room_type:
            st.success(f"✅ Room '{room_name}' created successfully!")
            
            # Show room invite link
            invite_link = f"https://culturalstoryteller.com/room/{room_name.replace(' ', '-').lower()}"
            st.info(f"📤 Share this link: {invite_link}")

def show_create_room_form(room_type):
    """Show room creation form"""
    st.markdown(f"#### Create {room_type.title()} Room")
    
    with st.form(f"create_{room_type}_room"):
        room_name = st.text_input("Room Name")
        topic = st.text_input("Topic")
        max_participants = st.number_input("Max Participants", 2, 20, 8)
        
        submitted = st.form_submit_button("Create Room")
        
        if submitted and room_name:
            st.success(f"Room '{room_name}' created!")

def join_voice_room(room):
    """Join voice room"""
    st.success(f"🎤 Joining '{room['name']}'...")
    
    # Mock WebRTC connection
    st.markdown("""
    <div class="voice-panel">
        <div style="text-align: center; padding: 20px;">
            <h3 style="color: white;">🎤 Connected to Voice Room</h3>
            <div style="margin: 20px 0;">
                <span style="color: #4CAF50; font-size: 1.2rem;">● CONNECTED</span>
            </div>
            <div style="display: flex; justify-content: center; gap: 15px; margin-top: 20px;">
                <button style="background: #f44336; border: none; color: white; padding: 10px 15px; border-radius: 50%; font-size: 1.2rem;">🔇</button>
                <button style="background: #4CAF50; border: none; color: white; padding: 10px 15px; border-radius: 50%; font-size: 1.2rem;">🎤</button>
                <button style="background: #FF9800; border: none; color: white; padding: 10px 15px; border-radius: 50%; font-size: 1.2rem;">✋</button>
                <button style="background: #f44336; border: none; color: white; padding: 10px 15px; border-radius: 50%; font-size: 1.2rem;">📞</button>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def join_video_room(room):
    """Join video room"""
    st.success(f"📹 Joining '{room['name']}'...")
    
    # Mock video interface
    st.markdown("""
    <div style="background: black; height: 400px; border-radius: 15px; display: flex; align-items: center; justify-content: center; margin: 20px 0;">
        <div style="color: white; text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 20px;">📹</div>
            <h3>Video Room Active</h3>
            <p>Connected with {room['participants']} participants</p>
        </div>
    </div>
    """.format(room=room), unsafe_allow_html=True)
    
    # Video controls
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("🔇 Mute", use_container_width=True):
            st.info("Microphone muted")
    
    with col2:
        if st.button("📹 Camera", use_container_width=True):
            st.info("Camera toggled")
    
    with col3:
        if st.button("🖥️ Share", use_container_width=True):
            st.info("Screen sharing started")
    
    with col4:
        if st.button("✋ Raise Hand", use_container_width=True):
            st.info("Hand raised")
    
    with col5:
        if st.button("📞 Leave", use_container_width=True):
            st.success("Left the room")

def join_avatar_session(session):
    """Join avatar storytelling session"""
    st.success(f"🎭 Joining '{session['title']}'...")
    
    # Mock avatar session interface
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e3c72, #2a5298); height: 400px; border-radius: 15px; padding: 20px; margin: 20px 0;">
        <div style="text-align: center; color: white;">
            <h3>🎭 Avatar Session Active</h3>
            <div style="display: flex; justify-content: center; gap: 30px; margin: 30px 0;">
                <div style="text-align: center;">
                    <div style="font-size: 4rem;">👑</div>
                    <p>Akbar</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 4rem;">🧙‍♂️</div>
                    <p>Birbal</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 4rem;">🎭</div>
                    <p>You</p>
                </div>
            </div>
            <p>Interactive storytelling with animated avatars</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_microphone_test():
    """Show microphone test interface"""
    st.markdown("""
    <div class="voice-panel">
        <div style="text-align: center; padding: 20px;">
            <h4 style="color: white;">🎤 Microphone Test</h4>
            <div style="background: rgba(255,255,255,0.1); height: 40px; border-radius: 20px; margin: 15px 0; display: flex; align-items: center; justify-content: center;">
                <span style="color: #4CAF50;">● Listening...</span>
            </div>
            <p style="color: #cccccc;">Speak to test your microphone</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(1)
    st.success("✅ Microphone working properly!")

def show_camera_test():
    """Show camera test interface"""
    st.markdown("""
    <div style="background: black; height: 300px; border-radius: 15px; display: flex; align-items: center; justify-content: center; margin: 20px 0;">
        <div style="color: white; text-align: center;">
            <div style="font-size: 4rem;">📷</div>
            <p>Camera Preview</p>
            <p style="color: #4CAF50;">Camera Active</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ Camera working properly!")

def listen_to_room(room):
    """Listen to voice room without speaking"""
    st.info(f"👂 Listening to '{room['name']}' in listen-only mode")

def watch_room(room):
    """Watch video room without participating"""
    st.info(f"👁️ Watching '{room['name']}' in viewer mode")

def show_room_analytics(room):
    """Show room analytics"""
    st.markdown(f"#### 📊 Analytics for {room['name']}")
    st.info("Room analytics would be displayed here")

def show_room_settings(room):
    """Show room settings"""
    st.markdown(f"#### ⚙️ Settings for {room['name']}")
    st.info("Room settings would be displayed here")