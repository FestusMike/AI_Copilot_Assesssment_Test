#!/bin/bash

# Exit script on any error
set -e

echo "Running migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
exec gunicorn -b 0.0.0.0:8000 controller.wsgi:application --reload
