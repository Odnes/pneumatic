#!/bin/sh

# currently have to manually kill as Ctrl-C interrupts foregrounded only.
./.venv/bin/python3 -m gunicorn -b 127.0.0.1:5001 wsgi_frontend:app &
./.venv/bin/python3 -m gunicorn -b 127.0.0.1:5002 wsgi_admin:app
