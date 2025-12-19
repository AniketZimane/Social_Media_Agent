import requests
import json
import os
from typing import Dict
from dotenv import load_dotenv

load_dotenv()

class DynamicContentGenerator:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_AI_API_KEY")
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
    
    def generate_real_blog_content(self, topic: str, platform: str) -> Dict:
        """Generate real dynamic content using Google AI"""
        
        # Extract location from topic
        location = self._extract_location(topic)
        
        try:
            # Determine if it's a travel topic or other topic
            is_travel = any(word in topic.lower() for word in ['places', 'visit', 'travel', 'destination', 'city', 'town'])
            
            if is_travel:
                prompt = f"""Write a detailed travel blog about "{topic}" specifically about {location}.

IMPORTANT: Write about REAL places, attractions, and information about {location}. Do NOT write generic content.

Include:
- Specific attractions and landmarks in {location}
- Local food specialties of {location}
- Transportation options in {location}
- Best time to visit {location}
- Cultural highlights of {location}
- Practical travel tips for {location}
- Budget information for {location}

Write 500-700 words with specific details, not generic travel advice.
Use engaging tone with emojis and subheadings.
Make it informative and practical for actual travelers."""
            else:
                prompt = f"""Write a detailed, informative blog post about "{topic}" for {platform}.

IMPORTANT: Write ACTUAL CONTENT about {topic}, not a guide about how to write about it.

Requirements:
- 500-700 words of specific, factual content about {topic}
- Use emojis and subheadings for visual appeal
- Include practical information, examples, and real-world applications
- Add expert insights and actionable tips
- Make it engaging and informative for readers interested in {topic}
- End with compelling call-to-action

Write as an expert who has deep knowledge about {topic}."""

            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            headers = {"Content-Type": "application/json"}
            
            response = requests.post(
                f"{self.base_url}?key={self.google_api_key}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"Google AI Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                
                if content and len(content) > 200:
                    print("✅ Google AI generated content successfully")
                    # Generate appropriate title based on content type
                    if is_travel:
                        title = f"Complete Guide to {location}: Hidden Gems & Local Secrets"
                        cta = f"Planning to visit {location}? Share your travel plans in the comments!"
                        keywords = [location, "travel guide", "attractions", "tourism", "places to visit"]
                        hashtags = self._generate_location_hashtags(location, platform)
                    else:
                        title = self._extract_title_from_content(content, topic)
                        cta = f"What's your experience with {topic}? Share your thoughts in the comments!"
                        keywords = self._generate_topic_keywords(topic)
                        hashtags = self._generate_topic_hashtags(topic, platform)
                    
                    return {
                        "title": title,
                        "content": content,
                        "hashtags": hashtags,
                        "cta": cta,
                        "keywords": keywords
                    }
                else:
                    print("⚠️ Google AI returned empty content")
            else:
                print(f"❌ Google AI API Error: {response.status_code}")
                if response.text:
                    print(f"Error details: {response.text}")
                    
        except Exception as e:
            print(f"❌ Exception in Google AI call: {e}")
        
        # Fallback with location-specific content
        return self._generate_location_specific_fallback(location, platform)
    
    def _extract_location(self, topic: str) -> str:
        """Extract location name from topic"""
        topic_lower = topic.lower()
        
        # Common location patterns
        if "sawantwadi" in topic_lower:
            return "Sawantwadi"
        elif "pune" in topic_lower:
            return "Pune"
        elif "mumbai" in topic_lower:
            return "Mumbai"
        elif "goa" in topic_lower:
            return "Goa"
        elif "delhi" in topic_lower:
            return "Delhi"
        elif "bangalore" in topic_lower:
            return "Bangalore"
        else:
            # Extract last meaningful word as location
            words = topic.split()
            for word in reversed(words):
                if len(word) > 3 and word.lower() not in ['best', 'places', 'visit', 'blog', 'write']:
                    return word.title()
            return "this destination"
    
    def _generate_location_specific_fallback(self, location: str, platform: str) -> Dict:
        """Generate location-specific fallback content"""
        
        if location.lower() == "sawantwadi":
            content = """# 🏰 Sawantwadi: The Royal Heritage Town of Maharashtra

## 🎨 About Sawantwadi

Sawantwadi, located in the Sindhudurg district of Maharashtra, is a charming town known for its rich cultural heritage, beautiful palaces, and traditional crafts. Once the capital of the Sawantwadi princely state, this town offers a perfect blend of history, art, and natural beauty.

## 🏛️ Top Attractions

### Historical Sites
- **Sawantwadi Palace**: The magnificent royal palace showcasing Indo-Saracenic architecture
- **Moti Talao**: Beautiful lake in the heart of the town with a small island
- **Hiranyakeshi Temple**: Ancient temple dedicated to Goddess Hiranyakeshi
- **Narayan Palace**: Another royal residence with stunning architecture

### Cultural Experiences
- **Ganjifa Card Making**: Traditional hand-painted playing cards unique to Sawantwadi
- **Lacquerware Craft**: Beautiful wooden toys and decorative items
- **Local Markets**: Explore traditional crafts and handmade items

## 🍽️ Local Cuisine

### Must-Try Dishes
- **Malvani Cuisine**: Spicy coastal flavors with coconut and kokum
- **Solkadhi**: Refreshing drink made with kokum and coconut milk
- **Koliwada Fish Fry**: Fresh seafood preparations
- **Modak**: Traditional sweet dumplings

## 🚗 Getting There

### Transportation
- **By Road**: Well-connected via NH-66, about 80 km from Panaji, Goa
- **Nearest Railway**: Sawantwadi Railway Station on Konkan Railway
- **Nearest Airport**: Goa Airport (Dabolim) - 65 km away

### Best Time to Visit
- **October to March**: Pleasant weather perfect for sightseeing
- **Monsoon (June-September)**: Lush greenery but heavy rainfall

## 💰 Budget Information
- **Accommodation**: ₹800-2500 per night
- **Local transport**: ₹50-100 for auto-rickshaw rides
- **Food**: ₹100-300 per meal
- **Entry fees**: Most attractions are free or ₹10-20

## 📸 Photography Spots
1. **Moti Talao**: Scenic lake views
2. **Sawantwadi Palace**: Royal architecture
3. **Craft workshops**: Traditional artisans at work
4. **Hiranyakeshi Temple**: Spiritual and architectural beauty

Sawantwadi offers a unique glimpse into Maharashtra's royal heritage combined with traditional arts and crafts, making it a perfect destination for culture enthusiasts!"""

        else:
            content = f"""# 🌟 Exploring {location}: A Complete Travel Guide

## 🏛️ About {location}

{location} is a fascinating destination that offers visitors a unique blend of culture, history, and modern attractions. Whether you're interested in historical sites, local cuisine, or cultural experiences, {location} has something special to offer every traveler.

## 🎯 Top Attractions

### Must-Visit Places
- Historical landmarks and monuments
- Cultural sites and museums  
- Natural attractions and parks
- Religious and spiritual sites

### Local Experiences
- Traditional markets and shopping areas
- Local festivals and events
- Art and craft centers
- Scenic viewpoints

## 🍽️ Local Food Scene

### Signature Dishes
- Regional specialties unique to {location}
- Street food favorites
- Traditional sweets and snacks
- Local beverages and drinks

### Best Places to Eat
- Popular local restaurants
- Street food markets
- Traditional eateries
- Modern cafes and dining spots

## 🚗 Travel Information

### Getting There
- Transportation options to reach {location}
- Local transport within the city
- Best routes and connections

### When to Visit
- Ideal seasons for travel
- Weather considerations
- Festival times and special events

## 💡 Travel Tips

### Budget Planning
- Accommodation options and costs
- Food and dining expenses
- Transportation costs
- Entry fees and activity charges

### Practical Advice
- What to pack for your trip
- Local customs and etiquette
- Safety tips for travelers
- Best photography spots

{location} promises an unforgettable experience with its unique charm and attractions!"""

        return {
            "title": f"Ultimate Guide to {location}: Everything You Need to Know",
            "content": content,
            "hashtags": self._generate_location_hashtags(location, platform),
            "cta": f"Have you been to {location}? Share your favorite spots in the comments!",
            "keywords": [location, "travel", "tourism", "guide", "attractions", "places to visit"]
        }
    
    def _generate_location_hashtags(self, location: str, platform: str) -> list:
        """Generate location-specific hashtags"""
        base_tags = [f"#{location.replace(' ', '')}", "#travel", "#tourism"]
        
        platform_tags = {
            "instagram": ["#instatravel", "#wanderlust", "#explore", "#travelgram"],
            "twitter": ["#travel", "#vacation", "#explore", "#wanderlust"],
            "linkedin": ["#travel", "#business", "#networking", "#professional"],
            "youtube": ["#travel", "#vlog", "#tourism", "#guide"],
            "facebook": ["#travel", "#vacation", "#family", "#friends"]
        }
        
        platform_key = platform.lower().split()[-1] if " " in platform else platform.lower()
        specific_tags = platform_tags.get(platform_key, ["#travel", "#explore"])
        
        location_tags = ["#India", "#Maharashtra"] if location == "Sawantwadi" else ["#destination", "#vacation"]
        
        return base_tags + specific_tags + location_tags + ["#2024", "#guide"]
    
    def _extract_title_from_content(self, content: str, topic: str) -> str:
        """Extract appropriate title from AI-generated content"""
        lines = content.split('\n')
        
        # Look for title in first few lines
        for line in lines[:5]:
            clean_line = line.strip().replace('#', '').replace('*', '').strip()
            if len(clean_line) > 10 and len(clean_line) < 100:
                return clean_line
        
        # Fallback: generate title based on topic
        if 'ai' in topic.lower() or 'artificial intelligence' in topic.lower():
            return f"Understanding {topic}: Complete Guide for 2024"
        elif 'technology' in topic.lower():
            return f"{topic}: Latest Trends and Innovations"
        elif 'business' in topic.lower():
            return f"Mastering {topic}: Strategies for Success"
        else:
            return f"Complete Guide to {topic}: Everything You Need to Know"
    
    def _generate_topic_keywords(self, topic: str) -> list:
        """Generate keywords based on topic type"""
        topic_lower = topic.lower()
        base_keywords = [topic, "2024", "guide"]
        
        if 'ai' in topic_lower or 'artificial intelligence' in topic_lower:
            return base_keywords + ["technology", "machine learning", "automation", "innovation"]
        elif 'business' in topic_lower:
            return base_keywords + ["strategy", "success", "growth", "entrepreneurship"]
        elif 'technology' in topic_lower:
            return base_keywords + ["tech", "innovation", "digital", "future"]
        else:
            return base_keywords + ["tips", "advice", "information"]
    
    def _generate_topic_hashtags(self, topic: str, platform: str) -> list:
        """Generate hashtags based on topic type"""
        topic_lower = topic.lower()
        topic_clean = topic.replace(' ', '').replace('-', '')
        
        base_tags = [f"#{topic_clean}", "#2024"]
        
        if 'ai' in topic_lower or 'artificial intelligence' in topic_lower:
            topic_tags = ["#AI", "#ArtificialIntelligence", "#MachineLearning", "#Technology", "#Innovation"]
        elif 'business' in topic_lower:
            topic_tags = ["#Business", "#Entrepreneurship", "#Success", "#Strategy", "#Growth"]
        elif 'technology' in topic_lower:
            topic_tags = ["#Technology", "#Tech", "#Innovation", "#Digital", "#Future"]
        else:
            topic_tags = ["#Guide", "#Tips", "#Information", "#Knowledge"]
        
        platform_tags = {
            "instagram": ["#instagood", "#viral", "#explore"],
            "twitter": ["#thread", "#trending", "#viral"],
            "linkedin": ["#professional", "#business", "#career"],
            "youtube": ["#tutorial", "#educational", "#howto"],
            "facebook": ["#share", "#discussion", "#community"]
        }
        
        platform_key = platform.lower().split()[-1] if " " in platform else platform.lower()
        specific_tags = platform_tags.get(platform_key, ["#content"])
        
        return base_tags + topic_tags[:3] + specific_tags[:2] + ["#trending"]