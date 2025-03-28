from jsonschema_pydantic.types._type_parser import GenericTypeParser


class ObjectTypeParser(GenericTypeParser):
    mapped_type = object

    json_schema_type = "object"

    @staticmethod
    def from_properties(name, properties):
        from jsonschema_pydantic.schema_converter import SchemaConverter

        _type = SchemaConverter.build_object(name, properties)
        return _type, {}
