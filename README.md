# TestEm12-DPK

**Low-dose-energy electron Dose Point Kernels (DPK) in liquid water**, validated
against the Berger reference tables (ETRAN and EGSnrc) for mono-energetic
electron point sources. Built on the Geant4 `TestEm12` example, run in
Geant4-DNA track-structure mode.

---

## 🔬 What this test does

A mono-energetic e- point source (1 keV to a few MeV) is placed at the centre
of a liquid-water sphere, divided into thin concentric shells. The radial dose
profile deposited by the source is recorded and compared to the Berger DPK
reference data (`berger/Etran/*-DPK.ascii`, `berger/EGSnrc/*-DPK.ascii` in the
original repository) via `DPK-compare.C`. `dna.mac` configures the Geant4-DNA
physics constructor used for the comparison.

## 📚 Reference

- Source: `geant-validation-tests/src/TestEm12` (Geant4 `TestEm12` example,
  extended with the DPK benchmark by the Geant4-DNA collaboration).
- DPK reference data: Berger M.J., ETRAN and EGSnrc Monte Carlo codes.

## Import notes

- `main.cc`, `include/`, `src/` come from `TestEm12.cc`/`include`/`src` in
  `geant-validation-tests/src/TestEm12`.
- `macro/` contains the macros found directly in that source tree (incl.
  `dna.mac`), kept for reference, plus 4 concrete macros generated from
  `geant-config-generator`'s own `template.conf`/`params.conf` — see
  `validation/README.md`.
- `validation/parser.py` was **rewritten** for the `metadata()`/`parse()`
  module API that `ci-workflows/validation/export.py` actually calls (the
  first version, copied unmodified from
  `geant-config-generator/tests/geant4/TestEm12-DPK/parser.py`, used the old
  `gts.BaseParser` class API and would have failed CI the same way
  `fanoCavity` initially did:
  `AttributeError: module 'validation_parser' has no attribute 'metadata'`).
  See `validation/README.md` for details. The vendored `gts` package is no
  longer needed and was removed.
