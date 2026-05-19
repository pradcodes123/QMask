import random
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister
import qiskit.qasm3, qiskit.qasm2

rng = random.Random(1337)

# =========================================================
# SAFE HELPERS
# =========================================================

def add_measurements(circuit: QuantumCircuit) -> QuantumCircuit:
    if not any(i.operation.name == "measure" for i in circuit.data):
        if not circuit.cregs:
            circuit.add_register(ClassicalRegister(len(circuit.qubits), "c"))
        for i, q in enumerate(circuit.qubits[:len(circuit.clbits)]):
            circuit.measure(q, circuit.clbits[i])
    return circuit


def true_identity(out, q):
    """Only mathematically guaranteed identities"""
    choice = rng.choice(["xx", "hh", "ssdg", "rz"])
    
    if choice == "xx":
        out.x(q); out.x(q)
    elif choice == "hh":
        out.h(q); out.h(q)
    elif choice == "ssdg":
        out.s(q); out.sdg(q)
    else:
        theta = rng.uniform(0, 2*np.pi)
        out.rz(theta, q)
        out.rz(-theta, q)


# =========================================================
# LIGHT CLOAKING (SAFE)
# =========================================================

def cloak_pauli(out, name, q):
    """Equivalent Pauli decompositions"""
    if name == "x":
        out.rx(np.pi, q)
    elif name == "y":
        out.ry(np.pi, q)
    elif name == "z":
        out.rz(np.pi, q)


# =========================================================
# MODERATE CLOAKING
# =========================================================

def split_rotation(out, gate, q):
    """Split rotation safely"""
    theta = float(gate.params[0])
    k = rng.choice([2, 3])
    for _ in range(k):
        out.append(type(gate)(theta / k), [q])


def echo_cloak(out, q):
    """True identity echo"""
    out.x(q)
    out.x(q)


# =========================================================
# HEAVY CLOAKING
# =========================================================

def cloak_cx(out, c, t):
    """CX → H CZ H (valid equivalence)"""
    out.h(t)
    out.cz(c, t)
    out.h(t)


# =========================================================
# CORE OBFUSCATION
# =========================================================

def obfuscate(circuit: QuantumCircuit, level: int) -> QuantumCircuit:
    out = QuantumCircuit(*circuit.qregs, *circuit.cregs)

    instructions = list(circuit.data)

    for idx, instr in enumerate(instructions):
        op = instr.operation
        qargs = instr.qubits
        cargs = instr.clbits

        # ---- Preserve measurement exactly ----
        if op.name == "measure":
            out.append(op, qargs, cargs)
            continue

        handled = False

        # ---------- HEAVY ----------
        if level >= 2 and op.name == "cx":
            cloak_cx(out, qargs[0], qargs[1])
            handled = True

        # ---------- MODERATE ----------
        elif level >= 1 and op.name in ("rx", "ry", "rz"):
            split_rotation(out, op, qargs[0])
            handled = True

        # ---------- LIGHT ----------
        elif op.name in ("x", "y", "z"):
            cloak_pauli(out, op.name, qargs[0])
            handled = True

        # ---------- FALLBACK ----------
        if not handled:
            out.append(op, qargs, cargs)

        # ---------- SAFE NOISE ----------
        # Don't insert before measurement
        next_is_measure = (
            idx + 1 < len(instructions)
            and instructions[idx + 1].operation.name == "measure"
        )

        if not next_is_measure and len(qargs) == 1:
            if rng.random() < 0.3:
                true_identity(out, qargs[0])

            if level >= 1 and rng.random() < 0.2:
                echo_cloak(out, qargs[0])

    return out


# =========================================================
# LEVEL MAP
# =========================================================

LEVEL_MAP = {
    "light": 0,
    "moderate": 1,
    "heavy": 2
}


# =========================================================
# MAIN APPLY FUNCTION
# =========================================================

def apply(qasm_str: str, level: str = "light") -> dict:

    # Parse QASM
    if qasm_str.lstrip().startswith("OPENQASM 2"):
        qc = QuantumCircuit.from_qasm_str(qasm_str)
    elif qasm_str.startswith("OPENQASM 3"):
        qc = qiskit.qasm3.loads(qasm_str)
    else:
        raise ValueError("Unsupported QASM version")

    # Ensure measurements
    qc = add_measurements(qc.copy())

    # Level
    if level not in LEVEL_MAP:
        raise ValueError(f"Invalid level: {level}")

    lvl = LEVEL_MAP[level]

    # Obfuscate
    obf_qc = obfuscate(qc, lvl)

    # Convert back
    if qasm_str.startswith("OPENQASM 2"):
        obf_qasm = qiskit.qasm2.dumps(obf_qc)
    else:
        obf_qasm = qiskit.qasm3.dumps(obf_qc)

    return {
        "obfuscated_qasm": obf_qasm
    }