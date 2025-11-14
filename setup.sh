#!/bin/bash

# Install gunicorn if needed
pip install gunicorn

# Run your Flask app with gunicorn
exec gunicorn app:app --workers 3 --bind 0.0.0.0:$PORT --timeout 120

