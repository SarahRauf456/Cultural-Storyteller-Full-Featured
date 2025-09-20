import pyttsx3
import os
import tempfile
from utils.config import VOICE_CONFIG, get_api_key
import streamlit as st

def get_available_voices():
    """Get list of available voice personalities"""
    return VOICE_CONFIG['available_voices']

def initialize_tts_engine():
    """Initialize the text-to-speech engine"""
    try:
        engine = pyttsx3.init()
        
        # Get available system voices
        voices = engine.getProperty('voices')
        if voices:
            # Set a default voice (preferably female for storytelling)
            for voice in voices:
                if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break
            else:
                # If no female voice found, use the first available
                engine.setProperty('voice', voices[0].id)
        
        # Set default properties
        engine.setProperty('rate', 180)  # Speed of speech
        engine.setProperty('volume', 0.9)  # Volume level
        
        return engine
    except Exception as e:
        st.error(f"Failed to initialize TTS engine: {str(e)}")
        return None

def synthesize_speech(text, voice_personality="Wise Elder", speech_speed=1.0, save_file=None):
    """
    Synthesize speech from text using the specified voice personality
    
    Args:
        text (str): Text to convert to speech
        voice_personality (str): Voice personality to use
        speech_speed (float): Speed of speech (0.5 to 2.0)
        save_file (str): Optional file path to save audio
    
    Returns:
        str: Path to generated audio file or None if failed
    """
    try:
        engine = initialize_tts_engine()
        if not engine:
            return None
        
        # Adjust speech rate based on personality and speed setting
        base_rates = {
            'Wise Elder': 160,
            'Royal Narrator': 170,
            'Dramatic Storyteller': 190,
            'Gentle Grandmother': 150,
            'Heroic Warrior': 180,
            'Playful Youth': 200,
            'Mystical Sage': 140
        }
        
        base_rate = base_rates.get(voice_personality, 170)
        adjusted_rate = int(base_rate * speech_speed)
        engine.setProperty('rate', adjusted_rate)
        
        # Create temporary file if no save path provided
        if not save_file:
            temp_dir = tempfile.gettempdir()
            save_file = os.path.join(temp_dir, f"narration_{hash(text) % 10000}.wav")
        
        # Save speech to file
        engine.save_to_file(text, save_file)
        engine.runAndWait()
        
        return save_file
        
    except Exception as e:
        st.error(f"Speech synthesis failed: {str(e)}")
        return None

def get_voice_sample(voice_personality):
    """Get a sample text for testing voice personalities"""
    samples = {
        'Wise Elder': "In ancient times, when wisdom flowed like rivers through the hearts of men, there lived a sage whose words could move mountains.",
        'Royal Narrator': "Hear now the tale of kings and queens, of palaces grand and battles won, in the golden age of our glorious past.",
        'Dramatic Storyteller': "Lightning crashed across the midnight sky as our hero faced the greatest challenge of his life!",
        'Gentle Grandmother': "Come close, my dear children, and let me tell you a story that my grandmother told to me long ago.",
        'Heroic Warrior': "With sword in hand and courage in heart, the brave warrior charged into battle for honor and justice!",
        'Playful Youth': "Once upon a time, in a land filled with magic and wonder, the most amazing adventure was about to begin!",
        'Mystical Sage': "From the depths of ancient wisdom comes a tale shrouded in mystery and enlightenment."
    }
    
    return samples.get(voice_personality, "This is a sample of the selected voice personality.")

def play_voice_sample(voice_personality, speech_speed=1.0):
    """Generate and return audio sample for a voice personality"""
    sample_text = get_voice_sample(voice_personality)
    audio_file = synthesize_speech(sample_text, voice_personality, speech_speed)
    
    if audio_file and os.path.exists(audio_file):
        return audio_file
    return None

def create_narration_with_background_music(text, voice_personality, music_type=None):
    """
    Create narration with optional background music
    
    Args:
        text (str): Text to narrate
        voice_personality (str): Voice to use
        music_type (str): Type of background music
    
    Returns:
        str: Path to combined audio file
    """
    # Generate voice narration
    narration_file = synthesize_speech(text, voice_personality)
    
    if not narration_file:
        return None
    
    # If no background music requested, return narration only
    if not music_type:
        return narration_file
    
    # In a full implementation, you would:
    # 1. Load background music file based on music_type
    # 2. Mix the narration with background music
    # 3. Return the combined audio file
    
    # For now, return the narration file
    # This would be enhanced with audio mixing libraries like pydub
    return narration_file

def get_voice_personality_settings(personality):
    """Get detailed settings for a voice personality"""
    settings = {
        'Wise Elder': {
            'rate_modifier': 0.85,
            'pitch_modifier': 0.9,
            'pause_emphasis': True,
            'emotion': 'calm',
            'accent': 'neutral'
        },
        'Royal Narrator': {
            'rate_modifier': 0.95,
            'pitch_modifier': 0.85,
            'pause_emphasis': True,
            'emotion': 'dignified',
            'accent': 'formal'
        },
        'Dramatic Storyteller': {
            'rate_modifier': 1.1,
            'pitch_modifier': 1.2,
            'pause_emphasis': True,
            'emotion': 'expressive',
            'accent': 'theatrical'
        },
        'Gentle Grandmother': {
            'rate_modifier': 0.8,
            'pitch_modifier': 1.1,
            'pause_emphasis': False,
            'emotion': 'warm',
            'accent': 'soft'
        },
        'Heroic Warrior': {
            'rate_modifier': 1.05,
            'pitch_modifier': 0.8,
            'pause_emphasis': True,
            'emotion': 'bold',
            'accent': 'strong'
        },
        'Playful Youth': {
            'rate_modifier': 1.2,
            'pitch_modifier': 1.3,
            'pause_emphasis': False,
            'emotion': 'cheerful',
            'accent': 'energetic'
        },
        'Mystical Sage': {
            'rate_modifier': 0.7,
            'pitch_modifier': 0.85,
            'pause_emphasis': True,
            'emotion': 'mysterious',
            'accent': 'ancient'
        }
    }
    
    return settings.get(personality, settings['Wise Elder'])

def estimate_narration_duration(text, voice_personality, speech_speed=1.0):
    """
    Estimate the duration of narration in seconds
    
    Args:
        text (str): Text to be narrated
        voice_personality (str): Voice personality
        speech_speed (float): Speech speed multiplier
    
    Returns:
        float: Estimated duration in seconds
    """
    # Average reading speed is about 200 words per minute
    # But varies by personality and speech speed
    
    word_count = len(text.split())
    
    base_wpm = {
        'Wise Elder': 160,
        'Royal Narrator': 170,
        'Dramatic Storyteller': 190,
        'Gentle Grandmother': 150,
        'Heroic Warrior': 180,
        'Playful Youth': 200,
        'Mystical Sage': 140
    }
    
    wpm = base_wpm.get(voice_personality, 170) * speech_speed
    duration_minutes = word_count / wpm
    
    # Add extra time for pauses and dramatic effect
    if voice_personality in ['Wise Elder', 'Dramatic Storyteller', 'Mystical Sage']:
        duration_minutes *= 1.2
    
    return duration_minutes * 60  # Convert to seconds

def cleanup_temp_audio_files():
    """Clean up temporary audio files"""
    temp_dir = tempfile.gettempdir()
    try:
        for filename in os.listdir(temp_dir):
            if filename.startswith("narration_") and filename.endswith(".wav"):
                file_path = os.path.join(temp_dir, filename)
                try:
                    os.remove(file_path)
                except:
                    pass  # Ignore errors when cleaning up
    except:
        pass  # Ignore errors when accessing temp directory