import json


def generate_avro_schema(json_data, record_name="", namespace=""):
    """Generates an Avro schema from JSON data.

    Args:
        json_data: A string or dictionary representing the JSON data.
        record_name: The name of the Avro record.
        namespace: The namespace for the Avro schema.

    Returns:
        A python dict representing the Avro schema.
    """

    if isinstance(json_data, str):
        json_data = json.loads(json_data)

    fields = []
    for key, value in json_data.items():
        key_capitalized = key.capitalize()
        field_schema = {"name": key}

        if isinstance(value, str):
            field_schema["type"] = ["null", "string"]
            field_schema["default"] = None
        elif isinstance(value, bool):
            field_schema["type"] = ["null", "boolean"]
            field_schema["default"] = None
        elif isinstance(value, int):
            field_schema["type"] = ["null", "int"]
            field_schema["default"] = None
        elif isinstance(value, float):
            field_schema["type"] = ["null", "double"]
            field_schema["default"] = None
        elif isinstance(value, list):
            if value and all(isinstance(item, type(value[0])) for item in value):
                field_schema["type"] = {"type": "array", "items": type_to_avro(value[0], record_name=key_capitalized, namespace=f'{namespace}.{key}')}
            else:
                field_schema["type"] = {"type": "array", "items": "string"}

            field_schema["default"] = []
        elif isinstance(value, dict):
            # Make the default for an object to {} instead of null
            field_schema["type"] = generate_avro_schema(value, record_name=key_capitalized, namespace=f'{namespace}.{key}')
            field_schema["default"] = {}
        elif value is None:
            field_schema["type"] = "null"
        else:
            field_schema["type"] = ["null", "string"]
            field_schema["default"] = None

        fields.append(field_schema)

    avro_schema = {
        "type": "record",
        "name": record_name,
        "namespace": namespace,
        "fields": fields
    }

    return avro_schema


def type_to_avro(value, record_name, namespace):
    if isinstance(value, str):
        return "string"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "double"
    elif isinstance(value, dict):
        schema = generate_avro_schema(value, record_name, namespace)
        return schema
    elif value is None:
        return "null"
    else:
        return "string"
