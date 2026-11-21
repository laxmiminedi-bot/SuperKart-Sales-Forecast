# Use a lightweight Python 3.11 base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all frontend files (app.py, requirements.txt)
COPY . .

# Install dependencies without caching
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose port 8501 for the Streamlit UI
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.enableXsrfProtection=false"]
