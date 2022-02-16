# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV MULTIDICT_NO_EXTENSIONS=1
ENV YARL_NO_EXTENSIONS=1

WORKDIR /app
COPY ./python/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ./python .

# ONLY CHANGE THIS IDOT
CMD python main.py