FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY app.py job_specs.json requirements.txt ./

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED=1

# Expose port 5000 (Flask listens on 5000)
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]
