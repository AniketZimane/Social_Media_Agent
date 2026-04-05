import requests
import os
from urllib.parse import quote
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class ImageGenerator:
    def __init__(self):
        self.api_key = os.getenv("POLLINATIONS_API_KEY")
    
    def generate_from_title(self, title: str) -> str:
        """Generate contextual AI image using topic-specific prompts with API key"""
        try:
            import re
            from html import unescape
            
            # Clean and extract key terms from title
            clean_title = re.sub(r'[^\w\s]', '', title)[:40].strip()
            
            # Create contextual prompt based on topic
            key_words = clean_title.lower().split()
            
            # Topic-specific image styles
            if any(word in key_words for word in ['ai', 'tech', 'technology', 'digital']):
                prompt = f"futuristic technology {clean_title} digital art"
            elif any(word in key_words for word in ['travel', 'places', 'destination', 'visit']):
                prompt = f"beautiful travel destination {clean_title} photography"
            elif any(word in key_words for word in ['business', 'startup', 'marketing']):
                prompt = f"professional business {clean_title} modern office"
            elif any(word in key_words for word in ['food', 'recipe', 'cooking']):
                prompt = f"delicious food {clean_title} culinary photography"
            else:
                prompt = f"professional blog header {clean_title}"
            
            encoded_prompt = quote(prompt)
            
            # Use API key if available - build clean URL
            if self.api_key:
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630&apikey={self.api_key}"
            else:
                image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1200&height=630"
            
            # Ensure URL is clean (no HTML entities)
            image_url = unescape(image_url)
            
            return image_url
        except:
            return f"https://picsum.photos/1200/630?random={abs(hash(title)) % 1000}"
