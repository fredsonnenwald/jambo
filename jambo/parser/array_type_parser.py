from jambo.parser._type_parser import GenericTypeParser

from typing import TypeVar

from jambo.utils.properties_builder.mappings_properties_builder import (
    mappings_properties_builder,
)

V = TypeVar("V")


class ArrayTypeParser(GenericTypeParser):
    mapped_type = list

    json_schema_type = "array"

    @classmethod
    def from_properties(cls, name, properties):
        _item_type, _item_args = GenericTypeParser.get_impl(
            properties["items"]["type"]
        ).from_properties(name, properties["items"])

        _mappings = {
            "maxItems": "max_items",
            "minItems": "min_items",
            "uniqueItems": "unique_items",
        }

        return list[_item_type], mappings_properties_builder(properties, _mappings)
