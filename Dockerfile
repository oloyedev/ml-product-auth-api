# Use an official Python runtime as a parent image
FROM python:3.9-slim AS base

# Set the working directory in the container
WORKDIR /app

# Install dependencies first, to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download the model weights (replace with your actual URL if needed)
RUN wget -O best.pt https://your-storage-service.com/path/to/your/best.pt

# Copy the rest of the application code
COPY . .

# Final stage
FROM base AS final

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "app.py"]
