#!/bin/bash

# Export necessary environment variables
export FLASK_APP=app.py
export FLASK_ENV=production
export PYTHONPATH=$(pwd)

# Run any database migrations or setup tasks if necessary
# flask db upgrade

# Start the Flask application
flask run --host=0.0.0.0 --port=${PORT:-5000}
