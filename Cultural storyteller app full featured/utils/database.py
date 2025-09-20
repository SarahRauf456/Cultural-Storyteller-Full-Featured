import sqlite3
import json
import os
from datetime import datetime

DATABASE_FILE = "cultural_storyteller.db"

def init_database():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            user_type TEXT NOT NULL,
            email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP,
            profile_data TEXT,
            stats TEXT
        )
    ''')
    
    # Stories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            description TEXT,
            category TEXT,
            region TEXT,
            language TEXT,
            tags TEXT,
            duration TEXT,
            views INTEGER DEFAULT 0,
            likes INTEGER DEFAULT 0,
            settings TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            audio_file TEXT,
            video_file TEXT,
            images TEXT
        )
    ''')
    
    # Comments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER,
            user_id INTEGER,
            comment_text TEXT,
            comment_type TEXT DEFAULT 'text',
            audio_file TEXT,
            likes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Rooms table for voice/video calls
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_name TEXT NOT NULL,
            host_id INTEGER,
            room_type TEXT NOT NULL,
            topic TEXT,
            language TEXT,
            max_participants INTEGER DEFAULT 10,
            is_public BOOLEAN DEFAULT 1,
            status TEXT DEFAULT 'active',
            settings TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (host_id) REFERENCES users (id)
        )
    ''')
    
    # Room participants table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS room_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER,
            user_id INTEGER,
            role TEXT DEFAULT 'participant',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            left_at TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES rooms (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # User interactions table (likes, follows, etc.)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            target_type TEXT NOT NULL,
            target_id INTEGER NOT NULL,
            interaction_type TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(username, password_hash, user_type, email=None):
    """Create a new user"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (username, password_hash, user_type, email, profile_data, stats)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            username, 
            password_hash, 
            user_type, 
            email,
            json.dumps({"bio": "", "avatar": "", "preferences": {}}),
            json.dumps({"stories_created": 0, "views_received": 0, "likes_received": 0})
        ))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def verify_user(username, password_hash, user_type):
    """Verify user credentials"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id FROM users 
        WHERE username = ? AND password_hash = ? AND user_type = ?
    ''', (username, password_hash, user_type))
    
    result = cursor.fetchone()
    
    # Update last login
    if result:
        cursor.execute('''
            UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
        ''', (result[0],))
        conn.commit()
    
    conn.close()
    return result is not None

def get_user_by_username(username):
    """Get user information by username"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, username, user_type, email, profile_data, stats, created_at, last_login
        FROM users WHERE username = ?
    ''', (username,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return {
            'id': result[0],
            'username': result[1],
            'user_type': result[2],
            'email': result[3],
            'profile_data': json.loads(result[4]) if result[4] else {},
            'stats': json.loads(result[5]) if result[5] else {},
            'created_at': result[6],
            'last_login': result[7]
        }
    return None

def save_story(story_data, author):
    """Save a new story to the database"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO stories (
            title, author, content, description, category, region, 
            language, tags, duration, settings
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        story_data['title'],
        author,
        story_data['content'],
        story_data['description'],
        story_data['category'],
        story_data['region'],
        story_data['language'],
        json.dumps(story_data.get('tags', [])),
        story_data['duration'],
        json.dumps(story_data.get('settings', {}))
    ))
    
    story_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return story_id

def get_all_stories(limit=50):
    """Get all stories with pagination"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, title, author, description, category, region, language, 
               views, likes, created_at, duration, tags
        FROM stories 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (limit,))
    
    stories = []
    for row in cursor.fetchall():
        stories.append({
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'description': row[3],
            'category': row[4],
            'region': row[5],
            'language': row[6],
            'views': row[7],
            'likes': row[8],
            'created_at': row[9],
            'duration': row[10],
            'tags': json.loads(row[11]) if row[11] else []
        })
    
    conn.close()
    return stories

def get_recent_stories(limit=10):
    """Get recent stories for home page"""
    return get_all_stories(limit)

def search_stories(query, category=None, region=None, language=None):
    """Search stories with filters"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    sql = '''
        SELECT id, title, author, description, category, region, language, 
               views, likes, created_at, duration, tags
        FROM stories 
        WHERE (title LIKE ? OR description LIKE ? OR content LIKE ?)
    '''
    params = [f'%{query}%', f'%{query}%', f'%{query}%']
    
    if category and category != "All Categories":
        sql += ' AND category = ?'
        params.append(category)
    
    if region and region != "All Regions":
        sql += ' AND region = ?'
        params.append(region)
    
    if language and language != "All Languages":
        sql += ' AND language = ?'
        params.append(language)
    
    sql += ' ORDER BY created_at DESC LIMIT 50'
    
    cursor.execute(sql, params)
    
    stories = []
    for row in cursor.fetchall():
        stories.append({
            'id': row[0],
            'title': row[1],
            'author': row[2],
            'description': row[3],
            'category': row[4],
            'region': row[5],
            'language': row[6],
            'views': row[7],
            'likes': row[8],
            'created_at': row[9],
            'duration': row[10],
            'tags': json.loads(row[11]) if row[11] else []
        })
    
    conn.close()
    return stories

def get_user_stats():
    """Get platform statistics"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Get user counts by type
    cursor.execute('SELECT user_type, COUNT(*) FROM users GROUP BY user_type')
    user_stats = dict(cursor.fetchall())
    
    # Get story counts
    cursor.execute('SELECT COUNT(*) FROM stories')
    total_stories = cursor.fetchone()[0]
    
    # Get total views and likes
    cursor.execute('SELECT SUM(views), SUM(likes) FROM stories')
    views_likes = cursor.fetchone()
    
    conn.close()
    
    return {
        'users': user_stats,
        'total_stories': total_stories,
        'total_views': views_likes[0] or 0,
        'total_likes': views_likes[1] or 0
    }

def add_comment(story_id, user_id, comment_text, comment_type='text', audio_file=None):
    """Add a comment to a story"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO comments (story_id, user_id, comment_text, comment_type, audio_file)
        VALUES (?, ?, ?, ?, ?)
    ''', (story_id, user_id, comment_text, comment_type, audio_file))
    
    comment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return comment_id

