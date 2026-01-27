@echo off
echo Installing dependencies...
pip install -r web_requirements.txt

echo.
echo Starting Web Task Management Chatbot...
echo Visit http://localhost:5001 in your browser
echo.
python start_web_chatbot.py
pause