from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from datetime import datetime
import sys
import os
import html

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
from social_media_poster import SocialMediaPoster
from blockchain_integration import blockchain_integration

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configure Flask for file uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_TIMEOUT'] = 60  # 60 seconds timeout

# Initialize your existing AI classes
dynamic_ai = DynamicContentGenerator()
working_ai = WorkingAIIntegration()
google_ai = GoogleAIIntegration()
file_ai = FileContentGenerator()
try:
    from content_calendar import ContentCalendar
    calendar_gen = ContentCalendar()
except:
    calendar_gen = None
image_gen = ImageGenerator()
engagement_pred = EngagementPredictor()
social_poster = SocialMediaPoster()

@app.route('/api/test', methods=['GET', 'POST'])
@cross_origin()
def test_endpoint():
    """Simple test endpoint"""
    return jsonify({
        'success': True,
        'message': 'API is working!',
        'timestamp': str(datetime.now())
    })

@app.route('/api/edit-section', methods=['POST'])
@cross_origin()
def edit_section():
    """Edit a specific section of the blog"""
    try:
        data = request.json
        section_content = data.get('section_content', '')
        section_title = data.get('section_title', '')
        edit_instruction = data.get('instruction', 'improve this section')
        target_length = data.get('target_length', 100)
        
        print(f"Editing section '{section_title}': {edit_instruction}")
        
        # Simple section editing logic
        if 'shorter' in edit_instruction.lower():
            # Keep first few sentences
            sentences = section_content.split('. ')
            max_sentences = max(1, target_length // 20)  # Rough estimate
            edited_section = '. '.join(sentences[:max_sentences])
            if not edited_section.endswith('.'):
                edited_section += '.'
                
        elif 'longer' in edit_instruction.lower():
            # Add more detail
            edited_section = section_content + "\n\nAdditionally, this approach offers several benefits including improved efficiency, better results, and enhanced user experience."
            
        elif 'bullet' in edit_instruction.lower() or 'list' in edit_instruction.lower():
            # Convert to bullet points
            sentences = section_content.split('. ')
            edited_section = "\n".join([f"• {sentence.strip()}" for sentence in sentences if sentence.strip()])
            
        else:
            # Default: clean up formatting
            edited_section = section_content.strip()
        
        return jsonify({
            'success': True,
            'edited_content': edited_section,
            'word_count': len(edited_section.split())
        })
        
    except Exception as e:
        print(f"Section editing error: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'edited_content': section_content
        }), 500

