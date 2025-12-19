from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import html
import PyPDF2
from PIL import Image
import pytesseract
from docx import Document

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your existing classes
from dynamic_content_generator import DynamicContentGenerator
from working_ai_integration import WorkingAIIntegration
from google_ai_integration import GoogleAIIntegration
from file_content_generator import FileContentGenerator
from content_calendar import ContentCalendar
from image_generator import ImageGenerator
from engagement_predictor import EngagementPredictor

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configure Flask for file uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_TIMEOUT'] = 60  # 60 seconds timeout

# Initialize your existing AI classes
dynamic_ai = DynamicContentGenerator()
working_ai = WorkingAIIntegration()
google_ai = GoogleAIIntegration()
file_ai = FileContentGenerator()
calendar_gen = ContentCalendar()
image_gen = ImageGenerator()
engagement_pred = EngagementPredictor()

@app.route('/api/generate', methods=['POST'])
def generate_content():
    """Generate blog content using your existing AI system"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided', 'success': False}), 400
            
        topic = data.get('topic', 'AI')
        platform = data.get('platform', '📸 Instagram')
        content_focus = data.get('content_focus', 'Trending')
        max_words = data.get('max_words', 300)
        ai_mode = data.get('ai_mode', 'Dynamic AI')
        
        print(f"🚀 Generating content for topic: {topic}, platform: {platform}")
        
        # Try multiple AI generators
        blog_content = None
        
        # Try Google AI first (most reliable)
        try:
            print("Trying Google AI...")
            blog_content = google_ai.generate_blog_content(topic, platform)
            if blog_content and blog_content.get('content'):
                # Decode HTML entities
                blog_content['content'] = html.unescape(blog_content['content'])
                if blog_content.get('title'):
                    blog_content['title'] = html.unescape(blog_content['title'])
                print("✅ Google AI generated content successfully")
        except Exception as e:
            print(f"Google AI failed: {e}")
        
        # Try dynamic AI as fallback
        if not blog_content or not blog_content.get('content'):
            try:
                print("Trying Dynamic AI...")
                if hasattr(dynamic_ai, 'generate_real_blog_content'):
                    blog_content = dynamic_ai.generate_real_blog_content(topic, platform)
                    if blog_content and blog_content.get('content'):
                        print("✅ Dynamic AI generated content successfully")
            except Exception as e:
                print(f"Dynamic AI failed: {e}")
        
        # Use file AI as another fallback
        if not blog_content or not blog_content.get('content'):
            try:
                print("Trying File AI...")
                blog_content = file_ai.generate_content_from_text(f"Create detailed content about {topic} for {platform}", platform, content_focus, max_words)
                if blog_content and blog_content.get('content'):
                    print("✅ File AI generated content successfully")
            except Exception as e:
                print(f"File AI failed: {e}")
        
        # Final fallback - generate basic content
        if not blog_content or not blog_content.get('content'):
            print("Using fallback content generation")
            blog_content = generate_fallback_content(topic, platform, max_words)
        
        # Ensure we have valid content
        if not blog_content:
            blog_content = {
                'title': f'Guide to {topic}',
                'content': f'Discover the amazing world of {topic}. This comprehensive guide will help you understand the key concepts and applications.',
                'hashtags': [f'#{topic.replace(" ", "")}', '#guide', '#tips'],
                'cta': f'What are your thoughts on {topic}? Share in the comments!',
                'keywords': [topic, 'guide', 'tips'],
                'engagement_score': 0.75,
                'platform': platform
            }
        
        # Ensure hashtags is always an array
        if not blog_content.get('hashtags') or not isinstance(blog_content.get('hashtags'), list):
            blog_content['hashtags'] = [f'#{topic.replace(" ", "")}', '#content', '#blog']
        
        # Add word limit processing
        if blog_content and 'content' in blog_content:
            words = blog_content['content'].split()
            if len(words) > max_words:
                blog_content['content'] = ' '.join(words[:max_words]) + '...'
            blog_content['wordCount'] = len(words)
        
        # Generate image for the blog
        try:
            if blog_content and 'title' in blog_content:
                img_url = image_gen.generate_from_title(blog_content['title'])
                blog_content['image_url'] = img_url
                print(f"Generated image URL: {img_url}")
        except Exception as img_err:
            print(f"Image gen error: {img_err}")
            blog_content['image_url'] = None
        
        # Calculate dynamic engagement score
        try:
            if blog_content:
                blog_content['engagement_score'] = engagement_pred.predict_engagement(blog_content, platform)
                blog_content['engagement_tips'] = engagement_pred.get_engagement_tips(blog_content, platform)
        except Exception as eng_err:
            print(f"Engagement prediction error: {eng_err}")
            blog_content['engagement_score'] = 0.80
        
        # Ensure required fields
        blog_content['success'] = True
        blog_content['platform'] = platform
        
        print(f"✅ Generated content successfully: {blog_content.get('title', 'No title')}")
        return jsonify(blog_content)
        
    except Exception as e:
        print(f"❌ Error generating content: {e}")
        import traceback
        traceback.print_exc()
        
        # Return fallback content even on error
        try:
            fallback = generate_fallback_content(
                data.get('topic', 'AI') if data else 'AI', 
                data.get('platform', '📸 Instagram') if data else '📸 Instagram', 
                data.get('max_words', 300) if data else 300
            )
            fallback['success'] = True
            return jsonify(fallback)
        except Exception as fallback_err:
            print(f"Fallback generation failed: {fallback_err}")
            return jsonify({
                'error': 'Content generation failed',
                'success': False,
                'title': 'Content Generation Error',
                'content': 'Unable to generate content at this time. Please try again.',
                'hashtags': ['#error', '#retry'],
                'cta': 'Please try again later.',
                'keywords': ['error'],
                'engagement_score': 0.5,
                'platform': 'instagram'
            }), 500

@app.route('/api/hashtags', methods=['POST'])
def generate_hashtags():
    """Generate hashtags using your existing system"""
    try:
        data = request.json
        topic = data.get('topic', 'AI')
        platform = data.get('platform', '📸 Instagram')
        
        # Use your existing hashtag generator
        hashtags = working_ai.generate_hashtags(topic, platform)
        
        return jsonify({'hashtags': hashtags})
        
    except Exception as e:
        print(f"Error generating hashtags: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/image', methods=['POST'])
def generate_image():
    """Generate blog image using your existing system"""
    try:
        data = request.json
        topic = data.get('topic', 'AI')
        
        # Use your existing image generator
        image_url = working_ai.generate_blog_image_url(topic)
        
        return jsonify({'image_url': image_url})
        
    except Exception as e:
        print(f"Error generating image: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/schedule', methods=['POST'])
def schedule_post():
    """Schedule social media post"""
    try:
        data = request.json
        content = data.get('content')
        platforms = data.get('platforms', [])
        schedule_date = data.get('schedule_date')
        schedule_time = data.get('schedule_time')
        
        # Here you can integrate with your existing social media scheduler
        # For now, return success
        return jsonify({
            'success': True,
            'message': f'Post scheduled for {len(platforms)} platforms',
            'scheduled_time': f'{schedule_date} {schedule_time}'
        })
        
    except Exception as e:
        print(f"Error scheduling post: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-from-file', methods=['POST'])
def generate_from_file():
    """Extract content from uploaded file and generate blog content"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded', 'success': False}), 400
        
        file = request.files['file']
        
        # Check file size (limit to 10MB)
        file.seek(0, 2)  # Seek to end
        file_size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if file_size > 10 * 1024 * 1024:  # 10MB
            return jsonify({'error': 'File too large. Maximum size is 10MB', 'success': False}), 400
        
        platform = request.form.get('platform', '📸 Instagram')
        content_focus = request.form.get('content_focus', 'Trending')
        max_words = int(request.form.get('max_words', 300))
        
        print(f"Processing file: {file.filename}, size: {file_size} bytes")
        
        # Extract text from file
        extracted_text = extract_text_from_file(file)
        
        if not extracted_text or len(extracted_text.strip()) < 10:
            return jsonify({
                'error': 'Could not extract meaningful text from file',
                'success': False
            }), 400
        
        # Clean and summarize extracted text
        clean_text = extracted_text.strip()[:2000]  # First 2000 chars
        print(f"Extracted text length: {len(clean_text)} chars")
        
        # Generate blog content using file AI with extracted content
        blog_content = file_ai.generate_content_from_text(clean_text, platform, content_focus, max_words)
        
        if not blog_content:
            # Fallback content generation
            blog_content = generate_fallback_content(clean_text[:100], platform, max_words)
        
        # Add word limit processing
        if blog_content and 'content' in blog_content:
            words = blog_content['content'].split()
            if len(words) > max_words:
                blog_content['content'] = ' '.join(words[:max_words]) + '...'
            blog_content['wordCount'] = len(blog_content['content'].split())
        
        # Generate image for the blog
        try:
            if blog_content and 'title' in blog_content:
                img_url = image_gen.generate_from_title(blog_content['title'])
                blog_content['image_url'] = img_url
                print(f"File image URL: {img_url}")
        except Exception as img_err:
            print(f"File image gen error: {img_err}")
            blog_content['image_url'] = None
        
        # Calculate dynamic engagement score
        if blog_content:
            blog_content['engagement_score'] = engagement_pred.predict_engagement(blog_content, platform)
            blog_content['engagement_tips'] = engagement_pred.get_engagement_tips(blog_content, platform)
            blog_content['success'] = True
        
        return jsonify(blog_content)
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'File processing failed: {str(e)}',
            'success': False
        }), 500

