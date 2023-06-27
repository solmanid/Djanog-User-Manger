FROM python:latest

WORKDIR /code

COPY ./requirements.txt /code/

RUN pip install -r requirements.txt

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

RUN apt-get update &&\
    apt-get install -y binutils libproj-dev gdal-bin python3-gdal postgresql-client
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait

RUN pip install --upgrade pip
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir -p /docker-entrypoint-initdb.d