# CAD / Device Geometry

Place the device geometry here so the finite element analysis is reproducible by
others. Export from Autodesk Fusion in software-neutral formats:

- **`device.step`** (STEP / ISO 10303) — preferred; preserves exact parametric geometry.
- **`device.stl`** — mesh export, useful for 3D-printing replication.

Recommended to also include:
- A short `geometry_notes.md` describing key dimensions (e.g., axial length, bending
  span, torsion length, wall thickness) and the surface-thickening procedure used to
  conform the device to the defect bone morphology.
- The source bone scan reference (MRI/CT dataset identifier) if shareable.

These files are not included by default because they are exported from the original
Fusion project; add them before publishing the archive.