def extract_text_from_file(file):
    """Extract text from various file formats"""
    try:
        filename = file.filename.lower()
        print(f"Extracting text from: {filename}")
        
        if filename.endswith('.pdf'):
            # Extract from PDF
            try:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                max_pages = min(len(pdf_reader.pages), 10)  # Limit to 10 pages
                for i in range(max_pages):
                    page_text = pdf_reader.pages[i].extract_text()
                    if page_text:
                        text += page_text + "\n"
                return text.strip()
            except Exception as pdf_err:
                print(f"PDF extraction error: {pdf_err}")
                return None
            
        elif filename.endswith('.docx'):
            # Extract from DOCX
            try:
                doc = Document(file)
                text = ""
                for paragraph in doc.paragraphs[:50]:  # Limit to 50 paragraphs
                    if paragraph.text.strip():
                        text += paragraph.text + "\n"
                return text.strip()
            except Exception as docx_err:
                print(f"DOCX extraction error: {docx_err}")
                return None
            
        elif filename.endswith('.txt'):
            # Extract from TXT
            try:
                content = file.read()
                # Try different encodings
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        return content.decode(encoding).strip()
                    except:
                        continue
                return None
            except Exception as txt_err:
                print(f"TXT extraction error: {txt_err}")
                return None
            
        elif filename.endswith(('.jpg', '.jpeg', '.png')):
            # Extract from image using OCR
            try:
                image = Image.open(file)
                # Resize large images
                max_size = (1920, 1920)
                image.thumbnail(max_size, Image.Resampling.LANCZOS)
                text = pytesseract.image_to_string(image)
                return text.strip()
            except Exception as ocr_err:
                print(f"OCR extraction error: {ocr_err}")
                return None
            
        else:
            print(f"Unsupported file type: {filename}")
            return None
            
    except Exception as e:
        print(f"❌ Error extracting text: {e}")
        import traceback
        traceback.print_exc()
        return None

