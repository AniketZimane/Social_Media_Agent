@echo off
echo ========================================
echo 🎨 Starting AIML Image Generation API
echo ========================================

echo.
echo 🐍 Installing Python dependencies...
pip install requests python-dotenv flask flask-cors

echo.
echo 🔑 Please add your AIML API key to .env file:
echo AIML_API_KEY=api key

echo.
echo 🚀 Starting Image Generation API Server...
python aiml_image_generator.py

pause
