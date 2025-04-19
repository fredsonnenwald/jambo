from jambo.parser._type_parser import GenericTypeParser
from jambo.utils.properties_builder.mappings_properties_builder import (
    mappings_properties_builder,
)

import copy
from typing import TypeVar


V = TypeVar("V")


class ArrayTypeParser(GenericTypeParser):
    mapped_type = list

    json_schema_type = "array"

    @staticmethod
    def from_properties(name, properties, required=False):
        _item_type, _item_args = GenericTypeParser.get_impl(
            properties["items"]["type"]
        ).from_properties(name, properties["items"], required=True)

        _mappings = {
            "maxItems": "max_length",
            "minItems": "min_length",
        }

        wrapper_type = set if properties.get("uniqueItems", False) else list
        field_type = wrapper_type[_item_type]

        mapped_properties = mappings_properties_builder(
            properties,
            _mappings,
            required=required,
            default_mappings={"description": "description"},
        )

        default_list = properties.get("default")
        if default_list is not None:
            ArrayTypeParser.validate_default(
                field_type,
                mapped_properties,
                default_list,
            )

            if wrapper_type is list:
                mapped_properties["default_factory"] = lambda: copy.deepcopy(
                    wrapper_type(default_list)
                )
            else:
                mapped_properties["default_factory"] = lambda: wrapper_type(
                    default_list
                )

        if "default_factory" in mapped_properties and "default" in mapped_properties:
            del mapped_properties["default"]

        return field_type, mapped_properties
