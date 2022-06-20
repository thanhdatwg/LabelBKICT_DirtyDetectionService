import os, json
from src.utils.constants import KAFKA_CONSUMER_CONNECT, KAFKA_TOPIC, POSTGRESQL_CONNECT, SEGMENT_POLYP_MODEL_PATH, FULL_PATH_IMAGE_FOLDER
from src.controller.kafka_consumer import Consumer
from src.service.detect import get_ratio_result
kafka_consumer = Consumer(KAFKA_TOPIC, KAFKA_CONSUMER_CONNECT)

for message in kafka_consumer.consumer:
    message_value = message.value
    print(message_value)
    try:
        get_ratio_result(message_value)
    except KeyError as e:
        print(e)
        continue
