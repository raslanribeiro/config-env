from src.config_env import ConfigEnv

config = ConfigEnv()

aws = config.get("aws")
print(aws)

all = config.get("")
print(all)