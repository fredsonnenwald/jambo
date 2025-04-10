from jambo.parser import GenericTypeParser

from jsonschema.exceptions import SchemaError
from jsonschema.protocols import Validator
from pydantic import create_model
from pydantic.fields import Field

from typing import Type

from jambo.types.json_schema_type import JSONSchema


class SchemaConverter:
    """
    Converts JSON Schema to Pydantic models.

    This class is responsible for converting JSON Schema definitions into Pydantic models.
    It validates the schema and generates the corresponding Pydantic model with appropriate
    fields and types. The generated model can be used for data validation and serialization.
    """

    @staticmethod
    def build(schema: JSONSchema) -> Type:
        """
        Converts a JSON Schema to a Pydantic model.
        :param schema: The JSON Schema to convert.
        :return: A Pydantic model class.
        """
        if "title" not in schema:
            raise ValueError("JSON Schema must have a title.")

        return SchemaConverter.build_object(schema["title"], schema)

    @staticmethod
    def build_object(
        name: str,
        schema: JSONSchema,
    ) -> Type:
        """
        Converts a JSON Schema object to a Pydantic model given a name.
        :param name:
        :param schema:
        :return:
        """

        try:
            Validator.check_schema(schema)
        except SchemaError as e:
            raise ValueError(f"Invalid JSON Schema: {e}")

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
    ) -> tuple[type, dict]:
        _field_type, _field_args = GenericTypeParser.get_impl(
            properties["type"]
        ).from_properties(name, properties)

        _field_args = _field_args or {}

        if description := properties.get("description"):
            _field_args["description"] = description

        if name not in required_keys:
            _field_args["default"] = properties.get("default", None)

        if "default_factory" in _field_args and "default" in _field_args:
            del _field_args["default"]

        return _field_type, Field(**_field_args)
