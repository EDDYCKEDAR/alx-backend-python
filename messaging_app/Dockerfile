# Use official Python base image
FROM python:3.10

# Set working directory in container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose default Django port
EXPOSE 8000

# Run the app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "-p"]
