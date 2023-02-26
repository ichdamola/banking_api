#!/bin/bash


echo "installing dependencies..."
pip install -r requirements.txt

echo "Starting up project..."
echo "Vist: http://127.0.0.1:8000/docs/ in your preferred browser."
python manage.py runserver

