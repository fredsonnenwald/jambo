from jambo.parser._type_parser import GenericTypeParser

from pydantic import Field
from typing_extensions import Annotated

from typing import Union


class AnyOfTypeParser(GenericTypeParser):
    mapped_type = Union

    json_schema_type = "anyOf"

    @staticmethod
    def from_properties(name, properties, required=False):
        if "anyOf" not in properties:
            raise ValueError(f"Invalid JSON Schema: {properties}")

        if not isinstance(properties["anyOf"], list):
            raise ValueError(f"Invalid JSON Schema: {properties['anyOf']}")

        mapped_properties = dict()

        subProperties = properties["anyOf"]

        sub_types = [
            GenericTypeParser.get_impl(subProperty["type"]).from_properties(
                name, subProperty
            )
            for subProperty in subProperties
        ]

        default_value = properties.get("default")
        if default_value is not None:
            for sub_type, sub_property in sub_types:
                try:
                    GenericTypeParser.validate_default(
                        sub_type, sub_property, default_value
                    )
                    break
                except ValueError:
                    continue
            else:
                raise ValueError(
                    f"Invalid default value {default_value} for anyOf types: {sub_types}"
                )

            mapped_properties["default"] = default_value

        if not required:
            mapped_properties["default"] = mapped_properties.get("default")

        # By defining the type as Union, we can use the Field validator to enforce
        # the constraints on the union type.
        # We use Annotated to attach the Field validators to the type.
        field_types = [Annotated[t, Field(**v)] if v else t for t, v in sub_types]

        return Union[(*field_types,)], mapped_properties
