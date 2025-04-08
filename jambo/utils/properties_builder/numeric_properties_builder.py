def numeric_properties_builder(properties):
    _mappings = {
        "minimum": "ge",
        "exclusiveMinimum": "gt",
        "maximum": "le",
        "exclusiveMaximum": "lt",
        "multipleOf": "multiple_of",
    }

    return {
        _mappings[key]: value
        for key, value in properties.items()
        if key in _mappings
    }