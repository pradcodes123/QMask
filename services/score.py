def compute_score(
    general_metrics,
    specific_metrics,
    time_orig,
    time_obf
):

    # =========================
    # GENERAL METRICS
    # =========================

    semantic_accuracy = (
        general_metrics.get(
            "semantic_accuracy",
            100
        ) / 100
    )

    tvd = general_metrics.get("tvd", 0)

    # lower runtime overhead is better
    time_ratio = (
        time_obf / time_orig
        if time_orig else 1
    )

    runtime_score = min(
            1 / max(time_ratio, 0.001),
            1
        )

    # =========================
    # BASE SCORE
    # =========================

    score = (
        0.45 * semantic_accuracy +
        0.35 * (1 - tvd) +
        0.20 * runtime_score
    )

    # =========================
    # SPECIFIC METRIC PENALTIES
    # =========================

    depth_ratio = specific_metrics.get(
        "depth_ratio",
        1
    )

    score *= (
        1 - min(
            (depth_ratio - 1) * 0.1,
            0.2
        )
    )

    # TTN hierarchy penalty
    if (
        "hierarchy_preserved"
        in specific_metrics
    ):

        if not specific_metrics[
            "hierarchy_preserved"
        ]:

            score *= 0.9

    # IQP phase penalty
    if (
        "phase_structure_preserved"
        in specific_metrics
    ):

        if not specific_metrics[
            "phase_structure_preserved"
        ]:

            score *= 0.92

    # Reupload encoding penalty
    if (
        "encoding_structure_preserved"
        in specific_metrics
    ):

        if not specific_metrics[
            "encoding_structure_preserved"
        ]:

            score *= 0.93

    # clamp between 0 and 1
    score = max(0, min(score, 1))

    return round(score, 4)