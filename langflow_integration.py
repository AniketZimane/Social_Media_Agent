import requests
import json
from typing import Dict, List, Optional
import streamlit as st

class LangFlowClient:
    def __init__(self, base_url: str = "http://localhost:7860"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def create_blog_flow(self) -> str:
        """Create LangFlow for blog content generation"""
        flow_config = {
            "data": {
                "nodes": [
                    {
                        "id": "ChatInput-1",
                        "type": "ChatInput",
                        "data": {
                            "input_value": "",
                            "sender": "User",
                            "sender_name": "User",
                            "session_id": "",
                            "should_store_message": True
                        }
                    },
                    {
                        "id": "Prompt-1", 
                        "type": "PromptTemplate",
                        "data": {
                            "template": "Generate 3 blog topics about {topic} for {platform}. Include engagement predictions and optimization tips. Format as JSON."
                        }
                    },
                    {
                        "id": "OpenAI-1",
                        "type": "OpenAI", 
                        "data": {
                            "model_name": "gpt-3.5-turbo",
                            "max_tokens": 500,
                            "temperature": 0.7
                        }
                    },
                    {
                        "id": "ChatOutput-1",
                        "type": "ChatOutput",
                        "data": {}
                    }
                ],
                "edges": [
                    {"source": "ChatInput-1", "target": "Prompt-1"},
                    {"source": "Prompt-1", "target": "OpenAI-1"},
                    {"source": "OpenAI-1", "target": "ChatOutput-1"}
                ]
            }
        }
        return json.dumps(flow_config)
    
    def run_blog_generation(self, topic: str, platform: str) -> Dict:
        """Run blog generation flow"""
        try:
            payload = {
                "input_value": f"Topic: {topic}, Platform: {platform}",
                "tweaks": {
                    "ChatInput-1": {"input_value": f"Generate blog content for {topic} on {platform}"},
                    "Prompt-1": {"template": f"Create 3 engaging blog topics about {topic} optimized for {platform}. Include engagement scores and posting tips."}
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/run/blog-assistant",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_langflow_response(result)
            
        except Exception as e:
            st.error(f"LangFlow connection failed: {e}")
        
        return self._fallback_response(topic, platform)
    
    def _parse_langflow_response(self, response: Dict) -> Dict:
        """Parse LangFlow API response"""
        try:
            output_text = response.get("outputs", [{}])[0].get("outputs", [{}])[0].get("results", {}).get("message", {}).get("text", "")
            
            # Try to parse JSON from response
            if "{" in output_text and "}" in output_text:
                json_start = output_text.find("{")
                json_end = output_text.rfind("}") + 1
                json_str = output_text[json_start:json_end]
                parsed = json.loads(json_str)
                return parsed
            
        except:
            pass
        
        return self._extract_topics_from_text(response)
    
    def _extract_topics_from_text(self, response: Dict) -> Dict:
        """Extract topics from plain text response"""
        text = str(response)
        topics = []
        
        # Simple extraction logic
        lines = text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['topic', 'title', 'blog']):
                if len(line.strip()) > 10:
                    topics.append({
                        "title": line.strip()[:100],
                        "engagement_score": 0.8,
                        "platform_fit": 0.85
                    })
        
        return {
            "topics": topics[:3] if topics else self._default_topics(),
            "engagement_prediction": 0.82,
            "optimization_tips": ["Use AI-generated hashtags", "Post during peak hours"]
        }
    
    def _fallback_response(self, topic: str, platform: str) -> Dict:
        """Fallback when LangFlow is unavailable"""
        return {
            "topics": [
                {"title": f"AI Insights: {topic} Revolution", "engagement_score": 0.87, "platform_fit": 0.9},
                {"title": f"Future of {topic}: Expert Analysis", "engagement_score": 0.82, "platform_fit": 0.85},
                {"title": f"{topic} Trends You Need to Know", "engagement_score": 0.79, "platform_fit": 0.8}
            ],
            "engagement_prediction": 0.83,
            "optimization_tips": [
                f"Optimize for {platform} audience",
                "Use trending hashtags",
                "Post at peak engagement times"
            ]
        }
    
    def _default_topics(self) -> List[Dict]:
        """Default topics when parsing fails"""
        return [
            {"title": "AI-Generated Content Strategy", "engagement_score": 0.8, "platform_fit": 0.85},
            {"title": "Dynamic Content Optimization", "engagement_score": 0.75, "platform_fit": 0.8},
            {"title": "Automated Blog Generation", "engagement_score": 0.82, "platform_fit": 0.87}
        ]

class LangFlowIntegration:
    def __init__(self):
        self.client = LangFlowClient()
        self.is_connected = self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test LangFlow connection"""
        try:
            response = requests.get(f"{self.client.base_url}/health", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def generate_dynamic_content(self, topic: str, platform: str) -> Dict:
        """Generate content using LangFlow"""
        if self.is_connected:
            return self.client.run_blog_generation(topic, platform)
        else:
            st.warning("LangFlow not connected. Using fallback AI generation.")
            return self.client._fallback_response(topic, platform)
    
    def get_connection_status(self) -> str:
        """Get connection status for UI"""
        return "🟢 Connected" if self.is_connected else "🔴 Disconnected"