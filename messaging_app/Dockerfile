# Use Python base image
FROM python:3.10

# Set work directory
WORKDIR /app

# Copy requirements to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project to the container
COPY . .

# Expose Django default port
EXPOSE 8000

# Run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
docker run -p 8000:8000 messaging_app_image
