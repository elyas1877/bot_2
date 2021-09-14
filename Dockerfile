
FROM ubuntu:20.04
# FROM wiserain/libtorrent:1.2.6-alpine3.11-py3 AS libtorrent
# FROM node:alpine
ENV DEBIAN_FRONTEND noninteractive
FROM emmercm/libtorrent:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
RUN apk update
RUN apk add git python3 libpq-dev python-dev python3-pip \
    locales python3-lxml \
    curl pv jq ffmpeg

WORKDIR /usr/lib/
RUN ls
WORKDIR /usr/src/app

RUN python3 -c 'import libtorrent; print(libtorrent.__version__)'

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt && \
    apt-get -qq purge git

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY . .
COPY netrc /root/.netrc
RUN ls
RUN pwd

CMD ["bash","start.sh"]
