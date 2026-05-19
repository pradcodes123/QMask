from collections import Counter

ENTANGLING_GATES = ["cx", "cz", "swap"]

def count_entangling(qc):

    count = 0

    for instr, qargs, cargs in qc.data:

        if instr.name in ENTANGLING_GATES:
            count += 1

    return count


def compute_vqc_metrics(orig_qc, obf_qc):

    orig_depth = orig_qc.depth()
    obf_depth = obf_qc.depth()

    orig_ent = count_entangling(orig_qc)
    obf_ent = count_entangling(obf_qc)

    return {

        "depth_ratio":
            round(obf_depth / max(orig_depth, 1), 3),

        "entangling_gate_shift":
            obf_ent - orig_ent,

        "original_entangling":
            orig_ent,

        "obfuscated_entangling":
            obf_ent
    }