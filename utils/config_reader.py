try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib

from pathlib import Path


class ConfigReader:

    def __init__(self, file_path=None):
        if file_path:
            config_path = Path(file_path)
        else:
            # Auto-detect project root
            config_path = Path(__file__).resolve().parent.parent / "drivers" / "data_config.toml"

        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, "rb") as f:
            self.config = tomllib.load(f)

    def get(self, *keys):
        value = self.config
        for key in keys:
            value = value.get(key, {})
        return value

