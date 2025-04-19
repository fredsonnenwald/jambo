from jambo.parser import StringTypeParser

from unittest import TestCase


class TestStringTypeParser(TestCase):
    def test_string_parser_no_options(self):
        parser = StringTypeParser()

        properties = {"type": "string"}

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, str)

    def test_string_parser_with_options(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "maxLength": 10,
            "minLength": 1,
            "pattern": "^[a-zA-Z]+$",
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, str)
        self.assertEqual(type_validator["max_length"], 10)
        self.assertEqual(type_validator["min_length"], 1)
        self.assertEqual(type_validator["pattern"], "^[a-zA-Z]+$")

    def test_string_parser_with_default_value(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "default": "default_value",
            "maxLength": 20,
            "minLength": 5,
        }

        type_parsing, type_validator = parser.from_properties("placeholder", properties)

        self.assertEqual(type_parsing, str)
        self.assertEqual(type_validator["default"], "default_value")
        self.assertEqual(type_validator["max_length"], 20)
        self.assertEqual(type_validator["min_length"], 5)

    def test_string_parser_with_invalid_default_value_type(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "default": 12345,  # Invalid default value
            "maxLength": 20,
            "minLength": 5,
        }

        with self.assertRaises(ValueError):
            parser.from_properties("placeholder", properties)

    def test_string_parser_with_default_invalid_maxlength(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "default": "default_value",
            "maxLength": 2,
            "minLength": 1,
        }

        with self.assertRaises(ValueError):
            parser.from_properties("placeholder", properties)

    def test_string_parser_with_default_invalid_minlength(self):
        parser = StringTypeParser()

        properties = {
            "type": "string",
            "default": "a",
            "maxLength": 20,
            "minLength": 2,
        }

        with self.assertRaises(ValueError):
            parser.from_properties("placeholder", properties)
