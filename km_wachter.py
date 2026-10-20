# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.

SERVICE_INTERVAL_KM: int = 15000
WARN_AT_PERCENT: int = 80


def wear_percent(km_since_service: float, interval: int) -> float:
    """Return how worn the service window is, as a percentage (0–100+).

    Uses true division so a car at 14,900 of 15,000 km reads ~99.3 %,
    not 0 % as it did with the old integer-division floor.
    """
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True when this car has reached the service-warning threshold.

    If no last_service_km reading exists we cannot compute wear, so the
    car is left un-flagged rather than being treated as worn from km 0.
    """
    if "last_service_km" not in car:
        return False
    km_since = car["odometer"] - car["last_service_km"]
    return wear_percent(km_since, SERVICE_INTERVAL_KM) >= WARN_AT_PERCENT


def check_fleet(fleet: list[dict]) -> list[str]:
    """Flag every car that needs a service and return their IDs."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            flagged.append(car["id"])
            print(f"SERVICE DUE: {car['id']}")
    return flagged
