#!/usr/bin/bash 

VIRTUAL_ENV_NAME="hms_venv"

OS_TYPE=$(uname)

# Creating the Virtual environment
echo "Creating Environment"

if [ ${1,,} ]; then 
    VIRTUAL_ENV_NAME=$1
    python -m venv $VIRTUAL_ENV_NAME
    VIRTUAL_ENV_NAME=$1 
else 
    python -m venv "hms_venv"
    VIRTUAL_ENV_NAME="hms_venv" 
fi

# Activating the virtual env
echo "Activating Virtual Env"

if [[ "$OS_TYPE" == "Linux"* || "$OS_TYPE" == "Darwin"* ]]; then
    source $VIRTUAL_ENV_NAME/bin/activate
elif [[ "$os_type" == "Darwin" ]]; then
    .\$VIRTUAL_ENV_NAME\Scripts\Activate
fi

# Install requirements 
if [ -f "../requirements.txt" ]; then
    echo "Installing requirements"
    pip install -r "requirements.txt"
fi 