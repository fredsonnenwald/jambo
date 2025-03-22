from pydantic import TypeAdapter

from typing import Dict, List, Literal, NotRequired, TypedDict, Union

JSONSchemaType = Union[
    Literal["string", "number", "integer", "boolean", "array", "object", "null"],
    List[Literal["string", "number", "integer", "boolean", "array", "object", "null"]],
]


JSONSchemaProperty = TypedDict(
    "JSONSchemaProperty",
    {
        "type": JSONSchemaType,
        # Array-related properties
        "items": NotRequired[Union["JSONSchemaProperty", List["JSONSchemaProperty"]]],
        "minItems": NotRequired[int],
        "maxItems": NotRequired[int],
        "uniqueItems": NotRequired[bool],
        # String constraints
        "minLength": NotRequired[int],
        "maxLength": NotRequired[int],
        "pattern": NotRequired[str],
        "format": NotRequired[str],
        # Number constraints
        "minimum": NotRequired[Union[int, float]],
        "maximum": NotRequired[Union[int, float]],
        "exclusiveMinimum": NotRequired[Union[int, float]],
        "exclusiveMaximum": NotRequired[Union[int, float]],
        "multipleOf": NotRequired[Union[int, float]],
        # Enumerations
        "enum": NotRequired[List[Union[str, int, float, bool, None]]],
        "const": NotRequired[Union[str, int, float, bool, None]],
        # Conditional Subschemas
        "allOf": NotRequired[List["JSONSchemaProperty"]],
        "anyOf": NotRequired[List["JSONSchemaProperty"]],
        "oneOf": NotRequired[List["JSONSchemaProperty"]],
        "not_": NotRequired["JSONSchemaProperty"],
    },
)


# Implementing JSONSchema TypedDict
JSONSchema = TypedDict(
    "JSONSchema",
    {
        # General metadata
        "$schema": str,
        "$id": str,
        "title": str,
        "description": str,
        # Basic Type Definition
        "type": JSONSchemaType,
        # Object-related properties
        "properties": NotRequired[Dict[str, JSONSchemaProperty]],
        "required": NotRequired[List[str]],
    },
)


# Implementing Pydantic Validator

JSONSchemaValidator = TypeAdapter(JSONSchema)
