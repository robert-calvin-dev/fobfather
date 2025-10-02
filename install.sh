#!/bin/bash
# Install dependencies for FobFather backend

echo "Installing Python3 packages..."
pip3 install -r requirements.txt

echo "Set environment variables in your shell or .env file:"
echo "export ACCOUNT_SID='your_twilio_sid'"
echo "export AUTH_TOKEN='your_twilio_auth_token'"
echo "export TWILIO_PHONE='+1234567890'"
echo "export FLASK_ENV='development'"

echo "Done."
