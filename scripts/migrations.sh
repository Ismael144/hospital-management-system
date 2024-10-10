#!/usr/bin/bash

APP_NAME=$1

# Make migrations
echo "Making Migrations" 
if [ $APP_NAME ]; then 
    python manage.py makemigrations $APP_NAME
else 
    python manage.py makemigrations 
fi

# Applying the migrations 
echo "Applying the migrations"
python manage.py migrate