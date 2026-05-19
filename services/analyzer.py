from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import time
import io, base64
import matplotlib.pyplot as plt

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return img_base64

sim = AerSimulator()

def analyze_basic(original_qasm, obfuscated_qasm):

    orig_qc = QuantumCircuit.from_qasm_str(original_qasm)
    obf_qc  = QuantumCircuit.from_qasm_str(obfuscated_qasm)


    # transpile
    orig_t = transpile(orig_qc, sim)
    obf_t  = transpile(obf_qc, sim)

    # run original
    t0 = time.time()
    res_orig = sim.run(orig_t, shots=512).result()
    t1 = time.time()

    # run obfuscated
    t2 = time.time()
    res_obf = sim.run(obf_t, shots=512).result()
    t3 = time.time()

    return {
        "orig_counts": res_orig.get_counts(),
        "obf_counts": res_obf.get_counts(),
        "time_orig": t3 - t2,
        "time_obf": t1 - t0,
        "orig_qc": orig_qc,
        "obf_qc": obf_qc
    }