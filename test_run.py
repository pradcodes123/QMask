import matplotlib.pyplot as plt

techniques = [
    "Basis\nTransformation",
    "Cloaked\nGates",
    "Composite\nGates",
    "Inverse\nGates",
    "Delayed\nGates"
]

# Estimated from your current results
time_ratio = [
    1.30,
    1.45,
    1.62,
    2.05,
    1.85
]

tvd = [
    0.03,
    0.08,
    0.17,
    0.24,
    0.31
]

plt.figure(figsize=(8,6))

plt.scatter(
    time_ratio,
    tvd,
    s=180
)

for i in range(len(techniques)):
    plt.text(
        time_ratio[i]+0.02,
        tvd[i]+0.005,
        techniques[i],
        fontsize=10
    )

plt.xlabel("Execution Time Ratio",fontsize=13)
plt.ylabel("Total Variation Distance (TVD)",fontsize=13)

plt.title(
    "Security–Performance Trade-off of Different Obfuscation Techniques",
    fontsize=15,
    weight="bold"
)

plt.grid(alpha=0.3)

plt.xlim(1.1,2.2)
plt.ylim(0,0.35)

plt.tight_layout()
plt.savefig("Graph2_Tradeoff.png",dpi=300)
plt.show()