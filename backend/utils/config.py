import yaml
from functools import lru_cache
from pathlib import Path 


root_dir = Path(__file__).resolve().parent.parent
config_path = root_dir / "config"
@lru_cache
def get_config():
    with open(config_path / "config.yaml", "r") as f:
        return yaml.safe_load(f)
