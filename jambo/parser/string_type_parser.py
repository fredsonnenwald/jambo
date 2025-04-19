from jambo.parser._type_parser import GenericTypeParser
from jambo.utils.properties_builder.mappings_properties_builder import (
    mappings_properties_builder,
)


class StringTypeParser(GenericTypeParser):
    mapped_type = str

    json_schema_type = "string"

    @staticmethod
    def from_properties(name, properties, required=False):
        _mappings = {
            "maxLength": "max_length",
            "minLength": "min_length",
            "pattern": "pattern",
        }

        mapped_properties = mappings_properties_builder(properties, _mappings, required)

        default_value = properties.get("default")
        if default_value is not None:
            StringTypeParser.validate_default(str, mapped_properties, default_value)

        return str, mapped_properties
