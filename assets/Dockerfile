FROM alpine:3.18.4

RUN apk update && apk add bash openssh python3

WORKDIR /root
ADD ./ssh_key .
ADD ./mount.py .
ADD ./configuration.py .

CMD [ "python3", "-u", "mount.py" ]

HEALTHCHECK --interval=10s --timeout=10s CMD nc -w 1 -z -v 0.0.0.0 $SERVICE_PORT || exit 1