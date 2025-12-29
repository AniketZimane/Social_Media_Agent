import requests
import os
from dotenv import load_dotenv

load_dotenv()

class LinkedInPoster:
    def __init__(self):
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.base_url = "https://api.linkedin.com/v2"
    
    def get_user_profile(self):
        """Get user profile information"""
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
        
        response = requests.get(f"{self.base_url}/people/~", headers=headers)
        return response.json() if response.status_code == 200 else None
    
    def post_to_linkedin(self, content, title="", hashtags=None):
        """Post content to LinkedIn"""
        if not self.access_token:
            return {"success": False, "error": "LinkedIn access token not found"}
        
        # Get user profile first
        profile = self.get_user_profile()
        if not profile:
            return {"success": False, "error": "Could not get user profile"}
        
        user_id = profile.get('id')
        
        # Prepare post content
        post_text = f"{title}\n\n{content}"
        if hashtags:
            post_text += f"\n\n{' '.join(hashtags)}"
        
        # LinkedIn post payload
        post_data = {
            "author": f"urn:li:person:{user_id}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": post_text
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/ugcPosts",
                json=post_data,
                headers=headers
            )
            
            if response.status_code == 201:
                return {
                    "success": True,
                    "platform": "LinkedIn",
                    "post_id": response.headers.get('x-restli-id'),
                    "message": "Posted successfully to LinkedIn"
                }
            else:
                return {
                    "success": False,
                    "platform": "LinkedIn",
                    "error": f"LinkedIn API error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "platform": "LinkedIn",
                "error": f"Error posting to LinkedIn: {str(e)}"
            }

class TwitterPoster:
    def __init__(self):
        self.bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    
    def post_to_twitter(self, content, title="", hashtags=None):
        """Post content to Twitter (X)"""
        # Note: Twitter API v2 requires OAuth 1.0a for posting
        # This is a simplified implementation
        
        post_text = f"{title}\n\n{content}"
        if hashtags:
            # Limit hashtags for Twitter
            twitter_hashtags = hashtags[:5]  # Max 5 hashtags
            post_text += f"\n\n{' '.join(twitter_hashtags)}"
        
        # Truncate to Twitter's character limit
        if len(post_text) > 280:
            post_text = post_text[:277] + "..."
        
        # Mock implementation - replace with actual Twitter API v2 call
        return {
            "success": True,
            "platform": "Twitter",
            "post_id": "twitter_mock_123",
            "message": f"Posted to Twitter: {post_text[:50]}..."
        }

class FacebookPoster:
    def __init__(self):
        self.access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        self.page_id = os.getenv('FACEBOOK_PAGE_ID')
    
    def post_to_facebook(self, content, title="", hashtags=None):
        """Post content to Facebook"""
        if not self.access_token:
            return {"success": False, "error": "Facebook access token not found"}
        
        post_text = f"{title}\n\n{content}"
        if hashtags:
            post_text += f"\n\n{' '.join(hashtags)}"
        
        # Facebook Graph API endpoint
        url = f"https://graph.facebook.com/v18.0/{self.page_id}/feed"
        
        payload = {
            'message': post_text,
            'access_token': self.access_token
        }
        
        try:
            response = requests.post(url, data=payload)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "platform": "Facebook",
                    "post_id": result.get('id'),
                    "message": "Posted successfully to Facebook"
                }
            else:
                return {
                    "success": False,
                    "platform": "Facebook",
                    "error": f"Facebook API error: {response.status_code} - {response.text}"
                }
                
        except Exception as e:
            return {
                "success": False,
                "platform": "Facebook",
                "error": f"Error posting to Facebook: {str(e)}"
            }

# Test the integrations
if __name__ == "__main__":
    linkedin_poster = LinkedInPoster()
    
    test_content = {
        "title": "AI is Transforming Content Creation",
        "content": "Artificial Intelligence is revolutionizing how we create and optimize content across social media platforms. From automated writing to engagement prediction, AI tools are becoming essential for modern content creators.",
        "hashtags": ["#AI", "#ContentCreation", "#SocialMedia", "#Technology", "#Innovation"]
    }
    
    print("🔗 Testing LinkedIn integration...")
    result = linkedin_poster.post_to_linkedin(
        content=test_content["content"],
        title=test_content["title"],
        hashtags=test_content["hashtags"]
    )
    
    print(f"LinkedIn Result: {result}")