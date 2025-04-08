from jambo.parser._type_parser import GenericTypeParser


class BooleanTypeParser(GenericTypeParser):
    mapped_type = bool

    json_schema_type = "boolean"

    @staticmethod
    def from_properties(name, properties):
        return bool, {}
