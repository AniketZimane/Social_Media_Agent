import os
from pymongo import MongoClient
from datetime import datetime, timedelta
import hashlib
import secrets
from typing import Dict, Optional, List
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.mongo_uri = os.getenv('MONGO_URI', 'mongodb+srv://addeveloper1604_db_user:n6X706WnlprhNCmX@cluster0.q3xu0ul.mongodb.net/?appName=Cluster0')
        self.client = None
        self.db = None
        self.connect()
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client['agentic_ai_blog']
            # Test connection
            self.client.admin.command('ping')
            print("MongoDB connected successfully!")
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            raise
    
    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_session_token(self) -> str:
        """Generate secure session token"""
        return secrets.token_urlsafe(32)
    
    def register_user(self, username: str, email: str, password: str) -> Dict:
        """Register new user"""
        try:
            users = self.db.users
            
            # Check if user exists
            if users.find_one({"$or": [{"username": username}, {"email": email}]}):
                return {"success": False, "message": "User already exists"}
            
            # Create user
            user_data = {
                "username": username,
                "email": email,
                "password": self.hash_password(password),
                "created_at": datetime.now(),
                "last_login": None,
                "is_active": True
            }
            
            result = users.insert_one(user_data)
            return {
                "success": True, 
                "message": "User registered successfully",
                "user_id": str(result.inserted_id)
            }
        except Exception as e:
            return {"success": False, "message": f"Registration failed: {e}"}
    
    def login_user(self, username: str, password: str) -> Dict:
        """Login user and create session"""
        try:
            users = self.db.users
            sessions = self.db.sessions
            
            # Find user
            user = users.find_one({"username": username})
            if not user or user["password"] != self.hash_password(password):
                return {"success": False, "message": "Invalid credentials"}
            
            # Create session
            session_token = self.generate_session_token()
            session_data = {
                "user_id": str(user["_id"]),
                "username": username,
                "session_token": session_token,
                "created_at": datetime.now(),
                "expires_at": datetime.now() + timedelta(days=7),
                "is_active": True
            }
            
            sessions.insert_one(session_data)
            
            # Update last login
            users.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": datetime.now()}}
            )
            
            return {
                "success": True,
                "message": "Login successful",
                "session_token": session_token,
                "user_id": str(user["_id"]),
                "username": username
            }
        except Exception as e:
            return {"success": False, "message": f"Login failed: {e}"}
    
    def validate_session(self, session_token: str) -> Dict:
        """Validate session token"""
        try:
            sessions = self.db.sessions
            
            session = sessions.find_one({
                "session_token": session_token,
                "is_active": True,
                "expires_at": {"$gt": datetime.now()}
            })
            
            if not session:
                return {"success": False, "message": "Invalid or expired session"}
            
            return {
                "success": True,
                "user_id": session["user_id"],
                "username": session["username"]
            }
        except Exception as e:
            return {"success": False, "message": f"Session validation failed: {e}"}
    
    def logout_user(self, session_token: str) -> Dict:
        """Logout user and deactivate session"""
        try:
            sessions = self.db.sessions
            
            result = sessions.update_one(
                {"session_token": session_token},
                {"$set": {"is_active": False}}
            )
            
            if result.modified_count > 0:
                return {"success": True, "message": "Logged out successfully"}
            else:
                return {"success": False, "message": "Session not found"}
        except Exception as e:
            return {"success": False, "message": f"Logout failed: {e}"}
    
    def save_blog_session(self, user_id: str, session_data: Dict) -> Dict:
        """Save blog generation session"""
        try:
            blog_sessions = self.db.blog_sessions
            
            session_record = {
                "user_id": user_id,
                "topic": session_data.get("topic"),
                "platform": session_data.get("platform"),
                "content_focus": session_data.get("content_focus"),
                "generated_topics": session_data.get("generated_topics", []),
                "blog_content": session_data.get("blog_content"),
                "engagement_scores": session_data.get("engagement_scores", {}),
                "created_at": datetime.now()
            }
            
            result = blog_sessions.insert_one(session_record)
            return {
                "success": True,
                "message": "Session saved",
                "session_id": str(result.inserted_id)
            }
        except Exception as e:
            return {"success": False, "message": f"Failed to save session: {e}"}
    
    def get_user_sessions(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get user's previous blog sessions"""
        try:
            blog_sessions = self.db.blog_sessions
            
            sessions = list(blog_sessions.find(
                {"user_id": user_id}
            ).sort("created_at", -1).limit(limit))
            
            # Convert ObjectId to string
            for session in sessions:
                session["_id"] = str(session["_id"])
            
            return sessions
        except Exception as e:
            print(f"Error getting user sessions: {e}")
            return []
    
    def save_posting_history(self, user_id: str, post_data: Dict) -> Dict:
        """Save social media posting history"""
        try:
            posting_history = self.db.posting_history
            
            post_record = {
                "user_id": user_id,
                "title": post_data.get("title"),
                "platforms": post_data.get("platforms", []),
                "scheduled_time": post_data.get("scheduled_time"),
                "status": post_data.get("status", "scheduled"),
                "results": post_data.get("results", []),
                "created_at": datetime.now(),
                "posted_at": post_data.get("posted_at")
            }
            
            result = posting_history.insert_one(post_record)
            return {
                "success": True,
                "message": "Post history saved",
                "post_id": str(result.inserted_id)
            }
        except Exception as e:
            return {"success": False, "message": f"Failed to save post history: {e}"}
    
    def get_user_posting_history(self, user_id: str, limit: int = 20) -> List[Dict]:
        """Get user's posting history"""
        try:
            posting_history = self.db.posting_history
            
            posts = list(posting_history.find(
                {"user_id": user_id}
            ).sort("created_at", -1).limit(limit))
            
            # Convert ObjectId to string
            for post in posts:
                post["_id"] = str(post["_id"])
            
            return posts
        except Exception as e:
            print(f"Error getting posting history: {e}")
            return []
    
    def get_user_analytics(self, user_id: str) -> Dict:
        """Get user analytics data"""
        try:
            blog_sessions = self.db.blog_sessions
            posting_history = self.db.posting_history
            
            # Count sessions and posts
            total_sessions = blog_sessions.count_documents({"user_id": user_id})
            total_posts = posting_history.count_documents({"user_id": user_id})
            successful_posts = posting_history.count_documents({
                "user_id": user_id, 
                "status": "posted"
            })
            
            # Get recent activity
            recent_sessions = list(blog_sessions.find(
                {"user_id": user_id}
            ).sort("created_at", -1).limit(5))
            
            return {
                "total_sessions": total_sessions,
                "total_posts": total_posts,
                "successful_posts": successful_posts,
                "success_rate": (successful_posts / total_posts * 100) if total_posts > 0 else 0,
                "recent_sessions": len(recent_sessions)
            }
        except Exception as e:
            print(f"Error getting analytics: {e}")
            return {
                "total_sessions": 0,
                "total_posts": 0,
                "successful_posts": 0,
                "success_rate": 0,
                "recent_sessions": 0
            }

# Global database instance
db_manager = DatabaseManager()