"""Test model_group and model specs are written according to schema"""

import os
from typing import Dict, List

import yaml
from jsonschema import validate

from td_common.appdata import intel_data_df, comp_data_df
from td_common.config.params import (
    MODEL_GROUPS_SPEC_FILE,
    MODEL_GROUPS_SCHEMA_FILE,
    MODELS_SPEC_FILE,
    MODELS_SCHEMA_FILE,
)
from td_common.modules import deal as deal_module
from td_common.modules.deal import Deal


def get_yaml_file_as_dicts(filename: str) -> List[Dict]:
    """Read a yaml file and return its conversion to Dict"""
    with open(filename, 'r', encoding="utf-8") as y_file:
        specs = list(yaml.safe_load_all(y_file))
    return specs


def validate_spec(spec: Dict, schema: Dict):
    """Validate a spec file against a schema"""
    validate(instance=spec, schema=schema)


def test_model_group_names():
    """The model group specs all match the corresponding schema"""
    schema_list = get_yaml_file_as_dicts(MODEL_GROUPS_SCHEMA_FILE)
    assert len(schema_list) == 1, f"{MODEL_GROUPS_SCHEMA_FILE} does not contain exactly one schema"

    schema = schema_list[0]

    # validate the validation schema
    # TBD: make it work in Jenkins pod
    # jsonschema.Validator.check_schema(schema)

    group_list = get_yaml_file_as_dicts(MODEL_GROUPS_SPEC_FILE)

    # check that all group specs match the group schema
    for group in group_list:
        validate_spec(group, schema)

    group_name_list = [group.get('spec').get('name')
                 for group in group_list
                 ]

    # check that all groups have a class in deal_module with the same name
    for name in group_name_list:
        group_class = getattr(deal_module, name, None)
        if group_class is None:
            raise ValueError(f"group {name} does not have a class with the same name in deal.py")

    # check that module names are unique (not repeated)
    assert len(group_name_list) == len(set(group_name_list)), f"Model group names are not unique: {sorted(group_name_list)}"


def test_model_group_scopes():
    """Model group scopes refer to existent Deal features"""
    group_list = get_yaml_file_as_dicts(MODEL_GROUPS_SPEC_FILE)

    missing_list = []
    for group in group_list:
        g_name = group.get('spec').get('name')
        g_scope_keys = group.get('spec').get('scope').keys()
        for key in g_scope_keys:
            present = bool(getattr(Deal, key, None))
            if not present:
                missing_list.append((g_name, key))

    print(f"model group, scope features not in Deal:\n{missing_list}")
    assert missing_list == []


def test_models():
    """The model group specs all match the corresponding schema"""
    schema_list = get_yaml_file_as_dicts(MODELS_SCHEMA_FILE)
    assert len(schema_list) == 1, f"{MODELS_SCHEMA_FILE} does not contain exactly one schema"

    schema = schema_list[0]

    # validate the validation schema
    # TBD: make it work in Jenkins pod
    # jsonschema.Validator.check_schema(schema)

    model_list = get_yaml_file_as_dicts(MODELS_SPEC_FILE)

    # check that all model specs match the model schema
    for model in model_list:
        validate_spec(model, schema)

    model_name_list = [model.get('spec').get('name')
                 for model in model_list
                 ]

    # check that all models have a class in deal_module with the same name
    for name in model_name_list:
        model_class = getattr(deal_module, name, None)
        if model_class is None:
            raise ValueError(f"model {name} does not have a class with the same name in deal.py")

    assert len(model_name_list) == len(set(model_name_list)), f"Model names are not unique: {sorted(model_name_list)}"
