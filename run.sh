# #!/usr/bin/bash

if [ $1=="waitress" ]; then
    ./scripts/celery_tasks.sh && ./server.sh $1
else 
    ./scripts/celery_tasks.sh && ./server.sh
fi 