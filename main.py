import matplotlib
matplotlib.use("Agg")
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import io, base64
import matplotlib.pyplot as plt
from services.circuit_classifier import load_config
from typing import Optional
from services.metrics_router import compute_metrics
from services.score import compute_score

# =============================
# INIT APP + CORS (IMPORTANT)
# =============================

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return img_base64

# =============================
# IMPORTS
# =============================

from techniques import (
    cloaked_gates,
    composite_gates,
    basis_transformation,
    delayed_gates,
    inverse_gates
)

from services.analyzer import analyze_basic
from services.metrics_general import compute_all


# =============================
# REQUEST MODEL
# =============================

class AnalyzeRequest(BaseModel):
    qasm: str
    technique: str
    level: str
    circuit_name: Optional[str] = None


# =============================
# TECHNIQUE MAP
# =============================

TECHNIQUE_MAP = {
    "cloaked": cloaked_gates,
    "composite": composite_gates,
    "basis": basis_transformation,
    "delayed": delayed_gates,
    "inverse": inverse_gates
}



# =============================
# MAIN ENDPOINT
# =============================

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    try:
        print("CIRCUIT NAME:", req.circuit_name)
        config = load_config(req.circuit_name)

        print(config)
        # =============================
        # VALIDATE TECHNIQUE
        # =============================

        technique_module = TECHNIQUE_MAP.get(req.technique)

        if technique_module is None:
            return {"error": f"Invalid technique: {req.technique}"}

        # =============================
        # CLEAN INPUT
        # =============================

        qasm = req.qasm.strip()

        if "OPENQASM" not in qasm:
            return {"error": "Invalid QASM format"}

        # =============================
        # APPLY OBFUSCATION
        # =============================

        result = technique_module.apply(qasm, req.level)
        obf_qasm = result["obfuscated_qasm"]

        # =============================
        # RUN ANALYSIS
        # =============================

        analysis = analyze_basic(qasm, obf_qasm)

        orig_qc = analysis["orig_qc"]
        obf_qc = analysis["obf_qc"]

        # Draw circuits
        orig_fig = orig_qc.draw(output="mpl")
        orig_base64 = fig_to_base64(orig_fig)

        obf_fig = obf_qc.draw(output="mpl")
        obf_base64 = fig_to_base64(obf_fig)

        # =============================
        # COMPUTE METRICS
        # =============================

        metric_results = compute_metrics(
            config,
            analysis["orig_counts"],
            analysis["obf_counts"],
            orig_qc,
            obf_qc
        )

        # =============================
        # COMPUTE SCORE
        # =============================

        time_ratio = (
            analysis["time_obf"] / analysis["time_orig"]
            if analysis["time_orig"] > 0 else 1
        )

        score = compute_score(
            metric_results["general"],
            metric_results["specific"],
            analysis["time_orig"],
            analysis["time_obf"]
        )

        # =============================
        # RESPONSE
        # =============================

        return {
            "score": score,
            "general_metrics": metric_results["general"],
            "specific_metrics": metric_results["specific"],
            "counts_original": analysis["orig_counts"],
            "counts_obfuscated": analysis["obf_counts"],
            "time_orig": analysis["time_orig"],
            "time_obf": analysis["time_obf"],
            "images": {
                "original": orig_base64,
                "obfuscated": obf_base64
            }
        }

    except Exception as e:
        print(" ERROR:", e)
        return {"error": str(e)}