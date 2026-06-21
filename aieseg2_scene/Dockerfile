FROM python:3.11-slim

RUN pip install requests beautifulsoup4 paho-mqtt

WORKDIR /app

COPY app.py /app/app.py
COPY run.sh /app/run.sh

RUN chmod +x /app/run.sh

CMD ["/app/run.sh"]
