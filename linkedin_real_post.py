import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def get_linkedin_user_info():
    """Get LinkedIn user info to get person URN"""
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    try:
        # Use userinfo endpoint which works with w_member_social
        url = "https://api.linkedin.com/v2/userinfo"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print("[LINKEDIN] Getting user info...")
        response = requests.get(url, headers=headers)
        print(f"[LINKEDIN] Response Status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"[LINKEDIN] User data: {user_data}")
            
            # Get sub which contains the person ID
            sub = user_data.get('sub')
            if sub:
                print(f"[LINKEDIN] Person URN: urn:li:person:{sub}")
                return f"urn:li:person:{sub}"
        else:
            print(f"[LINKEDIN] Failed: {response.text}")
            
    except Exception as e:
        print(f"[LINKEDIN] Error: {e}")
    
    return None

def post_to_linkedin_real():
    """Post to LinkedIn with real API call"""
    
    # Get person URN
    person_urn = get_linkedin_user_info()
    if not person_urn:
        print("[LINKEDIN] Cannot get person URN")
        return False
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    try:
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        post_data = {
            "author": person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": "Testing AI-powered blog writing assistant with automated social media posting! 🤖 This system generates intelligent content and posts to multiple platforms. #AI #Automation #BlogWriting #SocialMedia #Innovation"
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        print("[LINKEDIN] Posting with real API...")
        response = requests.post(url, headers=headers, json=post_data)
        
        print(f"[LINKEDIN] Response Status: {response.status_code}")
        print(f"[LINKEDIN] Response: {response.text}")
        
        if response.status_code == 201:
            print("[LINKEDIN] SUCCESS: Real post published!")
            return True
        else:
            print(f"[LINKEDIN] FAILED: {response.text}")
            return False
            
    except Exception as e:
        print(f"[LINKEDIN] ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Starting LinkedIn Real Post...")
    success = post_to_linkedin_real()
    
    if success:
        print("Real LinkedIn post completed successfully!")
    else:
        print("LinkedIn post failed.")