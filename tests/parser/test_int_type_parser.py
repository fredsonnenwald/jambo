from jambo.parser import IntTypeParser

from unittest import TestCase


class TestIntTypeParser(TestCase):
    def test_int_parser_no_options(self):
        parser = IntTypeParser()

        properties = {"type": "integer"}

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, int)
        self.assertEqual(type_validator, {})

    def test_int_parser_with_options(self):
        parser = IntTypeParser()

        properties = {
            "type": "integer",
            "maximum": 10,
            "minimum": 1,
            "multipleOf": 2,
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, int)
        self.assertEqual(type_validator["le"], 10)
        self.assertEqual(type_validator["ge"], 1)
        self.assertEqual(type_validator["multiple_of"], 2)

    def test_int_parser_with_default(self):
        parser = IntTypeParser()

        properties = {
            "type": "integer",
            "default": 6,
            "maximum": 10,
            "minimum": 1,
            "multipleOf": 2,
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, int)
        self.assertEqual(type_validator["default"], 6)
        self.assertEqual(type_validator["le"], 10)
        self.assertEqual(type_validator["ge"], 1)
        self.assertEqual(type_validator["multiple_of"], 2)

    def test_int_parser_with_default_invalid_type(self):
        parser = IntTypeParser()

        properties = {
            "type": "integer",
            "default": "invalid",  # Invalid default value
            "maximum": 10,
            "minimum": 1,
            "multipleOf": 2,
        }

        with self.assertRaises(ValueError) as context:
            parser.from_properties("placeholder", properties)

        self.assertEqual(
            str(context.exception),
            "Default value must be a number, got str",
        )

    def test_int_parser_with_default_invalid_maximum(self):
        parser = IntTypeParser()

        properties = {
            "type": "integer",
            "default": 15,
            "maximum": 10,
            "minimum": 1,
            "multipleOf": 2,
        }

        with self.assertRaises(ValueError) as context:
            parser.from_properties("placeholder", properties)

        self.assertEqual(
            str(context.exception),
            "Default value exceeds maximum limit of 10",
        )

    def test_int_parser_with_default_invalid_minimum(self):
        parser = IntTypeParser()

        properties = {
            "type": "integer",
            "default": -5,
            "maximum": 10,
            "minimum": 1,
            "multipleOf": 2,
        }

        with self.assertRaises(ValueError) as context:
            parser.from_properties("placeholder", properties)

        self.assertEqual(
            str(context.exception),
            "Default value is below minimum limit of 1",
        )

    def test_int_parser_with_default_invalid_exclusive_maximum(self):
        parser = IntTypeParser()

        properties = {
            "type": "integer",
            "default": 10,
            "exclusiveMaximum": 10,
            "minimum": 1,
            "multipleOf": 2,
        }

        with self.assertRaises(ValueError) as context:
            parser.from_properties("placeholder", properties)

        self.assertEqual(
            str(context.exception),
            "Default value exceeds exclusive maximum limit of 10",
        )

    def test_int_parser_with_default_invalid_exclusive_minimum(self):
        parser = IntTypeParser()

        properties = {
            "type": "integer",
            "default": 1,
            "exclusiveMinimum": 1,
            "maximum": 10,
            "multipleOf": 2,
        }

        with self.assertRaises(ValueError) as context:
            parser.from_properties("placeholder", properties)

        self.assertEqual(
            str(context.exception),
            "Default value is below exclusive minimum limit of 1",
        )

    def test_int_parser_with_default_invalid_multipleOf(self):
        parser = IntTypeParser()

        properties = {
            "type": "integer",
            "default": 5,
            "maximum": 10,
            "minimum": 1,
            "multipleOf": 2,
        }

        with self.assertRaises(ValueError) as context:
            parser.from_properties("placeholder", properties)

        self.assertEqual(
            str(context.exception),
            "Default value 5 is not a multiple of 2",
        )
