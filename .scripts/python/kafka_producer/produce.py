def publish_to_kafka(responses):
    topic = args['kafka_topic_name']
    print(f'Starting to publish to kafka topic {topic}')

    key_schema = load_schema(args['kafka_key_schema_file'])
    value_schema = load_schema(args['kafka_value_schema_file'])

    cert_file = args['cert_file']
    kafka_secret_name = args['kafka_configs_secret_name']
    schema_registry_client = KafkaProducer.initialize_schema_registry_client(kafka_secret_name, cert_file)
    key_serializer = AvroSerializer(schema_registry_client, key_schema)
    value_serializer = AvroSerializer(schema_registry_client, value_schema)
    producer = KafkaProducer(kafka_secret_name, cert_file)

    key = {'id': int(datetime.now(timezone.utc).timestamp())}
    for response in responses:
        producer.produce_message(topic, key, response, key_serializer, value_serializer)

    producer.flush_messages()
