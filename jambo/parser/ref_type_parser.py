from jambo.parser import GenericTypeParser
from jambo.types.type_parser_options import TypeParserOptions

from typing_extensions import Any, ForwardRef, TypeVar, Union, Unpack


RefType = TypeVar("RefType", bound=Union[int, str])


class RefTypeParser(GenericTypeParser):
    json_schema_type = "$ref"

    def from_properties_impl(
        self, name: str, properties: dict[str, Any], **kwargs: Unpack[TypeParserOptions]
    ) -> tuple[RefType, dict]:
        if "$ref" not in properties:
            raise ValueError(f"RefTypeParser: Missing $ref in properties for {name}")

        context = kwargs["context"]
        required = kwargs.get("required", False)

        if context is None:
            raise RuntimeError(
                f"RefTypeParser: Missing $content in properties for {name}"
            )

        if not properties["$ref"].startswith("#"):
            raise ValueError(
                "At the moment, only local references are supported. "
                "Look into $defs and # for recursive references."
            )

        ref_type = None
        mapped_properties = {}

        if properties["$ref"] == "#":
            if "title" not in context:
                raise ValueError(
                    "RefTypeParser: Missing title in properties for $ref #"
                )

            ref_type = ForwardRef(context["title"])

        elif properties["$ref"].startswith("#/$defs/"):
            target_name = None
            target_property = context
            for prop_name in properties["$ref"].split("/")[1:]:
                if prop_name not in target_property:
                    raise ValueError(
                        f"RefTypeParser: Missing {prop_name} in"
                        " properties for $ref {properties['$ref']}"
                    )
                target_name = prop_name
                target_property = target_property[prop_name]

            if target_name is None or target_property is None:
                raise ValueError(f"RefTypeParser: Invalid $ref {properties['$ref']}")

            ref_type, mapped_properties = GenericTypeParser.type_from_properties(
                target_name, target_property, **kwargs
            )

        else:
            raise ValueError(
                "RefTypeParser: Invalid $ref format. "
                "Only local references are supported."
            )

        if not required:
            mapped_properties["default"] = None

        return ref_type, mapped_properties
