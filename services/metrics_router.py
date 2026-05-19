from services.metrics_general import compute_all
from services.metrics_specific.vqc_metrics import compute_vqc_metrics
from services.metrics_specific.ttn_metrics import compute_ttn_metrics
from services.metrics_specific.iqp_metrics import compute_iqp_metrics
from services.metrics_specific.qaoa_metrics import compute_qaoa_metrics
from services.metrics_specific.reupload_metrics import compute_reupload_metrics
from services.metrics_specific.mpu_metrics import compute_mpu_metrics
from services.metrics_specific.sel_metrics import compute_sel_metrics
def compute_metrics(
    config,
    orig_counts,
    obf_counts,
    orig_qc,
    obf_qc
):

    # =========================
    # GENERAL METRICS
    # =========================

    general_metrics = compute_all(
        orig_counts,
        obf_counts
    )

    # =========================
    # SPECIFIC METRICS
    # =========================

    specific_metrics = {}

    if config is not None:

        family = config.get("type")

        if family == "vqc_model":

            specific_metrics = compute_vqc_metrics(
                orig_qc,
                obf_qc
            )

        elif family == "ttn":

            specific_metrics = compute_ttn_metrics(
            orig_qc,
            obf_qc
            )    
        elif family == "iqp":

            specific_metrics = compute_iqp_metrics(
                orig_qc,
                obf_qc
            )    

        elif family == "qaoa":

            specific_metrics = compute_qaoa_metrics(
                orig_qc,
                obf_qc
            )    

        elif family == "reupload":

            specific_metrics = compute_reupload_metrics(
                orig_qc,
                obf_qc
            )    

        elif family == "mpu":

            specific_metrics = compute_mpu_metrics(
                orig_qc,
                obf_qc
            )       

        elif family == "sel":

            specific_metrics = compute_sel_metrics(
                orig_qc,
                obf_qc
            )         
            
    print("SPECIFIC METRICS:", specific_metrics)        

    return {
        "general": general_metrics,
        "specific": specific_metrics
    }