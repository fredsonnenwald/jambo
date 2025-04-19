from pydantic import Field, TypeAdapter
from typing_extensions import Annotated, Self

from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar


T = TypeVar("T")


class GenericTypeParser(ABC, Generic[T]):
    mapped_type: Type[T] = None

    json_schema_type: str = None

    @staticmethod
    @abstractmethod
    def from_properties(
        name: str, properties: dict[str, any], required: bool = False
    ) -> tuple[T, dict]: ...

    @classmethod
    def get_impl(cls, type_name: str) -> Self:
        for subcls in cls.__subclasses__():
            if subcls.json_schema_type is None:
                raise RuntimeError(f"Unknown type: {type_name}")

            if subcls.json_schema_type == type_name:
                return subcls()

        raise ValueError(f"Unknown type: {type_name}")

    @staticmethod
    def validate_default(field_type: type, field_prop: dict, value):
        field = Annotated[field_type, Field(**field_prop)]
        TypeAdapter(field).validate_python(value)
