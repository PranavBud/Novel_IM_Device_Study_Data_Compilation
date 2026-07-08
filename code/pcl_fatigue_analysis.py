"""
PCL Fatigue (Cyclic Loading) Analysis
=====================================
Novel Conforming Intramedullary (IM) Device for Critical-Sized Bone Defects

Evaluates whether the device operates within the fatigue infinite-life regime
under normal and worst-case physiological loading, using a stress-life (S-N)
approach. Stress amplitudes are derived from FEA maximum Von Mises stress under
zero-based (R = 0) cyclic loading.

Methods / sources:
  - Endurance limit estimated as 0.4 x ultimate tensile strength (UTS).
    NOTE: this is a conventional engineering approximation used in the absence
    of material-specific PCL fatigue data; it is the least precisely-sourced
    value in the analysis and is stated as an estimate, not a measured value.
  - Basquin finite-life relationship: Sa = Sf' * (2N)^b, with polymeric
    exponent b = -0.1. (Used only to illustrate the finite-life region; the
    device never operates there.)
  - Operating stresses from FEA:
        Normal walking   : max Von Mises 309.745 PSI  -> amplitude 1.0678 MPa
        Worst-case trauma: max Von Mises 1102.985 PSI -> amplitude 3.8024 MPa
    (worst-case load = 8.5x body weight jump landing; Bauer et al., 2001)

Two figures are produced:
  fig6  - traditional S-N curve (finite-life slope + infinite-life floor)
  fig6b - threshold/margin view (recommended; cannot be misread as early failure)

Units: stress amplitude in MPa (PSI shown alongside). 1 MPa = 145.038 PSI.

Author: Pranav Reddy Budipalli
"""

import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Constants and inputs
# ----------------------------------------------------------------------
PSI_PER_MPA = 145.038

UTS = 16.0                       # MPa, PCL ultimate tensile strength
Se  = 0.4 * UTS                  # MPa, estimated endurance limit = 6.4 MPa
b   = -0.1                       # Basquin exponent (generic polymer estimate)
Sf_prime = UTS                   # fatigue strength coefficient

# FEA-derived max Von Mises stresses (PSI) -> zero-based amplitude = max / 2
walk_max_psi   = 309.745
trauma_max_psi = 1102.985
walk_amp_mpa   = (walk_max_psi   / PSI_PER_MPA) / 2     # 1.0678 MPa
trauma_amp_mpa = (trauma_max_psi / PSI_PER_MPA) / 2     # 3.8024 MPa

# ----------------------------------------------------------------------
# Plot style
# ----------------------------------------------------------------------
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"


def boldticks(ax):
    for lab in ax.get_xticklabels() + ax.get_yticklabels():
        lab.set_fontweight("bold")


# ======================================================================
# FIGURE 6 — traditional S-N curve (sloped finite-life + flat infinite-life)
# ======================================================================
stresses = np.linspace(Se, UTS, 200)             # finite-life region only
cycles   = 0.5 * (stresses / Sf_prime) ** (1 / b)
N_at_Se  = 0.5 * (Se / Sf_prime) ** (1 / b)       # "knee" where slope meets floor

fig, ax = plt.subplots(figsize=(12, 7.5))
ax.set_facecolor("#FCFCFB")
ax.axhspan(0.3, Se, alpha=0.10, color="#1D9E75")

# sloped Basquin region + flat endurance-limit floor
ax.loglog(cycles, stresses, color="#378ADD", lw=2.5,
          label="PCL S-N curve — finite-life (Basquin) region")
ax.loglog([N_at_Se, 1e10], [Se, Se], color="#378ADD", lw=2.5)

ax.axhline(Se, color="#A32D2D", lw=1.4, ls="--",
           label=f"Endurance limit = {Se:.3f} MPa ({Se*PSI_PER_MPA:.3f} PSI)")
ax.axvline(1e6, color="#BA7517", lw=1.3, ls=":", label="10^6 cycle benchmark")

xop = 5e2
ax.scatter([xop], [trauma_amp_mpa], s=150, color="#D85A30",
           edgecolor="white", lw=1.2, marker="D", zorder=6)
ax.scatter([xop], [walk_amp_mpa], s=150, color="#1D9E75",
           edgecolor="white", lw=1.2, zorder=6)
ax.text(xop * 1.9, trauma_amp_mpa,
        f"Worst-case trauma — {trauma_amp_mpa:.4f} MPa "
        f"({trauma_amp_mpa*PSI_PER_MPA:.3f} PSI; 8.5x BW)",
        va="center", ha="left", fontsize=10, color="#D85A30", fontweight="bold")
ax.text(xop * 1.9, walk_amp_mpa,
        f"Normal walking — {walk_amp_mpa:.4f} MPa "
        f"({walk_amp_mpa*PSI_PER_MPA:.3f} PSI)",
        va="center", ha="left", fontsize=10, color="#3B6D11", fontweight="bold")

