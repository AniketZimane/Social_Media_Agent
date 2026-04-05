#!/usr/bin/env python3
"""
Comprehensive cleanup script to remove unnecessary files
Main file: streamlit_api.py (Flask API server)
"""

import os
import shutil
from pathlib import Path

def cleanup_project():
    """Remove all unnecessary files and keep only essential ones"""
    
    print("🧹 COMPREHENSIVE PROJECT CLEANUP")
    print("=" * 50)
    print("Main file: streamlit_api.py (Flask API server)")
    print("Removing all unnecessary files...")
    print()
    
    # Files to KEEP (essential files only)
    essential_files = {
        # Core API and functionality
        "streamlit_api.py",           # Main Flask API server
        "google_ai_integration.py",   # Google AI integration
        "working_ai_integration.py",  # Backup AI integration
        "dynamic_content_generator.py", # Content generation
        "blockchain_integration.py",  # Blockchain functionality
        
        # AI Agents
        "metadata_agent.py",          # Hashtags & SEO
        "content_calendar.py",        # Scheduling
        "engagement_predictor.py",    # Analytics
        "image_generator.py",         # Image generation
        "social_media_poster.py",     # Publishing
        
        # Database and Auth
        "auth.py",                    # Authentication
        "database.py",                # MongoDB operations
        "test_mongodb.py",            # Database testing (keep for setup)
        
        # Configuration and Documentation
        "requirements.txt",           # Dependencies
        "README.md",                  # Main documentation
        ".env.template",              # Environment template
        ".gitignore",                 # Git ignore rules
        "BLOCKCHAIN_SETUP_GUIDE.md",  # Blockchain setup
        "SOCIAL_MEDIA_TOKEN_GUIDE.md", # Social media setup
        "AI_ARCHITECTURE_DOCUMENTATION.md", # AI documentation
        
        # Batch files (essential)
        "start_servers.bat",          # Main startup script
    }
    
    # Get all files in current directory
    all_files = [f for f in os.listdir('.') if os.path.isfile(f)]
    
    # Files to remove
    files_to_remove = [f for f in all_files if f not in essential_files]
    
    removed_count = 0
    kept_count = 0
    
    print("🗑️  REMOVING UNNECESSARY FILES:")
    print("-" * 30)
    
    for file_name in files_to_remove:
        try:
            os.remove(file_name)
            print(f"❌ Removed: {file_name}")
            removed_count += 1
        except Exception as e:
            print(f"⚠️  Failed to remove {file_name}: {e}")
    
    print(f"\n✅ KEEPING ESSENTIAL FILES:")
    print("-" * 30)
    
    for file_name in essential_files:
        if os.path.exists(file_name):
            print(f"✅ Kept: {file_name}")
            kept_count += 1
        else:
            print(f"⚠️  Missing: {file_name}")
    
    # Check directories
    print(f"\n📁 DIRECTORIES:")
    print("-" * 30)
    
    directories = ['react-ui', 'contracts']
    for dir_name in directories:
        if os.path.exists(dir_name):
            print(f"✅ Directory: {dir_name}/")
        else:
            print(f"❌ Missing: {dir_name}/")
    
    print(f"\n📊 CLEANUP SUMMARY:")
    print("=" * 50)
    print(f"🗑️  Files removed: {removed_count}")
    print(f"✅ Files kept: {kept_count}")
    print(f"📁 Directories: {len([d for d in directories if os.path.exists(d)])}")
    
    print(f"\n🚀 PROJECT STRUCTURE (CLEAN):")
    print("=" * 50)
    print("""
agentic-ai-project/
├── 🎯 Main Application
│   └── streamlit_api.py           # Flask API server (MAIN FILE)
│
├── 🤖 AI Components
│   ├── google_ai_integration.py   # Google Gemini AI
│   ├── working_ai_integration.py  # Backup AI
│   ├── dynamic_content_generator.py # Content engine
│   ├── metadata_agent.py          # Hashtags & SEO
│   ├── content_calendar.py        # Scheduling
│   ├── engagement_predictor.py    # Analytics
│   └── image_generator.py         # Image generation
│
├── 🔗 Blockchain & Social
│   ├── blockchain_integration.py  # Web3 integration
│   └── social_media_poster.py     # Publishing
│
├── 🔐 Database & Auth
│   ├── auth.py                    # Authentication
│   ├── database.py               # MongoDB
│   └── test_mongodb.py           # DB testing
│
├── ⚛️ Frontend
│   └── react-ui/                 # React application
│
├── 🏗️ Smart Contracts
│   └── contracts/                # Solidity contracts
│
├── 📚 Documentation
│   ├── README.md                 # Main docs
│   ├── AI_ARCHITECTURE_DOCUMENTATION.md
│   ├── BLOCKCHAIN_SETUP_GUIDE.md
│   └── SOCIAL_MEDIA_TOKEN_GUIDE.md
│
└── ⚙️ Configuration
    ├── requirements.txt          # Dependencies
    ├── .env.template            # Environment template
    ├── .gitignore              # Git ignore
    └── start_servers.bat       # Startup script
    """)
    
    print(f"\n🎯 HOW TO RUN:")
    print("=" * 50)
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Setup environment: cp .env.template .env")
    print("3. Start application: python streamlit_api.py")
    print("4. Or use batch file: start_servers.bat")
    
    print(f"\n✨ PROJECT IS NOW CLEAN AND OPTIMIZED!")
    print("Main entry point: streamlit_api.py")

if __name__ == "__main__":
    # Confirm before cleanup
    response = input("⚠️  This will remove many files. Continue? (y/N): ")
    if response.lower() in ['y', 'yes']:
        cleanup_project()
    else:
        print("Cleanup cancelled.")