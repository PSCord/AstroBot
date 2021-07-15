FROM python:3.9

WORKDIR /opt/astrobot
ADD requirements.txt .

RUN python -m pip install -r requirements.txt
