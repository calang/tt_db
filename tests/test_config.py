import pytest
from pathlib import Path
from config.params import Params


@pytest.fixture
def sample_params_file(tmp_path):
    params_content = """
    database:
        name: tt
        host: localhost
        port: 5432
    user: testuser
    """
    params_file = tmp_path / "params.yaml"
    params_file.write_text(params_content)
    return params_file


def test_params_singleton():
    """Test that Params class maintains singleton pattern"""
    params1 = Params()
    params2 = Params()
    assert params1 is params2


def test_params_loading(sample_params_file, monkeypatch):
    """Test parameters are loaded correctly from yaml"""
    monkeypatch.chdir(sample_params_file.parent)
    params = Params()
    
    
    assert params.params['database']['name'] == 'tt'
    assert params.params['database']['port'] == 5432
    assert params.params['user'] == 'testuser'


def test_params_get_with_default():
    """Test get method with default value"""
    params = Params()
    assert params.get('nonexistent', 'default') == 'default'


def test_missing_params_file():
    """Test error handling when params.yaml is missing"""
    with pytest.raises(FileNotFoundError):
        # Force reload by creating new instance in temp directory
        with pytest.chdir(Path('/tmp')):
            Params()

