import requests
import json
import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class WorkingAIIntegration:
    def __init__(self):
        self.google_api_key = os.getenv("GOOGLE_AI_API_KEY")
        self.replicate_token = os.getenv("REPLICATE_API_TOKEN")
    
    def generate_full_blog_content(self, topic: str, platform: str) -> Dict:
        """Generate complete blog using Google AI"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.google_api_key}"
            
            prompt = f"""Write a detailed, engaging blog post about "{topic}" for {platform}.

IMPORTANT: Write ACTUAL CONTENT about the topic, not a guide about how to write about it.

For example, if topic is "best places to visit in pune":
- Write about ACTUAL places like Shaniwar Wada, Aga Khan Palace, Sinhagad Fort
- Include specific details, addresses, timings, entry fees
- Mention local food, culture, history
- Give practical travel tips

Requirements:
- 600-800 words of specific, factual content
- Use emojis and subheadings for visual appeal
- Include practical information (timings, costs, how to reach)
- Add personal recommendations and insider tips
- Make it engaging and informative
- End with compelling call-to-action

Write as an expert who has actually experienced/visited/used what you're writing about."""

            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                
                if content and len(content) > 100:
                    return self._parse_blog_content(content, topic, platform)
            
        except Exception as e:
            print(f"Google AI error: {e}")
        
        return self._generate_quality_fallback(topic, platform)
    
    def generate_blog_image_url(self, topic: str) -> str:
        """Generate image using free Unsplash API"""
        try:
            # Use Unsplash for free high-quality images
            query = topic.replace(" ", "+")
            url = f"https://source.unsplash.com/1200x630/?{query},blog,professional"
            return url
        except:
            return f"https://source.unsplash.com/1200x630/?technology,blog"
    
    def generate_hashtags(self, topic: str, platform: str) -> List[str]:
        """Generate hashtags using Google AI"""
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.google_api_key}"
            
            prompt = f"Generate 15 trending hashtags for '{topic}' on {platform}. Return as comma-separated list without explanations."
            
            payload = {
                "contents": [{
                    "parts": [{"text": prompt}]
                }]
            }
            
            response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                content = result.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                
                # Extract hashtags
                hashtags = []
                for word in content.replace(",", " ").split():
                    clean_word = word.strip().replace("#", "")
                    if len(clean_word) > 2 and clean_word.isalnum():
                        hashtags.append(f"#{clean_word}")
                
                return hashtags[:15] if hashtags else self._fallback_hashtags(topic, platform)
                
        except Exception as e:
            print(f"Hashtag generation error: {e}")
        
        return self._fallback_hashtags(topic, platform)
    
    def _parse_blog_content(self, content: str, topic: str, platform: str) -> Dict:
        """Parse AI-generated content into structured format"""
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Extract title (first substantial line)
        title = lines[0] if lines else f"Complete Guide to {topic}"
        title = title.replace("**", "").replace("#", "").strip()
        
        # Extract main content (skip title, take substantial paragraphs)
        content_lines = []
        for line in lines[1:]:
            if len(line) > 50 and not line.startswith("#") and "hashtag" not in line.lower():
                content_lines.append(line)
        
        # Take more content for richer blogs
        blog_content = "\n\n".join(content_lines[:8]) if content_lines else self._generate_topic_specific_content(topic)
        
        # Extract hashtags from content
        hashtags = []
        for line in lines:
            if "#" in line:
                tags = [word for word in line.split() if word.startswith("#")]
                hashtags.extend(tags)
        
        if not hashtags:
            hashtags = self._fallback_hashtags(topic, platform)
        
        return {
            "title": title[:100],
            "content": blog_content,
            "hashtags": hashtags[:10],
            "cta": f"What are your thoughts on {topic}? Share your experience in the comments!",
            "keywords": [topic, platform.split()[-1], "guide", "2024", "trends"]
        }
    
    def _generate_quality_fallback(self, topic: str, platform: str) -> Dict:
        """High-quality fallback content"""
        title = f"The Ultimate {topic} Guide: Everything You Need to Know"
        
        content = self._generate_topic_specific_content(topic)

        return {
            "title": title,
            "content": content,
            "hashtags": self._fallback_hashtags(topic, platform),
            "cta": f"Ready to dive deeper into {topic}? Follow for more expert insights and practical tips!",
            "keywords": self._generate_topic_keywords(topic)
        }
    
    def _fallback_hashtags(self, topic: str, platform: str) -> List[str]:
        """Generate smart fallback hashtags"""
        topic_clean = topic.replace(" ", "").replace("-", "")
        
        base_tags = [f"#{topic_clean}", "#2024", "#trending"]
        
        platform_tags = {
            "instagram": ["#instagood", "#viral", "#explore", "#reels"],
            "twitter": ["#thread", "#breaking", "#news", "#viral"],
            "linkedin": ["#professional", "#business", "#career", "#leadership"],
            "youtube": ["#tutorial", "#howto", "#subscribe", "#educational"],
            "facebook": ["#community", "#share", "#discussion", "#insights"]
        }
        
        platform_key = platform.lower().split()[-1] if " " in platform else platform.lower()
        specific_tags = platform_tags.get(platform_key, ["#content", "#digital", "#innovation"])
        
        general_tags = ["#AI", "#technology", "#future", "#innovation", "#success"]
        
        all_tags = base_tags + specific_tags + general_tags
        return all_tags[:12]
    
    def _generate_topic_keywords(self, topic: str) -> List[str]:
        """Generate topic-specific SEO keywords"""
        topic_lower = topic.lower()
        base_keywords = [topic, "2024", "guide"]
        
        if any(word in topic_lower for word in ['places', 'visit', 'travel', 'pune']):
            return base_keywords + ["travel", "tourism", "attractions", "sightseeing", "vacation", "destinations"]
        elif any(word in topic_lower for word in ['ai', 'artificial intelligence', 'technology']):
            return base_keywords + ["technology", "innovation", "machine learning", "future", "automation"]
        elif any(word in topic_lower for word in ['business', 'marketing', 'startup']):
            return base_keywords + ["business", "strategy", "growth", "success", "entrepreneurship"]
        else:
            return base_keywords + ["tips", "advice", "information", "knowledge", "expertise"]
    
    def _generate_topic_specific_content(self, topic: str) -> str:
        """Generate specific content based on the topic"""
        topic_lower = topic.lower()
        
        # Travel/Places content
        if any(word in topic_lower for word in ['places', 'visit', 'travel', 'pune', 'mumbai', 'delhi', 'bangalore']):
            city = 'Pune' if 'pune' in topic_lower else 'the destination'
            return f"""# 🏙️ Discover Amazing Places in {city}

## 🏠 Top Attractions

### Historical Sites
- **Shaniwar Wada**: The iconic 18th-century fortification and palace
- **Aga Khan Palace**: Beautiful Indo-Saracenic architecture and Gandhi memorial
- **Sinhagad Fort**: Ancient hill fortress perfect for trekking

### Cultural Experiences
- **Dagdusheth Halwai Ganpati Temple**: Famous Ganesh temple
- **Pataleshwar Cave Temple**: 8th-century rock-cut temple
- **Raja Dinkar Kelkar Museum**: Fascinating collection of artifacts

## 🍽️ Local Food & Culture

### Must-Try Dishes
- **Misal Pav**: Spicy curry with bread rolls
- **Vada Pav**: Mumbai's favorite street food
- **Puran Poli**: Sweet flatbread delicacy

### Best Areas to Explore
- **FC Road**: Shopping and food paradise
- **Koregaon Park**: Upscale dining and cafes
- **Camp Area**: Traditional markets and eateries

## 🚗 Practical Information

### Getting Around
- **Auto-rickshaws**: Most convenient for short distances
- **Uber/Ola**: Reliable app-based transportation
- **PMPML Buses**: Budget-friendly public transport

### Best Time to Visit
- **October to March**: Pleasant weather for sightseeing
- **Monsoon (June-September)**: Beautiful but can be challenging for outdoor activities

### Budget Tips
- Street food costs ₹20-50 per item
- Auto-rickshaw rides: ₹10-15 per km
- Entry fees for most attractions: ₹5-25

## 📸 Instagram-Worthy Spots

1. **Parvati Hill**: Panoramic city views
2. **Osho Garden**: Peaceful Japanese-style garden
3. **Shaniwar Wada**: Majestic architecture
4. **Sinhagad Fort**: Sunset views

Whether you're a history buff, foodie, or adventure seeker, this city offers something special for everyone!"""
        
        # Technology content
        elif any(word in topic_lower for word in ['ai', 'artificial intelligence', 'machine learning', 'technology']):
            return f"""# 🤖 Understanding {topic}: A Complete Overview

## 🚀 What is {topic}?

{topic} represents one of the most significant technological advances of our time. It's transforming industries, changing how we work, and opening up new possibilities we never imagined.

## 📊 Key Applications

### Current Uses
- **Healthcare**: Diagnostic assistance and drug discovery
- **Finance**: Fraud detection and algorithmic trading
- **Transportation**: Autonomous vehicles and route optimization
- **Entertainment**: Personalized recommendations and content creation

### Emerging Applications
- **Education**: Personalized learning experiences
- **Agriculture**: Crop monitoring and yield optimization
- **Climate**: Weather prediction and environmental monitoring

## 🛠️ Tools and Platforms

### Popular Frameworks
- **TensorFlow**: Google's open-source platform
- **PyTorch**: Facebook's research-focused framework
- **Scikit-learn**: User-friendly machine learning library

### Cloud Services
- **AWS AI Services**: Comprehensive AI toolkit
- **Google Cloud AI**: Advanced machine learning capabilities
- **Microsoft Azure AI**: Enterprise-focused solutions

## 📚 Learning Resources

### Online Courses
- **Coursera**: Andrew Ng's Machine Learning Course
- **edX**: MIT's Introduction to AI
- **Udacity**: AI Programming Nanodegree

### Books
- "Hands-On Machine Learning" by Aurélien Géron
- "Pattern Recognition and Machine Learning" by Christopher Bishop
- "The Hundred-Page Machine Learning Book" by Andriy Burkov

## 🔮 Future Trends

- **Explainable AI**: Making AI decisions more transparent
- **Edge Computing**: Bringing AI to mobile devices
- **Quantum Machine Learning**: Next-generation computing power

The field is evolving rapidly, offering exciting opportunities for innovation and career growth!"""
        
        # Business/Marketing content
        elif any(word in topic_lower for word in ['business', 'marketing', 'startup', 'entrepreneur']):
            return f"""# 💼 Mastering {topic}: Strategies for Success

## 🎯 Understanding the Landscape

{topic} in today's digital age requires a blend of traditional wisdom and modern innovation. Success comes from understanding your market, knowing your customers, and delivering exceptional value.

## 📈 Key Strategies

### Market Research
- **Customer Surveys**: Direct feedback from your target audience
- **Competitor Analysis**: Understanding market positioning
- **Trend Analysis**: Staying ahead of industry changes

### Digital Presence
- **Social Media Marketing**: Building brand awareness
- **Content Marketing**: Providing value to attract customers
- **SEO Optimization**: Improving online visibility

## 🛠️ Essential Tools

### Analytics
- **Google Analytics**: Website performance tracking
- **Facebook Insights**: Social media analytics
- **HubSpot**: Comprehensive marketing platform

### Productivity
- **Slack**: Team communication
- **Trello**: Project management
- **Zoom**: Video conferencing

## 💡 Expert Tips

### Building Relationships
- Focus on long-term customer value
- Provide exceptional customer service
- Build a strong network of industry contacts

### Financial Management
- Track key performance indicators (KPIs)
- Maintain healthy cash flow
- Invest in growth opportunities wisely

## 🚀 Growth Strategies

- **Content Creation**: Share valuable insights regularly
- **Partnerships**: Collaborate with complementary businesses
- **Innovation**: Stay ahead with new products/services
- **Customer Feedback**: Continuously improve based on input

Success in {topic} requires persistence, adaptability, and a customer-first mindset!"""
        
        # Generic fallback for other topics
        else:
            return f"""# 🌟 Exploring {topic}: A Comprehensive Look

## 🔍 What You Need to Know

{topic} is an fascinating subject that deserves deeper exploration. Whether you're just getting started or looking to expand your knowledge, understanding the fundamentals is crucial.

## 📚 Key Aspects

### Important Elements
- **Foundation**: Building strong basic understanding
- **Applications**: Real-world uses and benefits
- **Best Practices**: Proven methods and approaches
- **Common Challenges**: What to watch out for

### Getting Started
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
- Mentor newcomers in the field

## 🚀 Moving Forward

{topic} offers many opportunities for growth and development. The key is to stay curious, keep learning, and apply what you discover in meaningful ways.

Remember: every expert was once a beginner. With dedication and the right approach, you can master any subject!"""