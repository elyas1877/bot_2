# FROM wiserain/libtorrent:1.2.6-alpine3.11-py3 AS libtorrent
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive

# FROM alpine:3.11

FROM emmercm/libtorrent:latest

#libboost-all-dev
WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
RUN apk update
RUN apk add --no-cache --virtual git python3 postgresql-dev python3-dev py3-pip
    # locales python3-lxml \
    ffmpeg \

# COPY --from=libtorrent /libtorrent-build/usr/lib/ /usr/lib/

WORKDIR /usr/lib
RUN ls
WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
COPY requirements.txt .

# RUN git clone --recurse-submodules https://github.com/arvidn/libtorrent.git
# WORKDIR libtorrent
# RUN ls
# RUN pwd
# RUN python3 setup.py build
# RUN python setup.py install
RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 -c 'import libtorrent; print(libtorrent.__version__)'
RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

COPY . .
COPY netrc /root/.netrc
RUN ls
RUN pwd

CMD ["bash","start.sh"]
