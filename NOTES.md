# What I checked, and what the agent got wrong
## What the agent got wrong
- **Missing reading assumption:** The agent decided to return False for cars with no odometer reading, assuming "not due." That's a judgment call I had to evaluate, not a universal truth.

- **The silent constant:** MILES_PER_KM had been wrong since 2015. The agent missed it entirely; I only caught it by manually reading through the code.


## What I checked before I accepted its work
- **Ran unit tests:** Executed py -m pytest test_km_wachter.py test_fleet_report.py -v and watched it go from 3 failing to 5 passing.
- **Verification script:** Ran py verify.py to confirm it hit 10/11.
- **Manual line check:** Verified km_wachter.py line 14 myself to make sure SERVICE_INTERVAL_KM (15000) and WARN_AT_PERCENT (80) were left completely untouched.

## What the data actually said
- **The surprise:** Total mileage (odometer_km, +0.3%) and age (age_years, -0.2%) predicted almost nothing.
- **The real predictors:** Breakdowns were driven entirely by km_since_service (+60.8%) and avg_daily_km (+21.5%).
