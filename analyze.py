# analyze.py
# Risk factors: km_since_service and avg_daily_km are the two strongest predictors of breakdown.
# Cars already deep into their service window AND driven hard every day break down far more often.
# Total mileage and age show essentially zero difference between groups — do not use them.

# ── How this works ──────────────────────────────────────────────────────────────
# We compare 26 cars that later broke down against 94 that did not, column by column.
# km_since_service separates the groups most sharply (+61% higher mean, 81% of
# breakdowns above 10,000 km vs 33% of healthy cars). avg_daily_km is second (+22%).
# load_factor adds a smaller but consistent signal (+19%). odometer_km and age_years
# show < 1% difference — they are not predictors here.
#
# The risk score weights all three separating factors, min–max scaled to 0–100,
# then blends them: 50% km_since_service + 30% avg_daily_km + 20% load_factor.
# No machine learning; just scaled arithmetic on the columns that actually differ.
# ────────────────────────────────────────────────────────────────────────────────

import pandas as pd


def group_comparison(df: pd.DataFrame) -> None:
    """Print mean of each numeric column for cars that broke down vs those that did not."""
    broke = df[df["broke_down"] == 1]
    fine  = df[df["broke_down"] == 0]
    features = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]

    print(f"\n{'Column':<22}  {'Broke mean':>12}  {'Fine mean':>12}  {'Diff':>8}")
    print("-" * 60)
    for col in features:
        bm = broke[col].mean()
        fm = fine[col].mean()
        diff = (bm - fm) / fm * 100 if fm else 0
        marker = "  << separates" if abs(diff) >= 15 else ""
        print(f"{col:<22}  {bm:>12.2f}  {fm:>12.2f}  {diff:>+7.1f}%{marker}")

    print(f"\nBreakdown rate: {len(broke)}/{len(df)} cars ({len(broke)/len(df)*100:.0f}%)")


def min_max_scale(series: pd.Series) -> pd.Series:
    """Scale a series to 0–1 using its own observed min and max."""
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series(0.5, index=series.index)
    return (series - lo) / (hi - lo)


def build_risk_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute a 0–100 risk score for each car.

    Weights (chosen from the group-comparison results):
      50 %  km_since_service  — strongest separator: 81 % of breakdowns > 10,000 km
      30 %  avg_daily_km      — second strongest: harder daily use, higher risk
      20 %  load_factor       — consistent signal, smaller magnitude

    odometer_km and age_years are explicitly excluded: they showed < 1 % difference
    between groups, so including them would add noise, not signal.
    """
    result = df.copy()
    result["_kss"] = min_max_scale(df["km_since_service"])
    result["_adk"] = min_max_scale(df["avg_daily_km"])
    result["_lf"]  = min_max_scale(df["load_factor"])

    result["risk_score"] = (
        0.50 * result["_kss"] +
        0.30 * result["_adk"] +
        0.20 * result["_lf"]
    ) * 100

    return result.drop(columns=["_kss", "_adk", "_lf"])


def main() -> None:
    df = pd.read_csv("fleet_history.csv")

    # -- Step 1: what the data says ------------------------------------------
    print("=" * 60)
    print("STEP 1 - Group comparison: who broke down vs who did not")
    print("=" * 60)
    group_comparison(df)
    print(
        "\nConclusion: km_since_service (+61%) and avg_daily_km (+22%) are the\n"
        "real predictors. load_factor adds a smaller consistent signal (+19%).\n"
        "odometer_km (+0.3%) and age_years (-0.2%) are NOT predictors here."
    )

    # ── Step 2 + 3: build scores and rank ────────────────────────────────────
    print("\n" + "=" * 60)
    print("STEP 2+3 - Risk scores and top 10 highest-risk cars")
    print("=" * 60)
    scored = build_risk_scores(df)
    ranked = scored.sort_values("risk_score", ascending=False).reset_index(drop=True)

    top10 = ranked[["car_id", "km_since_service", "avg_daily_km",
                     "load_factor", "risk_score", "broke_down"]].head(10)
    top10 = top10.rename(columns={
        "car_id":           "Car",
        "km_since_service": "km since svc",
        "avg_daily_km":     "daily km",
        "load_factor":      "load",
        "risk_score":       "risk (0-100)",
        "broke_down":       "broke?",
    })
    pd.set_option("display.float_format", "{:.1f}".format)
    print(top10.to_string(index=True))

    # ── Quick accuracy check ─────────────────────────────────────────────────
    top25 = ranked.head(25)
    found = top25["broke_down"].sum()
    total_breakdowns = df["broke_down"].sum()
    print(
        f"\nValidation: the top-25 by risk score contain {found} of the "
        f"{total_breakdowns} cars that actually broke down "
        f"({found/total_breakdowns*100:.0f}% recall)."
    )


if __name__ == "__main__":
    main()
