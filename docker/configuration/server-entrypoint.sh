#!/bin/sh

until cd /bom-server/
do
    echo "Waiting for server volume..."
done


# until python3 manage.py makemigrations
# do
#     echo "Waiting for migrations to be ready..."
#     sleep 2
# done

until python3 manage.py migrate --no-input
do
    echo "Waiting for db to be ready..."
    sleep 2
done


until python3 manage.py collectstatic --no-input
do 
    echo "Collecting static files..."
    sleep 2
done

ls -ltrh staticfiles


# python3 manage.py createsuperuser --noinput

gunicorn configuration.wsgi:application --bind 0.0.0.0:8000 --workers 1 --threads 1

# for debug
# python3 manage.py runserver 0.0.0.0:8000