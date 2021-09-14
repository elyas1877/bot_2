FROM ubuntu:18.04

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
RUN apt-get -qq update
RUN apt-get -qq install -y git python3 libpq-dev python-dev libboost-all-dev python3-pip \
    locales python3-lxml \
    curl pv jq ffmpeg
COPY requirements.txt .

RUN git clone --recurse-submodules https://github.com/arvidn/libtorrent.git
WORKDIR libtorrent
RUN ls
RUN pwd

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
