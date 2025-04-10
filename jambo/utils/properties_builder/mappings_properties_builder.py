def mappings_properties_builder(properties, mappings, default_mappings=None):
    default_mappings = default_mappings or {
        "default": "default",
        "description": "description",
    }

    mappings = default_mappings | mappings

    return {
        mappings[key]: value for key, value in properties.items() if key in mappings
    }
