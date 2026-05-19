import  random, math
import numpy as np
from qiskit import QuantumCircuit, ClassicalRegister
import qiskit.qasm2, qiskit.qasm3
from qiskit.circuit.library import U3Gate, UnitaryGate
from qiskit.quantum_info import Operator


def add_measurements(circuit: QuantumCircuit) -> QuantumCircuit:
    if not any(inst.operation.name == "measure" for inst in circuit.data):
        if not circuit.clbits:
            circuit.add_register(ClassicalRegister(circuit.num_qubits, "c"))
        for q in range(circuit.num_qubits):
            circuit.measure(q, q)
    return circuit


def random_u3_params():
    theta = random.uniform(0, math.pi)
    phi = random.uniform(0, 2 * math.pi)
    lam = random.uniform(0, 2 * math.pi)
    return theta, phi, lam

def u3_matrix(theta, phi, lam):
    return Operator(U3Gate(theta, phi, lam)).data

def conjugated_gate(original_op, theta, phi, lam):
    u = u3_matrix(theta, phi, lam)
    u_dag = u3_matrix(-theta, -lam, -phi)

    if original_op.num_qubits == 1:
        G = Operator(original_op).data
        mat = u @ G @ u_dag
    else:
        U_full = u
        U_dag_full = u_dag
        for _ in range(1, original_op.num_qubits):
            U_full = np.kron(U_full, u)
            U_dag_full = np.kron(U_dag_full, u_dag)
        G = Operator(original_op).data
        mat = U_full @ G @ U_dag_full

    name = original_op.name.upper()
    if name.startswith("c"): name = name[1:] + "_ctrl"
    return UnitaryGate(mat, label=f"Obf_{name}")


def selective_gate_obfuscation(circuit: QuantumCircuit, level: str = "heavy"):
    total_candidates = sum(
        1 for inst in circuit.data
        if inst.operation.name not in {"measure", "barrier"}
    )
    if total_candidates == 0:
        return circuit

    # Normalize level input
    level = level.lower()

    if level == "light":
        num_to_obfuscate = total_candidates // 3
    elif level == "moderate":
        num_to_obfuscate = (2 * total_candidates) // 3
    elif level == "heavy":
        num_to_obfuscate = total_candidates
    else:
        raise ValueError("level must be 'light', 'moderate', or 'heavy'")
    # Pick random gates to obfuscate
    candidates = [(i, inst) for i, inst in enumerate(circuit.data)
                  if inst.operation.name not in {"measure", "barrier"}]
    chosen_indices = set(random.sample([i for i, _ in candidates], num_to_obfuscate)
                        if num_to_obfuscate > 0 else [])

    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    obf_count = 0
    i = 0

    while i < len(circuit.data):
        inst = circuit.data[i]

        # Skip non-obfuscated or special instructions
        if i not in chosen_indices or inst.operation.name in {"measure", "barrier"}:
            new_circuit.append(inst.operation, inst.qubits, inst.clbits)
            i += 1
            continue

        # === OBFUSCATE THIS GATE ===
        theta, phi, lam = random_u3_params()
        op = inst.operation
        qargs = inst.qubits
        clbits = inst.clbits

        conj_gate = conjugated_gate(op, theta, phi, lam)
        u_pre = U3Gate(theta, phi, lam)
        u_post = U3Gate(-theta, -lam, -phi)

        # Always insert U_pre  - on each involved qubit
        for q in qargs:
            new_circuit.append(u_pre, [q], [])

        # Add conjugated gate (preserve condition if any)
        if hasattr(op, "condition") and op.condition is not None:
            new_circuit.append(conj_gate, qargs, clbits)
            new_circuit.data[-1].operation.c_if(*op.condition)
        else:
            new_circuit.append(conj_gate, qargs, clbits)

        # Always insert U_post  - on each involved qubit
        for q in qargs:
            new_circuit.append(u_post, [q], [])

        obf_count += 1
        i += 1
    return new_circuit


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

    # 3. Validate level
    if level not in {"light", "moderate", "heavy"}:
        raise ValueError(f"Invalid level: {level}")

    # 4. Apply obfuscation
    obf_qc = selective_gate_obfuscation(qc, level=level)

    # 5. Convert back
    if is_qasm2:
        obf_qasm = qiskit.qasm2.dumps(obf_qc)
    else:
        obf_qasm = qiskit.qasm3.dumps(obf_qc)

    return {
        "obfuscated_qasm": obf_qasm
    }

