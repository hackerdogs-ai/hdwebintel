# Dockerfile-flask
# We simply inherit the Python 3 image. This image does
# not particularly care what OS runs underneath
#FROM python:3.7.8
FROM ubuntu:latest
LABEL maintainer="Tej Redkar <dynamicdeploy@live.com>"

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
#RUN apt-get install -y python3.7 python3-pip
RUN pip install uwsgi
RUN pip install whois
# Set an environment variable with the directory
# where we'll be running the app
ENV APP /app
# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $APP
WORKDIR $APP
# Expose the port uWSGI will listen on
EXPOSE 5000
# Copy the requirements file in order to install
# Python dependencies
COPY requirements.txt .
#COPY requirements-noversions.txt .
# Install Python dependencies
RUN pip3 install -r requirements.txt
#RUN python3 -m spacy download en
RUN python3 -m spacy download en_core_web_lg
# We copy the rest of the codebase into the image
COPY . .
#WORKDIR ./dnspython
#RUN python3 setup.py install
WORKDIR $APP
RUN apt-get install whois
# https://forums.docker.com/t/unable-to-mount-directory-to-container-mount-destination-not-absolute/110112
#VOLUME APP
# Finally, we run uWSGI with the ini file we
# created earlier
CMD [ "uwsgi", "--ini", "app.ini" ]