FROM centos:7
COPY elasticsearch-8.2.0-linux-x86_64.tar.gz /opt
COPY elasticsearch-8.2.0-linux-x86_64.tar.gz.sha512 /opt
RUN cd /opt \
    && groupadd elasticsearch \
    && useradd -c "elasticsearch" -g elasticsearch elasticsearch \
    && yum update -y \
    && yum upgrade -y \
    && yum -y install wget perl-Digest-SHA \
    && shasum -a 512 -c elasticsearch-8.2.0-linux-x86_64.tar.gz.sha512 \
    && tar -xzf elasticsearch-8.2.0-linux-x86_64.tar.gz \
    && rm elasticsearch-8.2.0-linux-x86_64.tar.gz elasticsearch-8.2.0-linux-x86_64.tar.gz.sha512 \
    && mkdir /var/lib/data && chmod -R 777 /var/lib/data \
    && chown -R elasticsearch:elasticsearch /opt/elasticsearch-8.2.0 \
    && yum -y remove wget perl-Digest-SHA && \
    yum clean all
USER elasticsearch
WORKDIR /opt/elasticsearch-8.2.0/
COPY elasticsearch.yml  config/
EXPOSE 9200 9300
ENTRYPOINT ["bin/elasticsearch"]