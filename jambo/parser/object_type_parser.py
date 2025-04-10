from jambo.parser._type_parser import GenericTypeParser


class ObjectTypeParser(GenericTypeParser):
    mapped_type = object

    json_schema_type = "object"

    @staticmethod
    def from_properties(name, properties):
        from jambo.schema_converter import SchemaConverter

        return (
            SchemaConverter.build_object(name, properties),
            {},  # The second argument is not used in this case
        )
