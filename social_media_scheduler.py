import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

class SocialMediaScheduler:
    def __init__(self):
        self.platforms = {
            "Facebook": {"api_url": "https://graph.facebook.com/v18.0/", "enabled": False},
            "Twitter": {"api_url": "https://api.twitter.com/2/", "enabled": False},
            "LinkedIn": {"api_url": "https://api.linkedin.com/v2/", "enabled": False},
            "Instagram": {"api_url": "https://graph.facebook.com/v18.0/", "enabled": False}
        }
        self.scheduled_posts = []
    
    def connect_platform(self, platform: str, access_token: str) -> bool:
        """Connect social media platform with access token"""
        try:
            if platform == "Facebook":
                # Verify Facebook token
                response = requests.get(f"https://graph.facebook.com/me?access_token={access_token}")
                if response.status_code == 200:
                    self.platforms[platform]["token"] = access_token
                    self.platforms[platform]["enabled"] = True
                    return True
            
            elif platform == "Twitter":
                # Verify Twitter token (Bearer token for API v2)
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.get("https://api.twitter.com/2/users/me", headers=headers)
                if response.status_code == 200:
                    self.platforms[platform]["token"] = access_token
                    self.platforms[platform]["enabled"] = True
                    return True
            
            elif platform == "LinkedIn":
                # Verify LinkedIn token
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.get("https://api.linkedin.com/v2/people/~", headers=headers)
                if response.status_code == 200:
                    self.platforms[platform]["token"] = access_token
                    self.platforms[platform]["enabled"] = True
                    return True
            
            elif platform == "Instagram":
                # Instagram uses Facebook Graph API
                response = requests.get(f"https://graph.facebook.com/me/accounts?access_token={access_token}")
                if response.status_code == 200:
                    self.platforms[platform]["token"] = access_token
                    self.platforms[platform]["enabled"] = True
                    return True
                    
        except Exception as e:
            st.error(f"Error connecting {platform}: {e}")
        
        return False
    
    def schedule_post(self, content: Dict, platforms: List[str], schedule_date: datetime) -> Dict:
        """Schedule post for multiple platforms"""
        scheduled_post = {
            "id": len(self.scheduled_posts) + 1,
            "content": content,
            "platforms": platforms,
            "schedule_date": schedule_date,
            "status": "scheduled",
            "created_at": datetime.now()
        }
        
        self.scheduled_posts.append(scheduled_post)
        return scheduled_post
    
    def post_to_facebook(self, content: Dict, token: str) -> Dict:
        """Post to Facebook"""
        try:
            print(f"[FACEBOOK] Attempting to post: {content['title'][:50]}...")
            url = f"https://graph.facebook.com/me/feed"
            
            post_data = {
                "message": f"{content['title']}\n\n{content['content'][:500]}...\n\n{' '.join(content['hashtags'][:10])}",
                "access_token": token
            }
            
            response = requests.post(url, data=post_data)
            if response.status_code == 200:
                print(f"[FACEBOOK] ✅ SUCCESS: Post published")
                return {"success": True, "post_id": response.json().get('id', 'unknown'), "message": "Posted successfully"}
            else:
                print(f"[FACEBOOK] ❌ FAILED: Status {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}", "message": "Failed to post"}
            
        except Exception as e:
            print(f"[FACEBOOK] ❌ ERROR: {e}")
            return {"success": False, "error": str(e), "message": "Connection error"}
    
    def post_to_twitter(self, content: Dict, token: str) -> Dict:
        """Post to Twitter"""
        try:
            print(f"[TWITTER] Attempting to post: {content['title'][:50]}...")
            url = "https://api.twitter.com/2/tweets"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            tweet_text = f"{content['title']}\n\n{' '.join(content['hashtags'][:5])}"
            if len(tweet_text) > 280:
                tweet_text = tweet_text[:277] + "..."
            
            data = {"text": tweet_text}
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 201:
                print(f"[TWITTER] ✅ SUCCESS: Tweet published")
                return {"success": True, "post_id": response.json().get('data', {}).get('id', 'unknown'), "message": "Tweeted successfully"}
            else:
                print(f"[TWITTER] ❌ FAILED: Status {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}", "message": "Failed to tweet"}
            
        except Exception as e:
            print(f"[TWITTER] ❌ ERROR: {e}")
            return {"success": False, "error": str(e), "message": "Connection error"}
    
    def post_to_linkedin(self, content: Dict, token: str) -> Dict:
        """Post to LinkedIn"""
        try:
            print(f"[LINKEDIN] Attempting to post: {content['title'][:50]}...")
            url = "https://api.linkedin.com/v2/ugcPosts"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            
            post_data = {
                "author": "urn:li:person:YOUR_PERSON_ID",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": f"{content['title']}\n\n{content['content'][:1000]}...\n\n{' '.join(content['hashtags'][:5])}"
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(url, headers=headers, json=post_data)
            if response.status_code == 201:
                print(f"[LINKEDIN] ✅ SUCCESS: Post published")
                return {"success": True, "post_id": response.json().get('id', 'unknown'), "message": "Posted to LinkedIn"}
            else:
                print(f"[LINKEDIN] ❌ FAILED: Status {response.status_code}")
                return {"success": False, "error": f"HTTP {response.status_code}", "message": "Failed to post"}
            
        except Exception as e:
            print(f"[LINKEDIN] ❌ ERROR: {e}")
            return {"success": False, "error": str(e), "message": "Connection error"}
    
    def post_to_instagram(self, content: Dict, token: str) -> Dict:
        """Post to Instagram (requires image)"""
        try:
            print(f"[INSTAGRAM] Simulating post: {content['title'][:50]}...")
            # Instagram requires media - simulating for now
            print(f"[INSTAGRAM] ⚠️ SIMULATED: Image upload required")
            return {"success": True, "post_id": "simulated_ig_post", "message": "Simulated (needs image)"}
            
        except Exception as e:
            print(f"[INSTAGRAM] ❌ ERROR: {e}")
            return {"success": False, "error": str(e), "message": "Connection error"}
    
    def execute_scheduled_posts(self):
        """Execute posts that are due"""
        current_time = datetime.now()
        print(f"\n[SCHEDULER] Checking scheduled posts at {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        for post in self.scheduled_posts:
            if post["status"] == "scheduled" and post["schedule_date"] <= current_time:
                print(f"[SCHEDULER] Executing post ID {post['id']}: {post['content']['title'][:50]}...")
                success_count = 0
                post_results = []
                
                for platform in post["platforms"]:
                    platform_name = platform.split()[1] if ' ' in platform else platform
                    
                    if self.platforms.get(platform_name, {}).get("enabled"):
                        token = self.platforms[platform_name]["token"]
                        
                        if platform_name == "Facebook":
                            result = self.post_to_facebook(post["content"], token)
                        elif platform_name == "Twitter":
                            result = self.post_to_twitter(post["content"], token)
                        elif platform_name == "LinkedIn":
                            result = self.post_to_linkedin(post["content"], token)
                        elif platform_name == "Instagram":
                            result = self.post_to_instagram(post["content"], token)
                        
                        post_results.append({"platform": platform_name, **result})
                        if result["success"]:
                            success_count += 1
                
                # Update post status
                post["results"] = post_results
                if success_count > 0:
                    post["status"] = "posted"
                    post["posted_at"] = current_time
                    print(f"[SCHEDULER] ✅ Post {post['id']} completed: {success_count}/{len(post['platforms'])} platforms")
                else:
                    post["status"] = "failed"
                    print(f"[SCHEDULER] ❌ Post {post['id']} failed on all platforms")
    
    def get_platform_status(self) -> Dict:
        """Get connection status of all platforms"""
        return {platform: data["enabled"] for platform, data in self.platforms.items()}
    
    def get_scheduled_posts(self) -> List[Dict]:
        """Get all scheduled posts"""
        return self.scheduled_posts

def show_social_media_scheduler(blog_content: Dict = None):
    """Display social media scheduler interface"""
    
    scheduler = SocialMediaScheduler()
    
    st.header("📅 Social Media Auto-Posting")
    
    # Platform Connection Section
    st.subheader("🔗 Connect Social Media Accounts")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Available Platforms:**")
        
        # Facebook Connection
        if st.checkbox("📘 Facebook"):
            fb_token = st.text_input("Facebook Access Token:", type="password", key="fb_token")
            if st.button("Connect Facebook", key="connect_fb"):
                if scheduler.connect_platform("Facebook", fb_token):
                    st.success("✅ Facebook connected successfully!")
                else:
                    st.error("❌ Failed to connect Facebook")
        
        # Twitter Connection
        if st.checkbox("🐦 Twitter"):
            twitter_token = st.text_input("Twitter Bearer Token:", type="password", key="twitter_token")
            if st.button("Connect Twitter", key="connect_twitter"):
                if scheduler.connect_platform("Twitter", twitter_token):
                    st.success("✅ Twitter connected successfully!")
                else:
                    st.error("❌ Failed to connect Twitter")
    
    with col2:
        # LinkedIn Connection
        if st.checkbox("💼 LinkedIn"):
            linkedin_token = st.text_input("LinkedIn Access Token:", type="password", key="linkedin_token")
            if st.button("Connect LinkedIn", key="connect_linkedin"):
                if scheduler.connect_platform("LinkedIn", linkedin_token):
                    st.success("✅ LinkedIn connected successfully!")
                else:
                    st.error("❌ Failed to connect LinkedIn")
        
        # Instagram Connection
        if st.checkbox("📸 Instagram"):
            instagram_token = st.text_input("Instagram Access Token:", type="password", key="instagram_token")
            if st.button("Connect Instagram", key="connect_instagram"):
                if scheduler.connect_platform("Instagram", instagram_token):
                    st.success("✅ Instagram connected successfully!")
                else:
                    st.error("❌ Failed to connect Instagram")
    
    # Connection Status
    st.subheader("📊 Connection Status")
    status = scheduler.get_platform_status()
    
    status_cols = st.columns(4)
    for i, (platform, connected) in enumerate(status.items()):
        with status_cols[i]:
            status_icon = "🟢" if connected else "🔴"
            st.write(f"{status_icon} {platform}")
    
    # Scheduling Section
    if blog_content:
        st.subheader("📅 Schedule Blog Post")
        
        # Platform Selection
        selected_platforms = st.multiselect(
            "Select platforms to post:",
            [p for p, data in scheduler.platforms.items() if data["enabled"]],
            default=[p for p, data in scheduler.platforms.items() if data["enabled"]]
        )
        
        # Date and Time Selection
        col_date, col_time = st.columns(2)
        
        with col_date:
            schedule_date = st.date_input("Schedule Date:", datetime.now().date())
        
        with col_time:
            schedule_time = st.time_input("Schedule Time:", datetime.now().time())
        
        # Combine date and time
        schedule_datetime = datetime.combine(schedule_date, schedule_time)
        
        # Post Preview
        st.subheader("📝 Post Preview")
        
        preview_platform = st.selectbox("Preview for platform:", selected_platforms if selected_platforms else ["Facebook"])
        
        if preview_platform:
            st.write(f"**{preview_platform} Preview:**")
            
            if preview_platform == "Twitter":
                preview_text = f"{blog_content['title']}\n\n{' '.join(blog_content['hashtags'][:5])}"
                if len(preview_text) > 280:
                    preview_text = preview_text[:277] + "..."
                st.text_area("Tweet Preview:", preview_text, height=100)
            
            elif preview_platform == "LinkedIn":
                preview_text = f"{blog_content['title']}\n\n{blog_content['content'][:500]}...\n\n{' '.join(blog_content['hashtags'][:5])}"
                st.text_area("LinkedIn Preview:", preview_text, height=150)
            
            else:  # Facebook, Instagram
                preview_text = f"{blog_content['title']}\n\n{blog_content['content'][:300]}...\n\n{' '.join(blog_content['hashtags'][:10])}"
                st.text_area("Post Preview:", preview_text, height=150)
        
        # Schedule Button
        if st.button("📅 Schedule Post", type="primary"):
            if selected_platforms:
                scheduled_post = scheduler.schedule_post(blog_content, selected_platforms, schedule_datetime)
                st.success(f"✅ Post scheduled for {schedule_datetime.strftime('%Y-%m-%d %H:%M')} on {', '.join(selected_platforms)}")
                
                # Show scheduled post details
                st.json({
                    "Post ID": scheduled_post["id"],
                    "Platforms": scheduled_post["platforms"],
                    "Schedule Date": scheduled_post["schedule_date"].strftime("%Y-%m-%d %H:%M"),
                    "Status": scheduled_post["status"]
                })
            else:
                st.error("Please select at least one platform")
    
    # Scheduled Posts Management
    st.subheader("📋 Scheduled Posts")
    
    scheduled_posts = scheduler.get_scheduled_posts()
    
    if scheduled_posts:
        for post in scheduled_posts:
            with st.expander(f"Post #{post['id']} - {post['status'].title()}"):
                st.write(f"**Title:** {post['content']['title']}")
                st.write(f"**Platforms:** {', '.join(post['platforms'])}")
                st.write(f"**Scheduled:** {post['schedule_date'].strftime('%Y-%m-%d %H:%M')}")
                st.write(f"**Status:** {post['status']}")
                
                if post['status'] == 'scheduled':
                    if st.button(f"Cancel Post #{post['id']}", key=f"cancel_{post['id']}"):
                        post['status'] = 'cancelled'
                        st.success("Post cancelled")
    else:
        st.info("No scheduled posts yet")
    
    # Auto-execution (in real app, this would run as background service)
    if st.button("🚀 Execute Due Posts Now"):
        scheduler.execute_scheduled_posts()
        st.success("Checked and executed due posts!")

# Instructions for getting API tokens
def show_api_instructions():
    """Show instructions for getting social media API tokens"""
    
    st.subheader("🔑 How to Get API Tokens")
    
    with st.expander("📘 Facebook Access Token"):
        st.write("""
        1. Go to [Facebook Developers](https://developers.facebook.com/)
        2. Create a new app or use existing one
        3. Add Facebook Login product
        4. Generate User Access Token with `pages_manage_posts` permission
        5. For pages: Get Page Access Token from Graph API Explorer
        """)
    
    with st.expander("🐦 Twitter Bearer Token"):
        st.write("""
        1. Apply for [Twitter Developer Account](https://developer.twitter.com/)
        2. Create a new project/app
        3. Generate Bearer Token from Keys and Tokens section
        4. For posting: You'll need OAuth 1.0a tokens (Consumer Key/Secret + Access Token/Secret)
        """)
    
    with st.expander("💼 LinkedIn Access Token"):
        st.write("""
        1. Create app at [LinkedIn Developers](https://www.linkedin.com/developers/)
        2. Request access to LinkedIn Share API
        3. Implement OAuth 2.0 flow to get access token
        4. Ensure you have `w_member_social` permission
        """)
    
    with st.expander("📸 Instagram Access Token"):
        st.write("""
        1. Use Facebook Graph API (Instagram is owned by Facebook)
        2. Create Facebook app with Instagram Basic Display
        3. Get Instagram User Access Token
        4. For business accounts: Use Instagram Graph API
        """)

if __name__ == "__main__":
    show_api_instructions()
    show_social_media_scheduler()