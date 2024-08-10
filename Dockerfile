FROM python:alpine3.19

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install system dependencies
RUN apt-get update && apt-get install -y \
    python3-venv \
    && apt-get clean

# create and activate a virtual environment
RUN python3 -m venv /app/venv

# set the virtual environment as the default
ENV PATH="/app/venv/bin:$PATH"

# upgrade pip in the virtual environment
RUN pip install --upgrade pip

# install dependencies
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

# copy the application code
COPY . /app

ENTRYPOINT [ "gunicorn", "core.wsgi", "-b", "0.0.0.0:8000" ]
