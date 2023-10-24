# Use an official Python runtime as a parent image
FROM python:latest

# Install Node.js and npm
RUN apt-get update && \
    apt-get install -y nodejs npm

# Set working directory
WORKDIR /app

# Install Bootstrap, Popper.js via npm
RUN npm install bootstrap@5 popper.js 

# Create static assets directory
RUN mkdir -p static/css && mkdir -p static/js 

# Copy the necessary files to static folder
RUN cp node_modules/bootstrap/dist/css/bootstrap.min.css static/css/ && \
    cp node_modules/bootstrap/dist/js/bootstrap.bundle.min.js static/js/ 

# Cleanup
RUN apt-get remove -y nodejs npm && \
    apt-get autoremove -y && \
    apt-get clean

# Install necessary Python packages
RUN pip install --no-cache-dir Flask docker

# Copy application files
COPY ./app/ /app/

# The command to run the application
CMD ["python", "app.py"]
