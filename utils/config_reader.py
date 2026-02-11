try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib

import os
class ConfigReader:

    def __init__(self, file_path=r"C:\Users\u633481\my_ci_cd_project\python-ci-cd-demo\drivers\data_config.toml"):
        with open(file_path, "rb") as f:
            self.config = tomllib.load(f)

    def get(self, *keys):
        value=self.config
        for key in keys:
            value=value.get(key,{})
        return value

