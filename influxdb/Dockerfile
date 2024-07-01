FROM influxdb:2

EXPOSE 8086

ENV DOCKER_INFLUXDB_INIT_MODE=setup \
    DOCKER_INFLUXDB_INIT_USERNAME=ADMIN_USERNAME \
    DOCKER_INFLUXDB_INIT_PASSWORD=ADMIN_PASSWORD \
    DOCKER_INFLUXDB_INIT_ORG=ORG_NAME \
    DOCKER_INFLUXDB_INIT_BUCKET=brainrotbucket

COPY init-influxdb.sh /docker-entrypoint-initdb.d/init-influxdb.sh

RUN chmod +x /docker-entrypoint-initdb.d/init-influxdb.sh

VOLUME ["/var/lib/influxdb2", "/etc/influxdb2", "/shared-token"]
