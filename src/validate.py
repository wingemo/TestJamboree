import json
from jsonschema import validate, ValidationError

def validate_json_file(file_path, schema_path):
    try:
        # Läs in JSON-filen
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        # Läs in JSON-schema
        with open(schema_path, 'r') as schema_file:
            schema = json.load(schema_file)

        # Validera JSON-filen mot JSON-schemat
        validate(json_data, schema)
        print(f"Validation successful: {file_path} is valid according to {schema_path}")
    except FileNotFoundError:
        print("File not found. Please provide valid file and schema paths.")
    except json.JSONDecodeError:
        print(f"Invalid JSON format in {file_path}. Please check the file.")
    except ValidationError as e:
        print(f"Validation error: {e.message}")

# Exempel på användning:
# Ange sökvägar för din JSON-fil och JSON-schema
json_file_path = 'path/to/your/test_config.json'
json_schema_path = 'path/to/your/test_config_schema.json'

validate_json_file(json_file_path, json_schema_path)
