from pegy_tracker.calculations.validation import cap_outliers, validate_positive


def test_validate_positive_updates_flags() -> None:
    flags: list[str] = []
    assert validate_positive(None, "pe", flags) is False
    assert flags == ["missing:pe"]

    flags.clear()
    assert validate_positive(0.0, "pe", flags) is False
    assert flags == ["nonpositive:pe"]

    flags.clear()
    assert validate_positive(3.2, "pe", flags) is True
    assert flags == []


def test_cap_outliers_clips_and_flags() -> None:
    flags: list[str] = []
    assert cap_outliers(-1.0, 0.0, 1.0, "growth", flags) == 0.0
    assert flags == ["clipped_low:growth"]

    flags.clear()
    assert cap_outliers(2.0, 0.0, 1.0, "growth", flags) == 1.0
    assert flags == ["clipped_high:growth"]

    flags.clear()
    assert cap_outliers(0.5, 0.0, 1.0, "growth", flags) == 0.5
    assert flags == []
