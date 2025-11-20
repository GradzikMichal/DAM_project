from kafka import KafkaConsumer, KafkaProducer
import json
from .image_class import ImageClass

producer = KafkaProducer(
        bootstrap_servers=['broker-1:9093'],
        # acks=0,
        value_serializer=lambda o: o.toJSON(),
        api_version=(3,9),
    )
consumer = KafkaConsumer(
        "image_to_process",
        bootstrap_servers=['broker-1:9093'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        api_version=(3, 9),
        auto_offset_reset='earliest',
        group_id='2'
    )

def send_img_data_using_kafka(img_data: ImageClass):
    print("Creating kafka producer...: ")

    print("Sending data to kafka server: ")
    print(img_data.toJSON())
    future = producer.send("image_to_process", img_data)
    future.get(timeout=10)
    producer.flush()


def receive_img_data_using_kafka():
    #probably change to return whole data or change kafka to return only id -> add topic
    print("Waiting for messages on kafka consumer...")
    for message in consumer:
        image_data = message.value
        print(image_data)
        if image_data["image_id"] is not None and image_data["saved_file"] is None:
            return image_data["image_id"]
