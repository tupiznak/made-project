FROM grafana/grafana-oss
USER root
RUN apk add --update npm

COPY mongodb-grafana /var/lib/grafana/plugins/mongodb-grafana
RUN cd /var/lib/grafana/plugins/mongodb-grafana && npm install
USER grafana

ENV GF_PLUGINS_ALLOW_LOADING_UNSIGNED_PLUGINS=grafana-mongodb-datasource

ENTRYPOINT ["/bin/sh", "-c" , "npm run server --prefix $GF_PATHS_PLUGINS/mongodb-grafana & /run.sh"]

