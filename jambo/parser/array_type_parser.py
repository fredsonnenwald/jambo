import copy

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
            "maxItems": "max_length",
            "minItems": "min_length",
        }

        wrapper_type = set if properties.get("uniqueItems", False) else list

        mapped_properties = mappings_properties_builder(
            properties, _mappings, {"description": "description"}
        )

        if "default" in properties:
            default_list = properties["default"]
            if not isinstance(default_list, list):
                raise ValueError(
                    f"Default value must be a list, got {type(default_list).__name__}"
                )

            if len(default_list) > properties.get("maxItems", float("inf")):
                raise ValueError(
                    f"Default list exceeds maxItems limit of {properties.get('maxItems')}"
                )

            if len(default_list) < properties.get("minItems", 0):
                raise ValueError(
                    f"Default list is below minItems limit of {properties.get('minItems')}"
                )

            if not all(isinstance(item, _item_type) for item in default_list):
                raise ValueError(
                    f"All items in the default list must be of type {_item_type.__name__}"
                )

            if wrapper_type is list:
                mapped_properties["default_factory"] = lambda: copy.deepcopy(
                    wrapper_type(default_list)
                )
            else:
                mapped_properties["default_factory"] = lambda: wrapper_type(
                    default_list
                )

        return wrapper_type[_item_type], mapped_properties
