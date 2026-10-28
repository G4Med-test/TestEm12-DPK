#!/usr/bin/env python

# TestEm12-DPK portal parser: metadata() reads the macro, parse() the ROOT
# histogram "8" ("normalized edep profile", d(E/E0)/d(r/r0) vs r/r0) written
# to output.root.
#
# Ported from geant-config-generator/tests/geant4/TestEm12-DPK/parser.py
# (gts.BaseParser + PyROOT) to the module-level metadata()/parse() API
# expected by ci-workflows/validation/export.py, reading ROOT with uproot
# (no PyROOT on the runner), matching the pattern used by LowEFrag.
import os

from geantval import getJSON, one_command, single_run


def metadata(commands):
    single_run(commands)
    energy, unit = one_command(commands, "/gun/energy").split()
    if unit != "keV":
        raise ValueError("Expected a keV beam energy, got: " + unit)
    return {"TEST": "TestEm12-DPK",
            "PHYSLIST": one_command(commands, "/testem/phys/addPhysics"),
            "FLUCT": one_command(commands, "/process/eLoss/fluct"),
            "PARTICLE": one_command(commands, "/gun/particle"),
            "ENERGY": float(energy)}  # keV


def read_dpk_profile(path):
    import uproot

    with uproot.open(path) as root:
        hist = root["8"]
        edges = hist.axis().edges(flow=False).tolist()
        values = hist.values(flow=False).tolist()
        # No asymmetric error option is set on this histogram in HistoManager.cc,
        # so (as with PyROOT's GetBinErrorUp/Low on the same histogram) up == low.
        errors = hist.errors(flow=False).tolist()
    # Only the filled range (the original parser trims leading/trailing zero bins).
    first = next(i for i, v in enumerate(values) if v > 0)
    last = len(values) - 1 - next(i for i, v in enumerate(reversed(values)) if v > 0)
    sel = slice(first, last + 1)
    return (edges[:-1][sel], edges[1:][sel], values[sel], errors[sel])


def parse(job):
    filename = os.path.join(job["path"], "output.root")
    binEdgeLow, binEdgeHigh, binContent, yErrors = read_dpk_profile(filename)
    yStatErrorsPlus = yStatErrorsMinus = yErrors

    physlist = job["PHYSLIST"] if job["FLUCT"] == "true" else job["PHYSLIST"] + "+NoFluct"

    rjson = getJSON(job, "histogram",
                     mctool_name="GEANT4",
                     mctool_model=physlist,
                     observableName="normalized energy profile",
                     targetName="water",
                     beamParticle=job["PARTICLE"],
                     beamEnergies=[job["ENERGY"]],
                     secondaryParticle="None",
                     binContent=binContent,
                     binEdgeLow=[round(x, 2) for x in binEdgeLow],
                     binEdgeHigh=[round(x, 2) for x in binEdgeHigh],
                     yStatErrorsPlus=yStatErrorsPlus,
                     yStatErrorsMinus=yStatErrorsMinus,
                     xAxisName="r/r_{0}",
                     yAxisName="d(E/E_{0})/d(r/r_{0})",
                     title="normalized energy profile")
    yield rjson
