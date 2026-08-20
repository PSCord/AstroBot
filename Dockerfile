FROM python:3.11

WORKDIR /opt/astrobot
ADD requirements.txt .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN python -m pip install -r requirements.txt
