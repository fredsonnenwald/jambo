from jambo.parser._type_parser import GenericTypeParser

from pydantic import Field, create_model
from pydantic.main import ModelT

from typing import Any


class ObjectTypeParser(GenericTypeParser):
    mapped_type = object

    json_schema_type = "type:object"

    def from_properties(
        self, name: str, properties: dict[str, Any], required: bool = False
    ):
        type_parsing = self.to_model(
            name, properties.get("properties", {}), properties.get("required", [])
        )
        type_properties = {}

        if "default" in properties:
            type_properties["default_factory"] = lambda: type_parsing.model_validate(
                properties["default"]
            )

        return type_parsing, type_properties

    def to_model(
        self, name: str, schema: dict[str, Any], required_keys: list[str], **kwargs
    ) -> type[ModelT]:
        """
        Converts JSON Schema object properties to a Pydantic model.
        :param name: The name of the model.
        :param properties: The properties of the JSON Schema object.
        :param required_keys: List of required keys in the schema.
        :return: A Pydantic model class.
        """
        fields = self._parse_properties(schema, required_keys, **kwargs)
        return create_model(name, **fields)

    @staticmethod
    def _parse_properties(
        properties: dict[str, Any], required_keys: list[str], **kwargs
    ) -> dict[str, tuple[type, Field]]:
        required_keys = required_keys or []

        fields = {}
        for name, prop in properties.items():
            is_required = name in required_keys
            parsed_type, parsed_properties = GenericTypeParser.type_from_properties(
                name, prop, required=is_required, **kwargs
            )
            fields[name] = (parsed_type, Field(**parsed_properties))

        return fields
