from jambo.parser import ObjectTypeParser
from jambo.types.json_schema_type import JSONSchema

from jsonschema.exceptions import SchemaError
from jsonschema.validators import validator_for
from pydantic import BaseModel


class SchemaConverter:
    """
    Converts JSON Schema to Pydantic models.

    This class is responsible for converting JSON Schema definitions into Pydantic models.
    It validates the schema and generates the corresponding Pydantic model with appropriate
    fields and types. The generated model can be used for data validation and serialization.
    """

    @staticmethod
    def build(schema: JSONSchema) -> type[BaseModel]:
        """
        Converts a JSON Schema to a Pydantic model.
        :param schema: The JSON Schema to convert.
        :return: A Pydantic model class.
        """

        try:
            validator = validator_for(schema)
            validator.check_schema(schema)
        except SchemaError as e:
            raise ValueError(f"Invalid JSON Schema: {e}")

        if "title" not in schema:
            raise ValueError("JSON Schema must have a title.")

        if (schema_type := schema.get("type", "undefined")) != "object":
            raise TypeError(
                f"Invalid JSON Schema: {schema_type}. Only 'object' can be converted to Pydantic models."
            )

        parsed_model = ObjectTypeParser.to_model(
            schema["title"],
            schema.get("properties"),
            schema.get("required"),
            context=schema,
            ref_cache=dict(),
        )

        if not issubclass(parsed_model, BaseModel):
            raise TypeError(
                f"Parsed model {parsed_model.__name__} is not a subclass of BaseModel."
            )

        return parsed_model
