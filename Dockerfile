
FROM ubuntu:20.04
# FROM wiserain/libtorrent:1.2.6-alpine3.11-py3 AS libtorrent
# FROM node:alpine
ENV DEBIAN_FRONTEND noninteractive
FROM emmercm/libtorrent:latest
ENV MUSL_LOCALE_DEPS cmake make musl-dev gcc gettext-dev libintl g++  libffi-dev openssl-dev

RUN apk add --no-cache \
    $MUSL_LOCALE_DEPS \
    && wget https://gitlab.com/rilian-la-te/musl-locales/-/archive/master/musl-locales-master.zip \
    && unzip musl-locales-master.zip \
      && cd musl-locales-master \
      && cmake -DLOCALE_PROFILE=OFF -D CMAKE_INSTALL_PREFIX:PATH=/usr . && make && make install \
      && cd .. && rm -r musl-locales-master

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
RUN apk update
RUN apk add git python3 libpq-dev python3-dev py3-pip ibxml2-dev \
    libxslt-dev \
    curl jq ffmpeg

WORKDIR /usr/lib/
RUN ls
WORKDIR /usr/src/app

RUN python3 -c 'import libtorrent; print(libtorrent.__version__)'

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt && \

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY . .
COPY netrc /root/.netrc
RUN ls
RUN pwd

CMD ["bash","start.sh"]
