import os
import requests
from dotenv import load_dotenv

load_dotenv()

def simple_linkedin_post():
    """Simple LinkedIn post using current API"""
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    # Try posting with minimal data
    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Minimal post structure
    post_data = {
        "author": "urn:li:member:~",
        "lifecycleState": "PUBLISHED", 
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": "Testing AI blog assistant! #AI #BlogWriting"
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    print("[LINKEDIN] Attempting simple post...")
    response = requests.post(url, headers=headers, json=post_data)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    return response.status_code == 201

if __name__ == "__main__":
    simple_linkedin_post()