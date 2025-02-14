import logging
from datetime import datetime, timezone
from producer import KafkaProducer
from confluent_kafka.schema_registry.avro import AvroSerializer

logging.basicConfig(level=logging.INFO)


def get_kafka_configs():
    # key_schema = load_schema(args['kafka_key_schema_file'])
    # value_schema = load_schema(args['kafka_value_schema_file'])

    # cert_file = args['cert_file']
    # kafka_secret_name = args['kafka_configs_secret_name']

    return {}, 'Topic_name', 'key_schema', 'value_schema'


def publish_to_kafka(response):
    kafka_configs, topic, key_schema, value_schema = get_kafka_configs()

    print(f'Starting to publish to kafka topic {topic}')

    schema_registry_client = KafkaProducer.initialize_schema_registry_client(kafka_configs)
    key_serializer = AvroSerializer(schema_registry_client, key_schema)
    value_serializer = AvroSerializer(schema_registry_client, value_schema)

    producer = KafkaProducer(kafka_configs)

    key = {'id': int(datetime.now(timezone.utc).timestamp())}
    producer.produce_message(topic, key, response, key_serializer, value_serializer)

    producer.flush_messages()


if __name__ == '__main__':
    print('OK')
