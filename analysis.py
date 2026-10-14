import pandas as pd
import matplotlib.pyplot as plt


def analyse(file):
    data = pd.read_csv(file)
    data = data[data["correct"] == True]
    data = data[(data["reaction_time_ms"] > 100) & (data["reaction_time_ms"] < 3000)]
    means = []
    for condition in data["condition"].unique():
        subset = data[data["condition"] == condition]
        means.append((condition, subset["reaction_time_ms"].mean()))
    return means


results = analyse("data/results.csv")
conditions = [x[0] for x in results]
reaction_times = [x[1] for x in results]
plt.bar(conditions, reaction_times)
plt.ylabel("Mean reaction time (ms)")
plt.tight_layout()
plt.savefig("figure1.png")
