import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def send_demo_linkedin_post():
    """Send a demo post to LinkedIn using the updated token"""
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not token:
        print("[LINKEDIN] ERROR: No token found in .env file")
        return False
    
    print(f"[LINKEDIN] Using token: {token[:20]}...")
    print(f"[LINKEDIN] Attempting demo post at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Demo content
    demo_content = {
        "title": "Agentic AI Blog Assistant Demo Post",
        "content": "Testing our AI-powered blog writing assistant with automated social media posting! This system can generate intelligent content and automatically post to multiple platforms. #AI #Automation #BlogWriting #SocialMedia #Innovation",
        "hashtags": ["#AI", "#Automation", "#BlogWriting", "#SocialMedia", "#Innovation"]
    }
    
    try:
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        post_data = {
            "author": "urn:li:person:YOUR_PERSON_ID",  # This needs to be replaced with actual person ID
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": f"{demo_content['title']}\n\n{demo_content['content']}\n\n{' '.join(demo_content['hashtags'])}"
                    },
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        print("[LINKEDIN] Sending POST request...")
        response = requests.post(url, headers=headers, json=post_data)
        
        print(f"[LINKEDIN] Response Status: {response.status_code}")
        print(f"[LINKEDIN] Response: {response.text}")
        
        if response.status_code == 201:
            print("[LINKEDIN] SUCCESS: Demo post published!")
            return True
        else:
            print(f"[LINKEDIN] FAILED: Status {response.status_code}")
            print(f"[LINKEDIN] Error details: {response.text}")
            return False
            
    except Exception as e:
        print(f"[LINKEDIN] ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Starting LinkedIn Demo Post...")
    success = send_demo_linkedin_post()
    
    if success:
        print("\nDemo post completed successfully!")
    else:
        print("\nDemo post failed. Check token and permissions.")