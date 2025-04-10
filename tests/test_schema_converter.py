from jambo.schema_converter import SchemaConverter

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
                "name": {"type": "string", "maxLength": 4, "minLength": 1},
                "email": {
                    "type": "string",
                    "maxLength": 50,
                    "minLength": 5,
                    "pattern": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
                },
            },
            "required": ["name"],
        }

        model = SchemaConverter.build(schema)

        self.assertEqual(model(name="John", age=30).name, "John")

        with self.assertRaises(ValueError):
            model(name=123, age=30, email="teste@hideyoshi.com")

        with self.assertRaises(ValueError):
            model(name="John Invalid", age=45, email="teste@hideyoshi.com")

        with self.assertRaises(ValueError):
            model(name="", age=45, email="teste@hideyoshi.com")

        with self.assertRaises(ValueError):
            model(name="John", age=45, email="hideyoshi.com")

    def test_validation_integer(self):
        schema = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "age": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 120,
                },
            },
            "required": ["age"],
        }

        model = SchemaConverter.build(schema)

        self.assertEqual(model(age=30).age, 30)

        with self.assertRaises(ValueError):
            model(age=-1)

        with self.assertRaises(ValueError):
            model(age=121)

    def test_validation_float(self):
        schema = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "age": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 120,
                },
            },
            "required": ["age"],
        }

        model = SchemaConverter.build(schema)

        self.assertEqual(model(age=30).age, 30.0)

        with self.assertRaises(ValueError):
            model(age=-1.0)

        with self.assertRaises(ValueError):
            model(age=121.0)

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
                "friends": {
                    "type": "array",
                    "items": {"type": "string"},
                    "minItems": 1,
                    "maxItems": 2,
                    "uniqueItems": True,
                },
            },
            "required": ["friends"],
        }

        model = SchemaConverter.build(schema)

        self.assertEqual(
            model(friends=["John", "Jane", "John"]).friends, {"John", "Jane"}
        )

        with self.assertRaises(ValueError):
            model(friends=[])

        with self.assertRaises(ValueError):
            model(friends=["John", "Jane", "Invalid"])

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

    def test_default_for_string(self):
        schema = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "default": "John",
                },
            },
            "required": ["name"],
        }

        model = SchemaConverter.build(schema)

        obj = model(name="John")

        self.assertEqual(obj.name, "John")

        # Test for default with maxLength
        schema_max_length = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "default": "John",
                    "maxLength": 2,
                },
            },
            "required": ["name"],
        }

        with self.assertRaises(ValueError):
            SchemaConverter.build(schema_max_length)

    def test_default_for_list(self):
        schema_list = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "friends": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["John", "Jane"],
                },
            },
            "required": ["friends"],
        }

        model_list = SchemaConverter.build(schema_list)

        self.assertEqual(model_list().friends, ["John", "Jane"])

        # Test for default with uniqueItems
        schema_set = {
            "title": "Person",
            "description": "A person",
            "type": "object",
            "properties": {
                "friends": {
                    "type": "array",
                    "items": {"type": "string"},
                    "default": ["John", "Jane"],
                    "uniqueItems": True,
                },
            },
            "required": ["friends"],
        }

        model_set = SchemaConverter.build(schema_set)

        self.assertEqual(model_set().friends, {"John", "Jane"})
