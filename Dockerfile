# Use Python 3.9 as base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy application files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "nps.py", "--server.port=8501", "--server.address=0.0.0.0"]
