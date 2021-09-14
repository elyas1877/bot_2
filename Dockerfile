FROM ubuntu:20.04 AS ubuntu
FROM wiserain/libtorrent:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
RUN apt-get -qq update
RUN apt-get -qq install -y git python3 libpq-dev python-dev python3-pip \
    locales python3-lxml \
    curl pv jq ffmpeg

RUN \
    BUILD_VER=$(python3 -c 'import libtorrent as lt; print(lt.version)') && \
    if [ $LIBTORRENT_VER = ${BUILD_VER%.*} ]; then \
        echo "Successfully built with version: ${BUILD_VER}"; \
    else \
        echo "Something went wrong: ${BUILD_VER}"; \
        exit 1; \
    fi

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
