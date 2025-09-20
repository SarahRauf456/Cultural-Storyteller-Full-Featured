import streamlit as st
from utils.database import get_user_by_username

def check_authentication():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user():
    """Get current logged in user"""
    return st.session_state.get('current_user', None)

def logout():
    """Logout current user"""
    st.session_state.authenticated = False
    st.session_state.user_type = None
    st.session_state.current_user = None
    st.rerun()

def require_auth(user_types=None):
    """Decorator to require authentication"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not check_authentication():
                st.warning("Please login to access this feature.")
                return None
            
            current_user_type = st.session_state.get('user_type')
            
            if user_types and current_user_type not in user_types:
                st.error(f"This feature is only available for {', '.join(user_types)} users.")
                return None
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

def is_storyteller():
    """Check if current user is a storyteller"""
    return st.session_state.get('user_type') == 'storyteller'

def is_audience():
    """Check if current user is audience"""
    return st.session_state.get('user_type') == 'audience'

def is_guest():
    """Check if current user is a guest"""
    return st.session_state.get('user_type') == 'guest'

def get_user_permissions():
    """Get current user permissions"""
    user_type = st.session_state.get('user_type', 'guest')
    
    permissions = {
        'storyteller': {
            'can_create_stories': True,
            'can_upload_content': True,
            'can_host_calls': True,
            'can_use_avatars': True,
            'can_comment': True,
            'can_like': True,
            'can_follow': True,
            'can_create_rooms': True,
            'can_access_analytics': True
        },
        'audience': {
            'can_create_stories': False,
            'can_upload_content': False,
            'can_host_calls': False,
            'can_use_avatars': True,
            'can_comment': True,
            'can_like': True,
            'can_follow': True,
            'can_create_rooms': False,
            'can_access_analytics': False
        },
        'guest': {
            'can_create_stories': False,
            'can_upload_content': False,
            'can_host_calls': False,
            'can_use_avatars': False,
            'can_comment': False,
            'can_like': False,
            'can_follow': False,
            'can_create_rooms': False,
            'can_access_analytics': False
        }
    }
    
    return permissions.get(user_type, permissions['guest'])

def check_permission(permission_name):
    """Check if current user has specific permission"""
    permissions = get_user_permissions()
    return permissions.get(permission_name, False)