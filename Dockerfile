FROM python:3-alpine

COPY . /japronto

RUN set -ex \
    && apk add --no-cache --virtual .build-deps \
               coreutils                        \
               gcc                              \
               libc-dev                         \
               linux-headers                    \
               make                             \
               openssl-dev                      \
               git                              \
                                                \
    && pip install uvloop pytoml                \
    && cd /japronto                             \
    && python setup.py -q bdist_wheel           \
    && pip install ./dist/*                     \
    && cd / && rm -rf /japronto                 \
                                                \
    && apk del --no-network .build-deps
