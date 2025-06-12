from jambo.parser import ObjectTypeParser, RefTypeParser

from typing_extensions import ForwardRef, get_type_hints

from unittest import TestCase


class TestRefTypeParser(TestCase):
    def test_ref_type_parser_with_def(self):
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
            "person",
            properties,
            context=properties,
            required=True,
        )

        self.assertIsInstance(type_parsing, type)

        obj = type_parsing(name="John", age=30)

        self.assertEqual(obj.name, "John")
        self.assertEqual(obj.age, 30)

    def test_ref_type_parser_with_forward_ref(self):
        properties = {
            "title": "person",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "emergency_contact": {
                    "$ref": "#",
                },
            },
        }

        type_parsing, type_validator = ObjectTypeParser().from_properties(
            "person",
            properties,
            context=properties,
            required=True,
        )
        type_parsing.update_forward_refs(person=type_parsing)

        self.assertIsInstance(type_parsing, type)

        type_hints = get_type_hints(type_parsing, globals(), locals())

        self.assertIsInstance(type_hints["emergency_contact"], ForwardRef)

        """
        This is a example of how to resolve ForwardRef in a dynamic model:
        ```python
            from typing import get_type_hints
            
            # Make sure your dynamic model has a name
            model = type_parsing
            model.update_forward_refs(person=model)  # 👈 resolve the ForwardRef("person")
            
            # Inject into globals manually
            globalns = globals().copy()
            globalns['person'] = model
            
            # Now you can get the resolved hints
            type_hints = get_type_hints(model, globalns=globalns)
        ```
        Use `TypeParserOptions.ref_cache` option to cache and resolve ForwardRefs
        inside the ObjectTypeParser.to_model method.
        """
