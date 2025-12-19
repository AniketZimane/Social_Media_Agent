import requests
import os
from urllib.parse import quote
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class ImageGenerator:
    def __init__(self):
        self.aiml_api_key = os.getenv("AIML_API_KEY")
        self.aiml_url = "https://api.aimlapi.com/images/generations"
        self.fallback_url = "https://image.pollinations.ai/prompt/"
    
    def generate_from_title(self, title: str) -> str:
        """Generate image using AIML API with fallback"""
        if self.aiml_api_key:
            aiml_result = self._generate_with_aiml(title)
            if aiml_result:
                return aiml_result
        
        return self._generate_with_pollinations(title)
    
    def _generate_with_aiml(self, title: str) -> Optional[str]:
        """Generate image using AIML API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.aiml_api_key}",
                "Content-Type": "application/json"
            }
            
            prompt = f"professional blog header image about {title}, modern design, clean layout, vibrant colors, high quality"
            
            payload = {
                "model": "flux-pro/v1.1",
                "prompt": prompt[:300],
                "image_size": "1200x630",
                "num_inference_steps": 4,
                "guidance_scale": 3.5,
                "num_images": 1
            }
            
            response = requests.post(self.aiml_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if result.get("data") and len(result["data"]) > 0:
                    image_url = result["data"][0].get("url")
                    print(f"✅ AIML image generated: {image_url}")
                    return image_url
            
            print(f"⚠️ AIML API failed: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"⚠️ AIML generation failed: {e}")
            return None
    
    def _generate_with_pollinations(self, title: str) -> str:
        """Fallback to Pollinations AI"""
        try:
            clean_title = title.replace(':', '').replace('?', '').strip()[:100]
            prompt = f"professional blog header image, {clean_title}, modern design, high quality, 16:9"
            encoded_prompt = quote(prompt)
            
            image_url = f"{self.fallback_url}{encoded_prompt}?width=1200&height=630&nologo=true"
            print(f"🎨 Pollinations image: {image_url}")
            return image_url
            
        except Exception as e:
            print(f"❌ Image generation error: {e}")
            return f"https://via.placeholder.com/1200x630/6366f1/ffffff?text={quote(title[:30])}"
