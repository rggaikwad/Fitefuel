FROM python:3.9

WORKDIR /app

COPY . /app

# Install system dependencies required for SQLite
RUN apt-get update && apt-get install -y sqlite3 libsqlite3-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "app/nps.py", "--server.port=8501"]
