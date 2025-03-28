from jsonschema_pydantic.types._type_parser import GenericTypeParser

from typing import TypeVar

V = TypeVar("V")


class ArrayTypeParser(GenericTypeParser):
    mapped_type = list

    json_schema_type = "array"

    @classmethod
    def from_properties(cls, name, properties):
        _item_type = properties["items"]["type"]
        if _item_type == "object":
            _item_type = type
        else:
            _item_type = GenericTypeParser.get_impl(_item_type).mapped_type

        return list[_item_type], {}
