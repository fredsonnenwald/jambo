from jambo.parser._type_parser import GenericTypeParser
from jambo.utils.properties_builder.numeric_properties_builder import numeric_properties_builder


class IntTypeParser(GenericTypeParser):
    mapped_type = int

    json_schema_type = "integer"

    @staticmethod
    def from_properties(name, properties):
        return int, numeric_properties_builder(properties)
