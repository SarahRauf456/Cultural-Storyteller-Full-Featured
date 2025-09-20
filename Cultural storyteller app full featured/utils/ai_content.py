import openai
import requests
import json
import streamlit as st
from utils.config import get_api_key, AI_CONFIG
import time

def generate_story_content(prompt, story_type="Historical Fiction", length="Medium (1000 words)", 
                         style="Traditional Storytelling", cultural_context=""):
    """
    Generate story content using AI based on the provided prompt
    
    Args:
        prompt (str): User's story prompt
        story_type (str): Type of story to generate
        length (str): Desired story length
        style (str): Writing style
        cultural_context (str): Cultural background/context
    
    Returns:
        dict: Generated story with title, description, and content
    """
    
    # Mock AI generation for demo (replace with actual OpenAI API call)
    # In production, you would use the OpenAI API here
    
    mock_stories = {
        "Historical Fiction": {
            "title": "The Wisdom of Emperor Akbar",
            "description": "A tale of justice and wisdom from the Mughal court, where Emperor Akbar's fair judgment resolves a complex dispute between merchants.",
            "content": """
            In the golden halls of Fatehpur Sikri, Emperor Akbar held court on a bright morning in the year 1590. The sun's rays filtered through the intricate jali work, casting dancing shadows on the marble floor where two merchants stood before the throne, their dispute echoing in the vast chamber.

            "Your Majesty," began Hakim, a textile merchant from Delhi, his voice trembling with emotion, "this man has cheated me of my rightful earnings. We agreed on a price for my finest silk, but now he refuses to pay the full amount."

            Opposite him stood Ramesh, a trader from Gujarat, his head held high despite the accusation. "Respected Emperor, I speak the truth when I say that the silk was not as promised. The quality was inferior to what we agreed upon. I paid what the goods were truly worth."

            Akbar listened carefully, his wise eyes observing both men. The court fell silent, waiting for the emperor's judgment. Birbal, his trusted advisor, watched from the side, knowing that his master would find a solution that served justice while teaching a valuable lesson.

            "Bring me samples of the disputed silk," commanded Akbar. When the material was presented, he examined it closely, feeling its texture and studying its weave under the light.

            After several minutes of contemplation, Akbar spoke: "I see that this silk is indeed of good quality, though perhaps not the finest grade. However, I also understand that expectations must be clearly communicated in any agreement."

            He then made a decision that surprised everyone: "Hakim, you will receive three-quarters of the originally agreed price, for your silk is good but not exceptional. Ramesh, you will pay this amount plus a small penalty for not communicating your concerns before taking the goods."

            "But why the additional penalty, Your Majesty?" asked Ramesh.

            "Because," replied Akbar with a gentle smile, "trust is the foundation of all trade. If you had concerns about the quality, you should have spoken immediately rather than accepting the goods and then refusing payment. This teaches us that honest communication prevents such disputes."

            Both merchants bowed, understanding the wisdom in the emperor's judgment. As they left the court, reconciled and wiser, Birbal approached Akbar.

            "Once again, Jahanpanah, your judgment serves justice while teaching valuable lessons."

            Akbar nodded thoughtfully. "Birbal, true leadership lies not just in making decisions, but in ensuring that every judgment strengthens the bonds of trust and understanding among our people."

            The story of this judgment spread throughout the empire, reminding all traders and merchants that fairness, communication, and trust were the pillars upon which successful commerce was built. And in the courts of Akbar, justice was not merely about punishment or reward, but about creating a society where wisdom prevailed over conflict.
            """
        },
        "Mythology Retelling": {
            "title": "The Test of Hanuman's Devotion",
            "description": "A retelling of how Lord Hanuman's unwavering devotion to Rama was tested and proved beyond all doubt.",
            "content": """
            In the celestial realm where gods convened to discuss the affairs of mortals and immortals alike, a great debate arose about the nature of true devotion. Some claimed that devotion was merely ritual, others argued it was service, but Sage Narada had a different perspective.

            "True devotion," declared Narada, his veena strings humming with divine melody, "transcends all forms and manifests as complete surrender of the self."

            "But how can we measure such devotion?" asked Indra, king of the gods.

            Narada's eyes twinkled with divine mischief. "Let us test the greatest devotee we know - Hanuman, the devoted servant of Lord Rama."

            And so, a test was devised. Hanuman was sitting in meditation at the foothills of Mount Govardhan when a beautiful brahmin appeared before him, claiming to be a great devotee of Lord Rama.

            "O mighty Hanuman," said the brahmin, "I have heard of your unparalleled devotion to Lord Rama. I too am his devotee, but I wonder - do you love Rama more, or does Rama love you more?"

            Hanuman opened his eyes, surprised by the strange question. "Respected brahmin, how can one measure the ocean of Lord Rama's love? I am but a humble servant."

            "But surely," persisted the brahmin, "your devotion must earn you special favor. Does Rama not grant you whatever you wish?"

            Hanuman shook his head gently. "I desire nothing except the opportunity to serve my Lord. My greatest joy is in chanting his name and carrying out his will."

            The brahmin smiled cunningly. "Then prove it. If your devotion is pure, tear open your chest and show me where Rama resides in your heart."

            Without hesitation, without question, and with complete faith, Hanuman placed his hands on his chest. The brahmin and all the hidden gods watched in amazement as Hanuman prepared to fulfill even this strange request.

            But just as he was about to act, the brahmin revealed his true form - it was Lord Rama himself, accompanied by Sita and Lakshman.

            "Stop, my dear Hanuman," said Rama, his voice filled with divine love. "Your willingness to do even this proves your devotion beyond any doubt. You were ready to give your very life without question, without seeking to understand why, simply because you believed it was my wish."

            Hanuman fell at Rama's feet, tears of joy streaming down his face. "My Lord, I would gladly give my life a thousand times if it serves your purpose."

            Rama lifted Hanuman gently. "This is why you are my greatest devotee, Hanuman. Not because you are powerful, not because you can leap across oceans or move mountains, but because your love is pure and selfless. You seek nothing for yourself, not even understanding - only the joy of service."

            The watching gods bowed in reverence, understanding now that true devotion was not about what one could gain, but what one was willing to give. And Hanuman's name became synonymous with selfless service and unwavering faith.

            From that day forward, whenever someone spoke of perfect devotion, they would remember Hanuman - not just for his mighty deeds, but for his readiness to surrender everything, even his own understanding, at the feet of his beloved Lord.

            The lesson echoed through the ages: True devotion asks no questions, seeks no rewards, and finds its greatest joy in the simple act of loving service.
            """
        }
    }
    
    # Simulate AI processing time
    time.sleep(2)
    
    # Return appropriate mock story based on story type
    story_key = story_type if story_type in mock_stories else "Historical Fiction"
    generated_story = mock_stories[story_key].copy()
    
    # Modify based on cultural context if provided
    if cultural_context:
        generated_story["description"] = f"{generated_story['description']} Set in the context of {cultural_context}."
    
    return generated_story

