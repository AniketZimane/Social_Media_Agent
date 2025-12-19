import requests
import json
from typing import List, Dict
import random
from datetime import datetime

class ContentSourceManager:
    """Manages multiple content sources for blog topic generation"""
    
    def __init__(self):
        self.sources = {
            "news_api": "https://newsapi.org/v2/everything",
            "reddit": "https://www.reddit.com/r/{}/hot.json",
            "hackernews": "https://hacker-news.firebaseio.com/v0/topstories.json"
        }
    
    def collect_news_content(self, topic: str, api_key: str = "demo") -> List[Dict]:
        """Collect content from news sources"""
        try:
            params = {
                "q": topic,
                "apiKey": api_key,
                "pageSize": 5,
                "sortBy": "popularity"
            }
            response = requests.get(self.sources["news_api"], params=params, timeout=5)
            
            if response.status_code == 200:
                articles = response.json().get("articles", [])
                return [
                    {
                        "title": article["title"],
                        "description": article["description"],
                        "source": "news",
                        "url": article["url"],
                        "published": article["publishedAt"],
                        "sentiment": random.uniform(0.6, 0.9)
                    }
                    for article in articles[:3]
                ]
        except Exception as e:
            print(f"News API error: {e}")
        
        # Fallback mock data
        return self._generate_mock_news(topic)
    
    def collect_social_trends(self, topic: str) -> List[Dict]:
        """Simulate social media trend collection"""
        social_platforms = ["Twitter", "Instagram", "TikTok", "LinkedIn"]
        trends = []
        
        for platform in social_platforms:
            trends.append({
                "title": f"{topic} trending on {platform}",
                "platform": platform,
                "engagement": random.randint(1000, 100000),
                "sentiment": random.uniform(0.5, 0.95),
                "hashtags": [f"#{topic.replace(' ', '')}", f"#{platform}Trends"],
                "source": "social_media"
            })
        
        return trends
    
    def collect_research_papers(self, topic: str) -> List[Dict]:
        """Simulate academic research collection"""
        research_topics = [
            f"Recent advances in {topic}",
            f"{topic}: A comprehensive review",
            f"Future directions in {topic} research",
            f"{topic} applications and implications"
        ]
        
        papers = []
        for research_topic in research_topics[:2]:
            papers.append({
                "title": research_topic,
                "abstract": f"This paper explores the latest developments in {topic}...",
                "source": "research",
                "citations": random.randint(10, 500),
                "year": random.choice([2023, 2024]),
                "sentiment": random.uniform(0.7, 0.9)
            })
        
        return papers
    
    def _generate_mock_news(self, topic: str) -> List[Dict]:
        """Generate mock news data when API fails"""
        mock_articles = [
            f"Breaking: {topic} Market Sees Major Breakthrough",
            f"Industry Leaders Discuss Future of {topic}",
            f"New Study Reveals {topic} Impact on Society",
            f"{topic} Innovation Drives Economic Growth",
            f"Experts Predict {topic} Will Transform Industries"
        ]
        
        return [
            {
                "title": title,
                "description": f"Latest developments and insights about {topic}",
                "source": "news",
                "url": "https://example.com",
                "published": datetime.now().isoformat(),
                "sentiment": random.uniform(0.6, 0.9)
            }
            for title in random.sample(mock_articles, 3)
        ]
    
    def aggregate_all_sources(self, topic: str) -> Dict[str, List[Dict]]:
        """Aggregate content from all sources"""
        return {
            "news": self.collect_news_content(topic),
            "social": self.collect_social_trends(topic),
            "research": self.collect_research_papers(topic)
        }
    
    def rank_content_by_relevance(self, content: Dict[str, List[Dict]], topic: str) -> List[Dict]:
        """Rank all content by relevance and engagement potential"""
        all_content = []
        
        for source_type, items in content.items():
            for item in items:
                item["source_type"] = source_type
                item["relevance_score"] = self._calculate_relevance(item, topic)
                all_content.append(item)
        
        return sorted(all_content, key=lambda x: x["relevance_score"], reverse=True)
    
    def _calculate_relevance(self, item: Dict, topic: str) -> float:
        """Calculate content relevance score"""
        base_score = 0.5
        
        # Title relevance
        if topic.lower() in item["title"].lower():
            base_score += 0.3
        
        # Sentiment boost
        base_score += item.get("sentiment", 0.5) * 0.2
        
        # Source type weighting
        source_weights = {
            "news": 1.0,
            "research": 0.9,
            "social_media": 0.8
        }
        
        source_type = item.get("source_type", "news")
        base_score *= source_weights.get(source_type, 1.0)
        
        return min(base_score, 1.0)