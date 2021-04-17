FROM python:3.7-buster as build

WORKDIR /price_watch
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .
RUN pip install .