def generate_story_from_openai(prompt, story_type, length, style, cultural_context):
    """
    Generate story using actual OpenAI API (when API key is available)
    """
    api_key = get_api_key('openai')
    
    if not api_key:
        st.warning("OpenAI API key not configured. Using mock content.")
        return generate_story_content(prompt, story_type, length, style, cultural_context)
    
    try:
        openai.api_key = api_key
        
        # Construct detailed prompt
        system_prompt = f"""
        You are a master storyteller specializing in cultural and traditional stories from India. 
        Create a {story_type} story in {style} writing style.
        The story should be approximately {length} and incorporate {cultural_context} cultural elements.
        
        Make the story engaging, culturally authentic, and appropriate for preservation of cultural heritage.
        Include moral lessons or wisdom typical of traditional Indian storytelling.
        """
        
        user_prompt = f"""
        Create a story based on this prompt: {prompt}
        
        Please format the response as JSON with the following structure:
        {{
            "title": "Story Title",
            "description": "Brief story description",
            "content": "Full story content with proper paragraphs"
        }}
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=AI_CONFIG['story_generation']['max_tokens'],
            temperature=AI_CONFIG['story_generation']['temperature']
        )
        
        # Parse the JSON response
        story_json = json.loads(response.choices[0].message.content)
        return story_json
        
    except Exception as e:
        st.error(f"OpenAI API error: {str(e)}")
        return generate_story_content(prompt, story_type, length, style, cultural_context)

def generate_story_images(prompt, num_images=3):
    """
    Generate images for stories using AI image generation
    
    Args:
        prompt (str): Description for image generation
        num_images (int): Number of images to generate
    
    Returns:
        list: List of generated image URLs or paths
    """
    
    # Mock image generation (replace with actual AI image generation API)
    mock_images = [
        "https://images.pexels.com/photos/1587927/pexels-photo-1587927.jpeg",  # Palace
        "https://images.pexels.com/photos/2889344/pexels-photo-2889344.jpeg",  # Historical figure
        "https://images.pexels.com/photos/1586298/pexels-photo-1586298.jpeg"   # Cultural scene
    ]
    
    # Simulate processing time
    time.sleep(1)
    
    return mock_images[:num_images]

def generate_images_with_stability_ai(prompt, num_images=3):
    """
    Generate images using Stability AI API (when API key is available)
    """
    api_key = get_api_key('stability_ai')
    
    if not api_key:
        st.warning("Stability AI API key not configured. Using placeholder images.")
        return generate_story_images(prompt, num_images)
    
    try:
        # Stability AI API implementation would go here
        # For now, return mock images
        return generate_story_images(prompt, num_images)
        
    except Exception as e:
        st.error(f"Stability AI API error: {str(e)}")
        return generate_story_images(prompt, num_images)

def enhance_story_with_ai(original_story, enhancement_type="grammar_and_flow"):
    """
    Enhance existing story content using AI
    
    Args:
        original_story (str): Original story text
        enhancement_type (str): Type of enhancement to apply
    
    Returns:
        str: Enhanced story content
    """
    
    # Mock enhancement (replace with actual AI processing)
    enhancements = {
        "grammar_and_flow": "Enhanced for better grammar and narrative flow",
        "cultural_authenticity": "Enhanced with more authentic cultural details",
        "dramatic_effect": "Enhanced with more dramatic elements and suspense",
        "accessibility": "Enhanced for better readability and accessibility"
    }
    
    # Simulate processing
    time.sleep(1)
    
    # Return original story with a note (in production, this would be actual AI enhancement)
    return f"{original_story}\n\n[Story enhanced for: {enhancements.get(enhancement_type, 'general improvement')}]"

def generate_story_summary(story_content, max_length=200):
    """
    Generate a summary of story content
    
    Args:
        story_content (str): Full story text
        max_length (int): Maximum length of summary
    
    Returns:
        str: Story summary
    """
    
    # Simple extractive summary (in production, use AI summarization)
    sentences = story_content.split('. ')
    
    if len(sentences) <= 3:
        return story_content
    
    # Take first sentence and last sentence, plus one from middle
    summary_sentences = [
        sentences[0],
        sentences[len(sentences)//2],
        sentences[-1]
    ]
    
    summary = '. '.join(summary_sentences)
    
    # Trim if too long
    if len(summary) > max_length:
        summary = summary[:max_length-3] + "..."
    
    return summary

def suggest_story_tags(story_content, cultural_context=""):
    """
    Suggest relevant tags for a story based on its content
    
    Args:
        story_content (str): Story text
        cultural_context (str): Cultural background
    
    Returns:
        list: Suggested tags
    """
    
    # Simple keyword-based tagging (in production, use AI for better analysis)
    keyword_tags = {
        'akbar': ['Mughal', 'Emperor', 'Historical', 'Wisdom'],
        'birbal': ['Akbar-Birbal', 'Wit', 'Court', 'Wisdom'],
        'hanuman': ['Mythology', 'Devotion', 'Ramayana', 'Spiritual'],
        'rama': ['Ramayana', 'Mythology', 'Dharma', 'Epic'],
        'krishna': ['Mythology', 'Mahabharata', 'Divine', 'Wisdom'],
        'palace': ['Royal', 'Historical', 'Architecture'],
        'court': ['Royal', 'Justice', 'Historical'],
        'devotion': ['Spiritual', 'Faith', 'Religious'],
        'wisdom': ['Moral', 'Teaching', 'Philosophy'],
        'brave': ['Heroic', 'Courage', 'Adventure'],
        'princess': ['Royal', 'Heroic', 'Historical'],
        'merchant': ['Trade', 'Commerce', 'Social']
    }
    
    content_lower = story_content.lower()
    suggested_tags = set()
    
    for keyword, tags in keyword_tags.items():
        if keyword in content_lower:
            suggested_tags.update(tags)
    
    # Add cultural context tags if provided
    if cultural_context:
        if 'mughal' in cultural_context.lower():
            suggested_tags.add('Mughal Era')
        if 'rajasthan' in cultural_context.lower():
            suggested_tags.add('Rajasthani')
        if 'south' in cultural_context.lower():
            suggested_tags.add('South Indian')
    
    return list(suggested_tags)[:8]  # Limit to 8 tags

def generate_moral_lesson(story_content):
    """
    Extract or generate moral lesson from story content
    
    Args:
        story_content (str): Story text
    
    Returns:
        str: Moral lesson or key takeaway
    """
    
    # Simple keyword-based moral extraction (in production, use AI)
    morals = {
        'justice': "True justice considers all perspectives and seeks fair solutions for everyone involved.",
        'wisdom': "Wisdom lies not just in knowledge, but in the compassionate application of that knowledge.",
        'devotion': "Pure devotion seeks nothing in return and finds joy in selfless service.",
        'honesty': "Honesty and transparent communication prevent misunderstandings and build trust.",
        'courage': "True courage is not the absence of fear, but the determination to do what is right despite fear.",
        'humility': "Humility opens the door to learning and growth, while pride closes it.",
        'friendship': "Genuine friendship is built on mutual respect, understanding, and shared values."
    }
    
    content_lower = story_content.lower()
    
    for keyword, moral in morals.items():
        if keyword in content_lower:
            return moral
    
    # Default moral if no specific keywords found
    return "Every story teaches us something valuable about life, relationships, and the human experience."