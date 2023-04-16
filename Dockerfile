FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y openjdk-11-jdk
RUN wget https://archive.apache.org/dist/hadoop/common/hadoop-3.3.0/hadoop-3.3.0.tar.gz && \
    tar -xzf hadoop-3.3.0.tar.gz && \
    rm hadoop-3.3.0.tar.gz && \
    mv hadoop-3.3.0 /usr/local/hadoop

RUN pip install requests pandas hdfs pyspark sqlalchemy

WORKDIR /app
COPY scrip.py .

EXPOSE 50070 9000
CMD /usr/local/hadoop/sbin/start-dfs.sh && python scrip.py