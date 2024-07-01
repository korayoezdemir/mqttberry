from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from paho.mqtt.client import Client as MqttClient
import time
import logging
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levellevel - %(message)s')
logger = logging.getLogger(__name__)

def read_influxdb_token():
    try:
        with open('/shared/influx_token.env', 'r') as file:
            token = file.readline().strip()
            print(f"Read token: {token}")
            return token
    except Exception as e:
        print(f"Error reading token: {e}")
        return None

# InfluxDB settings
INFLUXDB_URL = "http://influxdb:8086"
INFLUXDB_TOKEN = read_influxdb_token()
INFLUXDB_ORG = "orgbrainrot"
INFLUXDB_BUCKET = "brainrotbucket"

# InfluxDB client
influx_db_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN)
write_api = influx_db_client.write_api(write_options=SYNCHRONOUS)

class Client:
    def __init__(self):
        self._client = MqttClient()
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message

    def connect(self, host, port=1883, keepalive=60):
        self._client.connect(host, port, keepalive)
        self._client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        logger.info("Connected with result code "+str(rc))
        # Subscribe to all topics
        client.subscribe("#")

    def on_message(self, client, userdata, msg):
        logger.info("Topic: %s, Message: %s" % (msg.topic, msg.payload.decode()))
        try:
            # Parse JSON payload
            payload = json.loads(msg.payload.decode())
            points = []

            # Extract relevant fields only if topic is SENSOR
            if 'SENSOR' in msg.topic:
                if 'DHT11' in payload:
                    temperature = payload['DHT11'].get('Temperature')
                    humidity = payload['DHT11'].get('Humidity')
                    dew_point = payload['DHT11'].get('DewPoint')
                    if temperature is not None:
                        point = Point("mqtt_message").tag("topic", msg.topic).field("Temperature", temperature)
                        points.append(point)
                    if humidity is not None:
                        point = Point("mqtt_message").tag("topic", msg.topic).field("Humidity", humidity)
                        points.append(point)
                    if dew_point is not None:
                        point = Point("mqtt_message").tag("topic", msg.topic).field("DewPoint", dew_point)
                        points.append(point)

                if 'SGP30' in payload:
                    eco2 = payload['SGP30'].get('eCO2')
                    tvoc = payload['SGP30'].get('TVOC')
                    a_humidity = payload['SGP30'].get('aHumidity')
                    if eco2 is not None:
                        point = Point("mqtt_message").tag("topic", msg.topic).field("eCO2", eco2)
                        points.append(point)
                    if tvoc is not None:
                        point = Point("mqtt_message").tag("topic", msg.topic).field("TVOC", tvoc)
                        points.append(point)
                    if a_humidity is not None:
                        point = Point("mqtt_message").tag("topic", msg.topic).field("aHumidity", a_humidity)
                        points.append(point)

            # Write points to InfluxDB
            if points:
                write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, points)
                logger.info("Message written to InfluxDB")
            else:
                logger.warning("No relevant fields found in the message payload")

        except json.JSONDecodeError:
            logger.warning("Received non-JSON message payload, not written to InfluxDB")
        except Exception as e:
            logger.error(f"Failed to write message to InfluxDB: {e}")

logger.info("Starting MQTT client")
client = Client()
client.connect('mosquitto')
