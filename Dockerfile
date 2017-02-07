FROM gliderlabs/alpine:3.4

RUN apk update

RUN apk add --no-cache python fabric openssl

WORKDIR /opt/when-expires

COPY ./*.* /opt/when-expires
