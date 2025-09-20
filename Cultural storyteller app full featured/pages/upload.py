import streamlit as st
from utils.ai_content import generate_story_content, generate_story_images
from utils.voice_synthesis import get_available_voices, synthesize_speech
from utils.database import save_story
import time

def show_upload_page():
    """Display story upload/creation page"""
    user_type = st.session_state.get('user_type', 'guest')
    
    if user_type == 'guest':
        st.warning("🚫 Story creation is only available for registered users. Please login to continue.")
        return
    
    st.markdown('<div class="main-header"><h1>📤 Create Your Cultural Story</h1></div>', unsafe_allow_html=True)
    
    # Story creation tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Manual Creation", "🤖 AI Assistant", "🎵 Voice Recording", "🖼️ Visual Story"])
    
    with tab1:
        show_manual_story_creation()
    
    with tab2:
        show_ai_story_creation()
    
    with tab3:
        show_voice_recording()
    
    with tab4:
        show_visual_story_creation()

def show_manual_story_creation():
    """Manual story creation form"""
    st.markdown("### ✍️ Write Your Story Manually")
    
    with st.form("manual_story_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("📖 Story Title *", placeholder="Enter your story title")
            category = st.selectbox("🏷️ Category *", [
                "Historical", "Mythological", "Folk Tales", "Wisdom", 
                "Heroic", "Romance", "Family Heritage", "Regional Tales"
            ])
            region = st.selectbox("📍 Region *", [
                "North India", "South India", "East India", "West India", 
                "Central India", "Northeast India", "Pan-Indian"
            ])
        
        with col2:
            language = st.selectbox("🗣️ Primary Language *", [
                "Hindi", "English", "Tamil", "Bengali", "Telugu", "Marathi",
                "Gujarati", "Malayalam", "Kannada", "Punjabi", "Other"
            ])
            estimated_duration = st.selectbox("⏱️ Estimated Duration", [
                "Less than 5 minutes", "5-10 minutes", "10-15 minutes", 
                "15-20 minutes", "20+ minutes"
            ])
            tags = st.text_input("🏷️ Tags", placeholder="Enter tags separated by commas")
        
        description = st.text_area(
            "📝 Story Description *", 
            placeholder="Provide a brief description of your story...",
            height=100
        )
        
        story_content = st.text_area(
            "📚 Full Story Content *", 
            placeholder="Write your complete story here...",
            height=400
        )
        
        # Story settings
        st.markdown("#### 🎛️ Story Settings")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            enable_voice = st.checkbox("🎵 Enable Voice Narration", value=True)
            enable_comments = st.checkbox("💬 Allow Comments", value=True)
        
        with col2:
            is_public = st.checkbox("🌍 Make Public", value=True)
            allow_remixing = st.checkbox("🔄 Allow Remixing", value=False)
        
        with col3:
            adult_content = st.checkbox("🔞 Contains Adult Themes", value=False)
            educational = st.checkbox("🎓 Educational Content", value=False)
        
        submitted = st.form_submit_button("🚀 Publish Story", use_container_width=True)
        
        if submitted:
            if title and category and region and language and description and story_content:
                # Process the story
                with st.spinner("📝 Publishing your story..."):
                    time.sleep(2)  # Simulate processing
                    
                    story_data = {
                        "title": title,
                        "category": category,
                        "region": region,
                        "language": language,
                        "description": description,
                        "content": story_content,
                        "tags": tags.split(",") if tags else [],
                        "duration": estimated_duration,
                        "settings": {
                            "voice_enabled": enable_voice,
                            "comments_enabled": enable_comments,
                            "is_public": is_public,
                            "allow_remixing": allow_remixing,
                            "adult_content": adult_content,
                            "educational": educational
                        }
                    }
                    
                    # Save to database (mock)
                    save_story(story_data, st.session_state.current_user['username'])
                
                st.success("✅ Story published successfully!")
                
                # Show voice generation options
                if enable_voice:
                    show_voice_generation_options(story_data)
                
            else:
                st.error("❌ Please fill in all required fields marked with *")

def show_ai_story_creation():
    """AI-assisted story creation"""
    st.markdown("### 🤖 AI Story Assistant")
    
    st.info("💡 Let AI help you create compelling cultural stories based on your prompts!")
    
    with st.form("ai_story_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            story_prompt = st.text_area(
                "🎯 Story Prompt *",
                placeholder="Describe the story you want to create. E.g., 'A tale about a brave princess from medieval Kashmir who saves her kingdom'",
                height=150
            )
            
            story_type = st.selectbox("📚 Story Type", [
                "Historical Fiction", "Mythology Retelling", "Folk Tale", 
                "Wisdom Story", "Heroic Adventure", "Family Saga"
            ])
        
        with col2:
            target_audience = st.selectbox("👥 Target Audience", [
                "Children (5-12)", "Teenagers (13-18)", "Adults (18+)", "All Ages"
            ])
            
            story_length = st.selectbox("📏 Story Length", [
                "Short (500 words)", "Medium (1000 words)", 
                "Long (2000 words)", "Epic (3000+ words)"
            ])
            
            cultural_context = st.text_input(
                "🏛️ Cultural Context",
                placeholder="E.g., Mughal era, South Indian traditions, Bengali heritage"
            )
        
        ai_style = st.selectbox("✍️ Writing Style", [
            "Traditional Storytelling", "Modern Narrative", "Poetic", 
            "Conversational", "Dramatic", "Humorous"
        ])
        
        generate_images = st.checkbox("🎨 Generate Story Images", value=True)
        generate_voice = st.checkbox("🎵 Generate Voice Narration", value=True)
        
        submitted = st.form_submit_button("🎨 Generate Story", use_container_width=True)
        
        if submitted:
            if story_prompt:
                with st.spinner("🤖 AI is crafting your story..."):
                    # Simulate AI story generation
                    generated_story = generate_story_content(
                        prompt=story_prompt,
                        story_type=story_type,
                        length=story_length,
                        style=ai_style,
                        cultural_context=cultural_context
                    )
                    
                    time.sleep(3)  # Simulate processing time
                
                st.success("✅ Story generated successfully!")
                
                # Display generated content
                st.markdown("#### 📖 Generated Story")
                st.markdown(f"**Title:** {generated_story['title']}")
                st.markdown(f"**Description:** {generated_story['description']}")
                
                with st.expander("📚 View Full Story Content"):
                    st.markdown(generated_story['content'])
                
                # Image generation
                if generate_images:
                    st.markdown("#### 🎨 Generated Images")
                    show_generated_images(story_prompt)
                
                # Voice generation options
                if generate_voice:
                    st.markdown("#### 🎵 Voice Generation")
                    show_ai_voice_options(generated_story)
                
                # Allow editing and publishing
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✏️ Edit Story", use_container_width=True):
                        st.info("Story loaded in editor for customization!")
                
                with col2:
                    if st.button("🚀 Publish Story", use_container_width=True):
                        st.success("Story published to your profile!")
                
            else:
                st.error("❌ Please provide a story prompt!")

def show_voice_recording():
    """Voice recording interface"""
    st.markdown("### 🎤 Record Your Voice Story")
    
    st.info("🎵 Record your story directly or upload audio files for processing!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🎤 Live Recording")
        
        # Mock recording interface
        st.markdown("""
        <div class="voice-panel">
            <div style="text-align: center; padding: 30px;">
                <div style="font-size: 4rem; margin-bottom: 20px;">🎤</div>
                <h3 style="color: white; margin-bottom: 20px;">Ready to Record</h3>
                <div style="margin-bottom: 20px;">
                    <button style="background: #f44336; border: none; color: white; padding: 15px 30px; border-radius: 50px; font-size: 1.1rem; cursor: pointer;">
                        ● Start Recording
                    </button>
                </div>
                <p style="color: #cccccc; font-size: 0.9rem;">Click to start recording your story</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Recording controls
        recording_quality = st.selectbox("🎧 Recording Quality", ["High Quality", "Standard", "Mobile Optimized"])
        
        enable_noise_reduction = st.checkbox("🔇 Enable Noise Reduction", value=True)
        auto_transcribe = st.checkbox("📝 Auto-generate Transcript", value=True)
    
    with col2:
        st.markdown("#### 📁 Upload Audio File")
        
        audio_file = st.file_uploader(
            "Choose audio file", 
            type=['mp3', 'wav', 'ogg', 'm4a'],
            help="Upload your pre-recorded story audio"
        )
        
        if audio_file:
            st.audio(audio_file)
            
            # Audio processing options
            st.markdown("##### 🎛️ Audio Processing")
            
            enhance_audio = st.checkbox("✨ Enhance Audio Quality", value=True)
            remove_silence = st.checkbox("🤐 Remove Long Silences", value=True)
            normalize_volume = st.checkbox("🔊 Normalize Volume", value=True)
            
            if st.button("🎵 Process Audio", use_container_width=True):
                with st.spinner("🎵 Processing your audio..."):
                    time.sleep(2)
                st.success("Audio processed successfully!")
    
    # Story metadata for voice recordings
    st.markdown("#### 📋 Story Information")
    
    with st.form("voice_story_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("📖 Story Title *")
            category = st.selectbox("🏷️ Category *", [
                "Oral Tradition", "Personal Story", "Family History", 
                "Historical Account", "Folk Song", "Prayer/Chant"
            ])
        
        with col2:
            language = st.selectbox("🗣️ Language *", [
                "Hindi", "English", "Tamil", "Bengali", "Regional Dialect"
            ])
            region = st.selectbox("📍 Origin Region", [
                "North India", "South India", "East India", "West India"
            ])
        
        description = st.text_area("📝 Story Description")
        
        submitted = st.form_submit_button("🎤 Publish Voice Story", use_container_width=True)
        
        if submitted and title:
            st.success("🎵 Voice story published successfully!")

def show_visual_story_creation():
    """Visual story creation with image uploads and 3D transformation"""
    st.markdown("### 🖼️ Create Visual Stories")
    
    st.info("📸 Upload images and transform them into immersive 3D visual stories!")
    
    tab1, tab2, tab3 = st.tabs(["📸 Image Upload", "🌍 3D Transformation", "🎬 Story Assembly"])
    
    with tab1:
        st.markdown("#### 📸 Upload Your Images")
        
        uploaded_images = st.file_uploader(
            "Choose images for your story",
            type=['jpg', 'jpeg', 'png', 'bmp'],
            accept_multiple_files=True,
            help="Upload multiple images to create your visual story"
        )
        
        if uploaded_images:
            st.markdown(f"📁 **{len(uploaded_images)} images uploaded**")
            
            # Display uploaded images
            cols = st.columns(3)
            for i, image in enumerate(uploaded_images):
                with cols[i % 3]:
                    st.image(image, caption=f"Image {i+1}", use_column_width=True)
            
            # Image processing options
            st.markdown("##### 🎨 Image Enhancement")
            
            col1, col2 = st.columns(2)
            
            with col1:
                enhance_quality = st.checkbox("✨ AI Enhancement", value=True)
                color_correction = st.checkbox("🎨 Color Correction", value=True)
            
            with col2:
                add_effects = st.checkbox("🌟 Add Visual Effects", value=False)
                auto_crop = st.checkbox("✂️ Smart Cropping", value=True)
    
    with tab2:
        st.markdown("#### 🌍 3D Transformation")
        
        if 'uploaded_images' in locals() and uploaded_images:
            st.success("🎯 Images ready for 3D transformation!")
            
            # 3D conversion options
            col1, col2 = st.columns(2)
            
            with col1:
                depth_intensity = st.slider("🏔️ Depth Intensity", 0.1, 2.0, 1.0)
                parallax_effect = st.selectbox("🌊 Parallax Effect", [
                    "Subtle", "Moderate", "Dramatic", "Custom"
                ])
            
            with col2:
                lighting_setup = st.selectbox("💡 3D Lighting", [
                    "Natural", "Dramatic", "Soft", "Historical"
                ])
                camera_movement = st.selectbox("📹 Camera Animation", [
                    "Static", "Slow Pan", "Zoom In", "Cinematic"
                ])
            
            if st.button("🌍 Generate 3D Scenes", use_container_width=True):
                with st.spinner("🌍 Converting images to 3D..."):
                    time.sleep(3)
                
                st.success("✅ 3D scenes generated successfully!")
                
                # Mock 3D preview
                st.markdown("""
                <div class="avatar-container">
                    <div style="text-align: center;">
                        <h3 style="color: white;">🌍 3D Scene Preview</h3>
                        <p style="color: #cccccc;">Interactive 3D scene generated from your images</p>
                        <div style="background: linear-gradient(45deg, #667eea, #764ba2); height: 200px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-size: 1.2rem;">
                            🏛️ Interactive 3D Scene
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📸 Please upload images first in the Image Upload tab")
    
    with tab3:
        st.markdown("#### 🎬 Assemble Your Visual Story")
        
        with st.form("visual_story_form"):
            story_title = st.text_input("📖 Visual Story Title *")
            
            col1, col2 = st.columns(2)
            
            with col1:
                story_sequence = st.text_area(
                    "📋 Scene Sequence",
                    placeholder="Describe how images should be sequenced...",
                    height=150
                )
                
                background_music = st.selectbox("🎵 Background Music", [
                    "None", "Traditional Indian", "Peaceful Ambient", 
                    "Epic Orchestral", "Folk Melodies"
                ])
            
            with col2:
                narration_text = st.text_area(
                    "🎤 Narration Text",
                    placeholder="Write narration for each scene...",
                    height=150
                )
                
                transition_style = st.selectbox("🔄 Transition Style", [
                    "Fade", "Slide", "3D Rotation", "Cinematic Wipe"
                ])
            
            export_format = st.selectbox("📤 Export Format", [
                "Interactive Web Story", "MP4 Video", "3D VR Experience", "PDF Storybook"
            ])
            
            submitted = st.form_submit_button("🎬 Create Visual Story", use_container_width=True)
            
            if submitted and story_title:
                with st.spinner("🎬 Creating your visual story..."):
                    time.sleep(4)
                
                st.success("🎬 Visual story created successfully!")
                
                # Download options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button("📥 Download Story", "story_data", "story.html")
                
                with col2:
                    if st.button("🌍 Publish Online", use_container_width=True):
                        st.success("Story published to your profile!")
                
                with col3:
                    if st.button("📤 Share Link", use_container_width=True):
                        st.info("Story link copied to clipboard!")

def show_voice_generation_options(story_data):
    """Show voice generation options for stories"""
    st.markdown("#### 🎵 Generate Voice Narration")
    
    available_voices = get_available_voices()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        voice_personality = st.selectbox("🎭 Voice Personality", available_voices)
    
    with col2:
        speech_speed = st.slider("⏩ Speech Speed", 0.5, 2.0, 1.0, 0.1)
    
    with col3:
        add_music = st.checkbox("🎵 Add Background Music", value=False)
    
    if st.button("🎤 Generate Voice Narration", use_container_width=True):
        with st.spinner("🎵 Generating voice narration..."):
            # Simulate voice generation
            synthesize_speech(story_data['content'], voice_personality, speech_speed)
            time.sleep(3)
        
        st.success("🎵 Voice narration generated successfully!")
        
        # Play generated audio
        st.audio("data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+L2wWoWOqDY")

def show_generated_images(prompt):
    """Display AI generated images for stories"""
    st.markdown("🎨 Generating images for your story...")
    
    with st.spinner("🎨 Creating visual elements..."):
        time.sleep(2)
    
    # Mock generated images
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="height: 200px; background: linear-gradient(135deg, #ff9a9e, #fecfef); border-radius: 15px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <span style="font-size: 3rem;">🏰</span>
        </div>
        <p style="text-align: center; color: white;">Palace Scene</p>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="height: 200px; background: linear-gradient(135deg, #a8edea, #fed6e3); border-radius: 15px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <span style="font-size: 3rem;">👑</span>
        </div>
        <p style="text-align: center; color: white;">Royal Character</p>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="height: 200px; background: linear-gradient(135deg, #ffecd2, #fcb69f); border-radius: 15px; display: flex; align-items: center; justify-content: center; margin-bottom: 10px;">
            <span style="font-size: 3rem;">🌅</span>
        </div>
        <p style="text-align: center; color: white;">Landscape</p>
        """, unsafe_allow_html=True)
    
    st.success("🎨 Story images generated successfully!")

def show_ai_voice_options(story_data):
    """Show AI voice generation options"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🎭 Available AI Voices:**")
        voices = ["Wise Narrator", "Royal Storyteller", "Dramatic Reader", "Gentle Elder"]
        selected_voice = st.radio("Choose Voice", voices, horizontal=False)
    
    with col2:
        st.markdown("**🎛️ Voice Settings:**")
        emotion = st.selectbox("🎭 Emotion", ["Neutral", "Joyful", "Serious", "Mysterious"])
        accent = st.selectbox("🗣️ Accent", ["Standard", "Regional", "Classical"])
    
    if st.button("🎵 Generate AI Narration", use_container_width=True):
        with st.spinner("🤖 AI is creating your narration..."):
            time.sleep(3)
        st.success(f"✅ AI narration generated with {selected_voice} voice!")