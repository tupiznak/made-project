FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt /
COPY requirements.docker.txt /
COPY requirements.ml.txt /

RUN pip install --no-cache-dir -r /requirements.txt
RUN pip install --no-cache-dir -r /requirements.ml.txt
RUN pip install --no-cache-dir -r /requirements.docker.txt

COPY ml/lda/prepare.py /
RUN python /prepare.py
