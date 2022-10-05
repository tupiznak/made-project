FROM grafana/grafana-oss
USER root
COPY ./datasources /etc/grafana/provisioning/datasources
COPY ./grafana.ini /etc/grafana/
COPY ./dashboards /etc/grafana/provisioning/dashboards
RUN chown -R grafana:root /etc/grafana/provisioning/
USER grafana
