"""Functions for analysing reaction-time data."""

from pathlib import Path

import pandas as pd
import os

REQUIRED_COLUMNS = {
    "participant",
    "condition",
    "reaction_time_ms",
    "correct",
}


def load_data(path: Path) -> pd.DataFrame:
    """Load reaction-time observations from a CSV file."""
    if not path.exists():
        raise FileNotFoundError(f"Data file does not exist: {path}")

    return pd.read_csv(path)


def validate_columns(data: pd.DataFrame) -> None:
    """Check that all required columns are present."""
    missing = REQUIRED_COLUMNS - set(data.columns)

    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def validate_reaction_times(data: pd.DataFrame) -> None:
    """Check that reaction times are physically possible."""
    reaction_times = pd.Series(
        data["reaction_time_ms"],
        dtype="float64",
    )

    if reaction_times.isna().any():
        raise ValueError("Reaction times must not be missing")

    if (reaction_times <= 0).any():
        raise ValueError("Reaction times must be greater than zero")


def validate_data(data: pd.DataFrame) -> None:
    """Validate structural and domain assumptions about raw observations."""
    if data.empty:
        raise ValueError("Dataset contains no observations")

    validate_columns(data)
    validate_reaction_times(data)


def clean_trials(data: pd.DataFrame) -> pd.DataFrame:
    """Apply the predefined trial-exclusion criteria."""
    correct = pd.Series(
        data["correct"],
        dtype="bool",
    )

    reaction_times = pd.Series(
        data["reaction_time_ms"],
        dtype="float64",
    )

    plausible_rt = reaction_times.between(
        100,
        3000,
        inclusive="both",
    )

    return data.loc[correct & plausible_rt].copy()


def summarise(
    data: pd.DataFrame,
) -> list[tuple[str, float]]:
    """Calculate mean reaction time for each condition."""
    summary = data.groupby("condition", as_index=False).agg(
        mean_reaction_time=(
            "reaction_time_ms",
            "mean",
        )
    )

    conditions = summary["condition"].astype(str).tolist()
    means = summary["mean_reaction_time"].astype(float).tolist()

    return list(zip(conditions, means, strict=True))


def analyse(path: Path) -> list[tuple[str, float]]:
    """Run the complete reaction-time analysis."""
    data = load_data(path)

    validate_data(data)

    cleaned = clean_trials(data)

    if cleaned.empty:
        raise ValueError("No valid trials remain after cleaning")

    return summarise(cleaned)
