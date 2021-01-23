#!/bin/sh

# Make migrations and migrate the database.
echo "Making migrations and migrating the database. "
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py collectstatic --noinput
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', password='admin')" | python3 manage.py shell

daphne -b 0.0.0.0 -p 8000 --proxy-headers IronWind.asgi:application

exec "$@"
