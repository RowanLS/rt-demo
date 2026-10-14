"""Generate Figure 1 from the validated analysis."""

from pathlib import Path

import matplotlib.pyplot as plt

from rt_analysis.analysis import analyse


def main() -> None:
    """Write a bar chart of mean RTs by condition."""
    results = analyse(Path("data/results.csv"))
    names = [name for name, _ in results]
    values = [rt for _, rt in results]
    fig, ax = plt.subplots()
    ax.bar(names, values)
    ax.set(xlabel="Condition", ylabel="Mean reaction time (ms)")
    fig.tight_layout()
    fig.savefig("figure1.png")
    plt.close(fig)
    print("Wrote figure1.png")


if __name__ == "__main__":
    main()
