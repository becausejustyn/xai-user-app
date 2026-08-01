"""Shared functions for the XAI study demonstration."""

from __future__ import annotations

import json
import random
from collections.abc import Iterable, Mapping, MutableMapping, Sequence
from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
TRIALS_DIR = ROOT_DIR / "trials"
DEMO_STATE_PREFIX = "xai_demo_"


@dataclass(frozen=True)
class Trial:
    """Paths for one prediction and its two explanations."""

    trial_id: str
    prediction: Path
    explanation_a: Path
    explanation_b: Path


def load_trials(trials_dir: Path = TRIALS_DIR) -> list[Trial]:
    """Load valid trial folders in name order."""

    trials: list[Trial] = []
    for trial_dir in sorted(path for path in trials_dir.glob("trial_*") if path.is_dir()):
        prediction = trial_dir / "prediction.png"
        explanation_a = trial_dir / "explanation_a.png"
        explanation_b = trial_dir / "explanation_b.png"
        if not all(path.is_file() for path in (prediction, explanation_a, explanation_b)):
            continue
        trials.append(
            Trial(
                trial_id=trial_dir.name,
                prediction=prediction,
                explanation_a=explanation_a,
                explanation_b=explanation_b,
            )
        )
    return trials


def select_trials(trials: Sequence[Trial], count: int, seed: int) -> list[Trial]:
    """Select a repeatable random set of trials."""

    if count < 1:
        raise ValueError("The trial count must be at least 1.")
    if count > len(trials):
        raise ValueError("The trial count is larger than the available trial set.")
    return random.Random(seed).sample(list(trials), count)


def find_trials(trial_ids: Iterable[str], trials: Sequence[Trial]) -> list[Trial]:
    """Return trials in the sequence given by their identifiers."""

    trial_by_id = {trial.trial_id: trial for trial in trials}
    return [trial_by_id[trial_id] for trial_id in trial_ids]


def normalise_points(
    points_by_trial: Mapping[str, Sequence[Sequence[int]]], image_size: int
) -> dict[str, list[dict[str, float]]]:
    """Convert pixel points to values from zero to one."""

    if image_size < 1:
        raise ValueError("The image size must be at least 1.")
    return {
        trial_id: [
            {"x": round(point[0] / image_size, 4), "y": round(point[1] / image_size, 4)}
            for point in points
        ]
        for trial_id, points in sorted(points_by_trial.items())
    }


def build_export(
    preferences: Mapping[str, str] | None = None,
    points: Mapping[str, Sequence[Sequence[int]]] | None = None,
    survey: Mapping[str, str] | None = None,
    image_size: int = 384,
) -> str:
    """Build a data export that contains no participant identifier or file path."""

    data = {
        "format_version": 1,
        "explanation_preferences": dict(sorted((preferences or {}).items())),
        "important_points": normalise_points(points or {}, image_size),
        "survey": dict(survey or {}),
    }
    return json.dumps(data, indent=2, sort_keys=True)


def clear_demo_state(state: MutableMapping[str, object]) -> None:
    """Remove all demo values from a Streamlit session state object."""

    for key in list(state):
        if key.startswith(DEMO_STATE_PREFIX):
            del state[key]
