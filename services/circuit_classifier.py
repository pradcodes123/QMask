import json
import os

BASE_PATH = "frontend/data/predefined"

def load_config(circuit_name):

    if not circuit_name:
        return None

    path = os.path.join(
        BASE_PATH,
        circuit_name,
        "config.json"
    )

    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        config = json.load(f)

    return config