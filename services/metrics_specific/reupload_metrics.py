ENCODING_GATES = [
    "rx",
    "ry",
    "rz"
]

def count_encoding_gates(qc):

    count = 0

    for instr, qargs, cargs in qc.data:

        if instr.name in ENCODING_GATES:
            count += 1

    return count


def compute_reupload_metrics(orig_qc, obf_qc):

    orig_enc = count_encoding_gates(orig_qc)
    obf_enc = count_encoding_gates(obf_qc)

    return {

        "encoding_gate_shift":
            obf_enc - orig_enc,

        "encoding_density_ratio":
            round(
                obf_enc / max(orig_enc, 1),
                3
            ),

        "reupload_depth_growth":
            round(
                obf_qc.depth() /
                max(orig_qc.depth(), 1),
                3
            ),

        "encoding_structure_preserved":
            abs(obf_enc - orig_enc) <= 3
    }