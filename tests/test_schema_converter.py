from jsonschema_pydantic.schema_converter import SchemaConverter

from pydantic import BaseModel

from unittest import TestCase


def is_pydantic_model(cls):
    return isinstance(cls, type) and issubclass(cls, BaseModel)


class TestSchemaConverter(TestCase):
    def test_jsonschema_to_pydantic(self):
        schema = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
            "required": ["name"],
        }

        model = SchemaConverter.build(schema)

        self.assertTrue(is_pydantic_model(model))

    def test_validation_string(self):
        schema = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
            },
            "required": ["name"],
        }

        model = SchemaConverter.build(schema)

        self.assertEqual(model(name="John", age=30).name, "John")

    def test_validation_integer(self):
        schema = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "age": {"type": "integer"},
            },
            "required": ["age"],
        }

        model = SchemaConverter.build(schema)

        self.assertEqual(model(age=30).age, 30)

        self.assertEqual(model(age="30").age, 30)

    def test_validation_float(self):
        schema = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "age": {"type": "number"},
            },
            "required": ["age"],
        }

        model = SchemaConverter.build(schema)

        self.assertEqual(model(age=30).age, 30.0)

        self.assertEqual(model(age="30").age, 30.0)

    def test_validation_boolean(self):
        schema = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "is_active": {"type": "boolean"},
            },
            "required": ["is_active"],
        }

        model = SchemaConverter.build(schema)

        self.assertEqual(model(is_active=True).is_active, True)

        self.assertEqual(model(is_active="true").is_active, True)

    def test_validation_list(self):
        schema = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "friends": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["friends"],
        }

        model = SchemaConverter.build(schema)

        self.assertEqual(model(friends=["John", "Jane"]).friends, ["John", "Jane"])

    def test_validation_object(self):
        schema = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "address": {
                    "type": "object",
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"},
                    },
                    "required": ["street", "city"],
                },
            },
            "required": ["address"],
        }

        model = SchemaConverter.build(schema)

        obj = model(address={"street": "123 Main St", "city": "Springfield"})

        self.assertEqual(obj.address.street, "123 Main St")
        self.assertEqual(obj.address.city, "Springfield")
