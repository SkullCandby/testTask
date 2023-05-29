# pull the official base image
FROM python:3.8

# set working directory in the container
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

# copy the project
COPY . /app/
