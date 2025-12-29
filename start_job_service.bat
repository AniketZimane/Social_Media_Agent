@echo off
echo Starting Job Application Email Service...

cd /d "d:\Code\Innovative_things\agentic ai project"

echo Installing required packages...
pip install flask flask-cors

echo Starting email service on port 5001...
python job_application_service.py

pause