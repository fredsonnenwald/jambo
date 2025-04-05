from jambo.types._type_parser import GenericTypeParser


class IntTypeParser(GenericTypeParser):
    mapped_type = int

    json_schema_type = "integer"

    @staticmethod
    def from_properties(name, properties):
        return int, {}
