import os
import html
import re
import json
from typing import Dict, List
from dotenv import load_dotenv
import google.generativeai as genai
from metadata_agent import MetadataAgent

load_dotenv()


class BlogWriterAgent:
    """
    Enhanced AI Blog Writer Agent
    - Generates fully dynamic, platform-optimized content
    - Structured output with hashtags, CTAs, and engagement metrics
    - Better prompt engineering for consistent results
    """

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_AI_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_AI_API_KEY not set in environment")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        self.metadata_agent = MetadataAgent()

    # -------------------- PUBLIC METHOD --------------------
    def write_blog(self, topic: str, platform: str, word_count: int = None) -> Dict:
        """Generate complete blog content with all metadata
        
        Args:
            topic: The blog topic
            platform: Target platform (Instagram, LinkedIn, Twitter, etc.)
            word_count: Desired word count (None = platform default)
        """
        
        # Set platform-specific defaults if not provided
        if word_count is None:
            platform_defaults = {
                "instagram": 300,
                "twitter": 280,
                "linkedin": 800,
                "youtube": 1000,
                "facebook": 500,
                "medium": 1500,
                "tiktok": 150
            }
            word_count = platform_defaults.get(platform.lower(), 800)
        
        print(f"Generating AI content for: {topic} on {platform} ({word_count} words)")
        
        try:
            # Generate main content
            content_result = self._generate_content(topic, platform, word_count)
            
            # Generate all metadata using specialized agent
            metadata = self.metadata_agent.generate_metadata(topic, content_result, platform)
            
            # Extract or generate title
            title = self._extract_or_generate_title(content_result, topic)
            
            # Calculate engagement metrics
            engagement_score = self._calculate_engagement_score(
                content_result, platform, metadata.get('hashtags', [])
            )
            
            final_content = html.unescape(content_result)
            
            print(f"Successfully generated {len(final_content)} characters")
            
            return {
                "success": True,
                "title": title,
                "content": final_content,
                "hashtags": metadata.get('hashtags', []),
                "cta": metadata.get('cta', f"What are your thoughts on {topic}? Share below! 💭"),
                "keywords": metadata.get('keywords', []),
                "platform": platform,
                "engagement_score": engagement_score,
                "word_count": len(final_content.split()),
                "metadata": {
                    "reading_time": self._estimate_reading_time(final_content),
                    "platform_optimized": True,
                    "has_emojis": self._has_emojis(final_content),
                    "structure_score": self._evaluate_structure(final_content),
                    "metadata_generated": metadata.get('success', False)
                }
            }

        except Exception as e:
            print(f"AI generation failed: {e}")
            return self._generate_fallback_response(topic, platform, str(e))

    # -------------------- CONTENT GENERATION --------------------
    def _generate_content(self, topic: str, platform: str, word_count: int) -> str:
        """Generate main blog content with enhanced prompting"""
        
        platform_styles = {
            "instagram": "visual storytelling with emojis, short paragraphs, engaging hooks",
            "linkedin": "professional insights, data-driven, industry expertise, thought leadership",
            "twitter": "concise, punchy, thread-worthy insights with strong hooks",
            "youtube": "conversational, tutorial-style with clear sections and timestamps",
            "facebook": "community-focused, relatable stories, discussion-worthy",
            "medium": "in-depth analysis, storytelling, journalistic approach",
            "tiktok": "trendy, fast-paced, hook-first content with millennial/Gen-Z appeal"
        }
        
        style = platform_styles.get(platform.lower(), platform_styles["instagram"])
        
        # Detect topic category for specialized prompting
        topic_category = self._detect_topic_category(topic)
        
        prompt = f"""You are an expert content writer specializing in {platform} content.

TASK: Write a comprehensive, engaging blog post

TOPIC: {topic}
PLATFORM: {platform}
TARGET LENGTH: {word_count} words
STYLE: {style}
CATEGORY: {topic_category}

CONTENT REQUIREMENTS:
1. **Compelling Title** - Make it click-worthy and platform-appropriate
2. **Strong Hook** - First 2-3 sentences must grab attention
3. **Well-Structured Body**:
   - Use clear subheadings (## format) - adjust number based on length
   - Include bullet points for lists where appropriate
   - Use emojis naturally (adjust to content length and platform)
   - Include real examples, statistics, or case studies
   - Add actionable tips and insights
4. **Engaging Conclusion** - Summarize key takeaways (1-2 sentences)
5. **Call-to-Action** - Encourage engagement (1 sentence)

WRITING STYLE:
- Write in second person ("you") to connect with readers
- Use active voice and conversational tone
- Break up long paragraphs (3-4 sentences max)
- Include transitions between sections
- Add specific, concrete examples (not generic)
- Make it scannable with formatting
- ADAPT DEPTH to the word count: shorter = more concise, longer = more detailed

PLATFORM-SPECIFIC OPTIMIZATION FOR {platform.upper()}:
{self._get_platform_guidelines(platform)}

CRITICAL RULES:
❌ NO generic filler or fluff
❌ NO placeholders like [insert example]
❌ NO hashtags in the body (they'll be added separately)
❌ NO overly promotional language
✅ Write like a human expert, not a robot
✅ Provide genuine value and insights
✅ Use specific data and examples when relevant

Now write the complete blog post:"""

        response = self.model.generate_content(prompt)
        content = response.text if response and response.text else ""
        
        # Fallback if content is too short
        if len(content.strip()) < 300:
            print("⚠️ Initial content too short, regenerating...")
            simplified_prompt = f"""Write a detailed {word_count}-word blog post about: {topic}

Make it engaging and valuable for {platform} audience. Include:
- Catchy title
- Strong introduction
- 4-5 main sections with subheadings
- Practical examples and tips
- Clear conclusion

Write naturally and provide real value."""
            
            response = self.model.generate_content(simplified_prompt)
            content = response.text if response and response.text else content
        
        return content

    # -------------------- HELPER METHODS --------------------

    # -------------------- HELPER METHODS --------------------
    def _detect_topic_category(self, topic: str) -> str:
        """Detect topic category for specialized prompting"""
        topic_lower = topic.lower()
        
        categories = {
            "Technology": ["ai", "tech", "software", "app", "digital", "programming", "code"],
            "Business": ["business", "startup", "marketing", "sales", "finance", "entrepreneur"],
            "Lifestyle": ["lifestyle", "travel", "food", "fashion", "home", "wellness"],
            "Education": ["learn", "guide", "tutorial", "how to", "tips", "education"],
            "Entertainment": ["movie", "music", "game", "entertainment", "fun", "celebrity"]
        }
        
        for category, keywords in categories.items():
            if any(kw in topic_lower for kw in keywords):
                return category
        
        return "General"

    def _get_platform_guidelines(self, platform: str) -> str:
        """Get platform-specific writing guidelines"""
        guidelines = {
            "instagram": "- Use 3-5 emojis naturally\n- Short paragraphs (2-3 sentences)\n- Visual language\n- Trending topics",
            "linkedin": "- Professional tone but conversational\n- Data and insights\n- Industry credibility\n- Thought leadership",
            "twitter": "- Concise and punchy\n- Thread-worthy insights\n- Strong hooks\n- Quotable lines",
            "youtube": "- Conversational style\n- Clear structure\n- Tutorial approach\n- Timestamp-friendly sections",
            "facebook": "- Community-focused\n- Relatable stories\n- Discussion starters\n- Longer-form acceptable"
        }
        return guidelines.get(platform.lower(), "- Engaging and valuable content")

    def _extract_or_generate_title(self, content: str, topic: str) -> str:
        """Extract title from content or generate one"""
        lines = content.split('\n')
        
        # Try to find title in first few lines
        for line in lines[:5]:
            cleaned = line.replace('#', '').replace('*', '').strip()
            if cleaned and len(cleaned) > 10 and len(cleaned) < 120:
                return cleaned
        
        # Fallback: generate title
        words = topic.split()
        if len(words) <= 5:
            return f"Complete Guide to {topic}"
        else:
            return topic[:100]



    def _calculate_engagement_score(self, content: str, platform: str, hashtags: List[str]) -> float:
        """Calculate predicted engagement score"""
        score = 0.65
        
        # Content quality factors - adjust based on word count
        word_count = len(content.split())
        
        # Optimal word count varies by platform
        optimal_ranges = {
            "instagram": (250, 400),
            "twitter": (100, 280),
            "linkedin": (600, 1000),
            "youtube": (800, 1500),
            "facebook": (400, 800),
            "medium": (1000, 2000),
            "tiktok": (100, 200)
        }
        
        optimal_min, optimal_max = optimal_ranges.get(platform.lower(), (500, 1000))
        if optimal_min <= word_count <= optimal_max:
            score += 0.10
        elif word_count < optimal_min:
            score += 0.05  # Partial credit for concise content
        
        # Power words
        power_words = ["ultimate", "proven", "secret", "essential", "master", 
                       "transform", "boost", "unlock", "discover", "breakthrough"]
        power_word_count = sum(1 for word in power_words if word in content.lower())
        score += min(power_word_count * 0.02, 0.10)
        
        # Structure elements
        if "##" in content or "**" in content:
            score += 0.05
        
        # Hashtag quality
        if len(hashtags) >= 5:
            score += 0.05
        
        # Platform boost
        platform_boost = {
            "instagram": 0.08,
            "tiktok": 0.10,
            "youtube": 0.07,
            "linkedin": 0.04,
            "twitter": 0.03,
            "facebook": 0.05
        }
        score += platform_boost.get(platform.lower(), 0.03)
        
        return min(score, 0.98)

    def _estimate_reading_time(self, content: str) -> str:
        """Estimate reading time in minutes"""
        words = len(content.split())
        minutes = max(1, round(words / 200))
        return f"{minutes} min read"

    def _has_emojis(self, content: str) -> bool:
        """Check if content contains emojis"""
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "]+", 
            flags=re.UNICODE
        )
        return bool(emoji_pattern.search(content))

    def _evaluate_structure(self, content: str) -> float:
        """Evaluate content structure quality"""
        score = 0.5
        
        if "##" in content:  # Has subheadings
            score += 0.2
        if "\n\n" in content:  # Has paragraph breaks
            score += 0.1
        if any(marker in content for marker in ["- ", "* ", "1. "]):  # Has lists
            score += 0.1
        if len(content.split('\n')) > 10:  # Well-structured
            score += 0.1
        
        return min(score, 1.0)

    def _generate_fallback_response(self, topic: str, platform: str, error: str) -> Dict:
        """Generate fallback response on error"""
        return {
            "success": False,
            "title": f"Error: Unable to generate content for {topic}",
            "content": f"We encountered an issue generating content. Please try again.\n\nError details: {error}",
            "hashtags": [f"#{word.capitalize()}" for word in topic.split()[:3]],
            "cta": "Please try again with a different topic.",
            "keywords": [topic],
            "platform": platform,
            "engagement_score": 0.0,
            "word_count": 0,
            "error": error
        }


