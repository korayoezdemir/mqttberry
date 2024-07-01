# Use the official Mosquitto image as a base
FROM eclipse-mosquitto:latest

# Copy your custom configuration file into the container
# Note: Create a `mosquitto.conf` file in the same directory as this Dockerfile
COPY mosquitto.conf /mosquitto/config/mosquitto.conf

# Expose MQTT protocol standard port
EXPOSE 1883

# Expose WebSocket port if you are using WebSocket (optional)
EXPOSE 9001

# Run Mosquitto
CMD ["/usr/sbin/mosquitto", "-c", "/mosquitto/config/mosquitto.conf"]
