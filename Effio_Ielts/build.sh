#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

echo "==> Installing dependencies..."
pip install -r requirements.txt

echo "==> Collecting static files..."
python manage.py collectstatic --no-input --verbosity=2

echo "==> Running migrations..."
python manage.py migrate

echo "==> Creating superuser (if needed)..."
python manage.py create_superuser

echo "==> Build completed successfully!"