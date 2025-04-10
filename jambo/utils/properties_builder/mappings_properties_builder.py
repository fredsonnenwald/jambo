def mappings_properties_builder(properties, mappings):
    return {
        mappings[key]: value for key, value in properties.items() if key in mappings
    }
