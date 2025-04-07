from dataclasses import Field

from jambo.types._type_parser import GenericTypeParser


class IntTypeParser(GenericTypeParser):
    mapped_type = int

    json_schema_type = "integer"

    @staticmethod
    def from_properties(name, properties):
        _field_properties = dict()

        if "minimum" in properties:
            _field_properties["ge"] = properties["minimum"]

        if "maximum" in properties:
            _field_properties["le"] = properties["maximum"]

        if "multipleOf" in properties:
            _field_properties["multiple_of"] = properties["multipleOf"]

        return int, Field(**_field_properties)
