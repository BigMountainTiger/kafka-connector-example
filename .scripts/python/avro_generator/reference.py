import json


def generate_avro_schema(json_data, schema_name="Record", namespace="default"):
    """Generates an Avro schema from JSON data.

    Args:
        json_data: A string or dictionary representing the JSON data.
        schema_name: The name of the Avro schema record.
        namespace: The namespace for the Avro schema.

    Returns:
        A string representing the Avro schema.
    """

    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    fields = []
    for key, value in data.items():
        field_schema = {"name": key}
        if isinstance(value, str):
            field_schema["type"] = "string"
        elif isinstance(value, int):
            field_schema["type"] = "int"
        elif isinstance(value, float):
            field_schema["type"] = "double"
        elif isinstance(value, bool):
            field_schema["type"] = "boolean"
        elif isinstance(value, list):
            if value and all(isinstance(item, type(value[0])) for item in value):
                field_schema["type"] = {"type": "array", "items": type_to_avro(value[0])}
            else:
                field_schema["type"] = {"type": "array", "items": "string"}
        elif isinstance(value, dict):
            field_schema["type"] = generate_avro_schema(value, schema_name=key, namespace=namespace)
        elif value is None:
            field_schema["type"] = ["null", "string"]
        else:
            field_schema["type"] = "string"  # Default to string if type is unknown
        fields.append(field_schema)

    avro_schema = {
        "type": "record",
        "name": schema_name,
        "namespace": namespace,
        "fields": fields,
    }
    return json.dumps(avro_schema, indent=2)


def type_to_avro(value):
    if isinstance(value, str):
        return "string"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "double"
    if isinstance(value, bool):
        return "boolean"
    return "string"


# Example usage:
json_data = """
{
  "name": "John Doe",
  "age": 30,
  "city": "New York",
  "is_active": true,
  "address": {
    "street": "123 Main St",
    "zip_code": "10001"
  },
  "phone_numbers": ["123-456-7890", "987-654-3210"],
  "salary": 75000.50,
  "title": null
}
"""

avro_schema = generate_avro_schema(json_data)
print(avro_schema)
