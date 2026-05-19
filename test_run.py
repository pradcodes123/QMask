from techniques.cloakedGates import apply
from services.analyzer import analyze_basic
from services.metrics_general import compute_all

# 1. load circuit
with open("data/predefined/VQC_2/circuit.qasm") as f:
    qasm = f.read()

# 2. obfuscate
obf_qasm = apply(qasm, "light")["obfuscated_qasm"]

# 3. run analyzer → THIS defines result
result = analyze_basic(qasm, obf_qasm)

# 4. compute metrics
metrics = compute_all(result["orig_counts"], result["obf_counts"])

# 5. print everything
print("Counts original:", result["orig_counts"])
print("Counts obfuscated:", result["obf_counts"])

print("Time original:", result["time_orig"])
print("Time obfuscated:", result["time_obf"])

print("Metrics:", metrics)