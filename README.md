# About

Package to manage environment variables similar to npm config from nodejs

## Start

```bash
pip install config_env
mkdir config
vi config/default.json
```

```json
// default.json
{
    // Customer module configs
    "Customer": {
        "dbConfig": {
            "host": "localhost",
            "port": 5984,
            "dbName": "customers"
        },
        "credit": {
            "initialLimit": 100,
            // Set low for development
            "initialDays": 1
        }
    }
}
```

```bash
vi config/production.json
```

```json
{
    "Customer": {
        "dbConfig": {
            "host": "prod-db-server"
        },
        "credit": {
            "initialDays": 30
        }
    }
}
```

And if is necessary to hide secret values, it is recommended to use custom_environment_varibles.json to get environment variables:

```bash
vi config/custom_environment_varibles.json
```

```json
{
    "Customer": {
        "dbConfig": {
            "user": "MY_USERNAME",
            "password": "MY_PASSWORD"
        }
    }
}
```

Values preference order:

-   custom_environment_varibles -> production -> default

If custom_environment_varibles.json file does not exist or do not contain some key:value, it will come from produciton.json.

If producion.json file does not exist or do not contain some key:value, it will come from default.json.

## Using config_env

```python
# app.py
from config_env import config_env

config = config_env.config()

customer_host = config.get("Customer").get("dbConfig").get("host")

customer_credit = config.get("Customer").get("credit")
```
