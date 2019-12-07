# Streaming Processing Project

## Project Overview
Statistical analyses of San Francisco Crime data using Apache Spark Structured Streaming

## Development Environment

- Spark 2.4.3
- Scala 2.11.x
- Java 1.8.x
- Kafka build with Scala 2.11.x
- Python 3.6.x or 3.7.x

## Environment Setup (for Macs/Linux)
- Download Spark from https://spark.apache.org/downloads.html ("Prebuilt for Apache Hadoop 2.7 and later.")
- Download Kafka from https://kafka.apache.org/downloads, with Scala 2.11, version 2.3.0. 
- Download Scala 2.11.x. from the official site, or brew install scala (Mac)
- Run below to verify correct versions:
```
java -version
scala -version
Make sure your ~/.bash_profile looks like below (might be different depending on your directory):
export SPARK_HOME=/Users/dev/spark-2.4.3-bin-hadoop2.7
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_181.jdk/Contents/Home
export SCALA_HOME=/usr/local/scala/
export PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$SCALA_HOME/bin:$PATH
```
- install requirements 
```shell
start.sh
```

## Test
```shell

# run zookeeper
/usr/bin/zookeeper-server-start config/zookeeper.properties

# run kafka
/usr/bin/kafka-server-start config/server.properties

# run kafka producer
python kafka_server.py

# run kafka consumer
python consumer_server.py

# run spark job
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.3.4 --master local[*] data_stream.py
```

## Acknowledgements
Udacity

