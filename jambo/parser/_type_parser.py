from pydantic import Field, TypeAdapter
from typing_extensions import Annotated, Self

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar


T = TypeVar("T")


class GenericTypeParser(ABC, Generic[T]):
    json_schema_type: str = None

    type_mappings: dict[str, str] = None

    default_mappings = {
        "default": "default",
        "description": "description",
    }

    @classmethod
    def type_from_properties(
        cls, name: str, properties: dict[str, Any], **kwargs
    ) -> tuple[type, dict]:
        parser = cls._get_impl(properties)

        return parser().from_properties(name=name, properties=properties, **kwargs)

    @classmethod
    def _get_impl(cls, properties: dict[str, Any]) -> type[Self]:
        for subcls in cls.__subclasses__():
            schema_type, schema_value = subcls._get_schema_type()

            if schema_type not in properties:
                continue

            if schema_value is None or schema_value == properties[schema_type]:
                return subcls

        raise ValueError("Unknown type")

    @classmethod
    def _get_schema_type(cls) -> tuple[str, str | None]:
        if cls.json_schema_type is None:
            raise RuntimeError("TypeParser: json_schema_type not defined")

        schema_definition = cls.json_schema_type.split(":")

        if len(schema_definition) == 1:
            return schema_definition[0], None

        return schema_definition[0], schema_definition[1]

    @abstractmethod
    def from_properties(
        self, name: str, properties: dict[str, Any], required: bool = False
    ) -> tuple[T, dict]: ...

    def mappings_properties_builder(self, properties, required=False) -> dict[str, Any]:
        if self.type_mappings is None:
            raise NotImplementedError("Type mappings not defined")

        if not required:
            properties["default"] = properties.get("default", None)

        mappings = self.default_mappings | self.type_mappings

        return {
            mappings[key]: value for key, value in properties.items() if key in mappings
        }

    def validate_default(self, field_type: type, field_prop: dict, value) -> None:
        field = Annotated[field_type, Field(**field_prop)]
        TypeAdapter(field).validate_python(value)
