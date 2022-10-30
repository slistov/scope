FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

RUN mkdir -p /usr/share/elasticsearch/config
COPY elasticsearch.yml /usr/share/elasticsearch/config


RUN mkdir -p /usr/share/kibana/config/
COPY kibana.yml /usr/share/kibana/config/
