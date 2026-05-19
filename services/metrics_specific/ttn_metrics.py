from collections import defaultdict

def qubit_degree(qc):

    degree = defaultdict(int)

    for instr, qargs, cargs in qc.data:

        if len(qargs) >= 2:

            for q in qargs:

                idx = qc.qubits.index(q)

                degree[idx] += 1

    return degree


def compute_ttn_metrics(orig_qc, obf_qc):

    orig_deg = qubit_degree(orig_qc)
    obf_deg = qubit_degree(obf_qc)

    total_orig = sum(orig_deg.values())
    total_obf = sum(obf_deg.values())

    expansion = total_obf - total_orig

    return {

        "qubit_degree_expansion": expansion,

        "original_connectivity":
            total_orig,

        "obfuscated_connectivity":
            total_obf,

        "hierarchy_preserved":
            expansion <= 2
    }