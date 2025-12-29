import schedule
import time
import threading
import json
import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

class ScheduledPostManager:
    def __init__(self):
        self.scheduled_posts = []
        self.posts_file = "scheduled_posts.json"
        self.load_scheduled_posts()
        self.start_scheduler()
    
    def load_scheduled_posts(self):
        """Load scheduled posts from file"""
        try:
            if os.path.exists(self.posts_file):
                with open(self.posts_file, 'r', encoding='utf-8') as f:
                    self.scheduled_posts = json.load(f)
                    print(f"✅ Loaded {len(self.scheduled_posts)} scheduled posts")
            else:
                self.scheduled_posts = []
                print("📝 No existing scheduled posts found")
        except Exception as e:
            print(f"❌ Error loading scheduled posts: {e}")
            self.scheduled_posts = []
    
    def save_scheduled_posts(self):
        """Save scheduled posts to file"""
        try:
            with open(self.posts_file, 'w', encoding='utf-8') as f:
                json.dump(self.scheduled_posts, f, indent=2, ensure_ascii=False)
            print(f"💾 Saved {len(self.scheduled_posts)} scheduled posts")
        except Exception as e:
            print(f"❌ Error saving scheduled posts: {e}")
    
    def schedule_post(self, post_data):
        """Schedule a new post"""
        try:
            post_id = f"post_{int(time.time())}"
            
            # Validate required fields
            required_fields = ['content', 'title', 'platforms', 'scheduled_time']
            for field in required_fields:
                if field not in post_data or not post_data[field]:
                    raise ValueError(f"Missing required field: {field}")
            
            scheduled_post = {
                "id": post_id,
                "content": post_data.get("content", ""),
                "title": post_data.get("title", ""),
                "hashtags": post_data.get("hashtags", []),
                "platforms": post_data.get("platforms", []),
                "scheduled_time": post_data.get("scheduled_time", ""),
                "image_url": post_data.get("image_url", ""),
                "status": "scheduled",
                "created_at": datetime.now().isoformat()
            }
            
            self.scheduled_posts.append(scheduled_post)
            self.save_scheduled_posts()
            
            print(f"📅 Scheduled post: {post_id}")
            return post_id
            
        except Exception as e:
            print(f"❌ Error scheduling post: {e}")
            raise e
    
    def get_scheduled_posts(self):
        """Get all scheduled posts"""
        return self.scheduled_posts
    
    def delete_scheduled_post(self, post_id):
        """Delete a scheduled post"""
        self.scheduled_posts = [p for p in self.scheduled_posts if p["id"] != post_id]
        self.save_scheduled_posts()
    
    def post_to_platform(self, post_data, platform):
        """Post content to specific platform (mock implementation)"""
        print(f"🚀 Posting to {platform}:")
        print(f"Title: {post_data['title']}")
        print(f"Content: {post_data['content'][:100]}...")
        print(f"Hashtags: {' '.join(post_data['hashtags'][:5])}")
        
        # Mock API calls - replace with actual platform APIs
        if platform.lower() == "linkedin":
            return self.post_to_linkedin(post_data)
        elif platform.lower() == "twitter":
            return self.post_to_twitter(post_data)
        elif platform.lower() == "facebook":
            return self.post_to_facebook(post_data)
        else:
            return {"success": True, "message": f"Posted to {platform}"}
    
    def post_to_linkedin(self, post_data):
        """Post to LinkedIn (mock implementation)"""
        # Replace with actual LinkedIn API integration
        return {"success": True, "platform": "LinkedIn", "post_id": "linkedin_123"}
    
    def post_to_twitter(self, post_data):
        """Post to Twitter (mock implementation)"""
        # Replace with actual Twitter API integration
        return {"success": True, "platform": "Twitter", "post_id": "twitter_123"}
    
    def post_to_facebook(self, post_data):
        """Post to Facebook (mock implementation)"""
        # Replace with actual Facebook API integration
        return {"success": True, "platform": "Facebook", "post_id": "facebook_123"}
    
    def check_and_post_scheduled(self):
        """Check for posts that need to be published"""
        current_time = datetime.now()
        
        for post in self.scheduled_posts[:]:  # Create a copy to iterate
            if post["status"] == "scheduled":
                scheduled_time = datetime.fromisoformat(post["scheduled_time"])
                
                if current_time >= scheduled_time:
                    print(f"⏰ Time to post: {post['title']}")
                    
                    # Post to all selected platforms
                    results = []
                    for platform in post["platforms"]:
                        try:
                            result = self.post_to_platform(post, platform)
                            results.append(result)
                        except Exception as e:
                            print(f"Error posting to {platform}: {e}")
                            results.append({"success": False, "error": str(e)})
                    
                    # Update post status
                    post["status"] = "posted"
                    post["posted_at"] = current_time.isoformat()
                    post["results"] = results
                    
                    self.save_scheduled_posts()
    
    def start_scheduler(self):
        """Start the background scheduler"""
        def run_scheduler():
            schedule.every(1).minutes.do(self.check_and_post_scheduled)
            
            while True:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
        
        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()
        print("📅 Scheduler started - checking every minute")

# Initialize the scheduler
post_manager = ScheduledPostManager()

# API Endpoints
@app.route('/api/schedule-post', methods=['POST'])
def schedule_post():
    """Schedule a new post"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        required_fields = ['content', 'title', 'platforms', 'scheduled_time']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return jsonify({
                'success': False, 
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        post_id = post_manager.schedule_post(data)
        return jsonify({'success': True, 'post_id': post_id, 'message': 'Post scheduled successfully'})
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/scheduled-posts', methods=['GET'])
def get_scheduled_posts():
    """Get all scheduled posts"""
    posts = post_manager.get_scheduled_posts()
    return jsonify({'success': True, 'posts': posts})

@app.route('/api/scheduled-posts/<post_id>', methods=['DELETE'])
def delete_scheduled_post(post_id):
    """Delete a scheduled post"""
    post_manager.delete_scheduled_post(post_id)
    return jsonify({'success': True, 'message': 'Post deleted'})

@app.route('/api/post-now', methods=['POST'])
def post_now():
    """Post content immediately"""
    data = request.json
    
    results = []
    for platform in data.get('platforms', []):
        try:
            result = post_manager.post_to_platform(data, platform)
            results.append(result)
        except Exception as e:
            results.append({"success": False, "platform": platform, "error": str(e)})
    
    return jsonify({'success': True, 'results': results})

if __name__ == '__main__':
    print("🚀 Starting Scheduled Post Manager on http://localhost:5003")
    print("📅 Auto-posting system is active!")
    app.run(debug=True, port=5003)