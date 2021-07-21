# syntax=docker/dockerfile:1
FROM ubuntu:latest

RUN apt-get -y update
RUN apt-get install python3 -y
RUN apt-get install -y --no-install-recommends \
    python3-pip 

RUN apt install -y curl && \
      curl -LO https://storage.googleapis.com/kubernetes-release/release/`curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt`/bin/linux/amd64/kubectl && \
      chmod +x ./kubectl && \
      mv ./kubectl /usr/local/bin/kubectl


WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt 
COPY controller.py .

