#!/usr/bin/env python3
"""
Cleanup script to remove unnecessary files and organize the project
"""

import os
import shutil
from pathlib import Path

def cleanup_project():
    """Remove unnecessary files and organize project structure"""
    
    # Files to remove (test files, demos, backups)
    files_to_remove = [
        # Test files
        "test_ai_urls.py",
        "test_api.py", 
        "test_auth_fix.py",
        "test_auth.py",
        "test_db_connection.py",
        "test_fixed_ai.py",
        "test_image_fix.py",
        "test_login.py",
        "test_metadata_agent.py",
        "test_real_ai_images.py",
        "test_streamlit_auth.py",
        
        # Demo files
        "demo_post.py",
        "demo_social_post.py",
        "final_demo.py",
        
        # Simple/Quick test files
        "simple_ai_integration.py",
        "simple_auth_test.py", 
        "simple_image_gen.py",
        "quick_image_fix.py",
        
        # Backup files
        "working_ai_integration_backup.py",
        
        # LinkedIn test files
        "get_linkedin_profile.py",
        "linkedin_personal_test.py",
        "linkedin_real_post.py",
        "linkedin_shares_post.py",
        "linkedin_simple_post.py",
        "linkedin_ugc_post.py",
        "linkedin_v2_post.py",
        
        # Unused integrations
        "ai_integrations.py",
        "aiml_image_generator.py",
        "free_ai_integration.py",
        "replicate_integration.py",
        "langflow_integration.py",
        
        # Unused APIs
        "react_auth_api.py",
        "video_jobs_api.py",
        "social_media_apis.py",
        
        # Unused batch files
        "start_enhanced_app.bat",
        "start_image_api.bat", 
        "start_job_service.bat",
        "start_react_auth.bat",
        
        # Unused services
        "job_application_service.py",
        "scheduled_post_manager.py",
        "social_media_scheduler.py",
        
        # Unused components
        "content_agent.py",
        "content_sources.py",
        "rag_knowledge_base.py",
        "rag_knowledge.py",
        "voice_assistant.py",
        "workflow_diagram.py",
        
        # Extra documentation
        "AUTO_POSTING_SETUP_GUIDE.md",
        "VIDEO_JOBS_README.md"
    ]
    
    print("🧹 Cleaning up project directory...")
    print("=" * 50)
    
    removed_count = 0
    
    for file_name in files_to_remove:
        file_path = Path(file_name)
        if file_path.exists():
            try:
                file_path.unlink()
                print(f"✅ Removed: {file_name}")
                removed_count += 1
            except Exception as e:
                print(f"❌ Failed to remove {file_name}: {e}")
        else:
            print(f"⚠️  Not found: {file_name}")
    
    print(f"\n🎉 Cleanup completed! Removed {removed_count} files.")
    print("\n📁 Remaining core files:")
    
    # List remaining important files
    core_files = [
        "main.py",
        "streamlit_api.py", 
        "google_ai_integration.py",
        "working_ai_integration.py",
        "dynamic_content_generator.py",
        "metadata_agent.py",
        "content_calendar.py",
        "engagement_predictor.py",
        "image_generator.py",
        "social_media_poster.py",
        "auth.py",
        "database.py",
        "test_mongodb.py",
        "file_content_generator.py",
        "requirements.txt",
        "README.md",
        ".env.template",
        ".gitignore"
    ]
    
    for file_name in core_files:
        if Path(file_name).exists():
            print(f"✅ {file_name}")
        else:
            print(f"❌ Missing: {file_name}")
    
    print(f"\n📂 React UI directory: {'✅ Present' if Path('react-ui').exists() else '❌ Missing'}")
    
    print("\n" + "=" * 50)
    print("🚀 Project is now clean and organized!")
    print("📖 Check README.md for setup instructions")

if __name__ == "__main__":
    cleanup_project()