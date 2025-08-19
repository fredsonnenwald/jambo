from jambo.parser._type_parser import GenericTypeParser
from jambo.types.type_parser_options import TypeParserOptions

from pydantic import BeforeValidator, Field, TypeAdapter, ValidationError
from typing_extensions import Annotated, Any, Union, Unpack


class OneOfTypeParser(GenericTypeParser):
    mapped_type = Union

    json_schema_type = "oneOf"

    def from_properties_impl(
        self, name, properties, **kwargs: Unpack[TypeParserOptions]
    ):
        if "oneOf" not in properties:
            raise ValueError(f"Invalid JSON Schema: {properties}")

        if not isinstance(properties["oneOf"], list):
            raise ValueError(f"Invalid JSON Schema: {properties['oneOf']}")

        mapped_properties = self.mappings_properties_builder(properties, **kwargs)

        sub_properties = properties["oneOf"]

        sub_types = [
            GenericTypeParser.type_from_properties(name, subProperty, **kwargs)
            for subProperty in sub_properties
        ]

        if not kwargs.get("required", False):
            mapped_properties["default"] = mapped_properties.get("default")

        field_types = [
            Annotated[t, Field(**v)] if self._has_meaningful_constraints(v) else t
            for t, v in sub_types
        ]

        union_type = Union[(*field_types,)]

        discriminator = properties.get("discriminator")
        if discriminator and isinstance(discriminator, dict):
            property_name = discriminator.get("propertyName")
            if property_name:
                validated_type = Annotated[
                    union_type, Field(discriminator=property_name)
                ]
                return validated_type, mapped_properties

        def validate_one_of(value: Any) -> Any:
            matched_count = 0
            validation_errors = []

            for field_type in field_types:
                try:
                    adapter = TypeAdapter(field_type)
                    adapter.validate_python(value)
                    matched_count += 1
                except ValidationError as e:
                    validation_errors.append(str(e))
                    continue

            if matched_count == 0:
                raise ValueError("Value does not match any of the oneOf schemas")
            elif matched_count > 1:
                raise ValueError(
                    "Value matches multiple oneOf schemas, exactly one expected"
                )

            return value

        validated_type = Annotated[union_type, BeforeValidator(validate_one_of)]
        return validated_type, mapped_properties

    @staticmethod
    def _has_meaningful_constraints(field_props):
        """
        Check if field properties contain meaningful constraints that require Field wrapping.
        Returns False if:
        - field_props is None or empty
        - field_props only contains {'default': None}
        Returns True if:
        - field_props contains a non-None default value
        - field_props contains other constraint properties (min_length, max_length, pattern, etc.)
        """
        if not field_props:
            return False

        # If only default is set and it's None, no meaningful constraints
        if field_props == {"default": None}:
            return False

        # If there are multiple properties or non-None default, that's meaningful
        return True
