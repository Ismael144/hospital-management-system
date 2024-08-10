#!/usr/bin/bash

celery -A hms worker --loglevel=info
celery -A hms beat --loglevel=info