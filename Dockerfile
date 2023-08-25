FROM python:3.9-slim-bookworm

RUN apt-get update && \
    apt-get autoclean && \
    apt-get install -y --no-install-recommends \
    python3-pyqt5

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install prometheus_client pyqt5

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN mkdir /app
COPY main.py /app/main.py

CMD python3 /app/main.py
