from jsonschema_pydantic.types import (
    ArrayTypeParser,
    FloatTypeParser,
    GenericTypeParser,
    IntTypeParser,
    ObjectTypeParser,
    StringTypeParser,
)

import unittest


class TestTypeParser(unittest.TestCase):
    def test_get_impl(self):
        self.assertEqual(GenericTypeParser.get_impl("integer"), IntTypeParser)
        self.assertEqual(GenericTypeParser.get_impl("string"), StringTypeParser)
        self.assertEqual(GenericTypeParser.get_impl("number"), FloatTypeParser)
        self.assertEqual(GenericTypeParser.get_impl("object"), ObjectTypeParser)
        self.assertEqual(GenericTypeParser.get_impl("array"), ArrayTypeParser)

    def test_int_parser(self):
        parser = IntTypeParser()
        expected_definition = (int, {})

        self.assertEqual(parser.from_properties("placeholder", {}), expected_definition)

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
        expected_definition = (object, {})

        self.assertEqual(parser.from_properties("placeholder", {}), expected_definition)

    def test_array_parser(self):
        parser = ArrayTypeParser()
        expected_definition = (list[str], {})

        properties = {"items": {"type": "string"}}

        self.assertEqual(
            parser.from_properties("placeholder", properties), expected_definition
        )
