#!/bin/sh

cd ./botlog
# python manage.py makemigrations --no-input
python manage.py migrate --no-input

python manage.py collectstatic --no-input

python manage.py superuser_create


python manage.py runserver 0.0.0.0:8000 & python manage.py bot_notify

# exit



