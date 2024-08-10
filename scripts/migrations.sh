#!/usr/bin/bash

# Make migrations
echo "Making Migrations" 
python manage.py makemigrations 

# Applying the migrations 
echo "Applying the migrations"
python manage.py migrate