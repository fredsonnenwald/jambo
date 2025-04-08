from jambo.parser._type_parser import GenericTypeParser


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

        return str, {
            _mappings[key]: value
            for key, value in properties.items()
            if key in _mappings
        }
