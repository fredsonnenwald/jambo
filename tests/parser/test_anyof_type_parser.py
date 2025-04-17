from jambo.parser.anyof_type_parser import AnyOfTypeParser

from typing import Union, get_args, get_origin
from unittest import TestCase


class TestAnyOfTypeParser(TestCase):
    def test_any_of_string_or_int(self):
        """
        Tests the AnyOfTypeParser with a string or int type.
        """

        properties = {
            "anyOf": [
                {"type": "string"},
                {"type": "integer"},
            ],
        }

        type_parsing, _ = AnyOfTypeParser.from_properties("placeholder", properties)

        # check union type has string and int
        self.assertEqual(get_origin(type_parsing), Union)
        self.assertIn(str, get_args(type_parsing))
        self.assertIn(int, get_args(type_parsing))
