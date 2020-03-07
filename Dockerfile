FROM alpine:3.11
LABEL maintainer "collelog <collelog.cavamin@gmail.com>"

EXPOSE 9683

WORKDIR /usr/local/

RUN set -eux && \
	apk upgrade --update && \
	apk add --no-cache py-pip tzdata && \
	\
	# timezone
	cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
	echo "Asia/Tokyo" > /etc/timezone && \
	apk del tzdata && \
	\
	mkdir /usr/local/speedtest && \
	cd /usr/local/speedtest && \
	\
	# install Python Package
	pip install speedtest-cli && \
	pip install prometheus-client && \
	\
	# cleaning
	rm -rf /tmp/* /var/cache/apk/*

COPY exec_speedtest.py /usr/local/speedtest/

WORKDIR /usr/local/speedtest

ENTRYPOINT ["/usr/bin/python", "-u", "/usr/local/speedtest/exec_speedtest.py"]
