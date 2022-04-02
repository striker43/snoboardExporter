FROM python:3.10-alpine

RUN pip install requests

ADD ./src/app.py /usr/src/app/app.py

WORKDIR /usr/src/app

CMD [ "python", "-u", "app.py"]
