from jambo.parser._type_parser import GenericTypeParser

import gc
from contextlib import contextmanager
from unittest import TestCase


@contextmanager
def with_test_parser():
    class InvalidGenericTypeParser(GenericTypeParser):
        mapped_type = str
        json_schema_type = "type:invalid"

        def from_properties(
            self, name: str, properties: dict[str, any], required: bool = False
        ): ...

    try:
        yield InvalidGenericTypeParser
    finally:
        del InvalidGenericTypeParser
        gc.collect()


class TestGenericTypeParser(TestCase):
    def test_invalid_get_impl(self):
        # Assuming GenericTypeParser is imported from the module
        with (
            with_test_parser(),
            self.assertRaises(ValueError),
        ):
            GenericTypeParser._get_impl({"type": "another_invalid_type"})

    def test_invalid_json_schema_type(self):
        # This is more for the developer's sanity check
        with (
            with_test_parser() as InvalidGenericTypeParser,
            self.assertRaises(RuntimeError),
        ):
            InvalidGenericTypeParser.json_schema_type = None
            GenericTypeParser._get_impl({"type": "another_invalid_type"})

    def test_invalid_mappings_properties_builder(self):
        with (
            with_test_parser() as InvalidGenericTypeParser,
            self.assertRaises(NotImplementedError),
        ):
            parser = InvalidGenericTypeParser()
            parser.mappings_properties_builder({}, required=False)
