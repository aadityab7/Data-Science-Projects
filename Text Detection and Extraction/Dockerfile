# syntax=docker/dockerfile:1

# Use an official Python runtime as the base image
FROM python:3.11-slim-buster

# Set the working directory in the container
RUN mkdir /code
WORKDIR /code

# Copy the dependencies file to the working directory
ADD requirements.txt /code/

# Install Flask and other dependencies
RUN pip install -r requirements.txt --no-cache-dir

# Copy the content of the local directory to the working directory
ADD . /code/

# Specify the command to run on container start
EXPOSE 8000 2222
#CMD ["python", "/code/app.py", "runserver", "0.0.0.0:8000"]