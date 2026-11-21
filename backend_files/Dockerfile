# Use a lightweight Python 3.11 base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all backend files (app.py, requirements.txt, superkart_model.joblib)
COPY . .

# Install dependencies without caching
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose port 7860 for the Flask API
EXPOSE 7860

# Start the Flask app via Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:7860", "app:superkart_api"]
 
