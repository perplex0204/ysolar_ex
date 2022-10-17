FROM node:16-alpine

LABEL MAINTAINER="YuShan Huang <contact@yushan.tw>"

#localtime
ENV TZ=Asia/Taipei

ADD . /app/vue/
WORKDIR /app/vue/


EXPOSE 8080
CMD [ "/bin/sh", "volume-to-host.sh" ]