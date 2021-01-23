# Official Python image from the Docker Hub
FROM python:3.8.6

# Prevent __pycache__/ file
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
    && apt-get install -y netcat apt-utils

COPY requirements.txt $APP_HOME
RUN pip install --upgrade pip
RUN pip install -r requirements.txt    

RUN useradd --user-group --create-home --no-log-init --shell /bin/bash seekwind
ENV APP_HOME=/home/seekwind/ironwind

# Create the staticfiles directory. This avoids permission errors. 
RUN mkdir -p $APP_HOME/static

# Change the workdir.
WORKDIR $APP_HOME
    
COPY . $APP_HOME
RUN chown -R seekwind:seekwind $APP_HOME   

USER seekwind:seekwind

ENTRYPOINT ["/home/seekwind/ironwind/entrypoint.sh"]
