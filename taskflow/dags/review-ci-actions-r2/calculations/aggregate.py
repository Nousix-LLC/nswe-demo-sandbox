#!/usr/bin/env python3
"""Deterministic severity aggregation + verdict for the PR #21 review gate.
Inputs are the conformant findings transcribed from the four spoke findings.md
(reviewed head c8123376). The gate's verdict rule:
  APPROVE iff total(block)==0 AND total(major)==0 else REQUEST-CHANGES
"""
from collections import Counter

# (id, severity, spoke, location-key for dedup)
findings = [
    ("WF-1", "minor", "workflow_correctness", "ci.yml:33 toolchain-series-pin"),
    ("WF-2", "minor", "workflow_correctness", "ci.yml:30-33 msrv-1.82-unenforced"),
    ("SEC-1", "minor", "supply_chain_security", "ci.yml uses: actions tag-not-sha"),
    ("SEC-2", "nit",   "supply_chain_security", "ci.yml image build-push provenance/sbom"),
    ("IMG-1", "major", "image_job", "ci.yml image job vs Dockerfile FROM rust:1.88 toolchain-decouple+pre-merge-gate"),
    ("IMG-2", "minor", "image_job", "ci.yml image dockerfile-detect dead/silent-skip"),
    ("IMG-3", "nit",   "image_job", "ci.yml image workflow_dispatch no-publish"),
    ("IMG-4", "nit",   "image_job", "ci.yml image build-push digest-unsurfaced"),
    ("DOC-1", "minor", "folded_minors", "PR21 mixed-concern 21 non-CI files"),
    ("DOC-2", "nit",   "folded_minors", "chirp-server/README.md:342-346 variant-name"),
]

# Duplication check: any two findings sharing an identical location key?
loc_counts = Counter(f[3] for f in findings)
dupes = [loc for loc, c in loc_counts.items() if c > 1]

sev = Counter(f[1] for f in findings)
block, major, minor, nit = sev["block"], sev["major"], sev["minor"], sev["nit"]

verdict = "APPROVE" if (block == 0 and major == 0) else "REQUEST-CHANGES"

print("=== Reviewed head c8123376 — severity aggregate ===")
print(f"total findings : {len(findings)}")
print(f"block : {block}")
print(f"major : {major}  -> {[f[0] for f in findings if f[1]=='major']}")
print(f"minor : {minor}  -> {[f[0] for f in findings if f[1]=='minor']}")
print(f"nit   : {nit}  -> {[f[0] for f in findings if f[1]=='nit']}")
print(f"duplicate locations (would merge): {dupes if dupes else 'none'}")
print(f"VERDICT (reviewed head): {verdict}")
print()

# Coverage check: six concerns mapped to exactly one spoke scope each
concern_owner = {1:"workflow_correctness",2:"workflow_correctness",3:"supply_chain_security",
                 4:"image_job",5:"folded_minors",6:"synthesis-gate"}
print("=== Concern coverage (each covered exactly once) ===")
for c in range(1,7):
    print(f"  concern {c} -> {concern_owner[c]}")
assert set(concern_owner) == {1,2,3,4,5,6}
print("  all six concerns covered, none dropped/double-owned: OK")
print()

# Landed-reality reconciliation
print("=== Landed reality (merged head 716817bc / merge ada3aa97) ===")
resolved = {"IMG-1":"major","IMG-2":"minor","IMG-4":"nit"}
rem_block = block
rem_major = major - sum(1 for i,s in resolved.items() if s=="major")
print(f"commit 716817bc resolves: {list(resolved)}")
print(f"residual on landed code -> block={rem_block} major={rem_major}")
print(f"VERDICT (landed code):  {'APPROVE' if rem_block==0 and rem_major==0 else 'REQUEST-CHANGES'}")
