from jambo.utils.properties_builder.mappings_properties_builder import (
    mappings_properties_builder,
)


def numeric_properties_builder(properties):
    _mappings = {
        "minimum": "ge",
        "exclusiveMinimum": "gt",
        "maximum": "le",
        "exclusiveMaximum": "lt",
        "multipleOf": "multiple_of",
        "default": "default",
    }

    mapped_properties = mappings_properties_builder(properties, _mappings)

    if "default" in properties:
        default_value = properties["default"]
        if not isinstance(default_value, (int, float)):
            raise ValueError(
                f"Default value must be a number, got {type(default_value).__name__}"
            )

        if default_value >= properties.get("maximum", float("inf")):
            raise ValueError(
                f"Default value exceeds maximum limit of {properties.get('maximum')}"
            )

        if default_value <= properties.get("minimum", float("-inf")):
            raise ValueError(
                f"Default value is below minimum limit of {properties.get('minimum')}"
            )

        if default_value > properties.get("exclusiveMaximum", float("inf")):
            raise ValueError(
                f"Default value exceeds exclusive maximum limit of {properties.get('exclusiveMaximum')}"
            )

        if default_value < properties.get("exclusiveMinimum", float("-inf")):
            raise ValueError(
                f"Default value is below exclusive minimum limit of {properties.get('exclusiveMinimum')}"
            )

        if "multipleOf" in properties:
            if default_value % properties["multipleOf"] != 0:
                raise ValueError(
                    f"Default value {default_value} is not a multiple of {properties['multipleOf']}"
                )

    return mapped_properties
