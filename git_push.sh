#!/usr/bin/bash

git add .

MESSAGE=$1

if [ MESSAGE ]; then 
    git commit -m "$MESSAGE"
    git push
else 
    echo "Provide a commit message."
fi