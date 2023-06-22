#FROM python:latest
#
#WORKDIR /code
#
#COPY ./requirements.txt /code/
#
#RUN pip install -U pip
#RUN pip install -r requirements.txt
#
#EXPOSE 8000
#
#
#LABEL maintainer="PostGIS Project - https://postgis.net" \
#      org.opencontainers.image.description="PostGIS 3.3.3+dfsg-1.pgdg110+1 spatial database extension with PostgreSQL 11 bullseye" \
#      org.opencontainers.image.source="https://github.com/postgis/docker-postgis"
#
#ENV POSTGIS_MAJOR 3
#ENV POSTGIS_VERSION 3.3.3+dfsg-1.pgdg110+1
#
#RUN apt-get update \
#      && apt-cache showpkg postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR \
#      && apt-get install -y --no-install-recommends \
#           # ca-certificates: for accessing remote raster files;
#           #   fix: https://github.com/postgis/docker-postgis/issues/307
#           ca-certificates \
#           \
#           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR=$POSTGIS_VERSION \
#           postgresql-$PG_MAJOR-postgis-$POSTGIS_MAJOR-scripts \
#      && rm -rf /var/lib/apt/lists/*
#
#RUN mkdir -p /docker-entrypoint-initdb.d

FROM python:latest

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install -U pip
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