ax.set_xlabel("Cycles to failure (N)")
ax.set_ylabel("Stress amplitude — MPa (PSI in labels)")
ax.set_title("PCL fatigue (S-N) analysis — novel conforming IM device")
ax.set_xlim(1e2, 1e10); ax.set_ylim(0.5, 20)
ax.legend(prop={"weight": "bold", "size": 10}, loc="upper right")
ax.grid(True, alpha=0.22, lw=0.5, which="both")
ax.spines[["top", "right"]].set_visible(False)
boldticks(ax)
plt.tight_layout()
plt.savefig("fig6_fatigue_SN_curve.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

# ======================================================================
# FIGURE 6b — threshold / margin view (RECOMMENDED)
# Shows operating stresses vs the endurance-limit threshold with the
# safe (infinite-life) zone shaded; no cycle axis, no misleading "knee".
# ======================================================================
fig, ax = plt.subplots(figsize=(11, 7))
ax.set_facecolor("#FCFCFB")

ax.axhspan(0, Se, alpha=0.13, color="#1D9E75")        # safe zone
ax.axhspan(Se, 20, alpha=0.07, color="#A32D2D")       # fatigue-risk zone

ax.axhline(Se, color="#A32D2D", lw=2.2, ls="--",
           label=f"Fatigue endurance limit = {Se:.3f} MPa ({Se*PSI_PER_MPA:.3f} PSI)")

ax.axhline(trauma_amp_mpa, color="#D85A30", lw=1.6, alpha=0.55)
ax.axhline(walk_amp_mpa, color="#1D9E75", lw=1.6, alpha=0.55)
ax.scatter([0.5], [trauma_amp_mpa], s=200, color="#D85A30",
           edgecolor="white", lw=1.5, marker="D", zorder=6)
ax.scatter([0.5], [walk_amp_mpa], s=200, color="#1D9E75",
           edgecolor="white", lw=1.5, marker="o", zorder=6)

ax.text(0.62, trauma_amp_mpa,
        f"Worst-case jump-landing trauma\n{trauma_amp_mpa:.4f} MPa "
        f"({trauma_amp_mpa*PSI_PER_MPA:.3f} PSI) — 8.5x BW",
        va="center", ha="left", fontsize=10.5, color="#b8461f", fontweight="bold")
ax.text(0.62, walk_amp_mpa,
        f"Normal walking\n{walk_amp_mpa:.4f} MPa ({walk_amp_mpa*PSI_PER_MPA:.3f} PSI)",
        va="center", ha="left", fontsize=10.5, color="#2e7d32", fontweight="bold")

ax.text(2.7, Se + (20 - Se) * 0.05, "FATIGUE-RISK REGION\n(stress above endurance limit)",
        ha="center", va="center", fontsize=10, color="#A32D2D",
        style="italic", fontweight="bold")
ax.text(2.7, Se / 2, "INFINITE-LIFE REGION (safe)\nstress below endurance limit —\n"
        "no fatigue failure predicted",
        ha="center", va="center", fontsize=10.5, color="#2e7d32",
        style="italic", fontweight="bold")

margin = Se - trauma_amp_mpa
ax.annotate("", xy=(3.7, Se), xytext=(3.7, trauma_amp_mpa),
            arrowprops=dict(arrowstyle="<->", color="#534AB7", lw=1.8))
ax.text(3.78, (Se + trauma_amp_mpa) / 2,
        f"Safety margin\n{margin:.3f} MPa ({margin*PSI_PER_MPA:.1f} PSI)\n"
        f"= {margin/Se*100:.0f}% below limit",
        va="center", ha="left", fontsize=9.5, color="#534AB7", fontweight="bold")

ax.set_xlim(0, 5.2); ax.set_ylim(0, 11); ax.set_xticks([])
ax.set_ylabel("Cyclic stress amplitude — MPa (PSI in labels)")
ax.set_title("Device cyclic operating stress relative to the PCL fatigue endurance limit\n"
             "Both normal and worst-case loading fall within the infinite-life region")
ax.legend(prop={"weight": "bold", "size": 10}, loc="upper right")
ax.grid(True, axis="y", alpha=0.25, lw=0.5)
ax.spines[["top", "right", "bottom"]].set_visible(False)
boldticks(ax)
plt.tight_layout()
plt.savefig("fig6b_fatigue_endurance_margin.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

# ----------------------------------------------------------------------
# Console summary
# ----------------------------------------------------------------------
print("=" * 60)
print("PCL FATIGUE ANALYSIS — KEY VALUES")
print("=" * 60)
print(f"UTS:                 {UTS:.3f} MPa")
print(f"Endurance limit:     {Se:.3f} MPa ({Se*PSI_PER_MPA:.3f} PSI)  [0.4 x UTS estimate]")
print(f"Walking amplitude:   {walk_amp_mpa:.4f} MPa ({walk_amp_mpa*PSI_PER_MPA:.3f} PSI)")
print(f"Trauma amplitude:    {trauma_amp_mpa:.4f} MPa ({trauma_amp_mpa*PSI_PER_MPA:.3f} PSI)")
print(f"Margin below limit:  {margin:.4f} MPa ({margin/Se*100:.1f}% below endurance limit)")
print()
for name, amp in [("Walking", walk_amp_mpa), ("Worst-case trauma", trauma_amp_mpa)]:
    verdict = "INFINITE LIFE (below endurance limit)" if amp < Se else "FINITE LIFE"
    print(f"  {name:<18}: {amp:.4f} MPa -> {verdict}")
