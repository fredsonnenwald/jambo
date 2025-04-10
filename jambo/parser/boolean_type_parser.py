from jambo.parser._type_parser import GenericTypeParser
from jambo.utils.properties_builder.mappings_properties_builder import (
    mappings_properties_builder,
)


class BooleanTypeParser(GenericTypeParser):
    mapped_type = bool

    json_schema_type = "boolean"

    @staticmethod
    def from_properties(name, properties):
        _mappings = {
            "default": "default",
        }
        return bool, mappings_properties_builder(properties, _mappings)
