ENT_GATES = [
    "cx",
    "cz",
    "swap"
]

def count_ent_layers(qc):

    count = 0

    for instr, qargs, cargs in qc.data:

        if instr.name in ENT_GATES:
            count += 1

    return count


def compute_sel_metrics(orig_qc, obf_qc):

    orig_ent = count_ent_layers(orig_qc)
    obf_ent = count_ent_layers(obf_qc)

    return {

        "entanglement_shift":
            obf_ent - orig_ent,

        "entanglement_ratio":
            round(
                obf_ent / max(orig_ent, 1),
                3
            ),

        "learning_depth_growth":
            round(
                obf_qc.depth() /
                max(orig_qc.depth(), 1),
                3
            ),

        "learning_structure_preserved":
            abs(obf_ent - orig_ent) <= 2
    }