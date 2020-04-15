from kafka import KafkaConsumer
import cv2
import configparser
import numpy as np


def consumer(kafka_server, consumer_topic):
    # Create Kafka Consumer 
    consumer = KafkaConsumer(consumer_topic, bootstrap_servers=kafka_server)

    # Create window with freedom of dimensions
    cv2.namedWindow("distributed-video-streaming", cv2.WINDOW_NORMAL)

    for m in consumer:
        frame = m.value
        image = cv2.imdecode(np.fromstring(frame, dtype=np.uint8), 1)
        cv2.imshow("distributed-video-streaming", image)
        cv2.waitKey(25)

    cv2.destroyAllWindows()


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('configuration.ini')
    kafka_server = config['GENERAL']['kafka_server']
    consumer_topic = config['GENERAL']['producer_topic']
    consumer(kafka_server, consumer_topic)
