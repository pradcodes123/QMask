import random
from qiskit import QuantumCircuit, transpile, ClassicalRegister
import qiskit.qasm3, qiskit.qasm2

rng = random.Random(1337)

def add_measurements(circuit):
    # Check if the circuit already has measurements
    has_measurements = any(instruction.operation.name == "measure" for instruction in circuit.data)
    
    if not has_measurements:
        if not circuit.clbits:
            circuit.add_register(ClassicalRegister(len(circuit.qubits), 'c'))
        
        # Determine how many qubits to measure based on classical bits available
        num_clbits = len(circuit.clbits)
        qubits_to_measure = circuit.qubits[:min(num_clbits, len(circuit.qubits))]
        
        # Add measurements
        for i, qubit in enumerate(qubits_to_measure):
            circuit.measure(qubit, circuit.clbits[i])
    
    return circuit

def auxiliary_gate():
    sub_circuit = QuantumCircuit(1, name='auxiliary')
    sub_circuit.h(0)
    sub_circuit.h(0)
    sub_circuit.z(0)
    sub_circuit.x(0)
    sub_circuit.z(0)
    sub_circuit.x(0)
    auxiliary = sub_circuit.to_gate()
    auxiliary.name = 'auxiliary'
    return auxiliary

def restore_gate():
    sub_circuit = QuantumCircuit(1, name='restore')
    sub_circuit.x(0)
    sub_circuit.z(0)
    sub_circuit.x(0)
    sub_circuit.z(0)
    sub_circuit.h(0)
    sub_circuit.h(0)
    restore = sub_circuit.to_gate()
    restore.name = 'restore'
    return restore

def encapsulate_original_gate(gate, num_qubits):
    sub_circuit = QuantumCircuit(num_qubits, name='encapsulated')
    sub_circuit.append(gate, list(range(num_qubits)))
    encapsulated = sub_circuit.to_gate()
    encapsulated.name = 'FourierTransform'
    return encapsulated

def apply_auxiliary_gates(circuit, qr):
    for qubit in qr:
        circuit.append(auxiliary_gate(), [qubit])

def apply_restore_gates(circuit, qr):
    for qubit in qr:
        circuit.append(restore_gate(), [qubit])

def obfuscate_circuit(circuit, enable=False):
    if enable:
        qr = circuit.qubits
        apply_auxiliary_gates(circuit, qr)
        apply_restore_gates(circuit, qr)
    return circuit

def insert_obfuscation(circuit, level: int):
    if level == 0:
        encapsulate_prob = 0.3
        rounds = 1
        shell_repeats = 1

    elif level == 1:
        encapsulate_prob = 0.6
        rounds = 1
        shell_repeats = 2

    elif level == 2:
        encapsulate_prob = 0.85
        rounds = 2
        shell_repeats = 3

    else:
        raise ValueError("Invalid obfuscation level (use 0, 1, or 2)")

    c = circuit
    for _ in range(rounds):
        c = _insert_obfuscation_core(
            c,
            encapsulate_probability=encapsulate_prob,
            shell_repeats=shell_repeats
        )
    return c

def _insert_obfuscation_core(
    circuit,
    encapsulate_probability=0.5,
    shell_repeats=1
):
    new_circuit = QuantumCircuit(*circuit.qregs, *circuit.cregs)
    measurement_instructions = []
    obfuscation_done = False

    for instruction in circuit.data:
        instr = instruction.operation
        qargs = instruction.qubits
        cargs = instruction.clbits

        if instr.name == "measure":
            measurement_instructions.append((instr, qargs, cargs))
            continue

        if not obfuscation_done:
            for _ in range(shell_repeats):
                obfuscate_circuit(new_circuit, enable=True)
            obfuscation_done = True

        if rng.random() < encapsulate_probability:
            encapsulated_gate = encapsulate_original_gate(instr, len(qargs))
            new_circuit.append(encapsulated_gate, qargs, cargs)
        else:
            new_circuit.append(instr, qargs, cargs)

    if obfuscation_done:
        for _ in range(shell_repeats):
            obfuscate_circuit(new_circuit, enable=True)

    for instr, qargs, cargs in measurement_instructions:
        new_circuit.append(instr, qargs, cargs)

    return new_circuit


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

    # 3. Map level
    if level not in LEVEL_MAP:
        raise ValueError(f"Invalid level: {level}")

    lvl = LEVEL_MAP[level]

    # 4. Apply obfuscation
    obf_qc = insert_obfuscation(qc, lvl)

    # 5. Convert back
    if is_qasm2:
        obf_qasm = qiskit.qasm2.dumps(obf_qc)
    else:
        obf_qasm = qiskit.qasm3.dumps(obf_qc)

    return {
        "obfuscated_qasm": obf_qasm
    }