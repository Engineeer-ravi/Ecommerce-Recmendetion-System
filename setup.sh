#!/bin/bash

# Install dependencies (Render uses pip3)
pip3 install gunicorn

# Run Flask app with gunicorn
exec gunicorn app:app --workers 3 --bind 0.0.0.0:$PORT --timeout 120
