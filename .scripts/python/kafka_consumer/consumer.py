import json
import boto3
import requests
from requests.auth import HTTPBasicAuth
from confluent_kafka import Consumer, KafkaException, KafkaError
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext, MessageField


def get_secret(secret_name):
    client = boto3.client('secretsmanager', region_name='us-east-1')
    response = client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response['SecretString'])

    return secret


ca_location = '.scripts/kafka/cacert.pem'
topic = 'example_topic'
config = get_secret('kafka-configs-dev')


def get_avro_deserializer():
    schema_registry_url = config['schema_registry_url']
    username = config['username']
    password = config['password']

    with requests.Session() as s:
        s.auth = HTTPBasicAuth(username, password)
        s.verify = ca_location

        subject = f'{topic}-value'
        with s.get(f'{schema_registry_url}/subjects/{subject}/versions') as r:
            r.raise_for_status()
            version = max(r.json())

        with s.get(f'{schema_registry_url}/subjects/{subject}/versions/{version}') as r:
            r.raise_for_status()
            schema = r.json()
            schema = schema['schema']

    schema_registry_client = SchemaRegistryClient({
        'url': schema_registry_url,
        'ssl.ca.location': ca_location,
        'basic.auth.user.info': f'{username}:{password}'
    })

    return AvroDeserializer(schema_registry_client, schema)


def run_consumer():

    deserializer = get_avro_deserializer()

    consumer = Consumer({
        'bootstrap.servers': config['bootstrap_servers'],
        'security.protocol': 'SASL_SSL',
        'sasl.mechanism': 'PLAIN',
        'ssl.ca.location': ca_location,
        'sasl.username': config['username'],
        'sasl.password': config['password'],
        'group.id': f'example_group_id_{topic}',
        'enable.auto.commit': False,
        'auto.offset.reset': 'earliest'
    })
    consumer.subscribe([topic])

    try:
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"End of partition {msg.partition()} reached {msg.offset()}")
                    continue
                else:
                    raise KafkaException(msg.error())

            msg = deserializer(msg.value(), SerializationContext(msg.topic(), MessageField.VALUE))

            print(json.dumps(msg, indent=4))

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == '__main__':
    run_consumer()
