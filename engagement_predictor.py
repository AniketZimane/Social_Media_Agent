import re
from typing import Dict

class EngagementPredictor:
    def __init__(self):
        # Platform base engagement rates
        self.platform_base = {
            '📸 Instagram': 0.85,
            '🐦 Twitter': 0.78,
            '💼 LinkedIn': 0.82,
            '📺 YouTube': 0.88,
            '👥 Facebook': 0.75
        }
        
        # Engagement boosters
        self.emoji_boost = 0.03
        self.hashtag_boost = 0.02
        self.question_boost = 0.04
        self.list_boost = 0.03
        self.image_boost = 0.05
        self.length_optimal = (200, 500)  # Optimal word count range
    
    def predict_engagement(self, content: Dict, platform: str) -> float:
        """Dynamically calculate engagement score based on content analysis"""
        
        # Start with platform base
        score = self.platform_base.get(platform, 0.75)
        
        # Analyze content
        text = content.get('content', '')
        title = content.get('title', '')
        hashtags = content.get('hashtags', [])
        has_image = bool(content.get('image_url'))
        
        # 1. Emoji analysis
        emoji_count = len(re.findall(r'[\U0001F300-\U0001F9FF]', text + title))
        if emoji_count > 0:
            score += min(emoji_count * 0.01, self.emoji_boost)
        
        # 2. Hashtag optimization
        hashtag_count = len(hashtags)
        optimal_hashtags = self._get_optimal_hashtag_count(platform)
        if hashtag_count >= optimal_hashtags * 0.7:
            score += self.hashtag_boost
        
        # 3. Question engagement
        if '?' in text or '?' in title:
            score += self.question_boost
        
        # 4. List/bullet points
        if '*' in text or '•' in text or re.search(r'\d+\.', text):
            score += self.list_boost
        
        # 5. Image presence
        if has_image:
            score += self.image_boost
        
        # 6. Content length optimization
        word_count = len(text.split())
        if self.length_optimal[0] <= word_count <= self.length_optimal[1]:
            score += 0.03
        elif word_count < self.length_optimal[0]:
            score -= 0.02
        elif word_count > self.length_optimal[1] * 2:
            score -= 0.03
        
        # 7. Call-to-action presence
        cta = content.get('cta', '')
        if cta and len(cta) > 10:
            score += 0.02
        
        # 8. Title quality (length and engagement)
        if 40 <= len(title) <= 80:
            score += 0.02
        
        # 9. Keyword density
        keywords = content.get('keywords', [])
        if len(keywords) >= 3:
            score += 0.02
        
        # Cap score between 0.5 and 0.98
        score = max(0.5, min(0.98, score))
        
        return round(score, 2)
    
    def _get_optimal_hashtag_count(self, platform: str) -> int:
        """Get optimal hashtag count for platform"""
        optimal = {
            '📸 Instagram': 10,
            '🐦 Twitter': 3,
            '💼 LinkedIn': 5,
            '📺 YouTube': 8,
            '👥 Facebook': 5
        }
        return optimal.get(platform, 5)
    
    def get_engagement_tips(self, content: Dict, platform: str) -> list:
        """Generate tips to improve engagement"""
        tips = []
        
        text = content.get('content', '')
        hashtags = content.get('hashtags', [])
        has_image = bool(content.get('image_url'))
        
        # Check for improvements
        if not has_image:
            tips.append("Add an eye-catching image to boost engagement by 5%")
        
        emoji_count = len(re.findall(r'[\U0001F300-\U0001F9FF]', text))
        if emoji_count < 3:
            tips.append("Add more emojis (3-5) to make content more engaging")
        
        if '?' not in text:
            tips.append("Include a question to encourage audience interaction")
        
        optimal_hashtags = self._get_optimal_hashtag_count(platform)
        if len(hashtags) < optimal_hashtags * 0.7:
            tips.append(f"Use {optimal_hashtags} hashtags for optimal reach on {platform}")
        
        word_count = len(text.split())
        if word_count < 200:
            tips.append("Expand content to 200-500 words for better engagement")
        
        return tips[:3]  # Return top 3 tips
