FROM ghcr.io/runatlantis/atlantis:dev-debian

COPY terraform /usr/local/bin/terraform
COPY atlantis.var /tmp/atlantis.var
COPY atlantis.yaml /tmp/atlantis.yaml
COPY server.yaml /tmp/server.yaml
EXPOSE 4141