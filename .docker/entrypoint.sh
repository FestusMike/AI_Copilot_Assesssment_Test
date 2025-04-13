#!/bin/bash

# Exit script on any error
set -e

echo "Collecting static files..."
python manage.py collectstatic --no-input

echo "Running migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
exec gunicorn -b 0.0.0.0:3000 controller.wsgi:application --reload
