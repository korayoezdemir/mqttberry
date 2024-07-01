.PHONY: influxdb mosquitto influxdb-down mosquitto-down grafana grafana-down up down rebuild-influxdb rebuild-grafana connect-mqtt run-mqtt-loop ssh-raspi tunnel-to-rapsi delete-ssh-key stop-services-on-raspi rebuild-mosquitto rebuild-influxdb
influxdb:
	docker compose up -d influxdb

mosquitto:
	docker compose up -d mosquitto

grafana:
	docker compose up -d grafana

grafana-down:
	docker compose down grafana

influxdb-down:
	docker compose down influxdb

mosquitto-down:
	docker compose down mosquitto

up:
	docker compose up -d influxdb mosquitto grafana

down:
	docker compose down influxdb mosquitto grafana

rebuild-mosquitto:
	docker-compose down mosquitto
	docker volume rm sbc_mosquitto-data || true
	docker-compose up -d --build mosquitto

rebuild-influxdb:
	docker-compose down influxdb
	docker volume rm sbc_influxdb-data sbc_influxdb-config  sbc_shared || true
	docker-compose up -d --build influxdb

rebuild-grafana:
	docker-compose down grafana
	docker volume rm sbc_grafana-data || true
	docker-compose up -d --build grafana

connect-mqtt:
	cd mqtt && poetry run python3 mqtt/subscribe.py

run-mqtt-loop:
	cd mqtt && poetry run python3 mqtt/publish.py
