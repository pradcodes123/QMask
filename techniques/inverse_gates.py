import random
import qiskit
from qiskit import QuantumCircuit,  ClassicalRegister
import qiskit.qasm3, qiskit.qasm2

random.seed(42)

def add_measurements(circuit):
    # Check if the circuit already has measurements
    has_measurements = any(instruction.operation.name == "measure" for instruction in circuit.data)
    
    if not has_measurements:
        if not circuit.clbits:
            print("Warning: No classical registers found. Adding one.")
            circuit.add_register(ClassicalRegister(len(circuit.qubits), 'c'))
        
        # Determine how many qubits to measure based on classical bits available
        num_clbits = len(circuit.clbits)
        qubits_to_measure = circuit.qubits[:min(num_clbits, len(circuit.qubits))]
        
        # Add measurements
        for i, qubit in enumerate(qubits_to_measure):
            circuit.measure(qubit, circuit.clbits[i])
        print(f"Added measurements for {len(qubits_to_measure)} qubits to classical register.")
    
    return circuit

def apply_dynamic_obfuscation(circuit, qr):
    gates = [
        ('h', 'h'), ('x', 'x'), ('z', 'z'), ('s', 'sdg'),
        ('t', 'tdg'), ('cx', 'cx'), ('cz', 'cz'), ('cy', 'cy'), ('ccx', 'ccx')
    ]

    for q in qr:
        for gate_pair in random.sample(gates, k=len(gates)):
            apply_gate_pair(circuit, q, gate_pair)

def apply_gate_pair(circuit, q, gate_pair):
    gate1, gate2 = gate_pair
    num_qubits = len(circuit.qubits)
    if gate1 in ['cx', 'cz', 'cy', 'ccx']:
        if gate1 == 'ccx' and num_qubits >= 3:
            target_qubits = random.sample(circuit.qubits, k=3)
            circuit.ccx(target_qubits[0], target_qubits[1], target_qubits[2])
            circuit.ccx(target_qubits[0], target_qubits[1], target_qubits[2])
        elif num_qubits >= 2:
            target_qubits = random.sample(circuit.qubits, k=2)
            if gate1 == 'cx':
                circuit.cx(target_qubits[0], target_qubits[1])
                circuit.cx(target_qubits[0], target_qubits[1])
            elif gate1 == 'cz':
                circuit.cz(target_qubits[0], target_qubits[1])
                circuit.cz(target_qubits[0], target_qubits[1])
            elif gate1 == 'cy':
                circuit.cy(target_qubits[0], target_qubits[1])
                circuit.cy(target_qubits[0], target_qubits[1])
    else:
        getattr(circuit, gate1)(q)
        getattr(circuit, gate2)(q)

def obfuscate_circuit(circuit, level=0):
    """
    level 0 -> light
    level 1 -> moderate
    level 2 -> heavy
    """

    qr = circuit.qubits
    cr = circuit.clbits

    # strength knobs
    if level == 0:
        segments = 4        # fewer injections
    elif level == 1:
        segments = 3
    elif level == 2:
        segments = 2        # very frequent injections
    else:
        raise ValueError("level must be 0, 1, or 2")

    obfuscated_circuit = QuantumCircuit(len(qr), len(cr))

    qubit_map = {old_q: obfuscated_circuit.qubits[i] for i, old_q in enumerate(qr)}
    clbit_map = {old_c: obfuscated_circuit.clbits[i] for i, old_c in enumerate(cr)}

    segment_length = max(1, len(circuit.data) // segments)
    measurement_instructions = []

    for i, instruction in enumerate(circuit.data):
        instr = instruction.operation
        qargs = instruction.qubits
        cargs = instruction.clbits

        if instr.name == "measure":
            measurement_instructions.append(
                (instr,
                 [qubit_map[q] for q in qargs],
                 [clbit_map[c] for c in cargs])
            )
            continue

        # inject BEFORE
        if i % segment_length == 0:
            apply_dynamic_obfuscation(obfuscated_circuit, obfuscated_circuit.qubits)

        obfuscated_circuit.append(
            instr,
            [qubit_map[q] for q in qargs],
            [clbit_map[c] for c in cargs]
        )

        # inject AFTER (only moderate & heavy)
        if level >= 1 and i % segment_length == segment_length - 1:
            apply_dynamic_obfuscation(obfuscated_circuit, obfuscated_circuit.qubits)

    # heavy gets final blast
    if level == 2:
        apply_dynamic_obfuscation(obfuscated_circuit, obfuscated_circuit.qubits)

    for instr, qargs, cargs in measurement_instructions:
        obfuscated_circuit.append(instr, qargs, cargs)

    return obfuscated_circuit


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

    # 3. Level check
    if level not in LEVEL_MAP:
        raise ValueError(f"Invalid level: {level}")

    lvl = LEVEL_MAP[level]

    # 4. Apply obfuscation
    obf_qc = obfuscate_circuit(qc, level=lvl)

    # 5. Convert back
    if is_qasm2:
        obf_qasm =  qiskit.qasm2.dumps(obf_qc)
    else:
        obf_qasm = qiskit.qasm3.dumps(obf_qc)

    return {
        "obfuscated_qasm": obf_qasm
    }