FROM python:3.10

WORKDIR /opt/astrobot
ADD requirements.txt .

RUN python -m pip install -r requirements.txt
