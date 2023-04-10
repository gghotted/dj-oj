FROM gghotted/dind-python:latest


ADD requirements.txt /
RUN apt-get update \
    && apt-get install -y cron tree
RUN pip install --upgrade pip && pip install -r requirements.txt