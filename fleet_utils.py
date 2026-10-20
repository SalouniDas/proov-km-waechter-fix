# fleet_utils.py
# Shared helpers for KM-Waechter.

# Correct factor: 1 kilometre = 0.621371 miles.
# The old value (1.609) was km-per-mile — the inverse — making every UK
# mileage figure ~2.6× too large.
MILES_PER_KM: float = 0.621371


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles for the UK partner report."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a number to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a value as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list[float]) -> float:
    """Return the arithmetic mean of a list, or 0 if the list is empty."""
    if not values:
        return 0.0
    return sum(values) / len(values)
