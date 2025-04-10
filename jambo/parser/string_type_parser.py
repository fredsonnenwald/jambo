from jambo.parser._type_parser import GenericTypeParser
from jambo.utils.properties_builder.mappings_properties_builder import (
    mappings_properties_builder,
)


class StringTypeParser(GenericTypeParser):
    mapped_type = str

    json_schema_type = "string"

    @staticmethod
    def from_properties(name, properties):
        _mappings = {
            "maxLength": "max_length",
            "minLength": "min_length",
            "pattern": "pattern",
        }

        return str, mappings_properties_builder(properties, _mappings)
