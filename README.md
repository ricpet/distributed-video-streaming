# Distributed Video Streaming 

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://github.com/ricpet)


This repository contains a Python implementation of a distributed video streaming system that relays on Apache Kafka. Moreover, we provide a performance tool.

## Notes

In this project we will use ``confluentinc/cp-kafka:5.2.1``. 

For suggested hardware requirements of Apache Kafka please have a look [here](https://docs.confluent.io/current/kafka/deployment.html).


In this project we will use [python-kafka](https://kafka-python.readthedocs.io/en/master/index.html), note that other Apache Kafka Python clients are available, e.g., [confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python), [pykafka](https://github.com/Parsely/pykafka), etc. 

## Requirements 

* ``python 3.7`` 
* ``virtualenv``
* ``docker-compose``
* ``opencv``

## Getting started

Create a virualenv and install requirements

```
virtualenv --python=python3.7 env
. env/bin/activate
pip install -r requirements.txt
```

Deploy Apache Kafka by using docker-compose 

``docker-compose up -d``

## Run the video streaming system

Run the producer: 
``python producer.py video/coverr-golden-gate-bridge.mp4``

Run the consumer: 
``python consumer.py``

## Run the performance evaluation

``python performance.py``

