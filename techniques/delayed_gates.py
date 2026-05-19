import random
import qiskit
from qiskit import QuantumCircuit, ClassicalRegister



def add_measurements(circuit: QuantumCircuit) -> QuantumCircuit:
    if any(instr.operation.name == "measure" for instr in circuit.data):
        return circuit

    if not circuit.clbits:
        circuit.add_register(ClassicalRegister(len(circuit.qubits), "c"))

    for i, q in enumerate(circuit.qubits[:len(circuit.clbits)]):
        circuit.measure(q, circuit.clbits[i])

    return circuit

IDENTITY_SEQS = [
    ["h", "h"],
    ["x", "x"],
    ["y", "y"],
    ["z", "z"],
    ["s", "sdg"],
    ["t", "tdg"],
    ["h", "s", "h", "s", "h", "h"],
    ["z", "h", "z", "h", "z", "z"]
]


def apply_identity_junk(circuit: QuantumCircuit, qubits, density=1):
    for q in qubits:
        for _ in range(density):
            seq = random.choice(IDENTITY_SEQS)
            for gate in seq:
                getattr(circuit, gate)(q)

def obfuscate(circuit: QuantumCircuit, level: int) -> QuantumCircuit:
    """
    Level 0 → light identity padding
    Level 1 → repeated padding
    Level 2 → multi-round heavy padding
    """

    if level not in (0, 1, 2):
        raise ValueError("Invalid obfuscation level")

    out = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    qubits = circuit.qubits

    if level == 0:
        density, rounds = 1, 1
    elif level == 1:
        density, rounds = 2, 1
    else:
        density, rounds = 3, 2

    for _ in range(rounds):
        apply_identity_junk(out, qubits, density)

        for instr in circuit.data:
            out.append(instr.operation, instr.qubits, instr.clbits)

        apply_identity_junk(out, qubits, density)

    return out

LEVEL_MAP = {
    "light": 0,
    "moderate": 1,
    "heavy": 2
}

def apply(qasm_str: str, level: str = "light") -> dict:

    qasm_str = qasm_str.strip()
    is_qasm2 = qasm_str.startswith("OPENQASM 2")

    # 1. Parse
    if is_qasm2:
        qc = QuantumCircuit.from_qasm_str(qasm_str)
    else:
        qc = qiskit.qasm3.loads(qasm_str)

    # 2. Add measurements safely
    qc = add_measurements(qc.copy())

    # 3. Level mapping
    if level not in LEVEL_MAP:
        raise ValueError(f"Invalid level: {level}")
    lvl = LEVEL_MAP[level]

    # 4. Obfuscate
    obf_qc = obfuscate(qc, lvl)

    # 5. Convert back
    if is_qasm2:
        obf_qasm = qiskit.qasm2.dumps(obf_qc)
    else:
        obf_qasm = qiskit.qasm3.dumps(obf_qc)

    return {
        "obfuscated_qasm": obf_qasm
    }