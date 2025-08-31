"""Utility functions to handle yaml specs and their validating schemas"""

from functools import lru_cache

import yaml
import jsonschema as js


@lru_cache(maxsize=4)
def get_yaml_file_as_dict(filename: str) -> dict:
    """
    Read a yaml file and return its conversion to Dict
    assuming the file contains only one YAML file
    """
    with open(filename, 'r', encoding="utf-8") as y_file:
        specs = yaml.safe_load(y_file)
    return specs


def get_yaml_file_as_dict_list(filename: str) -> list[dict]:
    """
    Read a yaml file and return its conversion to a list of dicts
    given that the file might have more than one YAML documents
    """
    with open(filename, 'r', encoding="utf-8") as y_file:
        specs = list(yaml.safe_load_all(y_file))
    return specs


def put_dict_as_yaml_file(doc: dict, filename: str):
    """Write a Dict as a yaml file"""
    with open(filename, 'w', encoding="utf-8") as y_file:
        y_file.write(yaml.dump(doc))


def validate_schema(schema_filename: str):
    """
    Validate a YAML schema
    
    Raises:
        jsonschema.exceptions.SchemaError: when the contents of the schema_filename is not a valid schema
    """
    # load the validation schema
    schema = get_yaml_file_as_dict(schema_filename)
    # validate the validation schema
    js.Validator.check_schema(schema)


def validate_spec_file(spec_filename: str,
                       schema_filename: str
                       ):
    """
    Validate a spec file against a schema

    Args:
        spec_filename: name of the spec to validate
        schema_filename: name of the schema to validate with

    Raises:
        `jsonschema.exceptions.ValidationError`: if the instance is invalid
        `jsonschema.exceptions.SchemaError`: if the schema itself is invalid
    """
    # load the validation schema
    schema = get_yaml_file_as_dict(schema_filename)
    # load the spec
    spec = get_yaml_file_as_dict(spec_filename)
    # validate
    js.validate(instance=spec, schema=schema)
