#!/usr/bin/env python3
"""
FobFather Flask backend
/api/contact endpoint
- Validates input
- Sends SMS via Twilio or writes to outbox.json if credentials missing
- Returns JSON status
- Basic in-memory rate-limiting (2 min per phone)
"""

import os
import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS

try:
    from twilio.rest import Client
except ImportError:
    Client = None

app = Flask(__name__)
CORS(app, origins=["https://fobfather.ca"])

# Simple in-memory rate limit: {phone: timestamp_last_submission}
RATE_LIMIT = {}
RATE_LIMIT_SECONDS = 120  # 2 minutes

OUTBOX_FILE = 'outbox.json'
TWILIO_ACCOUNT_SID = os.environ.get('ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
TWILIO_PHONE = os.environ.get('TWILIO_PHONE')

def rate_limited(phone):
    now = time.time()
    last = RATE_LIMIT.get(phone, 0)
    if now - last < RATE_LIMIT_SECONDS:
        return True
    RATE_LIMIT[phone] = now
    return False

def send_twilio_sms(to, body):
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE]) or Client is None:
        # Fallback: write to outbox.json
        payload = {'to': to, 'body': body, 'timestamp': int(time.time())}
        try:
            if os.path.exists(OUTBOX_FILE):
                with open(OUTBOX_FILE, 'r') as f:
                    outbox = json.load(f)
            else:
                outbox = []
        except json.JSONDecodeError:
            outbox = []
        outbox.append(payload)
        with open(OUTBOX_FILE, 'w') as f:
            json.dump(outbox, f, indent=2)
        return 'fallback'
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(body=body, from_=TWILIO_PHONE, to=to)
    return message.sid

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Invalid JSON'}), 400

    name = data.get('name', '').strip() or 'Anonymous'
    phone = data.get('phone', '').strip()
    message_text = data.get('message', '').strip()
    preferred = data.get('preferred', '').strip()
    email = data.get('email', '').strip()

    if not phone or len(''.join(filter(str.isdigit, phone))) != 10:
        return jsonify({'message': 'Valid 10-digit phone required'}), 400

    if rate_limited(phone):
        return jsonify({'message': 'Please wait before sending another message'}), 429

    sms_body = f"FobFather Contact\nName: {name}\nPhone: {phone}\nMsg: {message_text[:80]}\nPreferred: {preferred}"

    try:
        result = send_twilio_sms(TWILIO_PHONE, sms_body)
        # Send confirmation to customer if phone provided
        if Client and TWILIO_PHONE and phone:
            conf_msg = "Thanks — we received your message. We’ll contact you within business hours to confirm. — FobFather"
            send_twilio_sms(phone, conf_msg)
        return jsonify({'message': 'Message sent successfully', 'result': result}), 200
    except Exception as e:
        return jsonify({'message': f'Failed to send message: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
