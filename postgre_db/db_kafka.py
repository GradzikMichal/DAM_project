from kafka import KafkaConsumer, KafkaProducer
import json
import socket
import db_connection as db


if __name__ == '__main__':
    consumer = KafkaConsumer(
        "add_image_to_db",
        bootstrap_servers=['broker-1:9093'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        api_version=(3, 9),
        auto_offset_reset='earliest',
        group_id='1'
    )
    producer = KafkaProducer(
        bootstrap_servers=['broker-1:9093'],
        value_serializer=lambda m: json.dumps(m).encode('utf-8'),
        api_version=(3, 9),
    )
    print("Waiting for images data...")
    for message in consumer:
        image_data = message.value
        print("Received images data...")
        db_connection = db.DB_connection(database="image_db", user="postgres", password="postgres")
        image_data["image_id"] = db_connection.insert_value(img_name=image_data["image_name"], folder_path=image_data["folder_path"], u_id=image_data["user_id"])
        future = producer.send("image_added_to_db", image_data)
        future.get(timeout=10)
        producer.flush()
        db_connection.__del__()
