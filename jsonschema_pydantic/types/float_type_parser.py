from jsonschema_pydantic.types._type_parser import GenericTypeParser


class FloatTypeParser(GenericTypeParser):
    mapped_type = float

    json_schema_type = "number"

    @staticmethod
    def from_properties(name, properties):
        return float, {}
