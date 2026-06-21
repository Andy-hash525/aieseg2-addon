FROM ghcr.io/hassio-addons/base-python:latest

RUN pip install requests beautifulsoup4 paho-mqtt

WORKDIR /app

COPY app.py /app/app.py

CMD ["bash", "-c", "python3 /app/app.py"]