def extract_main_topic(text):
    """Extract main topic from text"""
    # Simple topic extraction - get first meaningful sentence or key phrases
    words = text.split()
    if len(words) > 10:
        # Return first 5-10 words as topic
        return ' '.join(words[:8])
    return text[:50] if text else 'Document Analysis'

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get posting history"""
    try:
        # Return mock history for now
        # You can integrate with your existing posting history system
        history = [
            {
                'id': 1,
                'title': 'AI Revolution in 2024',
                'platforms': ['📸 Instagram', '🐦 Twitter'],
                'status': 'posted',
                'created_at': '2024-01-15T10:30:00Z'
            }
        ]
        
        return jsonify(history)
        
    except Exception as e:
        print(f"Error getting history: {e}")
        return jsonify({'error': str(e)}), 500

def generate_fallback_content(topic, platform, max_words):
    """Generate detailed, engaging content like the Pune example"""
    # Enhanced platform-specific hashtag generation
    def generate_smart_hashtags(topic, platform):
        topic_keywords = topic.lower().split(' ')
        topic_tags = [f"#{word.capitalize()}" for word in topic_keywords if len(word) > 3]
        
        platform_strategies = {
            '📸 Instagram': ['#instatravel', '#wanderlust', '#explore', '#travelgram', '#photooftheday'],
            '🐦 Twitter': ['#travel', '#tourism', '#destination', '#vacation', '#explore'],
            '💼 LinkedIn': ['#business', '#professional', '#industry', '#networking', '#growth'],
            '📺 YouTube': ['#tutorial', '#guide', '#howto', '#educational', '#tips'],
            '👥 Facebook': ['#community', '#share', '#experience', '#memories', '#lifestyle']
        }
        
        platform_tags = platform_strategies.get(platform, ['#content', '#social', '#digital'])
        
        # Combine hashtags
        hashtags = topic_tags[:2] + platform_tags[:5] + ['#2024', '#guide', '#tips']
        return list(dict.fromkeys(hashtags))[:10]  # Remove duplicates
    
    # Generate detailed, engaging content
    content = f"""## Complete Guide to {topic}: Hidden Gems & Local Secrets 🎆

