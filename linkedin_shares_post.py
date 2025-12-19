import os
import requests
from dotenv import load_dotenv

load_dotenv()

def post_linkedin_shares():
    """Post using LinkedIn Shares API which might work with just w_member_social"""
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    try:
        # Try shares API endpoint
        url = "https://api.linkedin.com/v2/shares"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        # Simple share post
        post_data = {
            "content": {
                "contentEntities": [],
                "title": "AI Blog Assistant Demo"
            },
            "distribution": {
                "linkedInDistributionTarget": {}
            },
            "owner": "urn:li:person:~",  # Use ~ for current user
            "subject": "Testing AI-powered blog writing assistant!",
            "text": {
                "text": "🤖 Testing our AI-powered blog writing assistant with automated social media posting! This system generates intelligent content and posts to multiple platforms automatically. #AI #Automation #BlogWriting #SocialMedia #Innovation"
            }
        }
        
        print("[LINKEDIN] Attempting post with Shares API...")
        print(f"[LINKEDIN] Using token: {token[:30]}...")
        
        response = requests.post(url, headers=headers, json=post_data)
        
        print(f"[LINKEDIN] Response Status: {response.status_code}")
        print(f"[LINKEDIN] Response Body: {response.text}")
        
        if response.status_code in [200, 201]:
            print("[LINKEDIN] SUCCESS: Post published via Shares API!")
            return True
        else:
            print(f"[LINKEDIN] FAILED: Status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"[LINKEDIN] ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Testing LinkedIn Shares API...")
    success = post_linkedin_shares()
    
    if success:
        print("LinkedIn Shares post successful!")
    else:
        print("LinkedIn Shares post failed.")