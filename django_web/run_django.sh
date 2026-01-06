#!/bin/env bash

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username ADMIN --noinput --email test@test.pl
python manage.py collectstatic --no-input --clear
gunicorn --bind 0.0.0.0:8000 --workers 3 dam_site.wsgi:application