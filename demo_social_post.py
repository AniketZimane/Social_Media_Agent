import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def demo_social_media_post():
    """Demo social media posting with terminal logging"""
    
    print("=" * 60)
    print("AGENTIC AI BLOG ASSISTANT - SOCIAL MEDIA DEMO")
    print("=" * 60)
    
    # Demo content
    demo_content = {
        "title": "AI-Powered Blog Writing Assistant Demo",
        "content": "Testing our intelligent blog writing system with automated social media posting! This AI can generate content and post to multiple platforms automatically.",
        "hashtags": ["#AI", "#BlogWriting", "#Automation", "#SocialMedia", "#Innovation"]
    }
    
    platforms = ["Facebook", "Twitter", "LinkedIn", "Instagram"]
    
    print(f"\n[DEMO] Starting social media posting at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[DEMO] Content: {demo_content['title']}")
    print(f"[DEMO] Platforms: {', '.join(platforms)}")
    print(f"[DEMO] Hashtags: {' '.join(demo_content['hashtags'])}")
    
    print("\n" + "-" * 50)
    print("POSTING RESULTS:")
    print("-" * 50)
    
    # Simulate posting to each platform
    results = []
    
    # Facebook
    print("[FACEBOOK] Attempting to post...")
    print("[FACEBOOK] SUCCESS: Post published to Facebook")
    results.append({"platform": "Facebook", "success": True, "message": "Posted successfully"})
    
    # Twitter  
    print("[TWITTER] Attempting to post...")
    print("[TWITTER] SUCCESS: Tweet published")
    results.append({"platform": "Twitter", "success": True, "message": "Tweeted successfully"})
    
    # LinkedIn
    print("[LINKEDIN] Attempting to post...")
    token = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
    if token:
        print(f"[LINKEDIN] Using token: {token[:20]}...")
        print("[LINKEDIN] FAILED: Insufficient permissions (needs r_liteprofile, w_member_social)")
        results.append({"platform": "LinkedIn", "success": False, "message": "Permission denied"})
    else:
        print("[LINKEDIN] FAILED: No token configured")
        results.append({"platform": "LinkedIn", "success": False, "message": "No token"})
    
    # Instagram
    print("[INSTAGRAM] Attempting to post...")
    print("[INSTAGRAM] SIMULATED: Image upload required")
    results.append({"platform": "Instagram", "success": True, "message": "Simulated (needs image)"})
    
    # Summary
    print("\n" + "=" * 50)
    print("POSTING SUMMARY:")
    print("=" * 50)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"Total platforms: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print(f"Success rate: {len(successful)/len(results)*100:.0f}%")
    
    print("\nDETAILED RESULTS:")
    for result in results:
        status = "SUCCESS" if result["success"] else "FAILED"
        print(f"  {result['platform']}: {status} - {result['message']}")
    
    print(f"\n[DEMO] Completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    return results

if __name__ == "__main__":
    demo_social_media_post()