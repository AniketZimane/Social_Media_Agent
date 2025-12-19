import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class FileContentGenerator:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        else:
            self.model = None
    
    def generate_content_from_text(self, extracted_text, platform, content_focus, max_words):
        """Generate detailed blog content from extracted file text like Pune example"""
        if not self.model:
            return self._create_detailed_content(extracted_text, platform, max_words)
        
        try:
            # Create a detailed prompt for engaging content
            prompt = f"""
            You are a professional content writer. Create an engaging blog post for {platform} based on this document content:
            
            Document Content:
            "{extracted_text[:1500]}"
            
            Instructions:
            1. Analyze the document and identify the main topic
            2. Create a comprehensive blog post ({max_words} words) that:
               - Uses the actual information from the document
               - Includes emojis for visual appeal
               - Has clear sections with ## and ### headings
               - Contains bullet points and lists
               - Provides practical insights from the document
               - Maintains an engaging, enthusiastic tone
            
            Structure:
            ## [Main Topic from Document]: Complete Guide 🎆
            
            ### ✨ What Makes This Special?
            [Extract key points from document]
            
            ### 📝 Key Highlights & Must-Know Facts
            **Essential Elements:**
            * [Point from document]
            * [Point from document]
            * [Point from document]
            
            ### 🚀 Getting Started
            [Practical steps from document]
            
            ### 💡 Pro Tips
            [Insights from document]
            
            Write the complete blog now:
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                ai_content = response.text
                
                # Extract title from content
                lines = ai_content.split('\n')
                title = "Complete Guide: Key Insights"
                
                for line in lines[:5]:
                    if line.strip() and '##' in line:
                        title = line.replace('#', '').strip()
                        break
                    elif line.strip() and len(line.strip()) > 30 and ':' in line:
                        title = line.strip()
                        break
                
                # Ensure content has engaging format
                if not any(emoji in ai_content for emoji in ['🎯', '✨', '🚀', '💡']):
                    ai_content = self._enhance_with_emojis(ai_content)
                
                # Limit words
                words = ai_content.split()
                if len(words) > max_words:
                    ai_content = ' '.join(words[:max_words]) + '...'
                
                return {
                    "title": title,
                    "content": ai_content,
                    "hashtags": self._generate_hashtags(extracted_text, platform),
                    "cta": "What are your thoughts on these insights? Share your experiences in the comments!",
                    "keywords": self._extract_keywords(extracted_text),
                    "engagement_score": 0.89,
                    "platform": platform,
                    "wordCount": len(ai_content.split())
                }
            
        except Exception as e:
            print(f"Google AI error: {e}")
        print(f"Extracted text preview: {extracted_text[:200]}...")
        
        return self._create_detailed_content(extracted_text, platform, max_words)
    
    def _parse_ai_response(self, response_text, platform, max_words):
        """Parse AI response into structured blog content"""
        lines = response_text.split('\n')
        
        title = "Key Insights from Document"
        content = response_text
        
        # Try to extract title
        for line in lines:
            if any(word in line.lower() for word in ['title:', 'heading:', '##', '#']):
                title = line.replace('Title:', '').replace('##', '').replace('#', '').strip()
                break
        
        # Limit words
        words = content.split()
        if len(words) > max_words:
            content = ' '.join(words[:max_words]) + '...'
        
        # Generate hashtags based on platform
        hashtags = self._generate_hashtags(title + ' ' + content[:100], platform)
        
        return {
            "title": title,
            "content": content,
            "hashtags": hashtags,
            "cta": "What are your thoughts on these insights? Share your perspective!",
            "keywords": self._extract_keywords(title + ' ' + content),
            "engagement_score": 0.85,
            "platform": platform,
            "wordCount": len(content.split())
        }
    
    def _create_detailed_content(self, extracted_text, platform, max_words):
        """Create detailed, engaging content like Pune example from extracted text"""
        # Extract key information from document
        sentences = extracted_text.split('. ')
        key_sentences = [s.strip() for s in sentences if len(s.strip()) > 15]
        
        # Extract main topic from first sentences
        sentences = [s.strip() for s in extracted_text.split('.') if len(s.strip()) > 20]
        first_sentence = sentences[0] if sentences else extracted_text[:100]
        
        # Get key words for topic
        words = first_sentence.split()
        main_topic = ' '.join(words[:5]).title() if len(words) > 5 else first_sentence[:50]
        
        # Create engaging, detailed content
        content = f"""## Complete Guide to {main_topic}: Hidden Gems & Local Secrets 🌟

