@echo off
echo 🚀 Setting up Agentic AI Blog Assistant with MongoDB...
echo.

echo 📦 Installing Python dependencies...
pip install pymongo
pip install -r requirements.txt

echo.
echo ✅ MongoDB integration setup complete!
echo.
echo 🔧 Configuration:
echo - MongoDB URI is already configured in .env file
echo - Database: agentic_ai_blog
echo - Collections: users, sessions, blog_sessions, posting_history
echo.
echo 🚀 To start the application:
echo streamlit run main.py
echo.
pause