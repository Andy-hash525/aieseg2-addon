FROM python:3.11-slim

RUN pip install requests beautifulsoup4 paho-mqtt

WORKDIR /app

COPY app.py /app/app.py

CMD ["python3", "/app/app.py"]