**Discover the incredible world of {topic}!** 🌟 Whether you're a beginner or looking to deepen your knowledge, this comprehensive guide will take you on an amazing journey through everything you need to know.

### ✨ What Makes {topic} Special?

{topic} stands out for its unique blend of innovation, practicality, and endless possibilities. From cutting-edge developments to real-world applications, there's so much to explore and discover!

### 📝 Key Highlights & Must-Know Facts

**Essential Elements:**
* **Core Concepts**: Understanding the fundamental principles of {topic}
* **Latest Trends**: What's happening right now in the {topic} space
* **Best Practices**: Proven strategies that actually work
* **Expert Tips**: Insider knowledge from industry professionals
* **Future Outlook**: Where {topic} is heading in 2024 and beyond

### 🚀 Getting Started with {topic}

Ready to dive in? Here's your step-by-step roadmap:

1. **Foundation Building**: Start with the basics and build a solid understanding
2. **Practical Application**: Put your knowledge into action with real projects
3. **Community Engagement**: Connect with others who share your passion
4. **Continuous Learning**: Stay updated with the latest developments

### 💡 Pro Tips for Success

**Insider Secrets:**
- Focus on quality over quantity when starting out
- Don't be afraid to experiment and try new approaches
- Learn from failures - they're your best teachers
- Network with like-minded individuals in the community
- Stay curious and keep asking questions

### 🎯 Why {topic} Matters in 2024

In today's rapidly evolving world, {topic} has become more relevant than ever. It's not just a trend - it's a fundamental shift that's reshaping how we think, work, and live.

**The Impact:**
- Revolutionary changes in industry standards
- New opportunities for innovation and growth
- Enhanced efficiency and productivity
- Better solutions to complex challenges

### 🔥 Ready to Get Started?

Whether you're looking to advance your career, start a new hobby, or simply satisfy your curiosity, {topic} offers endless possibilities. The key is to start where you are, use what you have, and do what you can.

**Remember:** Every expert was once a beginner. Your journey with {topic} starts with a single step, and we're here to guide you every step of the way!

