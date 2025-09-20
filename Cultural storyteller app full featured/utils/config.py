import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App Configuration
APP_CONFIG = {
    'app_name': 'Cultural Storyteller',
    'version': '1.0.0',
    'company': 'gfd Groups',
    'max_file_size': 100 * 1024 * 1024,  # 100MB
    'supported_audio_formats': ['mp3', 'wav', 'ogg', 'm4a'],
    'supported_video_formats': ['mp4', 'avi', 'mov', 'webm'],
    'supported_image_formats': ['jpg', 'jpeg', 'png', 'gif', 'bmp'],
    'max_story_length': 50000,  # characters
    'max_room_participants': 50,
    'default_language': 'English'
}

# API Keys (should be set via environment variables in production)
API_KEYS = {
    'openai_api_key': os.getenv('OPENAI_API_KEY'),
    'elevenlabs_api_key': os.getenv('ELEVENLABS_API_KEY'),
    'stability_ai_key': os.getenv('STABILITY_AI_KEY'),
    'google_cloud_key': os.getenv('GOOGLE_CLOUD_KEY'),
    'azure_speech_key': os.getenv('AZURE_SPEECH_KEY')
}

# Voice Configuration
VOICE_CONFIG = {
    'default_voice': 'Wise Elder',
    'available_voices': [
        'Wise Elder',
        'Royal Narrator',
        'Dramatic Storyteller',
        'Gentle Grandmother',
        'Heroic Warrior',
        'Playful Youth',
        'Mystical Sage'
    ],
    'voice_settings': {
        'speed_range': (0.5, 2.0),
        'pitch_range': (0.5, 2.0),
        'volume_range': (0.1, 1.0)
    }
}

# Avatar Configuration
AVATAR_CONFIG = {
    'available_avatars': [
        {
            'id': 'akbar',
            'name': 'Emperor Akbar',
            'description': 'Wise ruler of Mughal Empire',
            'voice_type': 'Royal, Authoritative',
            'emoji': '👑',
            'background': 'Royal Palace',
            'animations': ['wise_nod', 'royal_gesture', 'thoughtful_pose']
        },
        {
            'id': 'birbal',
            'name': 'Birbal',
            'description': 'Witty advisor and poet',
            'voice_type': 'Clever, Humorous',
            'emoji': '🧙‍♂️',
            'background': 'Court Room',
            'animations': ['witty_smile', 'clever_gesture', 'storytelling_pose']
        },
        {
            'id': 'tenali_rama',
            'name': 'Tenali Rama',
            'description': 'Court jester with wisdom',
            'voice_type': 'Sharp, Playful',
            'emoji': '🎭',
            'background': 'Royal Court',
            'animations': ['playful_wink', 'dramatic_gesture', 'thinking_pose']
        },
        {
            'id': 'lakshmibai',
            'name': 'Rani Lakshmibai',
            'description': 'Brave warrior queen',
            'voice_type': 'Strong, Inspiring',
            'emoji': '⚔️',
            'background': 'Battlefield',
            'animations': ['heroic_stance', 'inspiring_gesture', 'warrior_pose']
        }
    ]
}

# WebRTC Configuration
WEBRTC_CONFIG = {
    'ice_servers': [
        {'urls': ['stun:stun.l.google.com:19302']},
        {'urls': ['stun:stun1.l.google.com:19302']},
    ],
    'video_constraints': {
        'width': {'min': 320, 'ideal': 1280, 'max': 1920},
        'height': {'min': 240, 'ideal': 720, 'max': 1080},
        'frameRate': {'ideal': 30, 'max': 60}
    },
    'audio_constraints': {
        'echoCancellation': True,
        'noiseSuppression': True,
        'autoGainControl': True
    }
}

# Database Configuration
DATABASE_CONFIG = {
    'database_file': 'cultural_storyteller.db',
    'backup_interval': 3600,  # seconds
    'max_connections': 10
}

# AI Content Generation Settings
AI_CONFIG = {
    'story_generation': {
        'max_tokens': 4000,
        'temperature': 0.8,
        'presence_penalty': 0.1,
        'frequency_penalty': 0.1
    },
    'image_generation': {
        'default_style': 'cultural_art',
        'image_size': '1024x1024',
        'quality': 'high'
    },
    'voice_synthesis': {
        'default_model': 'eleven_monolingual_v1',
        'stability': 0.75,
        'similarity_boost': 0.75
    }
}

# UI Theme Configuration
THEME_CONFIG = {
    'primary_color': '#667eea',
    'secondary_color': '#764ba2',
    'accent_color': '#ffd700',
    'success_color': '#4CAF50',
    'warning_color': '#FF9800',
    'error_color': '#f44336',
    'background_gradient': 'linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #1e3c72 100%)',
    'card_background': 'rgba(255, 255, 255, 0.1)',
    'text_primary': '#ffffff',
    'text_secondary': '#cccccc',
    'text_muted': '#aaaaaa'
}

# Regional and Cultural Settings
CULTURAL_CONFIG = {
    'regions': [
        'North India',
        'South India',
        'East India',
        'West India',
        'Central India',
        'Northeast India',
        'Pan-Indian'
    ],
    'languages': [
        'Hindi',
        'English',
        'Tamil',
        'Bengali',
        'Telugu',
        'Marathi',
        'Gujarati',
        'Malayalam',
        'Kannada',
        'Punjabi',
        'Odia',
        'Assamese'
    ],
    'story_categories': [
        'Historical',
        'Mythological',
        'Folk Tales',
        'Wisdom Tales',
        'Heroic Adventures',
        'Romance',
        'Family Heritage',
        'Regional Legends',
        'Religious Stories',
        'Moral Tales'
    ]
}

# Export settings for stories
EXPORT_CONFIG = {
    'formats': ['html', 'pdf', 'mp4', 'audio', 'epub'],
    'quality_settings': {
        'video': {
            'hd': {'width': 1280, 'height': 720, 'bitrate': '2000k'},
            'sd': {'width': 854, 'height': 480, 'bitrate': '1000k'},
            'mobile': {'width': 640, 'height': 360, 'bitrate': '500k'}
        },
        'audio': {
            'high': {'bitrate': '320k', 'sample_rate': 48000},
            'standard': {'bitrate': '192k', 'sample_rate': 44100},
            'compressed': {'bitrate': '128k', 'sample_rate': 44100}
        }
    }
}

def get_config(config_type):
    """Get configuration by type"""
    configs = {
        'app': APP_CONFIG,
        'voice': VOICE_CONFIG,
        'avatar': AVATAR_CONFIG,
        'webrtc': WEBRTC_CONFIG,
        'database': DATABASE_CONFIG,
        'ai': AI_CONFIG,
        'theme': THEME_CONFIG,
        'cultural': CULTURAL_CONFIG,
        'export': EXPORT_CONFIG
    }
    return configs.get(config_type, {})

def get_api_key(service):
    """Get API key for specific service"""
    return API_KEYS.get(f'{service}_api_key')

def is_api_configured(service):
    """Check if API is configured for service"""
    return get_api_key(service) is not None