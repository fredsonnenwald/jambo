from jambo.types import (
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

        type_parsing, type_validator = parser.from_properties("placeholder", {})

        self.assertEqual(type_parsing, int)

    def test_float_parser(self):
        parser = FloatTypeParser()
        expected_definition = (float, {})

        self.assertEqual(parser.from_properties("placeholder", {}), expected_definition)

    def test_string_parser(self):
        parser = StringTypeParser()
        expected_definition = (str, {})

        self.assertEqual(parser.from_properties("placeholder", {}), expected_definition)

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
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"},
                },
            }
        }

        _type, _args = parser.from_properties("placeholder", properties)

        Model = get_args(_type)[0]
        obj = Model(name="name", age=10)

        self.assertEqual(obj.name, "name")
        self.assertEqual(obj.age, 10)
