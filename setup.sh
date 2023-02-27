#!/bin/bash


echo "installing dependencies..."
pip install -r requirements.txt

echo "Running test..."
python manage.py test

echo "Starting the service server..."
echo "Vist: http://127.0.0.1:8000/docs/ in your preferred browser."
python manage.py runserver

