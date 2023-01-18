FROM ghcr.io/runatlantis/atlantis:{latest version}

RUN cd /opt/stack \
COPY terraform /usr/local/bin/terraform
COPY server.yaml /tmp/server.yaml
COPY repo.yaml /tmp/repo.yaml
EXPOSE 4141