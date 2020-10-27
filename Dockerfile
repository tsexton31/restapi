# Use an offical Python runtime as a parent image
FROM python:3.8-slim

# Set up a working directory in /app
#basically sets up a VM then cd /app in the VM
WORKDIR /app

# Copy your Flask app into the working dir
COPY . /app

# Install any needed Python packages with pip
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 80

#download the image before building the container 
RUN docker pull bitnami/redis

#allow for the use of an empty password
RUN docker run --name redis_cont    \
    -e ALLOW_EMPTY_PASSWORD=yes \
    bitnami/redis:latest
    
#Bind the redis port when running docker (port was originally 6379:6379)
RUN docker run -p 5000:5000 –name redis_cont -d redis

#bind a local volume for persistent redis data (port originally 6379:6379)
RUN docker run -p 6379:6379 -d                  \
    -v $PWD/redis-data:/bitnami/redis/data  \
    --name redis_cont                       \
    bitnami/redis:latest # <-- Redis image

#Start redis server.
RUN redis-cli 

#to confirm it is running
#RUN redis-cli ping

#If the previous docker run command returns an invalid reference format error, try removing the -name tag or use the redis:latest command to pull from the latest image
#RUN docker run -p 6379:6379/tcp -d redis:latest
#Idk if the last 2 are needed but i put them just in case



# Run app.py when the container launches
CMD ["python3", "app.py"]


#command to use this file as insturctions
#tag is the name


#docker build flask-app
#docker run -p 8080:5000 flask.app

