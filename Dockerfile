FROM ubuntu:18.04

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
RUN apt-get -qq update
RUN apt-get -qq install -y git python3 libpq-dev python-dev wget libssl-dev python3-pip \
    locales python3-lxml \
    curl pv jq ffmpeg
RUN git clone --depth 1 --single-branch --branch boost-1.73.0 --recurse-submodules https://github.com/boostorg/boost.git
RUN git clone --depth 1 --single-branch --branch RC_2_0 --recurse-submodules https://github.com/arvidn/libtorrent.git
WORKDIR libtorrent
COPY build.sh $SRC/

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
