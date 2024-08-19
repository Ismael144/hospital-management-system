#!/usr/bin/bash

APP=$1

# Make migrations
echo "Making Migrations" 
if [ $APP ]; then 
    python manage.py makemigrations $APP
else 
    python manage.py makemigrations 
fi

# Applying the migrations 
echo "Applying the migrations"
python manage.py migrate