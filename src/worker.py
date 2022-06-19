import os, json

from src.constants import KAFKA_CONSUMER_CONNECT, KAFKA_TOPIC, POSTGRESQL_CONNECT, SEGMENT_POLYP_MODEL_PATH, FULL_PATH_IMAGE_FOLDER
from src.connection.sql_service import SQLService
from src.connection.kafka_consumer import Consumer
from src.model.model import SegmentPolyp

segment_polyp = SegmentPolyp(SEGMENT_POLYP_MODEL_PATH)
kafka_consumer = Consumer(KAFKA_TOPIC, KAFKA_CONSUMER_CONNECT)
postgresql_worker = SQLService(POSTGRESQL_CONNECT)


def get_path_image_file(message_value):
    message_value = json.loads(message_value.decode("utf-8"))
    if not message_value.get('image'):
        raise KeyError('Kafka message_value not key image')
    if not message_value['image'].get('originalImageFilename'):
        raise KeyError(
            'Kafka message_value image has null originalImageFilename')

    org_file_name = message_value['image']['originalImageFilename']
    full_path = os.path.join(FULL_PATH_IMAGE_FOLDER, org_file_name)
    return full_path


for message in kafka_consumer.consumer:
    message_value = message.value
    print(message_value)
    try:
        full_path_image = get_path_image_file(message_value)
    except KeyError as e:
        print(e)
        continue

    ratio_result = segment_polyp.ratio_mask_file(full_path_image)
    print(ratio_result)
    message_value_formatted = json.loads(message_value.decode("utf-8"))
    if ratio_result >= 0.8:
        result_status = 1
    else:
        result_status = 2

    sql_query_update_ratio_result = f"UPDATE image_service_image_tab SET classify = { result_status } where image_id =  {message_value_formatted['image']['id']} " 
    postgresql_worker.update(sql_query_update_ratio_result)
