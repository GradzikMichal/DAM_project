from kafka import KafkaConsumer, KafkaProducer
import json
import socket
import db_connection as db


if __name__ == '__main__':
    consumer = KafkaConsumer(
        "image_to_process",
        bootstrap_servers=['broker-1:9093'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        api_version=(3, 9),
        auto_offset_reset='earliest',
        group_id='1'
    )
    producer = KafkaProducer(
        bootstrap_servers=['broker-1:9093'],
        # acks=0,
        value_serializer=lambda m: json.dumps(m).encode('utf-8'),
        api_version=(3, 9),
    )

    for message in consumer:
        print("Waiting for images data...")
        image_data = message.value
        print(image_data)
        print("Received images data...")

        if image_data["image_id"] is None and image_data["saved_file"] is False:
            db_connection = db.DB_connection(database="image_db", user="postgres", password="postgres")
            image_data["image_id"] = db_connection.insert_value(img_name=image_data["image_name"], folder_path=image_data["folder_path"], u_id=image_data["user_id"])
            future = producer.send("image_to_process", image_data)
            future.get(timeout=10)
            producer.flush()
            db_connection.__del__()
