"""A deliberately simple typed analysis interface."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def analyse(file: Path) -> list[tuple[str, float]]:
    """Return mean reaction time for each condition."""
    data = pd.read_csv(file)
    correct = pd.Series(data["correct"], dtype="bool")
    data = data.loc[correct]
    rt = pd.Series(data["reaction_time_ms"], dtype="float64")
    data = data.loc[rt.between(100, 3000)]
    summary = data.groupby("condition", as_index=False).agg(
        rt=("reaction_time_ms", "mean")
    )
    names: list[str] = summary["condition"].astype(str).tolist()
    means: list[float] = summary["rt"].astype(float).tolist()
    return list(zip(names, means, strict=True))


if __name__ == "__main__":
    results = analyse(Path("data/results.csv"))
    fig, ax = plt.subplots()
    ax.bar([name for name, _ in results], [rt for _, rt in results])
    ax.set_ylabel("Mean reaction time (ms)")
    fig.tight_layout()
    fig.savefig("figure1.png")
    plt.close(fig)
