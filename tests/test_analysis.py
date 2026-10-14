"""Behavioural and domain validation tests using synthetic data."""

import pandas as pd
import pytest

from rt_analysis.analysis import clean_trials, summarise, validate_data


def test_incorrect_trials_are_excluded() -> None:
    """A regression test for the correctness filter."""
    data = pd.DataFrame(
        {
            "participant": ["P1", "P1"],
            "condition": ["control", "control"],
            "reaction_time_ms": [400.0, 500.0],
            "correct": [True, False],
        }
    )
    assert clean_trials(data)["reaction_time_ms"].tolist() == [400.0]


def test_out_of_range_trials_are_excluded() -> None:
    """Predefined trimming thresholds are applied to a copy."""
    data = pd.DataFrame(
        {
            "participant": ["P1"] * 3,
            "condition": ["control"] * 3,
            "reaction_time_ms": [50.0, 400.0, 4000.0],
            "correct": [True] * 3,
        }
    )
    assert clean_trials(data)["reaction_time_ms"].tolist() == [400.0]
    assert len(data) == 3


def test_negative_rt_is_rejected() -> None:
    """Physically impossible values fail validation."""
    data = pd.DataFrame(
        {
            "participant": ["P1"],
            "condition": ["control"],
            "reaction_time_ms": [-250.0],
            "correct": [True],
        }
    )
    with pytest.raises(ValueError, match="greater than zero"):
        validate_data(data)


def test_condition_means() -> None:
    """The scientific summary matches hand-calculated values."""
    data = pd.DataFrame(
        {
            "participant": ["P1", "P2", "P1", "P2"],
            "condition": ["control", "control", "treatment", "treatment"],
            "reaction_time_ms": [400.0, 500.0, 300.0, 400.0],
            "correct": [True] * 4,
        }
    )
    assert summarise(data) == [("control", 450.0), ("treatment", 350.0)]


def test_negative_reaction_times_are_rejected() -> None:
    """Physically impossible reaction times should fail validation."""
    data = pd.DataFrame(
        {
            "participant": ["P01"],
            "condition": ["control"],
            "reaction_time_ms": [-250.0],
            "correct": [True],
        }
    )

    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        validate_data(data)
