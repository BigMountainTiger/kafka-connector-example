import logging
from confluent_kafka import Producer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

logger = logging.getLogger()


class BasicKafkaProducer:
    def __init__(self, basic_config):

        self.kafka_bootstrap = basic_config['bootstrap_servers']
        self.schema_registry_url = basic_config['schema_registry_url']

        self.initialize_producer()
        self.initialize_schema_registry_client()

    def initialize_producer(self):
        self.producer = Producer({
            'bootstrap.servers': f'{self.kafka_bootstrap}',
            'debug': 'all',
            'acks': 'all',
            'retries': 0,
            'linger.ms': 1
        }, logger=logger)

    def initialize_schema_registry_client(self):
        self.schema_registry_client = SchemaRegistryClient({
            'url': self.schema_registry_url
        })

    def get_avro_serializer(self, schema_text):
        return AvroSerializer(self.schema_registry_client, schema_text)

    def produce_message(self, topic, key, value):
        self.producer.produce(topic=topic, key=key, value=value, on_delivery=self.delivery_report)

    def flush_messages(self):
        self.producer.flush()
        logger.info("Flushed all messages")

    def delivery_report(self, err, msg):
        if err is not None:
            logger.error(f'Message delivery failed: {err}')
        else:
            logger.info(f'Delivered - {msg.topic()} Partition - [{msg.partition()}] Offset - {msg.offset()}')


class SSLKafkaProducer(BasicKafkaProducer):
    def __init__(self, basic_config, security_config):

        self.certificate_path = security_config['certificate_path']
        self.username = security_config['username']
        self.password = security_config['password']

        super().__init__(basic_config)

    def initialize_producer(self):
        # The security.protocol should be "sasl_ssl" to an actual SSL server
        # Replace "plaintext" to "sasl_ssl"
        self.producer = Producer({
            'bootstrap.servers': self.kafka_bootstrap,
            'security.protocol': 'plaintext',
            'sasl.mechanisms': 'PLAIN',
            'ssl.ca.location': self.certificate_path,
            'sasl.username': self.username,
            'sasl.password': self.password,
            'debug': 'all',
            'acks': 'all',
            'retries': 0,
            'linger.ms': 1
        }, logger=logger)

    def initialize_schema_registry_client(self):
        self.schema_registry_client = SchemaRegistryClient({
            'url': self.schema_registry_url,
            'ssl.ca.location': self.certificate_path,
            'basic.auth.user.info': f'{self.username}:{self.password}'
        })
