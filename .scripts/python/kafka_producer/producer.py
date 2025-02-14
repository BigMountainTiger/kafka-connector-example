import json
import logging
import boto3
from botocore.exceptions import ClientError
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext, MessageField

logger = logging.getLogger()


class KafkaProducer:
    def __init__(self, secret_name, certificate_path):
        logger.info('Inside init')

        kafka_configs = get_secret(secret_name)

        self.certificate_path = certificate_path
        self.kafka_password = kafka_configs['password']
        self.kafka_username = kafka_configs['username']
        self.kafka_bootstrap = kafka_configs['bootstrap_servers']

        # Initialize the Kafka Producer
        self.producer = None
        self.initialize_producer()

    def initialize_producer(self):
        try:
            self.producer = Producer({
                'bootstrap.servers': f'{self.kafka_bootstrap}',
                'security.protocol': 'sasl_ssl',
                'sasl.mechanisms': 'PLAIN',
                'ssl.ca.location': self.certificate_path,
                'sasl.username': f'{self.kafka_username}',
                'sasl.password': f'{self.kafka_password}',
                'debug': 'all',
                'acks': 'all',
                'retries': 0,
                'linger.ms': 1
            }, logger=logger)
        except Exception as err:
            logger.error('Exception while getting producer config . Error is : {}'.format(err))
            raise err

    def delivery_report(self, err, msg):
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.info(
                f"Message delivered to Topic - {msg.topic()} Partition - [{msg.partition()}] Offset - {msg.offset()}")

    def produce_message(self, topic, key, value, key_serializer, value_serializer, flush_messages=True):
        """
            Produces a message to the specified Kafka topic.
            Args:
                topic (str): The Kafka topic to which the message will be produced.
                key (Any): The key of the message.
                value (Any): The value of the message.
                key_serializer (Callable): A function to serialize the key.
                value_serializer (Callable): A function to serialize the value.
                flush_messages (bool, optional): Whether to flush messages immediately after producing. Defaults to True.
            Raises:
                Exception: If there is an error producing the message to the topic.
        """
        try:

            self.producer.produce(topic=topic,
                                  key=key_serializer(key, SerializationContext(topic, MessageField.KEY)),
                                  value=value_serializer(value, SerializationContext(topic, MessageField.VALUE)),
                                  on_delivery=self.delivery_report)

            if flush_messages:
                # Wait for any outstanding messages to be delivered and delivery report
                self.producer.flush()
                logger.info(f'Successfully processed message with event: {key}')
        except Exception as e:
            raise Exception(f'Error producing to topic. {str(e)}')

    def flush_messages(self):
        """Flush the producer so all messages are sent."""
        try:
            self.producer.flush()
            logger.info("Flushed all messages")
        except Exception as e:
            logger.error(f"Error flushing producer: {str(e)}")
            raise e

    @staticmethod
    def initialize_schema_registry_client(secret_name, certificate_path):
        """
            Initialize the Schema Registry Client using the provided secret name and certificate path.
            This function retrieves Kafka configurations from a secret store and uses them to configure
            the Schema Registry Client. It handles the necessary SSL and authentication settings.
            Args:
                secret_name (str): The name of the secret containing Kafka configurations.
                certificate_path (str): The file path to the SSL certificate.
            Returns:
                SchemaRegistryClient: An instance of the SchemaRegistryClient configured with the provided settings.
            Raises:
                Exception: If there is an error during the initialization of the Schema Registry Client.
        """
        kafka_configs = get_secret(secret_name)

        try:
            schema_registry_conf = {
                'url': kafka_configs['schema_registry_url'],
                'ssl.ca.location': certificate_path,
                'basic.auth.user.info': kafka_configs['username'] + ":" + kafka_configs['password']
            }
            return SchemaRegistryClient(schema_registry_conf)
        except Exception as err:
            logger.error('Exception while initializing Schema Registry Client. Error is : {}'.format(err))
            raise err


secret_manager_client = boto3.client('secretsmanager', region_name='us-east-1')


def get_secret(secret_name):
    try:
        response = secret_manager_client.get_secret_value(SecretId=secret_name)
        secret = json.loads(response['SecretString'])
        return secret
    except ClientError as e:
        logger.error(f'Error retrieving secret {secret_name}: {e}')
        raise e
