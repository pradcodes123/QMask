PHASE_GATES = [
    "z",
    "rz",
    "p",
    "s",
    "t",
    "cz"
]

def count_phase_gates(qc):

    count = 0

    for instr, qargs, cargs in qc.data:

        if instr.name in PHASE_GATES:
            count += 1

    return count


def compute_iqp_metrics(orig_qc, obf_qc):

    orig_phase = count_phase_gates(orig_qc)
    obf_phase = count_phase_gates(obf_qc)

    ratio = (
        obf_phase / max(orig_phase, 1)
    )

    return {

        "phase_gate_ratio":
            round(ratio, 3),

        "original_phase_gates":
            orig_phase,

        "obfuscated_phase_gates":
            obf_phase,

    }