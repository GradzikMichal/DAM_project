from kafka.admin import KafkaAdminClient, NewTopic

if __name__ == "__main__":
    admin_client = KafkaAdminClient(
        bootstrap_servers="broker-1:9093",
        client_id='test',
    )
    topics_to_create = ["add_image_to_db", "image_added_to_db","image_to_recognize", "image_recognized"]

    topic_list = []
    existing_topics = admin_client.list_topics()
    for topic in topics_to_create:
        if topic not in existing_topics:
            topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))
    if len(topic_list) > 0:
        admin_client.create_topics(new_topics=topic_list, validate_only=False)
    print("Adding topics finished. Existing topics: ", admin_client.list_topics())


