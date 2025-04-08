from jambo.parser._type_parser import GenericTypeParser
from jambo.utils.properties_builder.numeric_properties_builder import numeric_properties_builder


class FloatTypeParser(GenericTypeParser):
    mapped_type = float

    json_schema_type = "number"

    @staticmethod
    def from_properties(name, properties):
        return float, numeric_properties_builder(properties)
