from kafka import KafkaConsumer
import json
import socket
import db_connection as con


if __name__ == '__main__':
    kafka_ip = socket.gethostbyname("broker-1")
    consumer = KafkaConsumer(
        "image_to_process",
        bootstrap_servers=[kafka_ip+':19092'],
        auto_offset_reset='earliest',  # Start from the earliest message
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    for message in consumer:
        print("Waiting for images data...")
        image_data = message.value
        if image_data["image_id"] is None and image_data["saved_file"] is None:
            pass
            #send to db