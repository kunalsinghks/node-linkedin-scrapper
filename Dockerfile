ARG PORT=443
FROM cypress/browser:latest

# Install Python 3
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Print Python user base
RUN echo $(python3 -m site --user-base)

# Set PATH for Python
ENV PATH /root/.local/bin:${PATH}

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip3 install --user -r requirements.txt

# Copy the application code
COPY . .

# Command to run the application
CMD uvicorn main:app --host 0.0.0.0 --port $PORT
