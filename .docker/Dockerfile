# Use the official Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /copilot

# Copy only the requirements first for caching
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . /copilot

# Give execution permission to entrypoint script
RUN chmod +x /copilot/.docker/entrypoint.sh

# Expose the application port
EXPOSE 8000

# Use entrypoint script instead of CMD
ENTRYPOINT ["/copilot/.docker/entrypoint.sh"]
