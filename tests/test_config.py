import pytest
from pathlib import Path
from config.params import Params


def test_params_singleton():
    """Test that Params class maintains singleton pattern"""
    params1 = Params()
    params2 = Params()
    assert params1 is params2


def test_params_loading():
    """Test parameters are loaded correctly from yaml"""
    params = Params()
    assert params.params['db_spec_schema'] == 'specs/db_spec_schema.yaml'
    assert params.params.get('db_spec_schema') == 'specs/db_spec_schema.yaml'


def test_params_get_with_default():
    """Test get method with default value"""
    params = Params()
    assert params.get('nonexistent', 'default') == 'default'
