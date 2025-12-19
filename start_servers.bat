@echo off
echo Starting Agentic AI Blog Assistant...
echo.

echo 1. Starting Python API Server (Flask)...
start "Python API" cmd /k "cd /d "%~dp0" && python streamlit_api.py"

timeout /t 3 /nobreak >nul

echo 2. Starting React Frontend...
start "React Frontend" cmd /k "cd /d "%~dp0react-ui" && set PORT=3002 && npm start"

echo.
echo ✅ Both servers starting...
echo 📡 Python API: http://localhost:5000
echo 🌐 React Frontend: http://localhost:3002
echo.
pause