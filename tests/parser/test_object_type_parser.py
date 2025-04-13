from unittest import TestCase

from jambo.parser import ObjectTypeParser


class TestObjectTypeParser(TestCase):
    def test_object_type_parser(self):
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