# -------------------- COMPATIBILITY WRAPPER --------------------
class GoogleAIIntegration:
    """Backward-compatible wrapper"""
    
    def __init__(self):
        self.agent = BlogWriterAgent()
    
    def generate_blog_content(self, topic: str, platform: str, word_count: int = None) -> Dict:
        """Generate blog content (compatible with old API)
        
        Args:
            topic: Blog topic
            platform: Target platform
            word_count: Desired word count (None = platform default)
        """
        return self.agent.write_blog(topic, platform, word_count)


# -------------------- DEMO & TESTING --------------------
if __name__ == "__main__":
    print("=" * 60)
    print("🤖 Enhanced Social Media Blog Writer Agent")
    print("=" * 60)
    
    agent = BlogWriterAgent()
    
    # Test with multiple examples
    test_cases = [
        ("AI Tools Every Startup Founder Should Use in 2025", "LinkedIn", 1000),
        ("Best Travel Destinations for Digital Nomads", "Instagram", 400),
        ("Quick Python Tips for Beginners", "Twitter", 280)
    ]
    
    for topic, platform, word_count in test_cases[:1]:  # Run first test
        print(f"\n📝 Generating: {topic}")
        print(f"📱 Platform: {platform}")
        print(f"📊 Target Words: {word_count}\n")
        
        result = agent.write_blog(topic, platform, word_count)
        
        if result["success"]:
            print(f"✅ SUCCESS!")
            print(f"\n{'='*60}")
            print(f"TITLE: {result['title']}")
            print(f"{'='*60}")
            print(f"\nCONTENT ({result['word_count']} words):")
            print(result['content'][:1000] + "...\n")
            print(f"{'='*60}")
            print(f"HASHTAGS ({len(result['hashtags'])}):")
            print(" ".join(result['hashtags']))
            print(f"\n{'='*60}")
            print(f"CTA: {result['cta']}")
            print(f"\n{'='*60}")
            print(f"METADATA:")
            print(f"  • Engagement Score: {result['engagement_score']:.2f}")
            print(f"  • Reading Time: {result['metadata']['reading_time']}")
            print(f"  • Has Emojis: {result['metadata']['has_emojis']}")
            print(f"  • Structure Score: {result['metadata']['structure_score']:.2f}")
            print(f"  • Keywords: {', '.join(result['keywords'][:5])}")
        else:
            print(f"❌ FAILED: {result.get('error')}")
        
        print("\n" + "=" * 60 + "\n")