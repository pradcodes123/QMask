def semantic_accuracy(orig_counts, obf_counts):
    total = sum(orig_counts.values())

    if total == 0:
        return 100.0

    correct = sum(
        min(orig_counts.get(k, 0), obf_counts.get(k, 0))
        for k in set(orig_counts) | set(obf_counts)
    )

    return 100.0 * correct / total


def tvd(orig_counts, obf_counts, shots=None):
    if shots is None:
        shots = sum(orig_counts.values())

    keys = set(orig_counts) | set(obf_counts)

    return sum(
        abs(orig_counts.get(k, 0) - obf_counts.get(k, 0))
        for k in keys
    ) / (2 * shots)


def dfc(orig_counts, obf_counts, shots=None):
    if shots is None:
        shots = sum(orig_counts.values())

    # "Correct" = outcomes that existed in original
    correct = sum(obf_counts.get(k, 0) for k in orig_counts.keys())

    # Worst wrong outcome
    wrong_max = max(
        (obf_counts.get(k, 0) for k in obf_counts.keys() if k not in orig_counts),
        default=0
    )

    return (correct - wrong_max) / shots


def compute_all(orig_counts, obf_counts):
    return {
        "semantic_accuracy": semantic_accuracy(orig_counts, obf_counts),
        "tvd": tvd(orig_counts, obf_counts),
        "dfc": dfc(orig_counts, obf_counts)
    }