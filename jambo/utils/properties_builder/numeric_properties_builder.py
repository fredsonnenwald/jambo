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
    }

    return mappings_properties_builder(properties, _mappings)
