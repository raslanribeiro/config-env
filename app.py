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
            filename = file.split(".")[0] + "_config"
            filenames.append(filename)
            exec(f"{filename} = {eval(open(path).read())}")

    if PYTHON_ENV == None or "DEFAULT":
        if "default.json" in files:
            exec("config.update(default_config)")
        else:
            raise ValueError(f"Missing config file default.json")
    else:
        if f"{PYTHON_ENV.lower()}.json" in files:
            exec(f"config.update({PYTHON_ENV.lower()}_config)")
        else:
            raise ValueError(f"Missing config file {PYTHON_ENV.lower()}.json")
    if "custom_environment_variables.json" in files:
        custom_config = __evaluate_environment_variables(
            eval("custom_environment_variables_config")
        )
        custom_config_cleaned = __cleanNullTerms(custom_config)
        config = __update_dictionary(config, custom_config_cleaned)
    return config


if __name__ == "__main__":
    PYTHON_ENV = os.getenv("PYTHON_ENV")
    config = config()
