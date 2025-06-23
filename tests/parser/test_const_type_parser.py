from typing_extensions import Annotated, get_args, get_origin
from webbrowser import get
from jambo.parser import ConstTypeParser

from unittest import TestCase


class TestConstTypeParser(TestCase):
    def test_parse_const_type(self):
        parser = ConstTypeParser()

        expected_const_value = "United States of America"
        properties = {
            "const": expected_const_value
        }

        parsed_type, parsed_properties = parser.from_properties(
            "country", properties
        )

        self.assertEqual(get_origin(parsed_type), Annotated)

        self.assertIn(str, get_args(parsed_type))