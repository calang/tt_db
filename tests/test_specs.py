"""Test schema used to define the tt data base"""


from config.params import params
from src.utils.spec_handling import (
    get_yaml_file_as_dict,
    validate_schema,
    validate_spec_file,
)


def Xtest_schema():
    validate_schema(params.get('db_spec_schema'))


def test_tt_spec():
    validate_spec_file(params.get('tt_spec'), params.get('db_spec_schema'))
