FROM python:3.9-slim-buster
MAINTAINER Chetan Kini <ckini123@gmail.com>

ENV INSTALL_PATH /urlwarden
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "urlwarden.app:create_app()"
