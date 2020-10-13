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
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "app.py"]


#command to use this file as insturctions
#tag is the name


#docker build flask-app
#docker run -p 8080:5000 flask.app

