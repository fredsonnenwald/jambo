from jsonschema_pydantic.types._type_parser import GenericTypeParser


class StringTypeParser(GenericTypeParser):
    mapped_type = str

    json_schema_type = "string"

    @staticmethod
    def from_properties(name, properties):
        return str, {}
