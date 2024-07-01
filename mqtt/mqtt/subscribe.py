from paho.mqtt.client import Client as MqttClient

class Client:
    def __init__(self):
        self._client = MqttClient()
        self._client.on_connect = self.on_connect
        self._client.on_message = self.on_message

    def connect(self, host, port=1883, keepalive=60):
        self._client.connect(host, port, keepalive)
        self._client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        # Subscribe to all topics
        client.subscribe("#")

    def on_message(self, client, userdata, msg):
        print(f"Topic: {msg.topic}, Message: {msg.payload.decode()}")

if __name__ == '__main__':
    client = Client()
    client.connect('localhost')
