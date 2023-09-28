#!/bin/sh

until cd /bom-server/
do
    echo "Waiting for server volume..."
done

pwd


until python3 manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done


until python3 manage.py collectstatic --noinput
do 
    echo "Collecting static files..."
    slepp 2
done

# echo '----------------------------------------------------------------------------'
# echo 'test'
# echo '----------------------------------------------------------------------------'
# ls -ltrh /
# echo '----------------------------------------------------------------------------'
# ls -ltrh /static
# echo '----------------------------------------------------------------------------'
# ls -ltrh /SysAssist-backend/
# echo '----------------------------------------------------------------------------'
# ls -ltrh /SysAssist-backend/static
# echo '----------------------------------------------------------------------------'
# ls -ltrh /static/rest_framework/js
# echo '----------------------------------------------------------------------------'


# python3 manage.py createsuperuser --noinput

gunicorn configuration.wsgi --bind 0.0.0.0:8000 
# --workers 1 --threads 1

# for debug
python3 manage.py runserver 0.0.0.0:8000