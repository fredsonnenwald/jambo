from jambo.types.json_schema_type import JSONSchema

from typing_extensions import NotRequired, TypedDict


class TypeParserOptions(TypedDict):
    required: bool
    context: JSONSchema
    ref_cache: NotRequired[dict[str, type]]
