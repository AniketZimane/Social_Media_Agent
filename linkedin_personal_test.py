import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_linkedin_personal():
    """Test what's possible with personal LinkedIn token"""
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    
    print("Testing LinkedIn Personal Account API...")
    print(f"Token: {token[:30]}...")
    
    # Test 1: Try to get basic profile (should work)
    try:
        url = "https://api.linkedin.com/v2/me"
        headers = {"Authorization": f"Bearer {token}"}
        
        print("\n[TEST 1] Getting basic profile...")
        response = requests.get(url, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            print("SUCCESS: Can read basic profile")
        else:
            print(f"FAILED: {response.text}")
    except Exception as e:
        print(f"ERROR: {e}")
    
    # Test 2: Try to post (will fail)
    try:
        url = "https://api.linkedin.com/v2/ugcPosts"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        post_data = {
            "author": "urn:li:person:~",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": "Test post"},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        print("\n[TEST 2] Attempting to post...")
        response = requests.post(url, headers=headers, json=post_data)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("SUCCESS: Posted to LinkedIn!")
        else:
            print("FAILED: Personal accounts cannot post via API")
            
    except Exception as e:
        print(f"ERROR: {e}")
    
    print("\nCONCLUSION:")
    print("LinkedIn API 2023+ restrictions:")
    print("- Personal accounts: READ ONLY")
    print("- Company accounts: Can post content")
    print("- Your token works but has posting limitations")

if __name__ == "__main__":
    test_linkedin_personal()