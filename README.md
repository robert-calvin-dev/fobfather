# FobFather Backend — Flask + Twilio

## Overview
Minimal backend for FobFather website. Provides `/api/contact` POST endpoint for contact form submission.

Features:
- Validates input
- Rate-limits submissions per phone (2 minutes)
- Sends SMS to business + confirmation to customer
- Fallback to `outbox.json` if Twilio credentials missing
- CORS restricted to `https://fobfather.ca`

## Setup

1. Clone repository / download server folder.
2. Install dependencies:

Linux/macOS:
```bash
bash install.sh
