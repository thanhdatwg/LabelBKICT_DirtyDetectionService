import os
from dotenv import load_dotenv

load_dotenv()

SEGMENT_POLYP_MODEL_PATH = 'weights/segment_polyp.pth'

FULL_PATH_IMAGE_FOLDER = os.getenv('IMAGE_SERVICE_ORIGINAL_IMAGE_DIR')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
KAFKA_CONSUMER_CONNECT = {
    'group_id': os.getenv('KAFKA_GROUP_ID'),
    'bootstrap_servers': [os.getenv('KAFKA_SERVER')],
}

POSTGRESQL_CONNECT = {
    'database': os.getenv('DB_DATABASE'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
}

STATUS = {
    'undetected': 0,
    'dirty': 1,
    'clean': 2
}
