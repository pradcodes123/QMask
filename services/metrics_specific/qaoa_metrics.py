MIXER_GATES = [
    "rx",
    "x"
]

COST_GATES = [
    "rz",
    "cz",
    "cp"
]

def count_gate_family(qc, family):

    count = 0

    for instr, qargs, cargs in qc.data:

        if instr.name in family:
            count += 1

    return count


def compute_qaoa_metrics(orig_qc, obf_qc):

    orig_mix = count_gate_family(
        orig_qc,
        MIXER_GATES
    )

    obf_mix = count_gate_family(
        obf_qc,
        MIXER_GATES
    )

    orig_cost = count_gate_family(
        orig_qc,
        COST_GATES
    )

    obf_cost = count_gate_family(
        obf_qc,
        COST_GATES
    )

    return {

        "mixer_layer_shift":
            obf_mix - orig_mix,

        "cost_layer_shift":
            obf_cost - orig_cost,

        "depth_growth":
            round(
                obf_qc.depth() /
                max(orig_qc.depth(), 1),
                3
            ),

        "optimization_structure_preserved":
            abs(obf_mix - orig_mix) <= 2
    }