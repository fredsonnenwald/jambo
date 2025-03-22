from jsonschema_pydantic.types import JSONSchema, JSONSchemaValidator

from pydantic import ValidationError

from unittest import TestCase


class TestJsonSchemaValidator(TestCase):
    def test_jsonschema_validator(self):
        schema: JSONSchema = {
            "$schema": "http://json-schema.org/schema",
            "$id": "http://example.com/schema",
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
            "required": ["name"],
        }

        JSONSchemaValidator.validate_python(schema)

    def test_jsonschema_validator_fails(self):
        schema: JSONSchema = {
            "$schema": "http://json-schema.org/schema",
            "$id": "http://example.com/schema",
            "title": "Person",
            "description": "A person",
        }

        with self.assertRaises(ValidationError):
            JSONSchemaValidator.validate_python(schema)
