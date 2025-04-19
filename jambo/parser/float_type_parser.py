from jambo.parser._type_parser import GenericTypeParser
from jambo.utils.properties_builder.mappings_properties_builder import (
    mappings_properties_builder,
)


class FloatTypeParser(GenericTypeParser):
    mapped_type = float

    json_schema_type = "number"

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
            FloatTypeParser.validate_default(float, mapped_properties, default_value)

        return float, mapped_properties
