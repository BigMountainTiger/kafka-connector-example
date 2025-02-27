import os
import logging
from datetime import datetime, timezone
from producer import BasicKafkaProducer
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.serialization import SerializationContext, MessageField

logging.basicConfig(level=logging.INFO)


def get_kafka_configs():
    config = {
        'bootstrap_servers': os.environ['BOOTSTRAP_SERVERS'],
        'schema_registry_url': os.environ['SCHEMA_REGISTRY_URL'],
    }

    topic = os.environ['TOPIC']

    with open(os.environ['KEY_SCHEMA'], 'r') as f:
        key_schema = f.read()

    with open(os.environ['VALUE_SCHEMA'], 'r') as f:
        value_schema = f.read()

    return config, topic, key_schema, value_schema


def publish_to_kafka(data):
    kafka_configs, topic, key_schema, value_schema = get_kafka_configs()

    print(f'Starting to publish to kafka topic {topic}')
    producer = BasicKafkaProducer(kafka_configs)

    key_serializer = producer.get_avro_serializer(key_schema)
    value_serializer = producer.get_avro_serializer(value_schema)

    key = {'id': int(datetime.now(timezone.utc).timestamp())}
    serialized_key = key_serializer(key, SerializationContext(topic, MessageField.KEY))
    serialized_value = value_serializer(data, SerializationContext(topic, MessageField.VALUE))

    producer.produce_message(topic, serialized_key, serialized_value)
    producer.flush_messages()


if __name__ == '__main__':

    data = {
        'id': '1',
        'data"': 'initial value',
        'operation': 'INSERT'
    }

    publish_to_kafka(data)

    print('Done')
