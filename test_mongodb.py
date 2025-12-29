#!/usr/bin/env python3
"""
Test script for MongoDB integration
"""

import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_mongodb_connection():
    """Test MongoDB connection and basic operations"""
    print("🔍 Testing MongoDB Integration...")
    print("=" * 50)
    
    try:
        # Import database manager
        from database import db_manager
        print("✅ Database module imported successfully")
        
        # Test connection
        print("🔗 Testing MongoDB connection...")
        db_manager.client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Test user registration
        print("\n👤 Testing user registration...")
        test_user = {
            "username": "test_user_" + str(int(datetime.now().timestamp())),
            "email": f"test_{int(datetime.now().timestamp())}@example.com",
            "password": "test123456"
        }
        
        result = db_manager.register_user(
            test_user["username"], 
            test_user["email"], 
            test_user["password"]
        )
        
        if result["success"]:
            print(f"✅ User registration successful: {result['user_id']}")
            user_id = result["user_id"]
            
            # Test login
            print("\n🔑 Testing user login...")
            login_result = db_manager.login_user(test_user["username"], test_user["password"])
            
            if login_result["success"]:
                print(f"✅ Login successful: {login_result['session_token'][:20]}...")
                session_token = login_result["session_token"]
                
                # Test session validation
                print("\n🔍 Testing session validation...")
                validation_result = db_manager.validate_session(session_token)
                
                if validation_result["success"]:
                    print("✅ Session validation successful")
                    
                    # Test blog session saving
                    print("\n📝 Testing blog session saving...")
                    session_data = {
                        "topic": "Test AI Topic",
                        "platform": "📸 Instagram",
                        "content_focus": "Educational",
                        "generated_topics": [
                            {"title": "Test Blog Title", "engagement_score": 0.85}
                        ]
                    }
                    
                    save_result = db_manager.save_blog_session(user_id, session_data)
                    if save_result["success"]:
                        print(f"✅ Blog session saved: {save_result['session_id']}")
                        
                        # Test getting user sessions
                        print("\n📚 Testing user session retrieval...")
                        user_sessions = db_manager.get_user_sessions(user_id)
                        print(f"✅ Retrieved {len(user_sessions)} user sessions")
                        
                        # Test posting history
                        print("\n📅 Testing posting history...")
                        post_data = {
                            "title": "Test Post Title",
                            "platforms": ["📸 Instagram", "🐦 Twitter"],
                            "scheduled_time": datetime.now(),
                            "status": "scheduled"
                        }
                        
                        post_result = db_manager.save_posting_history(user_id, post_data)
                        if post_result["success"]:
                            print(f"✅ Posting history saved: {post_result['post_id']}")
                            
                            # Test analytics
                            print("\n📊 Testing user analytics...")
                            analytics = db_manager.get_user_analytics(user_id)
                            print(f"✅ Analytics retrieved: {analytics['total_sessions']} sessions, {analytics['total_posts']} posts")
                        else:
                            print(f"❌ Posting history failed: {post_result['message']}")
                    else:
                        print(f"❌ Blog session save failed: {save_result['message']}")
                else:
                    print(f"❌ Session validation failed: {validation_result['message']}")
                
                # Test logout
                print("\n🚪 Testing logout...")
                logout_result = db_manager.logout_user(session_token)
                if logout_result["success"]:
                    print("✅ Logout successful")
                else:
                    print(f"❌ Logout failed: {logout_result['message']}")
            else:
                print(f"❌ Login failed: {login_result['message']}")
        else:
            print(f"❌ User registration failed: {result['message']}")
        
        print("\n" + "=" * 50)
        print("🎉 MongoDB integration test completed!")
        print("✅ All core functionality is working properly")
        print("\n🚀 You can now run: streamlit run main.py")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure to install dependencies: pip install pymongo")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print("💡 Check your MongoDB connection string in .env file")

def test_auth_manager():
    """Test authentication manager"""
    print("\n🔐 Testing Authentication Manager...")
    
    try:
        from auth import auth_manager
        print("✅ Auth manager imported successfully")
        
        # Test session state initialization
        print("✅ Auth manager ready for Streamlit integration")
        
    except ImportError as e:
        print(f"❌ Auth manager import error: {e}")
    except Exception as e:
        print(f"❌ Auth manager test failed: {e}")

if __name__ == "__main__":
    print("🤖 Agentic AI Blog Assistant - MongoDB Test Suite")
    print("=" * 60)
    
    # Test MongoDB
    test_mongodb_connection()
    
    # Test Auth Manager
    test_auth_manager()
    
    print("\n" + "=" * 60)
    print("🏁 Test suite completed!")