
# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Try installing git
RUN apt-get -y update
RUN apt-get -y install git

# Set environment variables
# ENV FLASK_APP flaskr
# ENV HOST 0.0.0.0

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
