import os
import requests
from dotenv import load_dotenv

load_dotenv()

def post_linkedin_v2():
    """Post using LinkedIn API v2 with member URN format"""
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    try:
        # Use the newer API format that works with w_member_social only
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        
        # Use member URN format instead of person
        post_data = {
            "author": "urn:li:member:~",  # Use member instead of person
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": "🤖 Testing AI-powered blog writing assistant! This system generates intelligent content and posts to multiple platforms automatically. #AI #Automation #BlogWriting #SocialMedia"
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        print("[LINKEDIN] Posting with member URN format...")
        response = requests.post(url, headers=headers, json=post_data)
        
        print(f"[LINKEDIN] Response Status: {response.status_code}")
        print(f"[LINKEDIN] Response: {response.text}")
        
        if response.status_code == 201:
            print("[LINKEDIN] SUCCESS: Post published!")
            return True
        else:
            print(f"[LINKEDIN] FAILED: {response.text}")
            return False
            
    except Exception as e:
        print(f"[LINKEDIN] ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing LinkedIn v2 API with member URN...")
    success = post_linkedin_v2()
    
    if success:
        print("LinkedIn post successful!")
    else:
        print("LinkedIn post failed.")