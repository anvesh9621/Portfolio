#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies from portfolio_site/requirements.txt
pip install -r portfolio_site/requirements.txt

# Navigate to the Django project root directory where manage.py is located
cd portfolio_site

# Collect static files and apply database migrations
python manage.py collectstatic --no-input
python manage.py migrate
