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

# ssh
ENV SSH_PASSWD "root:Docker!"
RUN apt-get update \
        && apt-get install -y --no-install-recommends dialog \
        && apt-get update \
 && apt-get install -y --no-install-recommends openssh-server \
 && echo "$SSH_PASSWD" | chpasswd 

COPY sshd_config /etc/ssh/
COPY init.sh /usr/local/bin/	

RUN chmod u+x /usr/local/bin/init.sh

# Specify the command to run on container start
EXPOSE 8000

ENTRYPOINT ["init.sh"]