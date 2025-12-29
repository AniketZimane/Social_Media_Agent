@echo off
echo 🚀 Starting Agentic AI Blog Assistant with React Authentication...
echo.

echo 📦 Installing React dependencies...
cd react-ui
call npm install
echo.

echo 🔧 Starting React Authentication API (Port 5001)...
start "React Auth API" cmd /k "cd .. && python react_auth_api.py"

echo ⏳ Waiting for API to start...
timeout /t 3 /nobreak > nul

echo 🌐 Starting React Development Server (Port 3000)...
start "React App" cmd /k "npm start"

echo.
echo ✅ Services Started:
echo 🔗 React App: http://localhost:3000
echo 🔗 Auth API: http://localhost:5001
echo 🔗 Streamlit App: streamlit run main.py
echo.
echo 📝 Instructions:
echo 1. React app will open automatically
echo 2. Login/Register or continue as guest
echo 3. Use Streamlit app for advanced features
echo.
pause