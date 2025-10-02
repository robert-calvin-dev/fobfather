@echo off
REM Install dependencies for FobFather backend

pip3 install -r requirements.txt

echo Set environment variables:
echo set ACCOUNT_SID=your_twilio_sid
echo set AUTH_TOKEN=your_twilio_auth_token
echo set TWILIO_PHONE=+1234567890
echo set FLASK_ENV=development

echo Done.
pause
