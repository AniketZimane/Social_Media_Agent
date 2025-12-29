@echo off
echo ========================================
echo 🚀 Starting Agentic AI Blog Assistant
echo ========================================

echo.
echo 📦 Installing React dependencies...
cd react-ui
call npm install

echo.
echo 🐍 Installing Python dependencies...
cd ..
pip install flask flask-cors requests python-dotenv schedule

echo.
echo 🎬 Starting Video & Jobs API Server...
start "Video Jobs API" cmd /k "python video_jobs_api.py"

echo.
echo 🎨 Starting Image Generation API Server...
start "Image API" cmd /k "python aiml_image_generator.py"

echo.
echo 🕰️ Starting Scheduled Posts Manager...
start "Scheduler API" cmd /k "python scheduled_post_manager.py"

echo.
echo ⚛️ Starting React Development Server...
cd react-ui
start "React App" cmd /k "npm start"

echo.
echo ========================================
echo ✅ All servers started successfully!
echo ========================================
echo.
echo 📺 Video & Jobs API: http://localhost:5001
echo 🎨 Image Generation API: http://localhost:5002
echo 🕰️ Scheduled Posts API: http://localhost:5003
echo ⚛️ React App: http://localhost:3000
echo.
echo 🔑 Configure your API keys in .env file:
echo - AIML_API_KEY for image generation
echo - Social media tokens for auto-posting
echo.
echo Press any key to exit...
pause > nul