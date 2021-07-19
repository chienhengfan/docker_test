# syntax=docker/dockerfile:1

FROM python:3.7-slim-buster

WORKDIR /docker_test

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "docker_ex", "run"]
