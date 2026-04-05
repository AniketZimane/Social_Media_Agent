import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class SocialMediaPoster:
    def __init__(self):
        self.linkedin_token = os.getenv("LINKEDIN_ACCESS_TOKEN")
        self.facebook_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.facebook_page_id = os.getenv("FACEBOOK_PAGE_ID")
        
    def post_to_linkedin(self, content: str, image_url: str = None):
        """Post content to LinkedIn"""
        try:
            url = "https://api.linkedin.com/v2/ugcPosts"
            headers = {
                "Authorization": f"Bearer {self.linkedin_token}",
                "Content-Type": "application/json",
                "X-Restli-Protocol-Version": "2.0.0"
            }
            
            payload = {
                "author": "urn:li:person:YOUR_PERSON_ID",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": content[:3000]  # LinkedIn limit
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(url, headers=headers, json=payload)
            return {"success": response.status_code == 201, "platform": "LinkedIn", "response": response.json()}
        except Exception as e:
            return {"success": False, "platform": "LinkedIn", "error": str(e)}
    
    def post_to_facebook(self, content: str, image_url: str = None):
        """Post content to Facebook"""
        try:
            url = f"https://graph.facebook.com/v18.0/{self.facebook_page_id}/feed"
            params = {
                "message": content,
                "access_token": self.facebook_token
            }
            
            if image_url:
                params["link"] = image_url
            
            response = requests.post(url, params=params)
            return {"success": response.status_code == 200, "platform": "Facebook", "response": response.json()}
        except Exception as e:
            return {"success": False, "platform": "Facebook", "error": str(e)}
    
    def post_to_twitter(self, content: str, image_url: str = None):
        """Post content to Twitter (X)"""
        # Twitter API v2 requires OAuth 2.0
        return {"success": False, "platform": "Twitter", "error": "Not implemented - requires OAuth 2.0"}
    
    def post_to_instagram(self, content: str, image_url: str):
        """Post content to Instagram"""
        # Instagram requires image URL
        if not image_url:
            return {"success": False, "platform": "Instagram", "error": "Image required"}
        
        return {"success": False, "platform": "Instagram", "error": "Not implemented - requires Facebook Graph API"}
    
    def auto_post(self, blog_content: dict, platforms: list):
        """Auto post to multiple platforms"""
        results = []
        
        content = f"{blog_content.get('title', '')}\n\n{blog_content.get('content', '')[:500]}...\n\n{' '.join(blog_content.get('hashtags', [])[:5])}"
        image_url = blog_content.get('image_url')
        
        for platform in platforms:
            if platform == "💼 LinkedIn":
                result = self.post_to_linkedin(content, image_url)
            elif platform == "👥 Facebook":
                result = self.post_to_facebook(content, image_url)
            elif platform == "🐦 Twitter":
                result = self.post_to_twitter(content, image_url)
            elif platform == "📸 Instagram":
                result = self.post_to_instagram(content, image_url)
            else:
                result = {"success": False, "platform": platform, "error": "Unknown platform"}
            
            results.append(result)
        
        return results
