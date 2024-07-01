from paho.mqtt.client import Client as MqttClient
import time
import random

class Client:
    def __init__(self):
        self._client = MqttClient()

    def connect(self, host, port=1883, keepalive=60):
        self._client.connect(host, port, keepalive)

    def publish(self, topic, payload=None, qos=0, retain=False):
        self._client.publish(topic, payload, qos, retain)

if __name__ == '__main__':
    client = Client()
    client.connect('localhost')

    while True:
        time.sleep(4)
        client.publish('temperature', f'{round(random.uniform(24.5, 25.0), 1)}')
        client.publish('co2', f'{round(random.uniform(2, 5), 1)}')

