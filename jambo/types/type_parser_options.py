from typing_extensions import Any, NotRequired, TypedDict


class TypeParserOptions(TypedDict):
    required: bool
    context: dict[str, Any]
    ref_cache: NotRequired[dict[str, type]]
