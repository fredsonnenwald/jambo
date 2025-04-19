from jambo.parser._type_parser import GenericTypeParser
from jambo.utils.properties_builder.mappings_properties_builder import (
    mappings_properties_builder,
)


class IntTypeParser(GenericTypeParser):
    mapped_type = int

    json_schema_type = "integer"

    @staticmethod
    def from_properties(name, properties, required=False):
        _mappings = {
            "minimum": "ge",
            "exclusiveMinimum": "gt",
            "maximum": "le",
            "exclusiveMaximum": "lt",
            "multipleOf": "multiple_of",
            "default": "default",
        }
        mapped_properties = mappings_properties_builder(properties, _mappings, required)

        default_value = mapped_properties.get("default")
        if default_value is not None:
            IntTypeParser.validate_default(int, mapped_properties, default_value)

        return int, mapped_properties
