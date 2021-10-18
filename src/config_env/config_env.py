# import os
# import collections.abc


# class Config:
#     def __init__(self) -> None:
#         self.python_env = os.getenv("PYTHON_ENV")

#     def __cleanNullTerms(self, d: dict) -> dict:
#         clean = {}
#         for k, v in d.items():
#             if isinstance(v, dict):
#                 nested = self.__cleanNullTerms(v)
#                 if len(nested.keys()) > 0:
#                     clean[k] = nested
#             elif v is not None:
#                 clean[k] = v
#         return clean

#     def __update_dictionary(self, d, u):
#         for k, v in u.items():
#             if isinstance(v, collections.abc.Mapping):
#                 d[k] = self.__update_dictionary(d.get(k, {}), v)
#             else:
#                 d[k] = v
#         return d

#     def __evaluate_environment_variables(self, config: dict) -> dict:
#         for key, value in config.items():
#             if isinstance(value, dict):
#                 self.__evaluate_environment_variables(value)
#             else:
#                 config.update({key: os.getenv(value)})
#         return config

#     def config(self):
#         config = {}
#         dir = "./config/"
#         files = os.listdir(dir)
#         filenames = []
#         for file in files:
#             path = dir + file
#             if os.stat(path).st_size != 0:
#                 filename = file.split(".")[0].replace("-", "_") + "_config"
#                 filenames.append(filename)
#                 exec(f"{filename} = {eval(open(path).read())}")

#         if self.python_env == None or "DEFAULT":
#             if "default.json" in files:
#                 exec("config.update(default_config)")
#             else:
#                 raise ValueError(f"Missing config file default.json")
#         else:
#             if f"{self.python_env.lower().replace('-','_')}.json" in files:
#                 exec(f"config.update({self.python_env.lower()}_config)")
#             else:
#                 raise ValueError(f"Missing config file {self.python_env.lower()}.json")
#         if "custom_environment_variables.json" in files:
#             custom_config = self.__evaluate_environment_variables(
#                 eval("custom_environment_variables_config")
#             )
#             custom_config_cleaned = self.__cleanNullTerms(custom_config)
#             config = self.__update_dictionary(config, custom_config_cleaned)
#         return config




import os
import collections.abc


def __cleanNullTerms(d: dict) -> dict:
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = __cleanNullTerms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean

def __update_dictionary(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = __update_dictionary(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def __evaluate_environment_variables(config: dict) -> dict:
    for key, value in config.items():
        if isinstance(value, dict):
            __evaluate_environment_variables(value)
        else:
            config.update({key: os.getenv(value)})
    return config

def config():
    config = {}
    dir = "./config/"
    files = os.listdir(dir)
    filenames = []
    for file in files:
        path = dir + file
        if os.stat(path).st_size != 0:
            filename = file.split(".")[0].replace("-", "_") + "_config"
            filenames.append(filename)
            exec(f"{filename} = {eval(open(path).read())}")

    if os.getenv('PYTHON_ENV') == None or "DEFAULT":
        if "default.json" in files:
            exec("config.update(default_config)")
        else:
            raise ValueError(f"Missing config file default.json")
    else:
        if f"{sos.getenv('PYTHON_ENV').lower().replace('-','_')}.json" in files:
            exec(f"config.update({os.getenv('PYTHON_ENV').lower()}_config)")
        else:
            raise ValueError(f"Missing config file {os.getenv('PYTHON_ENV').lower()}.json")
    if "custom_environment_variables.json" in files:
        custom_config = __evaluate_environment_variables(
            eval("custom_environment_variables_config")
        )
        custom_config_cleaned = __cleanNullTerms(custom_config)
        config = __update_dictionary(config, custom_config_cleaned)
    return config