**Discover the incredible insights from this comprehensive analysis!** ✨ Whether you're exploring new concepts or deepening your understanding, this guide will take you on an amazing journey through the key findings and essential information.

### 🎯 What Makes This Special?

{main_topic} stands out for its unique approach and valuable insights. Based on our detailed analysis, here are the most important discoveries:

### 📝 Key Highlights & Must-Know Facts

**Essential Insights:**
* **Core Findings**: {key_sentences[0] if key_sentences else 'Comprehensive analysis of the main concepts'}
* **Important Details**: {key_sentences[1] if len(key_sentences) > 1 else 'Detailed examination of key elements'}
* **Practical Applications**: Real-world implications and usage scenarios
* **Expert Analysis**: Professional insights and recommendations
* **Future Outlook**: What this means for upcoming developments

### 🚀 Deep Dive Analysis

**Key Discoveries:**

{key_sentences[2] if len(key_sentences) > 2 else 'Advanced analysis reveals important patterns and trends that provide valuable insights for understanding the subject matter.'}

{key_sentences[3] if len(key_sentences) > 3 else 'The research demonstrates significant findings that contribute to our overall understanding of the topic.'}

### 💡 Pro Tips & Insights

**What You Need to Know:**
- Focus on the fundamental principles outlined in the analysis
- Pay attention to the practical applications mentioned
- Consider the long-term implications of these findings
- Look for opportunities to apply these insights in real scenarios
- Stay updated with related developments in this field

### 🎪 Why This Matters in 2024

In today's rapidly evolving landscape, understanding {main_topic} has become more crucial than ever. The insights revealed in this analysis provide:

**The Impact:**
- Revolutionary perspectives on current challenges
- New opportunities for innovation and growth
- Enhanced understanding of complex concepts
- Better strategies for practical implementation

### 🔥 Ready to Explore More?

Whether you're a researcher, professional, or curious learner, these insights offer valuable knowledge that can enhance your understanding and open new possibilities.

**Remember:** Knowledge is power, and these findings represent a significant step forward in our understanding of {main_topic}.

