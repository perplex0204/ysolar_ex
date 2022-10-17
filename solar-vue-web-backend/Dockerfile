FROM ubuntu:20.04

LABEL MAINTAINER="Klaus Chen <klaus_chen@paets.com.tw>"

WORKDIR /var/www/
ADD . /var/www/

RUN apt update -y && \
    apt install -y ca-certificates && \
    sed -i 's|http://archive.ubuntu.com/ubuntu/|https://nexus.cckuo.ee.ntust.edu.tw/repository/ubuntu/|g' /etc/apt/sources.list && \
    apt clean autoclean && \
    apt update -y && \
    DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata && \
    apt install -y python3 python3-pip && \
    apt install -y poppler-utils && \
    apt clean autoclean && \
    apt autoremove --yes && \
    rm -rf /var/lib/{apt,dpkg,cache,log}/

RUN mkdir -p /etc/xdg/pip && \
    /bin/bash -c 'echo -e "[global]\nindex = https://nexus.cckuo.ee.ntust.edu.tw/repository/pypi/pypi\nindex-url = https://nexus.cckuo.ee.ntust.edu.tw/repository/pypi/simple" |tee /etc/xdg/pip/pip.conf' && \
    pip3 config list -v && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

EXPOSE $APP_PORT

ENV LANG C.UTF-8

CMD gunicorn --workers $WORKERS --bind 0.0.0.0:$APP_PORT wsgi
