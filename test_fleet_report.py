# test_fleet_report.py
from fleet_report import fleet_summary

SAMPLE = [
    {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
    {"id": "VOS-2210", "odometer": 48400, "last_service_km": 45000},
]


def test_summary_counts_due_cars():
    # Only VOS-4471 is nearly worn (~99.3%), so exactly one car is due.
    assert fleet_summary(SAMPLE)["due"] == 1


def test_summary_does_not_crash_on_missing_reading():
    # A car with no last_service_km must not raise a KeyError — it should
    # contribute 0% wear and be treated as not due.
    fleet = [
        {"id": "VOS-4471", "odometer": 14900, "last_service_km": 0},
        {"id": "VOS-7788", "odometer": 92000},   # no last_service_km
    ]
    result = fleet_summary(fleet)
    assert "average_wear" in result
    assert result["due"] == 1   # only VOS-4471 is flagged; VOS-7788 has no reading


def test_wear_math_is_correct():
    # A car at 14,900 of its 15,000 km window must report close to 99.3% wear,
    # not 0% as the old integer-division floor produced.
    from km_wachter import wear_percent
    pct = wear_percent(14900, 15000)
    assert 99.0 <= pct <= 100.0, f"Expected ~99.3%, got {pct:.2f}%"
