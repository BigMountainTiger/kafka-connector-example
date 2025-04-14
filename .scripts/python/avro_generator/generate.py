# https://py-avro-schema.readthedocs.io/en/stable/

import os
import json
import _schema_generator


# path to the sample json data file
MODEL_FILE = os.environ['MODEL_FILE']

# path to the generated schema file
SCHEMA_FILE = os.environ['SCHEMA_FILE']

# Top level record name, ie. "Entities"
RECORD_NAME = os.environ['RECORD_NAME']

# Top level namespace, ie, "com.song.example"
NAMESPACE = os.environ['NAMESPACE']

with open(MODEL_FILE, "r") as f:
    model = json.loads(f.read())

schema = _schema_generator.generate_avro_schema(model, record_name=RECORD_NAME, namespace=NAMESPACE)
schema = json.dumps(schema, indent=4)

with open(SCHEMA_FILE, 'w') as f:
    f.write(schema)

print(f'Schema generated {SCHEMA_FILE}')
