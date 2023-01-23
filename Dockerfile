FROM python:alpine3.17

RUN apk add build-base libffi-dev openssl-dev bash

WORKDIR /app

COPY app.py /app
COPY requirements.txt /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "./app.py"]