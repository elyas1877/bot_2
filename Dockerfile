
# FROM ubuntu:21.04
# FROM wiserain/libtorrent:1.2.6-alpine3.11-py3 AS libtorrent
# FROM node:alpine
# FROM emmercm/libtorrent:latest
# FROM wiserain/libtorrent:latest-alpine3.15 AS libtorrent
FROM alpine:3.15
FROM emmercm/libtorrent:latest

ENV DEBIAN_FRONTEND noninteractive
#
# FROM wiserain/libtorrent:2.0.5-alpine3.15 AS libtorrent

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
RUN apk add git python3 postgresql-dev  python3-dev py3-pip bash libmagic boost-python3 boost-system libgcc libstdc++\
    libxslt-dev \
    curl jq ffmpeg

# COPY --from=libtorrent /libtorrent-build/usr/lib/ /usr/lib/


WORKDIR /usr/lib/
RUN ls

WORKDIR /usr/src/app


RUN python3 -c 'import libtorrent; print(libtorrent.__version__) ;'
RUN python3 -V
COPY requirements.txt .
RUN pip3 install wheel
RUN git clone https://github.com/pyrogram/pyrogram && cd pyrogram && python3 setup.py install
RUN pip3 install --no-cache-dir -r requirements.txt

# RUN locale-gen en_US.UTF-8
# ENV LANG en_US.UTF-8
WORKDIR /usr/lib/python3.9/site-packages
RUN ls
# ENV LANGUAGE en_US:en
# ENV LC_ALL en_US.UTF-8
WORKDIR /usr/src/app
COPY . .
COPY netrc /root/.netrc

RUN ls
RUN pwd
RUN ls
RUN chmod +rwx start.sh
RUN chmod +rwx bot12/__main__.py
RUN chmod +rwx bot12
# RUN chmod 777 /usr/lib/python3.9/site-packages/.wh.urllib3-1.26.5-py3.9.egg-info‏
CMD ["bash","start.sh"]
# CMD gunicorn bot12.__main__:aplication
