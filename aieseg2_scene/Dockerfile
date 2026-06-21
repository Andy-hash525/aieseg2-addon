FROM ghcr.io/home-assistant/base-python:3.12

RUN pip install requests beautifulsoup4 paho-mqtt

WORKDIR /app

COPY app.py /app/app.py

CMD ["python3", "/app/app.py"]
