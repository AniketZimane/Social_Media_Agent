import replicate
import os
from typing import Dict, List
from dotenv import load_dotenv
import json
import requests

load_dotenv()

class ReplicateIntegration:
    def __init__(self):
        self.api_token = os.getenv("REPLICATE_API_TOKEN")
        if self.api_token:
            os.environ["REPLICATE_API_TOKEN"] = self.api_token
    
    def generate_full_blog_content(self, topic: str, platform: str) -> Dict:
        """Generate complete blog content with hashtags"""
        try:
            prompt = f"""Write a complete blog post about "{topic}" optimized for {platform}.
            
            Include:
            1. Engaging title
            2. Full blog content (300-500 words)
            3. 10 relevant hashtags
            4. Call-to-action
            5. SEO keywords
            
            Format as JSON with fields: title, content, hashtags, cta, keywords"""
            
            output = replicate.run(
                "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
                input={
                    "prompt": prompt,
                    "max_new_tokens": 800,
                    "temperature": 0.7
                }
            )
            
            # Join output if it's a list
            content = "".join(output) if isinstance(output, list) else str(output)
            
            # Try to parse JSON
            if "{" in content and "}" in content:
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            
            # Fallback: extract from text
            return self._extract_blog_from_text(content, topic, platform)
            
        except Exception as e:
            print(f"Replicate error: {e}")
            return self._fallback_blog_content(topic, platform)
    
    def generate_blog_image(self, topic: str, style: str = "professional") -> str:
        """Generate blog image using Replicate"""
        try:
            prompt = f"Professional blog header image about {topic}, {style} style, high quality, 16:9 aspect ratio"
            
            output = replicate.run(
                "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
                input={
                    "prompt": prompt,
                    "width": 1024,
                    "height": 576,
                    "num_outputs": 1
                }
            )
            
            return output[0] if output else None
            
        except Exception as e:
            print(f"Image generation error: {e}")
            return None
    
    def generate_hashtags(self, topic: str, platform: str) -> List[str]:
        """Generate platform-specific hashtags"""
        try:
            prompt = f"Generate 15 trending hashtags for {topic} on {platform}. Return as comma-separated list."
            
            output = replicate.run(
                "meta/llama-2-7b-chat:8e6975e5ed6174911a6ff3d60540dfd4844201974602551e10e9e87ab143d81e",
                input={
                    "prompt": prompt,
                    "max_new_tokens": 100,
                    "temperature": 0.5
                }
            )
            
            content = "".join(output) if isinstance(output, list) else str(output)
            
            # Extract hashtags
            hashtags = []
            for word in content.split():
                if word.startswith('#') and len(word) > 2:
                    hashtags.append(word)
                elif ',' in content:
                    # Handle comma-separated format
                    tags = [tag.strip() for tag in content.split(',')]
                    hashtags.extend([f"#{tag.replace('#', '')}" for tag in tags if tag.strip()])
                    break
            
            return hashtags[:15] if hashtags else self._fallback_hashtags(topic, platform)
            
        except Exception as e:
            print(f"Hashtag generation error: {e}")
            return self._fallback_hashtags(topic, platform)
    
    def enhance_content_with_ai(self, content: str, platform: str) -> Dict:
        """Enhance existing content with AI suggestions"""
        try:
            prompt = f"""Enhance this content for {platform}:
            "{content}"
            
            Provide:
            1. Improved title
            2. Engagement score (0.7-0.95)
            3. 3 optimization tips
            4. Best posting time
            
            Format as JSON."""
            
            output = replicate.run(
                "meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d",
                input={
                    "prompt": prompt,
                    "max_new_tokens": 300,
                    "temperature": 0.6
                }
            )
            
            content = "".join(output) if isinstance(output, list) else str(output)
            
            if "{" in content and "}" in content:
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                json_str = content[json_start:json_end]
                return json.loads(json_str)
            
        except Exception as e:
            print(f"Content enhancement error: {e}")
        
        return {
            "improved_title": content[:50] + "...",
            "engagement_score": 0.82,
            "tips": ["Use trending hashtags", "Post at peak hours", "Add visual elements"],
            "best_time": "6-9 PM"
        }
    
    def _extract_blog_from_text(self, text: str, topic: str, platform: str) -> Dict:
        """Extract blog components from plain text"""
        lines = text.split('\n')
        
        title = f"The Ultimate Guide to {topic}"
        content = f"Discover everything you need to know about {topic}. This comprehensive guide covers the latest trends, insights, and practical tips to help you succeed."
        
        # Try to find title and content in text
        for i, line in enumerate(lines):
            if len(line.strip()) > 20 and i < 3:
                title = line.strip()[:100]
                break
        
        # Get content from remaining lines
        content_lines = [line.strip() for line in lines[1:] if len(line.strip()) > 20]
        if content_lines:
            content = " ".join(content_lines[:3])
        
        return {
            "title": title,
            "content": content,
            "hashtags": self._fallback_hashtags(topic, platform),
            "cta": f"What do you think about {topic}? Share your thoughts!",
            "keywords": [topic, platform.split()[-1], "trending", "2024"]
        }
    
    def _fallback_blog_content(self, topic: str, platform: str) -> Dict:
        """Fallback blog content when AI fails"""
        return {
            "title": f"The Future of {topic}: What You Need to Know",
            "content": f"In today's rapidly evolving world, {topic} is becoming increasingly important. This comprehensive guide explores the latest developments, trends, and insights that are shaping the future of {topic}. Whether you're a beginner or an expert, you'll find valuable information to help you stay ahead of the curve.",
            "hashtags": self._fallback_hashtags(topic, platform),
            "cta": f"Ready to dive deeper into {topic}? Follow for more insights!",
            "keywords": [topic, "future", "trends", "guide", "2024"]
        }
    
    def _fallback_hashtags(self, topic: str, platform: str) -> List[str]:
        """Fallback hashtags when AI generation fails"""
        base_tags = [f"#{topic.replace(' ', '')}", "#trending", "#2024"]
        
        platform_tags = {
            "instagram": ["#instagood", "#photooftheday", "#viral", "#explore"],
            "twitter": ["#breaking", "#news", "#thread", "#viral"],
            "linkedin": ["#professional", "#business", "#career", "#industry"],
            "youtube": ["#tutorial", "#howto", "#educational", "#subscribe"],
            "facebook": ["#community", "#share", "#like", "#follow"]
        }
        
        platform_key = platform.lower().split()[-1] if " " in platform else platform.lower()
        platform_specific = platform_tags.get(platform_key, ["#content", "#social", "#digital"])
        
        return base_tags + platform_specific + ["#AI", "#tech", "#innovation"]