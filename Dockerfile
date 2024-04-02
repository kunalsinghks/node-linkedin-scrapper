# Use the official Python image as base
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update \
    && apt-get install -y wget gnupg \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Chrome WebDriver using WebDriver Manager
RUN pip install --no-cache-dir selenium webdriver-manager

# Set the working directory in the container
WORKDIR /main

# Copy the local code to the container image
COPY . .

# Run the Python script when the container launches
CMD ["python", "main.py"]