🌟 **Join the discussion and share your thoughts on these fascinating discoveries!**"""
        
        # Limit words if necessary
        words = content.split()
        if len(words) > max_words:
            content = ' '.join(words[:max_words]) + '...'
        
        return {
            "title": f"Complete Guide to {main_topic}: Hidden Gems & Local Secrets",
            "content": content,
            "hashtags": self._generate_hashtags(extracted_text, platform),
            "cta": "What are your thoughts on these insights? Share your experiences in the comments!",
            "keywords": self._extract_keywords(extracted_text),
            "engagement_score": 0.87,
            "platform": platform,
            "wordCount": len(content.split())
        }
    
    def _enhance_with_emojis(self, content):
        """Add emojis to make content more engaging"""
        content = content.replace('##', '## ✨')
        content = content.replace('###', '### 🎯')
        content = content.replace('**Key', '**🔑 Key')
        content = content.replace('**Important', '**⭐ Important')
        content = content.replace('**Pro Tip', '**💡 Pro Tip')
        return content
    
    def _generate_hashtags(self, text, platform):
        """Generate platform-specific hashtags using AI and multiple sources"""
        try:
            # Try AI-powered hashtag generation first
            if self.model:
                ai_hashtags = self._ai_generate_hashtags(text, platform)
                if ai_hashtags:
                    return ai_hashtags
        except:
            pass
        
        # Fallback to smart hashtag generation
        return self._smart_hashtag_generation(text, platform)
    
    def _ai_generate_hashtags(self, text, platform):
        """AI-powered hashtag generation"""
        try:
            prompt = f"""
            Generate 12 trending hashtags for {platform} based on this content:
            "{text[:300]}..."
            
            Requirements:
            - Mix of popular and niche hashtags
            - Platform-optimized for {platform}
            - Include content-specific tags
            - Return as comma-separated list
            """
            
            response = self.model.generate_content(prompt)
            if response and response.text:
                hashtags = []
                for tag in response.text.split(','):
                    clean_tag = tag.strip().replace('#', '')
                    if clean_tag and len(clean_tag) > 2:
                        hashtags.append(f"#{clean_tag}")
                
                if len(hashtags) >= 5:
                    return hashtags[:12]
        except:
            pass
        return None
    
    def _smart_hashtag_generation(self, text, platform):
        """Smart hashtag generation with platform optimization"""
        # Extract keywords from content
        content_keywords = self._extract_content_hashtags(text)
        
        # Platform-specific hashtag strategies
        platform_strategies = {
            "📸 Instagram": {
                "popular": ["#instagood", "#photooftheday", "#viral", "#trending", "#explore"],
                "engagement": ["#like4like", "#follow4follow", "#instadaily", "#picoftheday"],
                "niche": ["#contentcreator", "#digitalmarketing", "#socialmedia"]
            },
            "🐦 Twitter": {
                "popular": ["#breaking", "#news", "#trending", "#viral", "#thread"],
                "engagement": ["#retweet", "#follow", "#twitterchat", "#discussion"],
                "niche": ["#tech", "#innovation", "#startup", "#business"]
            },
            "💼 LinkedIn": {
                "popular": ["#professional", "#business", "#career", "#leadership", "#networking"],
                "engagement": ["#thoughtleadership", "#industry", "#growth", "#success"],
                "niche": ["#corporatelife", "#workculture", "#productivity", "#skills"]
            },
            "📺 YouTube": {
                "popular": ["#youtube", "#subscribe", "#tutorial", "#howto", "#educational"],
                "engagement": ["#youtuber", "#content", "#video", "#learning"],
                "niche": ["#knowledge", "#tips", "#guide", "#expert"]
            },
            "👥 Facebook": {
                "popular": ["#facebook", "#community", "#share", "#like", "#follow"],
                "engagement": ["#discussion", "#social", "#connect", "#family"],
                "niche": ["#lifestyle", "#inspiration", "#motivation", "#stories"]
            }
        }
        
        strategy = platform_strategies.get(platform, {
            "popular": ["#content", "#social", "#digital"],
            "engagement": ["#share", "#follow", "#like"],
            "niche": ["#online", "#media", "#platform"]
        })
        
        # Combine different hashtag types
        hashtags = []
        hashtags.extend(content_keywords[:3])  # Content-specific
        hashtags.extend(strategy["popular"][:3])  # Popular platform tags
        hashtags.extend(strategy["engagement"][:2])  # Engagement tags
        hashtags.extend(strategy["niche"][:2])  # Niche tags
        hashtags.extend(["#AI", "#innovation", "#2024"])  # Trending general tags
        
        return list(dict.fromkeys(hashtags))[:12]  # Remove duplicates, limit to 12
    
    def _extract_content_hashtags(self, text):
        """Extract hashtags from content keywords"""
        # Simple keyword extraction and conversion to hashtags
        words = text.lower().split()
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were', 'this', 'that', 'these', 'those'}
        
        keywords = []
        for word in words:
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) > 3 and clean_word not in stop_words:
                keywords.append(f"#{clean_word}")
        
        # Return unique keywords, prioritize longer/more specific ones
        unique_keywords = list(dict.fromkeys(keywords))
        return sorted(unique_keywords, key=len, reverse=True)[:5]
    
    def _extract_keywords(self, text):
        """Extract keywords from text"""
        # Simple keyword extraction
        words = text.lower().split()
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an', 'is', 'are', 'was', 'were'}
        keywords = [word for word in words if len(word) > 3 and word not in common_words]
        return list(set(keywords))[:5]  # Return top 5 unique keywords