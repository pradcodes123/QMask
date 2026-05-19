import os
import json

BASE_PATH = "data/predefined"

def list_circuits():
    return [name for name in os.listdir(BASE_PATH) if not name.startswith(".")]

def load_circuit(name):
    folder = os.path.join(BASE_PATH, name)

    with open(os.path.join(folder, "circuit.qasm")) as f:
        qasm = f.read()

    with open(os.path.join(folder, "config.json")) as f:
        config = json.load(f)

    return {
        "qasm": qasm,
        "config": config
    }