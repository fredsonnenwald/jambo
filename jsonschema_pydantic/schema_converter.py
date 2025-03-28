from jsonschema_pydantic.types import GenericTypeParser

from jsonschema.exceptions import SchemaError
from jsonschema.protocols import Validator
from pydantic import create_model
from pydantic.fields import Field

import warnings
from typing import Type


class SchemaConverter:
    @staticmethod
    def build(schema):
        try:
            Validator.check_schema(schema)
        except SchemaError as e:
            raise ValueError(f"Invalid JSON Schema: {e}")

        if schema["type"] != "object":
            raise TypeError(
                f"Invalid JSON Schema: {schema['type']}. Only 'object' can be converted to Pydantic models."
            )

        return SchemaConverter.build_object(schema["title"], schema)

    @staticmethod
    def build_object(
        name: str,
        schema: dict,
    ):
        if schema["type"] != "object":
            raise TypeError(
                f"Invalid JSON Schema: {schema['type']}. Only 'object' can be converted to Pydantic models."
            )

        return SchemaConverter._build_model_from_properties(
            name, schema["properties"], schema.get("required", [])
        )

    @staticmethod
    def _build_model_from_properties(
        model_name: str, model_properties: dict, required_keys: list[str]
    ) -> Type:
        properties = SchemaConverter._parse_properties(model_properties, required_keys)

        return create_model(model_name, **properties)

    @staticmethod
    def _parse_properties(
        properties: dict, required_keys=None
    ) -> dict[str, tuple[type, Field]]:
        required_keys = required_keys or []

        fields = {}
        for name, prop in properties.items():
            fields[name] = SchemaConverter._build_field(name, prop, required_keys)

        return fields

    @staticmethod
    def _build_field(
        name, properties: dict, required_keys: list[str]
    ) -> tuple[type, Field]:
        _field_type, _field_args = GenericTypeParser.get_impl(
            properties["type"]
        ).from_properties(name, properties)

        _field_args = _field_args or {}

        if description := properties.get("description"):
            _field_args["description"] = description
        else:
            warnings.warn(
                f"Property {name} is missing a description. We highly recommend adding one."
            )

        _default_value = ... if name in required_keys else None
        return _field_type, Field(_default_value, **_field_args)
