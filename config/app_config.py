import json

import json
import threading

class AppConfig:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, config_path):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(AppConfig, cls).__new__(cls)
                    cls._instance._load_config(config_path)
        return cls._instance

    def _load_config(self, config_path):
        with open(config_path, 'r') as f:
            self._config = json.load(f)

    def get(self, key, default=None):
        return self._config.get(key, default)

    def all(self):
        return self._config
    
_app_config = AppConfig('app_config.json')

def get_llm_config():
    return _app_config.get('llm')

def get_entrez_config():
    return _app_config.get('entrez')

