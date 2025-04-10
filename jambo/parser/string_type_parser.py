from jambo.parser._type_parser import GenericTypeParser
from jambo.utils.properties_builder.mappings_properties_builder import (
    mappings_properties_builder,
)


class StringTypeParser(GenericTypeParser):
    mapped_type = str

    json_schema_type = "string"

    @staticmethod
    def from_properties(name, properties):
        _mappings = {
            "maxLength": "max_length",
            "minLength": "min_length",
            "pattern": "pattern",
        }

        mapped_properties = mappings_properties_builder(properties, _mappings)

        if "default" in properties:
            default_value = properties["default"]
            if not isinstance(default_value, str):
                raise ValueError(
                    f"Default value for {name} must be a string, "
                    f"but got {type(properties['default'])}."
                )

            if len(default_value) > properties.get("maxLength", float("inf")):
                raise ValueError(
                    f"Default value for {name} exceeds maxLength limit of {properties.get('maxLength')}"
                )

            if len(default_value) < properties.get("minLength", 0):
                raise ValueError(
                    f"Default value for {name} is below minLength limit of {properties.get('minLength')}"
                )

        return str, mapped_properties
