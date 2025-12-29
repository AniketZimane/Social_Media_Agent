import requests
import os
from dotenv import load_dotenv

load_dotenv()

class AIMLImageGenerator:
    def __init__(self):
        self.api_key = os.getenv('AIML_API_KEY')
        self.base_url = "https://api.aimlapi.com/v1/images/generations/"
        
    def generate_image_from_title(self, blog_title: str) -> dict:
        """Generate image based on blog title"""
        
        # Create a visual prompt based on the blog title
        visual_prompt = self._create_visual_prompt(blog_title)
        
        payload = {
            "model": "flux/schnell",
            "prompt": visual_prompt
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "content-type": "application/json"
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "image_url": result.get("data", [{}])[0].get("url", ""),
                "prompt": visual_prompt
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "prompt": visual_prompt
            }
    
    def _create_visual_prompt(self, title: str) -> str:
        """Create visual prompt based on blog title"""
        title_lower = title.lower()
        
        # AI/Technology themes
        if any(word in title_lower for word in ['ai', 'artificial intelligence', 'machine learning', 'tech', 'robot']):
            return f"Create a modern, futuristic illustration representing '{title}'. Include sleek technology elements, digital interfaces, and a professional blue and purple color scheme. High quality, clean design."
        
        # Business/Marketing themes
        elif any(word in title_lower for word in ['business', 'marketing', 'startup', 'growth', 'strategy']):
            return f"Create a professional business illustration for '{title}'. Include modern office elements, growth charts, and corporate imagery. Clean, minimalist design with blue and green accents."
        
        # Social Media themes
        elif any(word in title_lower for word in ['social media', 'instagram', 'twitter', 'linkedin', 'content']):
            return f"Create a vibrant social media themed illustration for '{title}'. Include social network icons, engagement symbols, and colorful modern design elements."
        
        # Education/Learning themes
        elif any(word in title_lower for word in ['learn', 'guide', 'tutorial', 'education', 'tips']):
            return f"Create an educational illustration for '{title}'. Include books, learning symbols, and knowledge-themed elements. Warm, inviting colors with professional styling."
        
        # Default creative prompt
        else:
            return f"Create a professional, modern illustration representing the concept of '{title}'. Use clean design, vibrant colors, and engaging visual elements that capture the essence of the topic."

# Flask API endpoint for image generation
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

image_generator = AIMLImageGenerator()

@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    """API endpoint to generate image from blog title"""
    data = request.json
    title = data.get('title', '')
    
    if not title:
        return jsonify({'success': False, 'error': 'Title is required'}), 400
    
    result = image_generator.generate_image_from_title(title)
    return jsonify(result)

if __name__ == '__main__':
    # Test the image generator
    generator = AIMLImageGenerator()
    
    test_titles = [
        "AI Tools Every Startup Founder Should Use in 2025",
        "Social Media Marketing Strategies for Small Business",
        "Complete Guide to Content Creation"
    ]
    
    for title in test_titles:
        print(f"\n🎨 Generating image for: {title}")
        result = generator.generate_image_from_title(title)
        
        if result['success']:
            print(f"✅ Success! Image URL: {result['image_url']}")
            print(f"📝 Prompt: {result['prompt']}")
        else:
            print(f"❌ Error: {result['error']}")
    
    # Start Flask server
    print("\n🚀 Starting Image Generation API on http://localhost:5002")
    app.run(debug=True, port=5002)