from jambo.parser import (
    ArrayTypeParser,
    FloatTypeParser,
    GenericTypeParser,
    IntTypeParser,
    ObjectTypeParser,
    StringTypeParser,
)

import unittest
from typing import get_args


class TestTypeParser(unittest.TestCase):
    def test_get_impl(self):
        self.assertEqual(GenericTypeParser.get_impl("integer"), IntTypeParser)
        self.assertEqual(GenericTypeParser.get_impl("string"), StringTypeParser)
        self.assertEqual(GenericTypeParser.get_impl("number"), FloatTypeParser)
        self.assertEqual(GenericTypeParser.get_impl("object"), ObjectTypeParser)
        self.assertEqual(GenericTypeParser.get_impl("array"), ArrayTypeParser)

    def test_int_parser(self):
        parser = IntTypeParser()

        type_parsing, type_validator = parser.from_properties(
            "placeholder",
            {
                "type": "integer",
                "minimum": 0,
                "exclusiveMinimum": 1,
                "maximum": 10,
                "exclusiveMaximum": 11,
                "multipleOf": 2,
            },
        )

        self.assertEqual(type_parsing, int)
        self.assertEqual(type_validator["ge"], 0)
        self.assertEqual(type_validator["gt"], 1)
        self.assertEqual(type_validator["le"], 10)
        self.assertEqual(type_validator["lt"], 11)
        self.assertEqual(type_validator["multiple_of"], 2)

    def test_float_parser(self):
        parser = FloatTypeParser()

        type_parsing, type_validator = parser.from_properties(
            "placeholder",
            {
                "type": "number",
                "minimum": 0,
                "exclusiveMinimum": 1,
                "maximum": 10,
                "exclusiveMaximum": 11,
                "multipleOf": 2,
            },
        )

        self.assertEqual(type_parsing, float)
        self.assertEqual(type_validator["ge"], 0)
        self.assertEqual(type_validator["gt"], 1)
        self.assertEqual(type_validator["le"], 10)
        self.assertEqual(type_validator["lt"], 11)
        self.assertEqual(type_validator["multiple_of"], 2)

    def test_string_parser(self):
        parser = StringTypeParser()

        type_parsing, type_validator = parser.from_properties(
            "placeholder",
            {
                "type": "string",
                "maxLength": 10,
                "minLength": 1,
                "pattern": "[a-zA-Z0-9]",
            },
        )

        self.assertEqual(type_parsing, str)
        self.assertEqual(type_validator["max_length"], 10)
        self.assertEqual(type_validator["min_length"], 1)
        self.assertEqual(type_validator["pattern"], "[a-zA-Z0-9]")

    def test_object_parser(self):
        parser = ObjectTypeParser()

        properties = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
            },
        }

        Model, _args = parser.from_properties("placeholder", properties)

        obj = Model(name="name", age=10)

        self.assertEqual(obj.name, "name")
        self.assertEqual(obj.age, 10)

    def test_array_of_string_parser(self):
        parser = ArrayTypeParser()
        expected_definition = (list[str], {})

        properties = {"items": {"type": "string"}}

        self.assertEqual(
            parser.from_properties("placeholder", properties), expected_definition
        )

    def test_array_of_object_parser(self):
        parser = ArrayTypeParser()

        properties = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                },
            },
            "maxItems": 10,
            "minItems": 1,
            "uniqueItems": True,
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing.__origin__, set)
        self.assertEqual(type_validator["max_length"], 10)
        self.assertEqual(type_validator["min_length"], 1)

        Model = get_args(type_parsing)[0]
        obj = Model(name="name", age=10)

        self.assertEqual(obj.name, "name")
        self.assertEqual(obj.age, 10)
