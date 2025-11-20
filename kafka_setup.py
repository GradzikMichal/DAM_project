from kafka import KafkaConsumer, KafkaProducer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError
import socket

if __name__ == "__main__":
    kafka_ip = socket.gethostbyname("broker-1")
    admin_client = KafkaAdminClient(
        bootstrap_servers=kafka_ip + ":29092",
        client_id='test',

    )
    topic_list = []
    #sending info about path etc to db and ml worker
    topic_list.append(NewTopic(name="image_to_process", num_partitions=1, replication_factor=1))

    #sending id to ml worker and
    topic_list.append(NewTopic(name="image_saved", num_partitions=1, replication_factor=1))
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    kafka_ip = socket.gethostbyname("broker-2")
    admin_client = KafkaAdminClient(
        bootstrap_servers=kafka_ip+":39092",
        client_id='test'
    )
    topic_list = []
    # sending info about ml worker status
    topic_list.append(NewTopic(name="analysis_status", num_partitions=1, replication_factor=1))
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
