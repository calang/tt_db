"""
Params class with single instance
storing the app params defined in the corresponding yaml file
"""

from pathlib import Path
import yaml
from src.utils.singleton import Singleton


class Params(dict, metaclass=Singleton):
    def __init__(self):
        super().__init__()
        self._load_params()
    
    def _load_params(self):
        """Load parameters from params.yaml file"""

        # Path of the current script file
        package_dir = Path(__file__).parent
        # Path to the YAML file in the same directory
        yaml_file_path = package_dir / 'params.yaml'

        try:
            with open(yaml_file_path, 'r') as f:
                self.update(yaml.safe_load(f))
        except FileNotFoundError:
            raise FileNotFoundError("params.yaml not found")
