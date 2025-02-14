# https://py-avro-schema.readthedocs.io/en/stable/

import os
import json
import _schema_generator


MODEL_FILE = os.environ['MODEL_FILE']
SCHEMA_FILE = os.environ['SCHEMA_FILE']

with open(MODEL_FILE, "r") as f:
    model = json.loads(f.read())

record_name = 'ExampleRecord'
namespace = 'example.namespace'
namespace = f'com.song.{namespace}'
schema = _schema_generator.generate_avro_schema(model, record_name=record_name, namespace=namespace)
schema = json.dumps(schema, indent=4)

with open(SCHEMA_FILE, 'w') as f:
    f.write(schema)

print(f'Schema generated {SCHEMA_FILE}')
