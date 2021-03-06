FROM python:3.9

EXPOSE 8001

COPY ./ /app

WORKDIR /app

RUN pip install -r requirements.txt