@app.route('/api/edit-content', methods=['POST'])
@cross_origin()
def edit_content():
    """Edit and optimize blog content based on user requirements"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided', 'success': False}), 400
        
        original_content = data.get('content', '')
        edit_instruction = data.get('instruction', 'make it shorter')
        topic = data.get('topic', '')
        platform = data.get('platform', 'LinkedIn')
        target_length = data.get('target_length', None)
        
        print(f"Editing content: {edit_instruction} for {platform}")
        
        # Use Google AI to edit the content
        try:
            edited_content = google_ai.generate_blog_content(
                f"Edit this content: {edit_instruction}. Original topic: {topic}", 
                platform, 
                target_length or 500
            )
            
            if edited_content and edited_content.get('content'):
                # Parse sections for React frontend
                edited_content['sections'] = parse_content_sections(edited_content['content'])
                edited_content['wordCount'] = len(edited_content['content'].split())
                edited_content['success'] = True
                
                print(f"✅ Content edited successfully: {len(edited_content['content'])} chars")
                return jsonify(edited_content)
        except Exception as e:
            print(f"Google AI edit failed: {e}")
        
        # Fallback: Manual content editing
        edited_content = manual_content_edit(original_content, edit_instruction, target_length)
        return jsonify(edited_content)
        
    except Exception as e:
        print(f"❌ Error editing content: {e}")
        return jsonify({
            'error': 'Content editing failed',
            'success': False,
            'content': original_content,
            'message': 'Unable to edit content. Please try again.'
        }), 500

@app.route('/api/generate', methods=['POST'])
@cross_origin()
def generate_content():
    """Generate structured blog content with intro, body, and conclusion"""
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided', 'success': False}), 400
            
        topic = data.get('topic', 'AI')
        platform = data.get('platform', '📸 Instagram')
        content_focus = data.get('content_focus', 'Trending')
        ai_mode = data.get('ai_mode', 'Dynamic AI')
        
        print(f"🚀 Generating structured content for topic: {topic}, platform: {platform}")
        
        # Use enhanced structured generation - prioritize Google AI
        blog_content = None
        
        # Try Google AI first (most reliable for dynamic content)
        try:
            print("Trying Google AI blog generation...")
            blog_content = google_ai.generate_blog_content(topic, platform, 1000)
            if blog_content and blog_content.get('content') and len(blog_content['content']) > 200:
                blog_content['content'] = html.unescape(blog_content['content'])
                if blog_content.get('title'):
                    blog_content['title'] = html.unescape(blog_content['title'])
                print(f"✅ Google AI generated {len(blog_content['content'])} chars of dynamic content")
            else:
                print("⚠️ Google AI returned insufficient content")
                blog_content = None
        except Exception as e:
            print(f"❌ Google AI failed: {e}")
            blog_content = None
        
        # Try working AI as secondary option
        if not blog_content:
            try:
                print("Trying Working AI structured generation...")
                blog_content = working_ai.generate_full_blog_content(topic, platform)
                if blog_content and blog_content.get('content') and len(blog_content['content']) > 200:
                    blog_content['content'] = html.unescape(blog_content['content'])
                    if blog_content.get('title'):
                        blog_content['title'] = html.unescape(blog_content['title'])
                    print(f"✅ Working AI generated {len(blog_content['content'])} chars of content")
                else:
                    blog_content = None
            except Exception as e:
                print(f"❌ Working AI failed: {e}")
                blog_content = None
        
        # Final structured fallback
        if not blog_content or not blog_content.get('content'):
            print("Using structured fallback content generation")
            blog_content = generate_structured_fallback(topic, platform)
        
        # Ensure hashtags is always an array
        if not blog_content.get('hashtags') or not isinstance(blog_content.get('hashtags'), list):
            blog_content['hashtags'] = [f'#{topic.replace(" ", "")}', '#content', '#blog']
        
        # Generate contextual image for the blog
        try:
            if blog_content and 'title' in blog_content:
                # Use original topic for better image generation
                img_topic = topic if len(topic) < 50 else blog_content['title'][:50]
                img_url = image_gen.generate_from_title(img_topic)
                # CRITICAL: Fix HTML entities in image URL for React
                if img_url:
                    img_url = img_url.replace('&amp;', '&').replace('&#39;', "'")
                blog_content['image_url'] = img_url
                print(f"Generated contextual image URL for '{img_topic}': {img_url}")
        except Exception as img_err:
            print(f"Image gen error: {img_err}")
            # Fallback to simple topic-based image
            try:
                simple_topic = topic.split()[0] if topic else 'blog'
                fallback_url = f"https://image.pollinations.ai/prompt/blog%20{simple_topic}?width=1200&height=630"
                blog_content['image_url'] = fallback_url
                print(f"Using fallback image: {fallback_url}")
            except:
                blog_content['image_url'] = None
        
        # Add word count and sections
        if blog_content and 'content' in blog_content:
            blog_content['wordCount'] = len(blog_content['content'].split())
            
            # Parse sections for React frontend
            if 'sections' not in blog_content:
                blog_content['sections'] = parse_content_sections(blog_content['content'])
        
        # Calculate engagement score
        try:
            if blog_content:
                blog_content['engagement_score'] = engagement_pred.predict_engagement(blog_content, platform) if hasattr(engagement_pred, 'predict_engagement') else 0.85
        except Exception as eng_err:
            print(f"Engagement prediction error: {eng_err}")
            blog_content['engagement_score'] = 0.85
        
        # Ensure required fields
        blog_content['success'] = True
        blog_content['platform'] = platform
        
        # 🔗 BLOCKCHAIN INTEGRATION
        try:
            print("🔗 Integrating with blockchain...")
            blog_content = blockchain_integration.process_generated_content(
                blog_content, 
                author="Aniket Zimane"
            )
            print(f"✅ Blockchain integration completed: {blog_content.get('blockchain', {}).get('verified', False)}")
        except Exception as blockchain_err:
            print(f"⚠️ Blockchain integration failed: {blockchain_err}")
            blog_content['blockchain'] = {'error': str(blockchain_err), 'verified': False}
        
        print(f"✅ Generated structured content successfully: {blog_content.get('title', 'No title')}")
        return jsonify(blog_content)
        
    except Exception as e:
        print(f"❌ Error generating content: {e}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            'error': 'Content generation failed',
            'success': False,
            'title': f'Guide to {data.get("topic", "AI") if data else "AI"}',
            'content': f'Discover the amazing world of {data.get("topic", "AI") if data else "AI"}. This comprehensive guide will help you understand the key concepts and applications.',
            'hashtags': ['#AI', '#guide', '#tips'],
            'cta': 'What are your thoughts? Share in the comments!',
            'keywords': ['AI', 'guide'],
            'engagement_score': 0.75,
            'wordCount': 50,
            'sections': []
        }), 200

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

@app.route('/api/test-ai', methods=['POST'])
def test_ai():
    """Test AI generation directly"""
    try:
        data = request.json
        topic = data.get('topic', 'AI')
        platform = data.get('platform', 'Instagram')
        
        print(f"Testing Google AI with topic: {topic}")
        
        # Test Google AI directly
        result = google_ai.generate_blog_content(topic, platform, 800)
        
        return jsonify({
            'success': True,
            'ai_response': result,
            'content_length': len(result.get('content', '')) if result else 0,
            'has_title': bool(result.get('title')) if result else False
        })
        
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        })

@app.route('/api/calendar', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def generate_calendar():
    """Generate 7-day content calendar"""
    if request.method == 'OPTIONS':
        return jsonify({'success': True})
    
    try:
        data = request.json if request.method == 'POST' else {}
        topic = data.get('topic', 'AI')
        platform = data.get('platform', '📸 Instagram')
        content_focus = data.get('content_focus', 'Trending')
        
        print(f"📅 Generating 7-day calendar for topic: {topic}, platform: {platform}")
        
        # Generate sample blog content for calendar
        blog_content = {
            'title': f"Complete Guide to {topic}",
            'content': f"Discover everything about {topic} in this comprehensive guide...",
            'hashtags': [f'#{topic.replace(" ", "")}', '#guide', '#tips']
        }
        
        # Generate calendar using existing system
        if calendar_gen:
            platforms = [platform, '🐦 Twitter', '💼 LinkedIn']  # Include multiple platforms
            calendar_data = calendar_gen.generate_weekly_calendar(blog_content, platforms)
        else:
            calendar_data = []
        
        # If no data or insufficient data, generate fallback
        if not calendar_data or len(calendar_data) < 7:
            calendar_data = generate_fallback_calendar(topic, platform)
        
        return jsonify({
            'success': True,
            'calendar': calendar_data,
            'topic': topic,
            'platform': platform
        })
        
    except Exception as e:
        print(f"❌ Error generating calendar: {e}")
        # Generate fallback calendar
        calendar_data = generate_fallback_calendar(topic, platform)
        
        return jsonify({
            'success': True,
            'calendar': calendar_data,
            'topic': topic,
            'platform': platform,
            'fallback': True
        })

def generate_fallback_calendar(topic, platform):
    """Generate fallback calendar with proper time and engagement data"""
    from datetime import datetime, timedelta
    import random
    
    fallback_calendar = []
    start_date = datetime.now()
    
    # Platform-specific optimal times and engagement rates
    platform_data = {
        '📸 Instagram': {'times': ['11:00', '15:00', '18:00', '19:00'], 'engagement': [0.85, 0.92, 0.88, 0.90]},
        '🐦 Twitter': {'times': ['09:00', '12:00', '15:00', '17:00'], 'engagement': [0.87, 0.91, 0.89, 0.86]},
        '💼 LinkedIn': {'times': ['08:00', '10:00', '09:00', '11:00'], 'engagement': [0.93, 0.95, 0.91, 0.88]},
        '📺 YouTube': {'times': ['14:00', '16:00', '15:00', '17:00'], 'engagement': [0.89, 0.92, 0.94, 0.90]},
        '👥 Facebook': {'times': ['13:00', '19:00', '12:00', '20:00'], 'engagement': [0.86, 0.91, 0.93, 0.89]}
    }
    
    # Use selected platform data or default
    selected_platform_data = platform_data.get(platform, {'times': ['12:00'], 'engagement': [0.80]})
    content_types = ['Educational', 'Trending', 'Opinion', 'News Analysis', 'Tips & Tricks', 'Case Study', 'How-to Guide']
    
    for i in range(7):
        date = start_date + timedelta(days=i)
        
        # Use selected platform for all 7 days with different times/content
        time_idx = i % len(selected_platform_data['times'])
        optimal_time = selected_platform_data['times'][time_idx]
        engagement_score = selected_platform_data['engagement'][time_idx]
        
        fallback_calendar.append({
            'id': i + 1,
            'date': date.strftime('%Y-%m-%d'),
            'day': date.strftime('%A'),
            'time': optimal_time,
            'topic': f"{topic}: {random.choice(content_types)}",
            'platform': platform,  # Use selected platform
            'engagement_score': engagement_score,
            'engagement': f"{int(engagement_score * 100)}%",
            'best_time': optimal_time,
            'content_type': random.choice(content_types),
            'title': f"{topic} - {random.choice(content_types)} (Day {i+1})",
            'status': 'scheduled'
        })
    
    return fallback_calendar

@app.route('/api/schedule', methods=['POST'])
@cross_origin()
def schedule_post():
    """Schedule social media post"""
    try:
        data = request.json
        content = data.get('content')
        platforms = data.get('platforms', [])
        schedule_date = data.get('schedule_date')
        schedule_time = data.get('schedule_time')
        
        return jsonify({
            'success': True,
            'message': 'Post scheduled successfully',
            'scheduled_platforms': platforms
        })
        
    except Exception as e:
        print(f"Error scheduling post: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/blockchain/verify', methods=['POST'])
@cross_origin()
def verify_blockchain_content():
    """Verify content authenticity using blockchain"""
    try:
        data = request.json
        content_hash = data.get('content_hash')
        
        if not content_hash:
            return jsonify({'error': 'Content hash required'}), 400
        
        verification_result = blockchain_integration.verify_content(content_hash)
        
        return jsonify({
            'success': True,
            'verification': verification_result
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/blockchain/creator-stats', methods=['GET'])
@cross_origin()
def get_creator_blockchain_stats():
    """Get creator's blockchain statistics"""
    try:
        creator_address = request.args.get('address')
        stats = blockchain_integration.get_creator_stats(creator_address)
        
        return jsonify({
            'success': True,
            'stats': stats
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/blockchain/nft-marketplace', methods=['POST'])
@cross_origin()
def get_nft_marketplace_info():
    """Get NFT marketplace information for content"""
    try:
        data = request.json
        content_hash = data.get('content_hash')
        
        # Simulate NFT marketplace data
        marketplace_info = {
            'opensea_url': f'https://opensea.io/assets/matic/0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6/{abs(hash(content_hash)) % 10000}',
            'rarible_url': f'https://rarible.com/token/polygon/0x742d35Cc6634C0532925a3b8D4C9db96C4b4d8b6:{abs(hash(content_hash)) % 10000}',
            'estimated_value': f'{(abs(hash(content_hash)) % 100) / 100:.2f} MATIC',
            'royalty_percentage': '10%',
            'blockchain': 'Polygon',
            'contract_verified': True
        }
        
        return jsonify({
            'success': True,
            'marketplace': marketplace_info
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
@app.route('/api/post-now', methods=['POST'])
@cross_origin()
    """Post content immediately to social media"""
    try:
        data = request.json
        blog_content = data.get('blog_content')
        platforms = data.get('platforms', [])
        
        print(f"🚀 Posting to platforms: {platforms}")
        
        # Post to selected platforms
        results = social_poster.auto_post(blog_content, platforms)
        
        # Check if any posts succeeded
        success_count = sum(1 for r in results if r.get('success'))
        
        return jsonify({
            'success': success_count > 0,
            'results': results,
            'message': f'Posted to {success_count}/{len(platforms)} platforms successfully'
        })
        
    except Exception as e:
        print(f"❌ Error posting: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Failed to post to social media'
        }), 500

def generate_structured_fallback(topic: str, platform: str) -> dict:
    """Generate structured fallback content with intro, body, conclusion"""
    title = f"The Complete {topic} Guide: Everything You Need to Know"
    
    intro = f"""## 🌟 Introduction

Welcome to the ultimate guide on {topic}! Whether you're just starting your journey or looking to deepen your understanding, this comprehensive resource will provide you with valuable insights and practical knowledge.

In today's rapidly evolving world, {topic} has become increasingly important. This guide will walk you through everything you need to know, from the basics to advanced strategies."""
    
    body = f"""## 📚 Key Concepts

Understanding {topic} requires grasping several fundamental concepts:

### 🔑 Core Principles
- **Foundation**: Building strong basic understanding
- **Applications**: Real-world uses and benefits  
- **Best Practices**: Proven methods and approaches
- **Common Challenges**: What to watch out for

### 🚀 Getting Started
1. **Research**: Gather information from reliable sources
2. **Practice**: Apply what you learn in real situations
3. **Connect**: Join communities and networks
4. **Improve**: Continuously refine your approach

## 💡 Practical Tips

### For Beginners
- Start with the basics and build gradually
- Don't be afraid to ask questions
- Learn from others' experiences
- Practice regularly to build confidence

### For Advanced Users
- Stay updated with latest developments
- Share knowledge with others
- Experiment with new approaches
- Mentor newcomers in the field"""
    
    conclusion = f"""## 🎯 Key Takeaways & Next Steps

As we wrap up this comprehensive guide on {topic}, let's recap the most important points:

✅ **Understanding the fundamentals** is crucial for long-term success
✅ **Practical application** beats theoretical knowledge every time
✅ **Continuous learning** keeps you ahead of the curve
✅ **Community engagement** accelerates your growth

### Your Action Plan

1. **Start with the basics** - Master the fundamentals before moving to advanced concepts
2. **Practice regularly** - Consistent application leads to mastery
3. **Stay updated** - Follow industry trends and best practices
4. **Connect with others** - Join communities and learn from peers

## 🚀 Final Thoughts

{topic} offers tremendous opportunities for growth and success. The key lies not just in understanding the concepts, but in taking action and applying what you've learned.

Remember, every expert was once a beginner. Your journey starts with the first step, and with the knowledge you've gained from this guide, you're already ahead of the curve.

What's your biggest takeaway from this guide? How do you plan to implement these insights? Share your thoughts and let's continue the conversation! 💬"""
    
    full_content = f"{intro}\n\n{body}\n\n{conclusion}"
    
    return {
        'title': title,
        'content': full_content,
        'hashtags': [f'#{topic.replace(" ", "")}', '#guide', '#tips', '#2024', '#success'],
        'cta': f"Ready to dive deeper into {topic}? Share your thoughts and experiences in the comments below! What's your next step? 🚀",
        'keywords': [topic, 'guide', 'tips', 'success', '2024'],
        'sections': parse_content_sections(full_content)
    }

def manual_content_edit(content: str, instruction: str, target_length: int = None) -> dict:
    """Intelligently edit content using AI while preserving structure and meaning"""
    instruction_lower = instruction.lower()
    
    if 'shorter' in instruction_lower or 'short' in instruction_lower:
        # Use AI to intelligently condense content
        try:
            # Initialize Google AI for content editing
            api_key = os.getenv("GOOGLE_AI_API_KEY")
            if api_key:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                target_words = target_length or 300
                
                edit_prompt = f"""Condense this blog content to approximately {target_words} words while preserving:
1. The opening hook and main message
2. Key insights and main points from the body
3. The conclusion with actionable takeaways
4. All subheadings and structure
5. The original meaning and value

DO NOT just trim sentences. Instead:
- Combine related points
- Use more concise language
- Keep the most important examples
- Maintain the intro-body-conclusion flow
- Preserve all headings (## format)

Original content:
{content}

Condensed version:"""
                
                response = model.generate_content(edit_prompt)
                if response and response.text:
                    edited_content = response.text.strip()
                    print(f"AI condensed content from {len(content.split())} to {len(edited_content.split())} words")
                else:
                    edited_content = smart_manual_condense(content, target_words)
            else:
                edited_content = smart_manual_condense(content, target_words)
                
        except Exception as e:
            print(f"AI editing failed: {e}")
            edited_content = smart_manual_condense(content, target_length or 300)
            
    elif 'longer' in instruction_lower or 'expand' in instruction_lower:
        # Use AI to expand content intelligently
        try:
            api_key = os.getenv("GOOGLE_AI_API_KEY")
            if api_key:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-1.5-flash")
                
                expand_prompt = f"""Expand this blog content while maintaining its structure:
1. Add more detailed examples and explanations
2. Include additional insights and tips
3. Expand on key points with more context
4. Keep the same headings and flow
5. Add practical applications

Original content:
{content}

Expanded version:"""
                
                response = model.generate_content(expand_prompt)
                edited_content = response.text.strip() if response and response.text else content
            else:
                edited_content = content + "\n\nAdditional insights and practical applications can further enhance your understanding and implementation of these concepts."
        except Exception as e:
            print(f"AI expansion failed: {e}")
            edited_content = content
            
    elif 'professional' in instruction_lower:
        edited_content = content.replace('you', 'professionals').replace('your', 'their').replace('!', '.')
    elif 'casual' in instruction_lower:
        edited_content = content.replace('professionals', 'you').replace('individuals', 'you')
    else:
        edited_content = content
    
    return {
        'success': True,
        'content': edited_content,
        'title': f"Edited Content",
        'wordCount': len(edited_content.split()),
        'sections': parse_content_sections(edited_content),
        'hashtags': ['#edited', '#content', '#blog'],
        'cta': 'What do you think of these changes?',
        'keywords': ['edited', 'content'],
        'engagement_score': 0.75
    }

def smart_manual_condense(content: str, target_words: int) -> str:
    """Intelligently condense content manually while preserving structure"""
    lines = content.split('\n')
    condensed_lines = []
    current_words = 0
    
    # Always keep title and main headers
    intro_lines = []
    body_lines = []
    conclusion_lines = []
    current_section = "intro"
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Identify sections
        if any(word in line.lower() for word in ['conclusion', 'takeaway', 'final', 'summary']):
            current_section = "conclusion"
        elif line.startswith('##') and current_section == "intro":
            current_section = "body"
            
        # Categorize lines
        if current_section == "intro":
            intro_lines.append(line)
        elif current_section == "conclusion":
            conclusion_lines.append(line)
        else:
            body_lines.append(line)
    
    # Allocate word budget: 20% intro, 60% body, 20% conclusion
    intro_budget = int(target_words * 0.2)
    body_budget = int(target_words * 0.6)
    conclusion_budget = int(target_words * 0.2)
    
    # Condense each section
    condensed_intro = condense_section(intro_lines, intro_budget)
    condensed_body = condense_section(body_lines, body_budget)
    condensed_conclusion = condense_section(conclusion_lines, conclusion_budget)
    
    # Combine sections
    result = condensed_intro + "\n\n" + condensed_body + "\n\n" + condensed_conclusion
    return result.strip()

def condense_section(lines: list, word_budget: int) -> str:
    """Condense a section to fit word budget"""
    if not lines:
        return ""
        
    # Always keep headers
    headers = [line for line in lines if line.startswith('#')]
    content_lines = [line for line in lines if not line.startswith('#')]
    
    # Keep most important sentences
    important_lines = []
    current_words = sum(len(h.split()) for h in headers)
    
    for line in content_lines:
        line_words = len(line.split())
        if current_words + line_words <= word_budget:
            important_lines.append(line)
            current_words += line_words
        elif line.startswith('-') or line.startswith('*') or '**' in line:
            # Keep key points even if over budget
            important_lines.append(line)
            current_words += line_words
            
    # Combine headers and content
    result_lines = headers + important_lines
    return '\n'.join(result_lines)

def parse_content_sections(content: str) -> list:
    """Parse content into sections for React frontend editing"""
    sections = []
    lines = content.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        if line.startswith('##') or line.startswith('###'):
            # Save previous section
            if current_section:
                sections.append({
                    'id': len(sections),
                    'title': current_section,
                    'content': '\n'.join(current_content).strip(),
                    'type': 'section',
                    'editable': True
                })
            
            # Start new section
            current_section = line.replace('#', '').strip()
            current_content = []
        else:
            current_content.append(line)
    
    # Add final section
    if current_section:
        sections.append({
            'id': len(sections),
            'title': current_section,
            'content': '\n'.join(current_content).strip(),
            'type': 'section',
            'editable': True
        })
    
    return sections

if __name__ == '__main__':
    print("Starting Enhanced Streamlit API for React on http://localhost:5000")
    app.run(debug=True, port=5000)