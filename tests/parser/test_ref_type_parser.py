from jambo.parser import RefTypeParser

from unittest import TestCase


class TestRefTypeParser(TestCase):
    def test_ref_type_parser_local_ref(self):
        properties = {
            "title": "person",
            "$ref": "#/$defs/person",
            "$defs": {
                "person": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "age": {"type": "integer"},
                    },
                }
            },
        }

        type_parsing, type_validator = RefTypeParser().from_properties(
            properties=properties,
            name="placeholder",
            context=properties,
            required=True,
        )

        self.assertIsInstance(type_parsing, type)

        obj = type_parsing(name="John", age=30)

        self.assertEqual(obj.name, "John")
        self.assertEqual(obj.age, 30)
