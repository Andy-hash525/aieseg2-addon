FROM python:3.11-slim

RUN pip install requests beautifulsoup4 paho-mqtt

COPY app.py /app.py
COPY run.sh /run.sh

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]