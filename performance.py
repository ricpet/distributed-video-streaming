# This is a porting of the original project available here: https://github.com/ActivisionGameScience/python-kafka-benchmark

from kafka import KafkaProducer
from kafka import KafkaConsumer
import configparser
import time


def calculate_thoughput(timing, n_messages=1000000, msg_size=100):
    print("Processed {0} messsages in {1:.2f} seconds".format(
        n_messages, timing))
    print("{0:.2f} MB/s".format(
        (msg_size * n_messages) / timing / (1024*1024)))
    print("{0:.2f} Msgs/s".format(n_messages / timing))


def producer_performance(kafka_server, consumer_topic, msg_payload, msg_count):
    producer = KafkaProducer(bootstrap_servers=kafka_server)
    producer_start = time.time()

    for i in range(msg_count):
        producer.send(consumer_topic, msg_payload)

    producer.flush()  # clear all local buffers and produce pending messages
    return time.time() - producer_start


def consumer_performance(kafka_server, consumer_topic, msg_count):

    consumer = KafkaConsumer(
        bootstrap_servers=kafka_server,
        auto_offset_reset='earliest',  # start at earliest topic
        group_id=None  # do no offest commit
    )
    msg_consumed_count = 0
    consumer_start = time.time()
    consumer.subscribe([consumer_topic])
    for msg in consumer:
        msg_consumed_count += 1
        if msg_consumed_count >= msg_count:
            break
    consumer_timing = time.time() - consumer_start
    consumer.close()
    return consumer_timing


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('configuration.ini')
    kafka_server = config['GENERAL']['kafka_server']
    consumer_topic = config['GENERAL']['producer_topic']
    msg_count = int(config['PERFORMANCE']['msg_count'])
    msg_size = int(config['PERFORMANCE']['msg_size'])
    msg_payload = msg_payload = ('testingkafka' * 20).encode()[:msg_size]

    producer_timings = {}
    consumer_timings = {}

    producer_timings['producer'] = producer_performance(
        kafka_server, consumer_topic, msg_payload, msg_count)
    consumer_timings['consumer'] = consumer_performance(
        kafka_server, consumer_topic, msg_count)

    calculate_thoughput(consumer_timings['consumer'])
