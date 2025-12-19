import os
import requests
from dotenv import load_dotenv

load_dotenv()

def post_linkedin_ugc():
    """Post using correct LinkedIn UGC Posts API format"""
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    try:
        # First get the authenticated user's profile
        profile_url = "https://api.linkedin.com/v2/people/~"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print("[LINKEDIN] Getting profile...")
        profile_response = requests.get(profile_url, headers=headers)
        print(f"[LINKEDIN] Profile Status: {profile_response.status_code}")
        
        if profile_response.status_code != 200:
            # Try without profile, use generic person URN
            print("[LINKEDIN] Using generic person URN...")
            
            url = "https://api.linkedin.com/v2/ugcPosts"
            
            # Simplified UGC post
            post_data = {
                "author": "urn:li:person:~",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": "🤖 Testing AI-powered blog writing assistant! This system generates content and posts automatically. #AI #Automation #BlogWriting"
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            print("[LINKEDIN] Posting UGC content...")
            response = requests.post(url, headers=headers, json=post_data)
            
            print(f"[LINKEDIN] UGC Response Status: {response.status_code}")
            print(f"[LINKEDIN] UGC Response: {response.text}")
            
            if response.status_code == 201:
                print("[LINKEDIN] SUCCESS: UGC post published!")
                return True
            else:
                print(f"[LINKEDIN] UGC FAILED: {response.text}")
                return False
        
    except Exception as e:
        print(f"[LINKEDIN] ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing LinkedIn UGC Posts API...")
    success = post_linkedin_ugc()
    
    if success:
        print("LinkedIn UGC post successful!")
    else:
        print("LinkedIn UGC post failed - token may need r_liteprofile permission too.")