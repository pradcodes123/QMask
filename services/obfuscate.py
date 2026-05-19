from qiskit import QuantumCircuit
import importlib

def apply_technique(qasm_str, technique_name):
    qc = QuantumCircuit.from_qasm_str(qasm_str)

    module = importlib.import_module(f"techniques.{technique_name}")
    obf_qc = module.apply(qc)

    return obf_qc.qasm()