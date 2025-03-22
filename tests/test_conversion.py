from jsonschema_pydantic import jsonschema_to_pydantic
from jsonschema_pydantic.types import JSONSchema

from unittest import TestCase


class TestConversion(TestCase):
    def test_jsonschema_to_pydantic(self):

        schema: JSONSchema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
            "required": ["name"],
        }

        model = jsonschema_to_pydantic(schema)

        assert model.__fields__.keys() == {"name", "age"}
        assert model.__fields__["name"].required is True
        assert model.__fields__["age"].required is False
        assert model.__fields__["name"].type_ == str
        assert model.__fields__["age"].type_ == int
