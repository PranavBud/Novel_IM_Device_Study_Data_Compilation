# Data Dictionary

This document defines every data file and column in this repository. All units
are stated explicitly. Conversion: 1 MPa = 145.038 PSI; 1 inch = 25.4 mm.

---

## data/cell_culture_summary.csv

Group-level summary statistics for the 28-day in vitro study. Means and standard
deviations are computed across the five replicates (n=5) per group.

| Column | Description | Units |
|---|---|---|
| `group` | Substrate condition: `titanium`, `novel_IM`, or `petri_control` | — |
| `timepoint_week` | Measurement week (0 = seeding/baseline) | weeks |
| `cell_count_mean` | Mean viable cell count | cells |
| `cell_count_sd` | Standard deviation of viable cell count | cells |
| `mineralization_pct_mean` | Mean Von Kossa-positive area | percent |
| `mineralization_pct_sd` | Standard deviation of mineralization | percent |

## data/cell_culture_raw.csv and raw_images for cell_culture+mineralization

Per-replicate measurements (one row per replicate per timepoint). This is the
source from which all summary statistics and inferential tests are derived.

| Column | Description | Units |
|---|---|---|
| `group` | `titanium`, `novel_IM`, or `petri_control` | — |
| `replicate` | Replicate identifier, 1–5 | — |
| `timepoint_week` | Measurement week, 0–4 | weeks |
| `cell_count` | Viable cells (hemocytometer, Trypan Blue exclusion) | cells |
| `mineralization_pct` | % Von Kossa-positive area (ImageJ thresholding) | percent |

## data/fea_results.csv and raw_images for Finite_Element_Analysis

Finite element analysis outputs for the four load cases (fine 1× mesh, full-scale
model, Autodesk Fusion).

| Column | Description | Units |
|---|---|---|
| `load_case` | `axial_compression`, `bending`, `torsion`, `worst_case_trauma` | — |
| `applied_load` | Magnitude of the applied load | see `applied_load_unit` |
| `applied_load_unit` | Unit of the applied load (PSI or Nm) | — |
| `max_von_mises_psi` / `_mpa` | Maximum Von Mises stress | PSI / MPa |
| `safety_factor` | Minimum safety factor for the load case | dimensionless |
| `derived_yield_psi` / `_mpa` | Device yield = max Von Mises × min safety factor | PSI / MPa |
| `max_displacement_in` / `_mm` | Maximum displacement | inches / mm |

The raw images explicity show the PSI values for Maximum Von Mises and inches for the Displacement values.

## data/mesh_convergence.csv

Mesh convergence study: three mesh densities for each of the three static studies.

| Column | Description | Units |
|---|---|---|
| `study` | `axial`, `bending`, or `torsion` | — |
| `mesh_density` | `fine_1x`, `medium`, or `coarse` | — |
| `max_von_mises_psi` | Maximum Von Mises stress | PSI |
| `safety_factor` | Minimum safety factor | dimensionless |
| `max_displacement_in` | Maximum displacement | inches |

## data/statistics_results.csv

Published inferential statistics (the authoritative values reported in the paper).

| Column | Description |
|---|---|
| `comparison` | Pairwise group comparison (e.g., `IM_vs_titanium`) |
| `metric` | `cell_count` or `mineralization` |
| `test` | Test and term (ANOVA effect or per-week Welch t-test) |
| `statistic` | Statistic type and degrees of freedom, e.g., `F(1;9)` or `t` |
| `value` | Statistic value |
| `p_value` | p-value (raw, for t-tests) |
| `cohens_d` | Cohen's d effect size (t-tests only) |
| `notes` | Bonferroni-adjusted p (`p_adj`) and significance notes |

---

## Measurement methods (summary)

- **Cell count:** viable cells quantified by hemocytometer with Trypan Blue
  exclusion at weekly intervals over 28 days.
- **Mineralization:** Von Kossa staining; % positive area quantified by ImageJ
  thresholding.
- **FEA:** static structural analysis in Autodesk Fusion; Von Mises stress,
  safety factor, and displacement extracted per load case.

## Model assumptions and limitations (read before reuse)

- The fatigue **endurance limit is estimated as 0.4 × ultimate tensile strength**,
  a conventional engineering approximation used in the absence of material-specific
  PCL fatigue data. It is the least precisely-sourced value in the analysis.
