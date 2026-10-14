"""Intentionally branch-heavy code for the complexity demonstration."""

from pathlib import Path

import pandas as pd


def analyse(
    file: Path,
    exclude_errors: bool = True,
    trim: bool = True,
    method: str = "mean",
    exclude_condition: str | None = None,
) -> list[tuple[str, float]]:
    """Analyse trials with an accumulating set of options."""
    data = pd.read_csv(file)
    if exclude_errors:
        correct = pd.Series(data["correct"], dtype="bool")
        data = data.loc[correct]
    if trim:
        rt = pd.Series(data["reaction_time_ms"], dtype="float64")
        data = data.loc[rt.between(100, 3000)]
    if exclude_condition is not None:
        condition = pd.Series(data["condition"], dtype="string")
        data = data.loc[condition != exclude_condition]
    if method == "mean":
        if exclude_errors:
            summary = data.groupby("condition", as_index=False).agg(
                rt=("reaction_time_ms", "mean")
            )
        else:
            summary = data.groupby("condition", as_index=False).agg(
                rt=("reaction_time_ms", "mean")
            )
    elif method == "median":
        if trim:
            summary = data.groupby("condition", as_index=False).agg(
                rt=("reaction_time_ms", "median")
            )
        else:
            summary = data.groupby("condition", as_index=False).agg(
                rt=("reaction_time_ms", "median")
            )
    else:
        raise ValueError(f"Unknown method: {method}")
    names: list[str] = summary["condition"].astype(str).tolist()
    values: list[float] = summary["rt"].astype(float).tolist()
    return list(zip(names, values, strict=True))


if __name__ == "__main__":
    print(analyse(Path("data/results.csv")))
