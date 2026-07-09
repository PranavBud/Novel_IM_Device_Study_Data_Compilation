# A Bioresorbable Conforming Intramedullary Device for Critical-Sized Bone Defects

Data, analysis code, and computational models supporting the study of a novel
bioresorbable polycaprolactone (PCL) conforming intramedullary (IM) device for the
treatment of critical-sized bone defects (CSD).

This repository is intended to make every number, figure, and statistic in the
accompanying paper fully reproducible from the underlying data.

Zenodo Repository DOI: 10.5281/zenodo.21267466

---

## What's here

```
.
├── data/                 Raw and summary data
│   ├── cell_culture_summary.csv         Group means ± SD (n=5), 28-day study
│   ├── cell_culture_raw_template.csv    Per-replicate template (fill with real data)
│   ├── fea_results.csv                  FEA outputs for all four load cases
│   ├── mesh_convergence.csv             Mesh convergence study (3 densities × 3 studies)
│   └── statistics_results.csv           Published ANOVA / t-test / Cohen's d / CI values
├── code/                 Analysis and modeling scripts
│   ├── reproduce_statistics.py          Regenerates the inferential statistics
│   ├── pcl_degradation_model.py         First-order Pitt degradation model (Figure)
│   └── pcl_fatigue_analysis.py          Stress-life fatigue analysis (Figures)
├── figures/              Final 300-DPI figure PNGs
├── cad/                  Device geometry (export STL/STEP from Autodesk Fusion here) at the different mesh quantities tested, and the defected bone the device prototype was designed around
├── raw_images/           Raw Microscopy Images and Finite Element Analysis Results
├── DATA_DICTIONARY.md    Every file and column, with units and methods
├── requirements.txt      Python dependencies
├── CITATION.cff          How to cite this repository
├── .zenodo.json          Metadata that auto-populates the Zenodo deposit
└── LICENSE               MIT (code) + CC BY 4.0 (data, figures, cad, raw images)

Note that the raw images for microscopy are limited to only one replicate of the study (n=1).
```

## Reproducing the results

Requires Python 3.10+ (only `numpy` and `matplotlib` are needed for the model
figures; the statistics script additionally uses `pandas`, `scipy`, `statsmodels`).

```bash
pip install -r requirements.txt

# Regenerate the degradation figure
python code/pcl_degradation_model.py

# Regenerate the fatigue figures
python code/pcl_fatigue_analysis.py

# Regenerate the inferential statistics (after populating data/cell_culture_raw.csv)
python code/reproduce_statistics.py
```

The model scripts read no external files — the FEA-derived inputs (e.g., maximum
Von Mises stresses) are defined at the top of each script and documented with their
sources. They are not computed by these scripts; they originate from Autodesk Fusion.

To reproduce the cell-culture statistics, first copy
`data/cell_culture_raw_template.csv` to `data/cell_culture_raw.csv` and populate it
with the per-replicate measurements (5 replicates per group, weeks 0–4). Running
`reproduce_statistics.py` then writes `data/statistics_results_reproduced.csv`, which
should match the published values in `data/statistics_results.csv`.

## Key results (at a glance)

- **Mechanics (FEA, fine mesh):** safety factors of 7.0 (axial), 8.0 (bending), and
  7.5 (torsion) under physiological loading; a positive margin (SF ≈ 2.0) under a
  worst-case 8.5× body-weight jump-landing load. Metrics vary only 2.1–3.8% across
  three mesh densities (converged).
- **Biology (in vitro, n=5, 28 days):** the novel IM matched the gold-standard petri
  dish control on both proliferation and mineralization (no significant differences;
  |d| ≤ 0.52), and substantially outperformed a titanium plate (2.64-fold more cells
  and a 25.43-percentage-point mineralization advantage by Week 4; all comparisons
  significant after Bonferroni correction).
- **Degradation/fatigue (modeled):** retained tensile strength through the healing
  window; both normal and worst-case cyclic stresses fall below the estimated
  fatigue endurance limit.

## Assumptions and limitations

Stated in full in `DATA_DICTIONARY.md`. In brief: the fatigue endurance limit is a
0.4 × UTS estimate (not measured PCL data); physiological loads are expressed as an
equivalent pressure over a reference area rather than true in-situ bone stress; and
FEA assumes linear-elastic behavior without in vivo degradation effects. These are
disclosed deliberately so the models can be reused and improved.

## How to archive on Zenodo (mint a DOI)

1. Push this repository to GitHub (public).
2. Go to https://zenodo.org, log in, and open **Settings → GitHub**.
3. Flip the toggle **on** for this repository.
4. On GitHub, create a release (e.g., tag `v1.0.0`). Zenodo automatically captures
   that release, reads `.zenodo.json`, and mints a DOI.
5. Add the DOI badge Zenodo gives you to the top of this README, and fill the `doi:`,
   `version:`, and `date-released:` fields in `CITATION.cff`.

## Citing

See `CITATION.cff`. After the first release, cite using the Zenodo DOI.

## License

Code in `code/` is released under the MIT License. Data in `data/`, figures in
`figures/`, images in `raw_images/`, and CAD files in `cad/` are released under CC BY 4.0. See `LICENSE`.
