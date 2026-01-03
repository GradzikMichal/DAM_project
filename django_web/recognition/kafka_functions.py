from kafka import KafkaConsumer, KafkaProducer
import json
from .image_class import ImageClass

producer = KafkaProducer(
    bootstrap_servers=['broker-1:9093'],
    api_version=(3, 9),
)


def add_img_to_db_using_kafka(img_data: ImageClass):
    print("Creating kafka producer...: ")
    print("Sending data to kafka server: ")
    print(img_data.toDbJSON())
    future = producer.send("add_image_to_db", img_data.toDbJSON())
    future.get(timeout=10)
    producer.flush()


def send_img_to_recognize(image: ImageClass):
    print("Sending image to recognition: ")
    future = producer.send("image_to_recognize", image.toRecognizeJSON())
    future.get(timeout=10)
    producer.flush()


def receive_img_id_from_db_using_kafka():
    #probably change to return whole data or change kafka to return only id -> add topic
    consumer = KafkaConsumer(
        "image_added_to_db",
        bootstrap_servers=['broker-1:9093'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        api_version=(3, 9),
        auto_offset_reset='earliest',
    )
    print("Waiting for messages on kafka consumer...")
    for message in consumer:
        image_data = message.value
        return image_data["image_id"]

def receive_img_from_recognize():
    consumer = KafkaConsumer(
        "image_recognized",
        bootstrap_servers=['broker-1:9093'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        api_version=(3, 9),
        auto_offset_reset='earliest',
    )
    print("Waiting for messages from recognition...")
    for message in consumer:
        image_results = message.value
        print(image_results)
