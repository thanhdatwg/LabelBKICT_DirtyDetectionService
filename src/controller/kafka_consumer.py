from kafka import KafkaConsumer


class Consumer:
    def __init__(self, topic, info_connect) -> None:
        self.info_connect = info_connect
        self.topic = topic
        self.consumer = KafkaConsumer(self.topic, **self.info_connect)
