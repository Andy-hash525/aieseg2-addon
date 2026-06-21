FROM python:3.11-slim

RUN pip install requests beautifulsoup4 paho-mqtt

COPY app.py /app.py
CMD ["python3", "/app.py"]