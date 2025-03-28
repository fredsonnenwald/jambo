from jsonschema_pydantic.types._type_parser import GenericTypeParser

from typing import TypeVar

V = TypeVar("V")


class ArrayTypeParser(GenericTypeParser):
    mapped_type = list

    json_schema_type = "array"

    @classmethod
    def from_properties(cls, name, properties):
        _item_type, _item_args = GenericTypeParser.get_impl(
            properties["items"]["type"]
        ).from_properties(name, properties["items"])

        return list[_item_type], {}
