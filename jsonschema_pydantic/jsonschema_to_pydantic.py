from jsonschema.exceptions import SchemaError
from jsonschema.protocols import Validator
from pydantic import create_model
from pydantic.fields import Field

import warnings
from typing import Type

_base_type_mappings = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
    "array": ...,
    "object": ...,
}


class ModelSchemaBuilder:
    @staticmethod
    def build(
        schema: dict,
    ):
        try:
            Validator.check_schema(schema)
        except SchemaError as e:
            raise ValueError(f"Invalid JSON Schema: {e}")

        if schema["type"] != "object":
            raise TypeError(
                f"Invalid JSON Schema: {schema['type']}. Only 'object' can be converted to Pydantic models."
            )

        return ModelSchemaBuilder._build_model_from_properties(
            schema["title"], schema["properties"], schema.get("required", [])
        )

    @staticmethod
    def _parse_properties(
        properties: dict, required_keys=None
    ) -> dict[str, tuple[type, Field]]:
        required_keys = required_keys or []

        fields = {}
        for name, prop in properties.items():
            fields[name] = ModelSchemaBuilder._build_field(name, prop, required_keys)

        return fields

    @staticmethod
    def _build_field(
        name, properties: dict, required_keys: list[str]
    ) -> tuple[type, Field]:
        _field_type = None
        _field_args = {}

        match properties["type"]:
            case "object":
                _field_type, _field_args = ModelSchemaBuilder._build_field_object(
                    name, properties
                )
            case "array":
                _field_type, _field_args = ModelSchemaBuilder._build_field_array(
                    name, properties
                )
            case "string":
                _field_type, _field_args = ModelSchemaBuilder._build_field_string(
                    properties
                )
            case "boolean":
                _field_type, _field_args = ModelSchemaBuilder._build_field_boolean(
                    properties
                )
            case "integer":
                _field_type, _field_args = ModelSchemaBuilder._build_field_int(
                    properties
                )
            case "number":
                _field_type, _field_args = ModelSchemaBuilder._build_field_float(
                    properties
                )
            case _:
                raise ValueError(f"Unsupported type: {properties['type']}")

        if description := properties.get("description"):
            _field_args["description"] = description
        else:
            warnings.warn(
                f"Property {name} is missing a description. We highly recommend adding one."
            )

        _default_value = ... if name in required_keys else None
        return _field_type, Field(_default_value, *_field_args)

    @staticmethod
    def _build_field_object(name, properties: dict) -> tuple[type, dict[str, any]]:
        _field_type = ModelSchemaBuilder._build_model_from_properties(
            name, properties["properties"], properties.get("required", [])
        )
        return _field_type, {}

    @staticmethod
    def _build_field_array(name, properties: dict) -> tuple[type, dict[str, any]]:
        _item_type = properties["items"]["type"]
        if _item_type == "object":
            _item_type = ModelSchemaBuilder._build_model_from_properties(
                name, properties["items"]["properties"]
            )
        else:
            _item_type = _base_type_mappings[_item_type]

        return list[_item_type], {}

    @staticmethod
    def _build_field_string(properties: dict) -> tuple[type, dict[str, any]]:
        return str, {}

    @staticmethod
    def _build_field_boolean(properties: dict) -> tuple[type, dict[str, any]]:
        return bool, {}

    @staticmethod
    def _build_field_int(properties: dict) -> tuple[type, dict[str, any]]:
        return int, {}

    @staticmethod
    def _build_field_float(properties: dict) -> tuple[type, dict[str, any]]:
        return float, {}

    @staticmethod
    def _build_model_from_properties(
        model_name: str, model_properties: dict, required_keys: list[str]
    ) -> Type:
        properties = ModelSchemaBuilder._parse_properties(
            model_properties, required_keys
        )

        return create_model(model_name, **properties)
