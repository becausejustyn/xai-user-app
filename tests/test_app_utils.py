import json

import pytest

from app_utils import build_export, clear_demo_state, load_trials, normalise_points, select_trials


def add_trial(root, trial_id, complete=True):
    trial_dir = root / trial_id
    trial_dir.mkdir()
    (trial_dir / "prediction.png").touch()
    (trial_dir / "explanation_a.png").touch()
    if complete:
        (trial_dir / "explanation_b.png").touch()
    return trial_dir


def test_load_trials_finds_complete_image_sets(tmp_path):
    add_trial(tmp_path, "trial_01")
    add_trial(tmp_path, "trial_02")
    add_trial(tmp_path, "trial_incomplete", complete=False)

    trials = load_trials(tmp_path)

    assert [trial.trial_id for trial in trials] == ["trial_01", "trial_02"]
    assert all(trial.prediction.is_file() for trial in trials)
    assert all(trial.explanation_a.is_file() for trial in trials)
    assert all(trial.explanation_b.is_file() for trial in trials)


def test_select_trials_is_repeatable_and_unique(tmp_path):
    for index in range(12):
        add_trial(tmp_path, f"trial_{index:02d}")
    trials = load_trials(tmp_path)

    first = select_trials(trials, 10, seed=42)
    second = select_trials(trials, 10, seed=42)

    assert first == second
    assert len({trial.trial_id for trial in first}) == 10


def test_select_trials_rejects_invalid_count(tmp_path):
    add_trial(tmp_path, "trial_01")
    trials = load_trials(tmp_path)

    with pytest.raises(ValueError):
        select_trials(trials, 0, seed=42)
    with pytest.raises(ValueError):
        select_trials(trials, len(trials) + 1, seed=42)


def test_normalise_points_uses_zero_to_one_scale():
    result = normalise_points({"trial_01": [(96, 192), (384, 0)]}, image_size=384)

    assert result == {
        "trial_01": [
            {"x": 0.25, "y": 0.5},
            {"x": 1.0, "y": 0.0},
        ]
    }


def test_export_has_no_identifier_or_file_path():
    export = build_export(
        preferences={"trial_01": "A"},
        points={"trial_01": [(10, 20)]},
        survey={"helpful": "Agree"},
    )
    data = json.loads(export)

    assert data["explanation_preferences"] == {"trial_01": "A"}
    assert "participant" not in export.lower()
    assert "trials/" not in export


def test_clear_demo_state_keeps_unrelated_values():
    state = {"xai_demo_points": {"trial_01": []}, "other": "keep"}

    clear_demo_state(state)

    assert state == {"other": "keep"}
