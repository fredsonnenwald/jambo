from jambo.parser._type_parser import GenericTypeParser
from jambo.utils.properties_builder.mappings_properties_builder import (
    mappings_properties_builder,
)


class BooleanTypeParser(GenericTypeParser):
    mapped_type = bool

    json_schema_type = "boolean"

    @staticmethod
    def from_properties(name, properties, required=False):
        _mappings = {
            "default": "default",
        }

        mapped_properties = mappings_properties_builder(properties, _mappings, required)

        default_value = properties.get("default")
        if default_value is not None and not isinstance(default_value, bool):
            raise ValueError(f"Default value for {name} must be a boolean.")

        return bool, mapped_properties
