import os
import requests
from dotenv import load_dotenv

load_dotenv()

def get_linkedin_profile():
    """Get LinkedIn profile information to get the person ID"""
    
    token = os.getenv("LINKEDIN_ACCESS_TOKEN")
    if not token:
        print("[LINKEDIN] ERROR: No token found")
        return None
    
    try:
        # Get profile info
        url = "https://api.linkedin.com/v2/people/~"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        print("[LINKEDIN] Getting profile information...")
        response = requests.get(url, headers=headers)
        
        print(f"[LINKEDIN] Response Status: {response.status_code}")
        
        if response.status_code == 200:
            profile_data = response.json()
            print(f"[LINKEDIN] Profile data: {profile_data}")
            
            # Extract person ID
            person_id = profile_data.get('id')
            if person_id:
                print(f"[LINKEDIN] Person ID: {person_id}")
                return person_id
            else:
                print("[LINKEDIN] No person ID found in response")
                return None
        else:
            print(f"[LINKEDIN] Failed to get profile: {response.text}")
            return None
            
    except Exception as e:
        print(f"[LINKEDIN] ERROR: {e}")
        return None

if __name__ == "__main__":
    get_linkedin_profile()