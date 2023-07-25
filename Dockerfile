FROM python:3.11.4-slim-bullseye as builder

RUN : \
    && apt-get update  \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* \
    && :

RUN mkdir -p /src
WORKDIR /src

COPY requirements.txt /src/

RUN pip3 install --no-cache-dir -r requirements.txt

FROM builder as testing

WORKDIR /src

COPY test_requirements.txt /src/
RUN pip3 install --no-cache-dir -r test_requirements.txt

COPY cli /src/cli
COPY server /src/server

ENTRYPOINT ["pytest"]

CMD ["cli"]