PARAM_GATES = [
    "rx",
    "ry",
    "rz",
    "u",
    "u1",
    "u2",
    "u3"
]

def count_param_gates(qc):

    count = 0

    for instr, qargs, cargs in qc.data:

        if instr.name in PARAM_GATES:
            count += 1

    return count


def compute_mpu_metrics(orig_qc, obf_qc):

    orig_param = count_param_gates(orig_qc)
    obf_param = count_param_gates(obf_qc)

    return {

        "parameter_gate_shift":
            obf_param - orig_param,

        "parameter_density_ratio":
            round(
                obf_param / max(orig_param, 1),
                3
            ),

        "unitary_depth_growth":
            round(
                obf_qc.depth() /
                max(orig_qc.depth(), 1),
                3
            ),

        "unitary_structure_preserved":
            abs(obf_param - orig_param) <= 3
    }