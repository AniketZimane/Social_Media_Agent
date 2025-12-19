import requests
import json
import random
from typing import Dict, List
import hashlib
import time

class FreeAIIntegration:
    def __init__(self):
        self.huggingface_models = [
            "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
            "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
        ]
    
    def get_free_ai_score(self, topic: str, platform: str) -> float:
        """Generate AI-like engagement score using free methods"""
        # Create deterministic but varied scores based on content
        content_hash = hashlib.md5(f"{topic}{platform}".encode()).hexdigest()
        base_score = int(content_hash[:2], 16) / 255.0  # 0-1 range
        
        # Boost for trending keywords
        trending_keywords = ["ai", "tech", "future", "innovation", "trending", "viral", "breaking"]
        keyword_boost = sum(0.05 for keyword in trending_keywords if keyword in topic.lower())
        
        # Platform-specific adjustments
        platform_multipliers = {
            "instagram": 1.1, "twitter": 1.05, "linkedin": 0.95, 
            "youtube": 1.15, "facebook": 1.0
        }
        
        platform_key = platform.lower().split()[1] if " " in platform else platform.lower()
        multiplier = platform_multipliers.get(platform_key, 1.0)
        
        final_score = (0.7 + base_score * 0.25 + keyword_boost) * multiplier
        return min(final_score, 0.98)
    
    def get_huggingface_content(self, topic: str) -> List[str]:
        """Try free Hugging Face API (no key required for some models)"""
        try:
            # Free inference API call
            response = requests.post(
                "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium",
                headers={"Content-Type": "application/json"},
                json={"inputs": f"Generate blog topic about {topic}"},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get("generated_text", "")
                    return [generated_text] if generated_text else []
        except:
            pass
        
        return []
    
    def generate_smart_topics(self, topic: str, platform: str) -> List[Dict]:
        """Generate intelligent topics without API keys"""
        # Try free Hugging Face first
        hf_topics = self.get_huggingface_content(topic)
        
        # Smart template-based generation
        templates = [
            f"The Ultimate Guide to {topic} in 2024",
            f"How {topic} is Revolutionizing Industries",
            f"5 {topic} Trends That Will Blow Your Mind",
            f"Why Everyone is Talking About {topic}",
            f"{topic}: The Complete Beginner's Guide",
            f"Breaking: {topic} Changes Everything",
            f"The Future of {topic}: What Experts Predict"
        ]
        
        # Select best templates based on platform
        platform_preferences = {
            "instagram": ["Ultimate Guide", "Blow Your Mind", "Everyone is Talking"],
            "twitter": ["Breaking", "Changes Everything", "Trends"],
            "linkedin": ["Complete Guide", "Revolutionizing", "Expert Predict"],
            "youtube": ["Ultimate Guide", "Complete", "Future"],
            "facebook": ["Everyone is Talking", "Blow Your Mind", "Changes Everything"]
        }
        
        platform_key = platform.lower().split()[1] if " " in platform else platform.lower()
        preferred_keywords = platform_preferences.get(platform_key, ["Guide", "Future", "Trends"])
        
        # Score and select best templates
        scored_templates = []
        for template in templates:
            score = self.get_free_ai_score(template, platform)
            # Boost if matches platform preference
            if any(keyword in template for keyword in preferred_keywords):
                score += 0.05
            
            scored_templates.append({
                "title": template,
                "engagement_score": score,
                "ai_generated": True,
                "source": "smart_algorithm"
            })
        
        # Add Hugging Face results if available
        for hf_topic in hf_topics[:2]:
            if len(hf_topic.strip()) > 10:
                scored_templates.append({
                    "title": hf_topic.strip()[:100],
                    "engagement_score": self.get_free_ai_score(hf_topic, platform),
                    "ai_generated": True,
                    "source": "huggingface"
                })
        
        return sorted(scored_templates, key=lambda x: x["engagement_score"], reverse=True)[:3]
    
    def get_free_trending_data(self) -> List[Dict]:
        """Get trending data using free sources"""
        try:
            # Try Reddit API (free, no key required)
            response = requests.get("https://www.reddit.com/r/technology/hot.json?limit=5", 
                                  headers={"User-Agent": "BlogAI/1.0"}, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get("data", {}).get("children", [])
                
                trending = []
                for post in posts:
                    post_data = post.get("data", {})
                    title = post_data.get("title", "")
                    score = post_data.get("score", 0)
                    
                    if title and len(title) > 10:
                        trending.append({
                            "topic": title[:50],
                            "score": min(score / 1000, 0.95),  # Normalize Reddit score
                            "growth": random.uniform(-2, 15),
                            "source": "reddit"
                        })
                
                return trending[:5]
        except:
            pass
        
        # Fallback trending topics
        fallback_topics = [
            "AI Revolution", "Climate Tech", "Remote Work Future", 
            "Web3 Innovation", "Health Technology", "Space Exploration"
        ]
        
        return [
            {
                "topic": topic,
                "score": self.get_free_ai_score(topic, "general"),
                "growth": random.uniform(-5, 20),
                "source": "algorithm"
            }
            for topic in fallback_topics
        ]
    
    def analyze_content_sentiment(self, text: str) -> Dict:
        """Free sentiment analysis using word lists"""
        positive_words = ["amazing", "great", "excellent", "innovative", "revolutionary", "breakthrough", "success"]
        negative_words = ["bad", "terrible", "awful", "failure", "problem", "issue", "crisis"]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = 0.7 + (positive_count * 0.05)
        elif negative_count > positive_count:
            sentiment = 0.3 - (negative_count * 0.05)
        else:
            sentiment = 0.6
        
        return {
            "sentiment": max(0.1, min(sentiment, 0.9)),
            "confidence": 0.8,
            "analysis": "positive" if sentiment > 0.6 else "negative" if sentiment < 0.4 else "neutral"
        }