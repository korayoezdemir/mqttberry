#!/bin/bash

INFLUXDB_CONFIG_FILE="/etc/influxdb2/influx-configs"
INFLUXDB_TOKEN=$(grep 'token = ' $INFLUXDB_CONFIG_FILE | sed -n 's/.*= "\(.*\)"/\1/p' | head -n 1)

echo "${INFLUXDB_TOKEN}" > /shared/influx_token.env