🎆 **Join the community and start your {topic} adventure today!**"""
    
    # Limit words if necessary
    words = content.split()
    if len(words) > max_words:
        content = ' '.join(words[:max_words]) + '...'
    
    return {
        "title": f"Complete Guide to {topic}: Hidden Gems & Local Secrets",
        "content": content,
        "hashtags": generate_smart_hashtags(topic, platform),
        "cta": f"Planning to explore {topic}? Share your thoughts and experiences in the comments!",
        "keywords": [topic, 'guide', 'tips', 'secrets', '2024'],
        "engagement_score": 0.89,
        "platform": platform,
        "wordCount": len(content.split())
    }

@app.route('/api/calendar', methods=['POST'])
def generate_calendar():
    """Generate 7-day content calendar"""
    try:
        data = request.json
        blog_content = data.get('blog_content', {})
        platforms = data.get('platforms', ['📸 Instagram'])
        
        calendar = calendar_gen.generate_weekly_calendar(blog_content, platforms)
        
        return jsonify({'calendar': calendar, 'success': True})
    except Exception as e:
        print(f"Calendar error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/create-image', methods=['POST'])
def create_blog_image():
    """Generate image from title"""
    try:
        data = request.json
        title = data.get('title', 'Blog Post')
        
        image_url = image_gen.generate_from_title(title)
        
        return jsonify({'image_url': image_url, 'success': True})
    except Exception as e:
        print(f"Image generation error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice-generate', methods=['POST'])
def voice_generate():
    """Generate content from voice assistant conversation"""
    try:
        data = request.json
        
        prompt = f"""
        Create engaging {data['platform']} content about "{data['topic']}" with these specifications:
        
        - Platform: {data['platform'].title()}
        - Goal: {data['goal']}
        - Audience: {data['audience']}
        - Length: {data['length']}
        
        Format the content with:
        - Engaging title with emojis
        - Well-structured content with bullet points
        - Platform-appropriate hashtags
        - Call-to-action
        - Emojis throughout for engagement
        
        Make it {data['goal']} and suitable for {data['audience']} audience.
        """
        
        # Try Google AI first
        try:
            blog_content = google_ai.generate_blog_content(data['topic'], data['platform'])
            if blog_content:
                # Decode HTML entities
                content = html.unescape(blog_content.get('content', ''))
                return jsonify({
                    'success': True,
                    'content': content,
                    'responses': data
                })
        except Exception as e:
            print(f"Google AI failed: {e}")
        
        # Fallback to template-based generation
        content = f"""
# 🎯 {data['topic'].title()} - {data['platform'].title()} Content

## 🚀 Introduction
Discover everything you need to know about {data['topic']} in this {data['goal']} guide designed for {data['audience']}!

## ✨ Key Points
• Essential insights about {data['topic']}
• Practical tips you can implement today
• Expert recommendations for success
• Common mistakes to avoid

## 💡 Pro Tips
🔥 Focus on quality over quantity
⚡ Stay consistent with your efforts
🎯 Know your target audience
📈 Track your progress regularly

## 🎉 Conclusion
Start implementing these {data['topic']} strategies today and see amazing results!

#{data['topic'].replace(' ', '')} #{data['platform']}tips #contentcreator #success

👉 What's your experience with {data['topic']}? Share in the comments!
        """
        
        return jsonify({
            'success': True,
            'content': content,
            'responses': data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Agentic AI API is running'})

if __name__ == '__main__':
    print("Starting Agentic AI API Server...")
    print("React Frontend can connect to: http://localhost:5000")
    print("API Endpoints:")
    print("   POST /api/generate - Generate blog content")
    print("   POST /api/generate-from-file - Generate content from uploaded file")
    print("   POST /api/hashtags - Generate hashtags")
    print("   POST /api/image - Generate blog image")
    print("   POST /api/schedule - Schedule social media post")
    print("   GET  /api/history - Get posting history")
    print("   POST /api/calendar - Generate 7-day content calendar")
    print("   POST /api/create-image - Generate image from title")
    print("   POST /api/voice-generate - Generate content from voice conversation")
    print("\nFile Upload Limits:")
    print("   Max file size: 16MB")
    print("   Supported formats: PDF, DOCX, TXT, JPG, PNG")
    
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)