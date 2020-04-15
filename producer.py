import sys
import time
import cv2
from kafka import KafkaProducer
import configparser


def produce_stream(input_file, kafka_server, producer_topic):
    # Start up producer
    producer = KafkaProducer(bootstrap_servers=kafka_server)

    # Open file
    video = cv2.VideoCapture(input_file)
    print('Publishing video...')

    while(video.isOpened()):
        success, frame = video.read()

        # Ensure file was read successfully
        if not success:
            print("bad read!")
            break
        # Convert image to png
        ret, buffer = cv2.imencode('.jpg', frame)

        # Convert to bytes and send to kafka
        producer.send(producer_topic, buffer.tobytes())

        time.sleep(0.1)
    video.release()
    print('Publish complete')


def produce_stream_from_camera(kafka_server, producer_topic):

    # Start up producer
    producer = KafkaProducer(bootstrap_servers=kafka_server)
    camera = cv2.VideoCapture(0)
    try:
        while(True):
            success, frame = camera.read()
            ret, buffer = cv2.imencode('.jpg', frame)
            producer.send(producer_topic, buffer.tobytes())
            # Choppier stream, reduced load on processor
            time.sleep(0.2)
    # Yeah! The expect like that sucks :-/
    except:
        print("\nExiting.")
        sys.exit(1)
    camera.release()


if __name__ == '__main__':
    """
    The producer publishes to Kafka Server a video file given as a system arg. 
    Otherwise it will default by streaming webcam feed.
    """

    config = configparser.ConfigParser()
    config.read('configuration.ini')
    kafka_server = config['GENERAL']['kafka_server']
    producer_topic = config['GENERAL']['producer_topic']

    if(len(sys.argv) > 1):
        video_path = sys.argv[1]
        print("Stream video...")
        produce_stream(video_path, kafka_server, producer_topic)
    else:
        print("Stream from camera...")
        produce_stream_from_camera(kafka_server, producer_topic)