FROM python:3.9-slim

RUN pip install paho-mqtt influxdb-client

COPY mqtt_influx.py /mqtt_influx.py

CMD ["python3", "mqtt_influx.py"]
