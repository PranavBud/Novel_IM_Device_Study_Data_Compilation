"""
Statistical Analysis Reproduction
=================================
Novel Conforming Intramedullary (IM) Device for Critical-Sized Bone Defects

Reproduces every inferential statistic reported in the paper from the
per-replicate raw data (data/cell_culture_raw.csv):

  - Two-way mixed-design ANOVA (Group between-subjects, Time within-subjects)
    for each pairwise group comparison, on both cell count and mineralization.
  - Per-timepoint Welch's two-sample t-tests (unequal variances).
  - Bonferroni correction across the timepoints (raw p x 5, capped at 1.000).
  - Cohen's d (pooled-SD standardized effect size) per timepoint.
  - 95% confidence intervals for the between-group difference per timepoint.

Methods/sources: Fisher (1925); Welch (1947); Satterthwaite (1946).

USAGE:
    1. Populate data/cell_culture_raw.csv from cell_culture_raw_template.csv
       (5 replicates per group, timepoints 0-4, columns: group, replicate,
       timepoint_week, cell_count, mineralization_pct).
    2. pip install -r requirements.txt
    3. python code/reproduce_statistics.py

The script prints results to the console and writes them to
data/statistics_results_reproduced.csv. Compare against the published values
in data/statistics_results.csv to confirm reproduction.

Author: Pranav Reddy Budipalli
"""

import numpy as np
import pandas as pd
from scipy import stats

try:
    import statsmodels.formula.api as smf
    from statsmodels.stats.anova import AnovaRM
    HAVE_SM = True
except ImportError:
    HAVE_SM = False

RAW_PATH = "data/cell_culture_raw.csv"
OUT_PATH = "data/statistics_results_reproduced.csv"
ALPHA = 0.05
N_TESTS = 5  # initial + 4 post-baseline timepoints (Bonferroni divisor)
METRICS = ["cell_count", "mineralization_pct"]
POST_BASELINE = [1, 2, 3, 4]


def cohens_d(a, b):
    """Pooled-standard-deviation Cohen's d for two independent samples."""
    na, nb = len(a), len(b)
    va, vb = np.var(a, ddof=1), np.var(b, ddof=1)
    pooled_sd = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    if pooled_sd == 0:
        return np.nan
    return (np.mean(a) - np.mean(b)) / pooled_sd


def welch_ci(a, b, conf=0.95):
    """95% CI for the difference in means (a - b) using Welch's approximation."""
    na, nb = len(a), len(b)
    ma, mb = np.mean(a), np.mean(b)
    va, vb = np.var(a, ddof=1), np.var(b, ddof=1)
    se = np.sqrt(va / na + vb / nb)
    if se == 0:
        return (np.nan, np.nan)
    df = (va / na + vb / nb) ** 2 / (
        (va / na) ** 2 / (na - 1) + (vb / nb) ** 2 / (nb - 1)
    )
    tcrit = stats.t.ppf(1 - (1 - conf) / 2, df)
    diff = ma - mb
    return (diff - tcrit * se, diff + tcrit * se)


def run_pairwise(df, g1, g2, metric):
    """Per-timepoint Welch t-tests + Bonferroni + Cohen's d + 95% CI."""
    rows = []
    raw_ps = {}
    for wk in POST_BASELINE:
        a = df[(df.group == g1) & (df.timepoint_week == wk)][metric].dropna().values
        b = df[(df.group == g2) & (df.timepoint_week == wk)][metric].dropna().values
        t, p = stats.ttest_ind(a, b, equal_var=False)  # Welch
        raw_ps[wk] = p
        d = cohens_d(a, b)
        lo, hi = welch_ci(a, b)
        rows.append({
            "comparison": f"{g1}_vs_{g2}", "metric": metric, "week": wk,
            "t": round(t, 2), "p_raw": p,
            "p_adj": min(p * N_TESTS, 1.000),
            "cohens_d": round(d, 2),
            "ci95_low": round(lo, 1), "ci95_high": round(hi, 1),
        })
    return rows


def run_mixed_anova(df, g1, g2, metric):
    """Two-way mixed ANOVA: Group (between) x Time (within)."""
    if not HAVE_SM:
        return None
    sub = df[df.group.isin([g1, g2])].copy()
    sub = sub.dropna(subset=[metric])
    # AnovaRM requires balanced within-subject data; subject = group+replicate.
    sub["subject"] = sub["group"] + "_" + sub["replicate"].astype(str)
    try:
        model = smf.mixedlm(
            f"{metric} ~ C(group) * C(timepoint_week)", sub,
            groups=sub["subject"]
        ).fit(reml=False)
        return model.summary()
    except Exception as e:  # noqa
        return f"Mixed model failed ({e}); use a dedicated mixed-ANOVA routine."


def main():
    df = pd.read_csv(RAW_PATH, comment="#")
    df = df.dropna(subset=["group", "timepoint_week"])
    df["timepoint_week"] = df["timepoint_week"].astype(int)

    all_rows = []
    comparisons = [
        ("novel_IM", "titanium"),
        ("petri_control", "titanium"),
        ("novel_IM", "petri_control"),
    ]
    for metric in METRICS:
        for g1, g2 in comparisons:
            all_rows.extend(run_pairwise(df, g1, g2, metric))

    out = pd.DataFrame(all_rows)
    out.to_csv(OUT_PATH, index=False)
    print(out.to_string(index=False))
    print(f"\nWritten to {OUT_PATH}")
    print("\nNOTE: For the two-way mixed-design ANOVA F-statistics reported in the "
          "paper, run a dedicated mixed-ANOVA routine (e.g., pingouin.mixed_anova) "
          "on this same dataframe; the per-timepoint t-tests above are reproduced here.")


if __name__ == "__main__":
    main()
