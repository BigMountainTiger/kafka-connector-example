import logging
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.serialization import SerializationContext, MessageField

logger = logging.getLogger()


class KafkaProducer:
    def __init__(self, kafka_configs):
        logger.info('Inside init')

        self.certificate_path = kafka_configs['certificate_path']
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
    def initialize_schema_registry_client(kafka_configs):
        try:
            schema_registry_conf = {
                'url': kafka_configs['schema_registry_url'],
                'ssl.ca.location': kafka_configs['certificate_path'],
                'basic.auth.user.info': kafka_configs['username'] + ":" + kafka_configs['password']
            }
            return SchemaRegistryClient(schema_registry_conf)
        except Exception as err:
            logger.error('Exception while initializing Schema Registry Client. Error is : {}'.format(err))
            raise err
