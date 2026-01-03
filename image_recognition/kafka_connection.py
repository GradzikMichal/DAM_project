from kafka import KafkaConsumer, KafkaProducer
import json
from image_recognition_model import recognize_image

if __name__ == '__main__':
    consumer = KafkaConsumer(
        "image_to_recognize",
        bootstrap_servers=['broker-1:9093'],
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        api_version=(3, 9),
        auto_offset_reset='earliest',
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
        recognition_results = recognize_image(image_data['image_bytes'])
        print(recognition_results)
        future = producer.send("image_recognized", {"DONE":"DONE"})
        future.get(timeout=10)
        producer.flush()
