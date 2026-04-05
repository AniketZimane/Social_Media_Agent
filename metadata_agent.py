import os
import re
from typing import Dict, List
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class MetadataAgent:
    """
    Specialized AI agent for generating blog metadata:
    - Dynamic hashtags extraction and generation
    - Compelling CTAs based on content
    - SEO keywords optimization
    """

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_AI_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_AI_API_KEY not set in environment")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate_metadata(self, topic: str, content: str, platform: str) -> Dict:
        """Generate all metadata for blog content"""
        
        print(f"Generating metadata for {platform} content...")
        
        try:
            # Generate hashtags
            hashtags = self._generate_hashtags(topic, content, platform)
            
            # Generate CTA
            cta = self._generate_cta(topic, content, platform)
            
            # Generate SEO keywords
            keywords = self._generate_keywords(topic, content)
            
            return {
                "hashtags": hashtags,
                "cta": cta,
                "keywords": keywords,
                "success": True
            }
            
        except Exception as e:
            print(f"Metadata generation failed: {e}")
            return {
                "hashtags": [f"#{topic.replace(' ', '')}"],
                "cta": f"What are your thoughts on {topic}? Share below! 💭",
                "keywords": topic.split(),
                "success": False,
                "error": str(e)
            }

    def _generate_hashtags(self, topic: str, content: str, platform: str) -> List[str]:
        """Generate platform-specific hashtags"""
        
        # Platform hashtag limits
        limits = {
            "instagram": 20,
            "linkedin": 5, 
            "twitter": 3,
            "youtube": 10,
            "facebook": 8,
            "tiktok": 15
        }
        
        max_tags = limits.get(platform.lower(), 10)
        
        prompt = f"""Analyze this blog content and generate {max_tags} highly relevant hashtags for {platform}:

TOPIC: {topic}
CONTENT: {content[:800]}...

Generate hashtags that are:
1. Directly related to the content themes
2. Mix of popular and niche tags
3. Platform-appropriate for {platform}
4. Trending and discoverable
5. Properly formatted with # symbol

PLATFORM GUIDELINES:
- Instagram: Mix trending + niche, lifestyle focused
- LinkedIn: Professional, industry-specific
- Twitter: Concise, trending topics
- YouTube: Searchable, category-based
- Facebook: Community-focused
- TikTok: Trendy, viral potential

Return ONLY hashtags separated by commas, no explanations.
Example: #AI, #Technology, #Innovation, #StartupLife"""

        try:
            response = self.model.generate_content(prompt)
            hashtags_text = response.text.strip()
            
            # Parse hashtags
            hashtags = [tag.strip() for tag in hashtags_text.split(',')]
            hashtags = [self._clean_hashtag(tag) for tag in hashtags]
            hashtags = [tag for tag in hashtags if tag and len(tag) > 2]
            
            return hashtags[:max_tags]
            
        except Exception as e:
            print(f"Hashtag generation failed: {e}")
            # Fallback to topic-based hashtags
            return self._generate_fallback_hashtags(topic, max_tags)

    def _generate_cta(self, topic: str, content: str, platform: str) -> str:
        """Generate compelling call-to-action"""
        
        prompt = f"""Create a compelling call-to-action for this {platform} post:

TOPIC: {topic}
CONTENT PREVIEW: {content[:500]}...

Generate a CTA that:
1. Encourages engagement (comments, shares, saves)
2. Is platform-appropriate for {platform}
3. Relates directly to the content
4. Uses engaging language with emojis
5. Asks a specific question or prompts action

PLATFORM STYLE:
- Instagram: Visual, emoji-rich, story-driven
- LinkedIn: Professional discussion, insights sharing
- Twitter: Quick engagement, retweets, replies
- YouTube: Subscribe, comment, watch more
- Facebook: Community discussion, sharing
- TikTok: Duets, comments, follows

Return ONLY the CTA text, no explanations.
Example: "What's your biggest challenge with AI implementation? Drop your thoughts below! 👇✨"
"""

        try:
            response = self.model.generate_content(prompt)
            cta = response.text.strip()
            
            # Clean up any quotes or extra formatting
            cta = cta.strip('"\'')
            
            return cta
            
        except Exception as e:
            print(f"CTA generation failed: {e}")
            return f"What are your thoughts on {topic}? Share your experience below! 💭✨"

    def _generate_keywords(self, topic: str, content: str) -> List[str]:
        """Generate SEO keywords from content"""
        
        prompt = f"""Extract 8-12 SEO keywords from this content:

TOPIC: {topic}
CONTENT: {content[:1000]}...

Extract keywords that are:
1. Highly relevant to the content
2. Good for SEO and discoverability
3. Mix of primary and long-tail keywords
4. Industry-specific terms
5. Trending search terms

Return ONLY keywords separated by commas, no explanations.
Example: AI, Machine Learning, Automation, Digital Transformation, Tech Innovation"""

        try:
            response = self.model.generate_content(prompt)
            keywords_text = response.text.strip()
            
            # Parse keywords
            keywords = [kw.strip() for kw in keywords_text.split(',')]
            keywords = [kw for kw in keywords if kw and len(kw) > 1]
            
            return keywords[:12]
            
        except Exception as e:
            print(f"Keywords generation failed: {e}")
            # Extract keywords from topic and content
            return self._extract_fallback_keywords(topic, content)

    def _clean_hashtag(self, tag: str) -> str:
        """Clean and format hashtag"""
        if not tag:
            return ""
        
        # Remove extra spaces and special chars
        tag = tag.strip()
        if not tag.startswith('#'):
            tag = '#' + tag
        
        # Remove spaces and special characters except #
        tag = re.sub(r'[^#\w]', '', tag)
        
        return tag

    def _generate_fallback_hashtags(self, topic: str, max_tags: int) -> List[str]:
        """Generate basic hashtags from topic"""
        words = topic.lower().split()
        hashtags = []
        
        # Add topic as hashtag
        topic_tag = '#' + ''.join(word.capitalize() for word in words)
        hashtags.append(topic_tag)
        
        # Add individual words
        for word in words:
            if len(word) > 3:
                hashtags.append(f'#{word.capitalize()}')
        
        # Add generic relevant tags
        generic_tags = ['#Innovation', '#Technology', '#Tips', '#Guide', '#Insights']
        hashtags.extend(generic_tags)
        
        return hashtags[:max_tags]

    def _extract_fallback_keywords(self, topic: str, content: str) -> List[str]:
        """Extract basic keywords from topic and content"""
        keywords = []
        
        # Add topic words
        keywords.extend(topic.split())
        
        # Extract common words from content
        words = re.findall(r'\b[A-Za-z]{4,}\b', content.lower())
        word_freq = {}
        
        for word in words:
            if word not in ['this', 'that', 'with', 'from', 'they', 'have', 'will', 'been', 'were']:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get most frequent words
        frequent_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        keywords.extend([word for word, freq in frequent_words[:8]])
        
        return list(set(keywords))[:10]