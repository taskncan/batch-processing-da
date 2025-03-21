FROM bitnami/spark:3.5.5-debian-12-r1

USER root

RUN apt-get update && apt-get install -y python3 python3-pip libpq-dev gcc build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/processing/ /app

CMD ["spark-submit", "spark_processing.py"]