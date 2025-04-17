from jambo.parser._type_parser import GenericTypeParser

from typing import Union


class AnyOfTypeParser(GenericTypeParser):
    mapped_type = Union

    json_schema_type = "anyOf"

    @staticmethod
    def from_properties(name, properties):
        if "anyOf" not in properties:
            raise ValueError(f"Invalid JSON Schema: {properties}")

        if not isinstance(properties["anyOf"], list):
            raise ValueError(f"Invalid JSON Schema: {properties['anyOf']}")

        subProperties = properties["anyOf"]

        types = [
            GenericTypeParser.get_impl(subProperty["type"]).from_properties(
                name, subProperty
            )
            for subProperty in subProperties
        ]

        return Union[*(t for t, v in types)], {}
