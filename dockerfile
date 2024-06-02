# Use an official Python runtime as a parent image
FROM python:3.7.9-slim

# Set the working directory in the container
WORKDIR /app

VOLUME /app/mlruns

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV ENV MLFLOW_TRACKING_URI=http://localhost:5000

# Copy and give execution rights to your start-up script
RUN chmod +x /app/start.sh

# Run your start-up script
CMD ["/app/start.sh"]
