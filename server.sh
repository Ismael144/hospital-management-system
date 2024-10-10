#!/usr/bin/bash

USE_WAITRESS="waitress"

./scripts/celery_tasks.sh

if [ $1==$USE_WAITRESS ]; then
    waitress-serve --listen=127.0.0.1:5000 hms:wsgi.application
    # ./scripts/
else
    python manage.py runserver
fi
