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

FROM builder as production

# install apache and mod-wsgi
RUN : \
    && apt-get update  \
    && apt-get install --no-install-recommends -y \
        apache2  \
        apache2-dev \
    && apt-get clean \
    && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/* \
    && pip3 install --no-cache-dir mod-wsgi==4.9.4 \
    && :

# create wsgi module config and enable it
RUN : \
    && mod_wsgi-express module-config > /etc/apache2/mods-available/wsgi.load \
    && a2enmod wsgi \
    && :

# copy apache config
ADD apache2/service_apache.conf /etc/apache2/sites-available/
ADD apache2/flask_api.wsgi /var/www/flask_api/

# enable apache sites
RUN : \
    && a2ensite service_apache.conf \
    && a2dissite 000-default \
    && :

WORKDIR /src

COPY server/swagger_server /src/swagger_server

# link apache config to docker logs
RUN : \
    && ln -sf /proc/self/fd/1 /var/log/apache2/access.log \
    && ln -sf /proc/self/fd/1 /var/log/apache2/error.log \
    && ln -sf /proc/self/fd/1 /var/log/apache2/other_vhosts_access.log \
    && :

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]