"""
Params class with single instance
storing the app params defined in the corresponding yaml file
"""

import yaml
from src.utils.singleton import Singleton

class Params(metaclass=Singleton):
    def __init__(self):
        self.params = {}
        self._load_params()
    
    def _load_params(self):
        """Load parameters from params.yaml file"""
        try:
            with open('config/params.yaml', 'r') as f:
                self.params = yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError("params.yaml not found")
    
    def get(self, key, default=None):
        """Get a parameter value by key"""
        return self.params.get(key, default)
    
    def __getitem__(self, key):
        """Allow dictionary-style access to parameters"""
        return self.params[key]

