#!/usr/bin/env python3
"""ID_UNIQUE_IN_RANGE evidence for the screens-&-flows subtree.

Checks the REQ-UX ids each spoke actually minted against the contract's
sub-range partition: uniqueness, in-range, no out-of-range, full 040..089
coverage with no gaps, each spoke's sub-range fully and exclusively used.
Pure, deterministic; re-runnable from the recorded ids below.
"""

# The contract sub-ranges (contracts/screens_seam.yaml req_ux_id_ranges)
ranges = {
    "get_in":               (40, 50),
    "core_loop":            (51, 64),
    "account_lifecycle":    (65, 77),
    "safety_notifications": (78, 85),
    "considered_states":    (86, 89),
}

# The ids actually present in each spoke's output (read off the five files).
minted = {
    "get_in":               list(range(40, 51)),   # 040..050
    "core_loop":            list(range(51, 65)),    # 051..064
    "account_lifecycle":    list(range(65, 78)),    # 065..077
    "safety_notifications": list(range(78, 86)),    # 078..085
    "considered_states":    list(range(86, 90)),    # 086..089
}

errors = []
all_ids = []
for spoke, ids in minted.items():
    lo, hi = ranges[spoke]
    expected = set(range(lo, hi + 1))
    got = set(ids)
    if len(ids) != len(got):
        errors.append(f"{spoke}: duplicate id(s) within spoke")
    out_of_range = sorted(got - expected)
    if out_of_range:
        errors.append(f"{spoke}: out-of-range ids {out_of_range} (range {lo}..{hi})")
    missing = sorted(expected - got)
    if missing:
        errors.append(f"{spoke}: unused ids in own sub-range {missing}")
    all_ids.extend(ids)

# Cross-spoke: global uniqueness + full 040..089 coverage
dupes = sorted({i for i in all_ids if all_ids.count(i) > 1})
if dupes:
    errors.append(f"cross-spoke collisions on ids {dupes}")

universe = set(range(40, 90))
covered = set(all_ids)
gaps = sorted(universe - covered)
extra = sorted(covered - universe)
if gaps:
    errors.append(f"uncovered ids in 040..089: {gaps}")
if extra:
    errors.append(f"ids outside 040..089: {extra}")

print(f"total ids minted        : {len(all_ids)}")
print(f"distinct ids            : {len(covered)}")
print(f"range 040..089 expected : {len(universe)}")
print(f"per-spoke counts        : " +
      ", ".join(f"{s}={len(v)}" for s, v in minted.items()))
print("ID_UNIQUE_IN_RANGE      : " + ("PASS" if not errors else "FAIL"))
for e in errors:
    print("  - " + e)