def get_story_comments(story_id):
    """Get comments for a story"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT c.id, c.comment_text, c.comment_type, c.audio_file, c.likes, c.created_at,
               u.username
        FROM comments c
        JOIN users u ON c.user_id = u.id
        WHERE c.story_id = ?
        ORDER BY c.created_at DESC
    ''', (story_id,))
    
    comments = []
    for row in cursor.fetchall():
        comments.append({
            'id': row[0],
            'text': row[1],
            'type': row[2],
            'audio_file': row[3],
            'likes': row[4],
            'created_at': row[5],
            'author': row[6]
        })
    
    conn.close()
    return comments

def create_room(room_data, host_id):
    """Create a new room for voice/video calls"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO rooms (
            room_name, host_id, room_type, topic, language, 
            max_participants, is_public, settings
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        room_data['name'],
        host_id,
        room_data['type'],
        room_data.get('topic', ''),
        room_data.get('language', 'English'),
        room_data.get('max_participants', 10),
        room_data.get('is_public', True),
        json.dumps(room_data.get('settings', {}))
    ))
    
    room_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return room_id

def get_active_rooms(room_type=None):
    """Get active rooms"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    if room_type:
        cursor.execute('''
            SELECT r.id, r.room_name, r.room_type, r.topic, r.language, r.max_participants,
                   u.username as host_username, COUNT(rp.user_id) as participant_count
            FROM rooms r
            JOIN users u ON r.host_id = u.id
            LEFT JOIN room_participants rp ON r.id = rp.room_id AND rp.left_at IS NULL
            WHERE r.status = 'active' AND r.room_type = ?
            GROUP BY r.id
            ORDER BY r.created_at DESC
        ''', (room_type,))
    else:
        cursor.execute('''
            SELECT r.id, r.room_name, r.room_type, r.topic, r.language, r.max_participants,
                   u.username as host_username, COUNT(rp.user_id) as participant_count
            FROM rooms r
            JOIN users u ON r.host_id = u.id
            LEFT JOIN room_participants rp ON r.id = rp.room_id AND rp.left_at IS NULL
            WHERE r.status = 'active'
            GROUP BY r.id
            ORDER BY r.created_at DESC
        ''')
    
    rooms = []
    for row in cursor.fetchall():
        rooms.append({
            'id': row[0],
            'name': row[1],
            'type': row[2],
            'topic': row[3],
            'language': row[4],
            'max_participants': row[5],
            'host': row[6],
            'participants': row[7]
        })
    
    conn.close()
    return rooms

def join_room(room_id, user_id, role='participant'):
    """Join a room as a participant"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO room_participants (room_id, user_id, role)
        VALUES (?, ?, ?)
    ''', (room_id, user_id, role))
    
    conn.commit()
    conn.close()

def leave_room(room_id, user_id):
    """Leave a room"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE room_participants 
        SET left_at = CURRENT_TIMESTAMP 
        WHERE room_id = ? AND user_id = ? AND left_at IS NULL
    ''', (room_id, user_id))
    
    conn.commit()
    conn.close()

def update_story_views(story_id):
    """Increment story view count"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE stories SET views = views + 1 WHERE id = ?
    ''', (story_id,))
    
    conn.commit()
    conn.close()

def like_story(story_id, user_id):
    """Like a story"""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Check if already liked
    cursor.execute('''
        SELECT id FROM user_interactions 
        WHERE user_id = ? AND target_type = 'story' AND target_id = ? AND interaction_type = 'like'
    ''', (user_id, story_id))
    
    if cursor.fetchone():
        return False  # Already liked
    
    # Add like interaction
    cursor.execute('''
        INSERT INTO user_interactions (user_id, target_type, target_id, interaction_type)
        VALUES (?, 'story', ?, 'like')
    ''', (user_id, story_id))
    
    # Increment story likes
    cursor.execute('''
        UPDATE stories SET likes = likes + 1 WHERE id = ?
    ''', (story_id,))
    
    conn.commit()
    conn.close()
    return True