# syntax=docker/dockerfile:1

FROM python:3.10.10-buster

RUN apt-get update && apt-get -y install vim && rm -rf /var/lib/list/*

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt -i  https://mirrors.aliyun.com/pypi/simple/

HEALTHCHECK --interval=60s --timeout=5s --retries=3 CMD curl -fs http://127.0.0.1:9002/health_check/ || exit 1

EXPOSE 9002

CMD ["python", "run.py"]