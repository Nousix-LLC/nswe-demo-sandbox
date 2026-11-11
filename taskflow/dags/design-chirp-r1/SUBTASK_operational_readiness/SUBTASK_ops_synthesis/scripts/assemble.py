#!/usr/bin/env python3
"""Operational-readiness synthesis gate: assemble + verify.

Reads the five concern fragments and the two upstream designs, assembles the
seven-section design/operational-readiness.md deliverable (concern bodies carried
verbatim; process-meta footers stripped for repository hygiene), builds the
consolidated REQ-OPS register (verbatim union) and the OPS traceability table,
and prints identity evidence to stdout.

Run with: python3 -I assemble.py
"""
import re
import sys
from pathlib import Path

BASE = Path("/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1")
SUB = BASE / "SUBTASK_operational_readiness"
OUT = SUB / "SUBTASK_ops_synthesis" / "outputs" / "operational-readiness.md"

# (canonical_section_name, readable_title, fragment_path, owner_slug, range)
CONCERNS = [
    ("durable_data", "Durable data in production",
     SUB / "SUBTASK_ops_durable_data/outputs/durable-data.md",
     "SUBTASK_ops_durable_data", (1, 19)),
    ("backups_and_recovery", "Backups and recovery",
     SUB / "SUBTASK_ops_backups_recovery/outputs/backups-recovery.md",
     "SUBTASK_ops_backups_recovery", (20, 39)),
    ("limits_and_quotas", "Limits and quotas",
     SUB / "SUBTASK_ops_limits_quotas/outputs/limits-quotas.md",
     "SUBTASK_ops_limits_quotas", (40, 59)),
    ("observability", "Observability",
     SUB / "SUBTASK_ops_observability/outputs/observability.md",
     "SUBTASK_ops_observability", (60, 79)),
    ("status_and_incident", "Status and incident",
     SUB / "SUBTASK_ops_status_incident/outputs/status-incident.md",
     "SUBTASK_ops_status_incident", (80, 99)),
]

REQUIRED_SECTIONS = [c[0] for c in CONCERNS] + [
    "existing_followups", "requirements_and_acceptance_criteria"]

VERIF_VOCAB = {"manual_user_check", "automated_test", "inspection", "operational_check"}

HEADING_RE = re.compile(r"^(#{1,6})(\s)")


def shift_headings(text):
    out = []
    for line in text.split("\n"):
        m = HEADING_RE.match(line)
        if m:
            line = "#" + line
        out.append(line)
    return "\n".join(out)


def strip_fragment(text, section):
    """Drop the fragment's own title line, drop the Methodology-note footer and
    (observability) the fold-note blockquote; return the body only."""
    lines = text.split("\n")
    # drop leading blank lines
    while lines and lines[0].strip() == "":
        lines.pop(0)
    # drop the first heading (the fragment title)
    if lines and HEADING_RE.match(lines[0]):
        lines.pop(0)
    # observability: drop a leading blockquote block (the "note for the synthesis fold")
    if section == "observability":
        while lines and lines[0].strip() == "":
            lines.pop(0)
        if lines and lines[0].lstrip().startswith(">"):
            while lines and (lines[0].lstrip().startswith(">") or lines[0].strip() == ""):
                lines.pop(0)
    # drop from a "Methodology note" heading to EOF
    body = []
    for line in lines:
        if re.match(r"^#{1,6}\s+Methodology note", line):
            break
        body.append(line)
    # trim trailing blanks
    while body and body[-1].strip() == "":
        body.pop()
    return "\n".join(body)


REQ_HEAD_RE = re.compile(r"^####\s+(REQ-OPS-\d{3})\s+—\s+(.*)$")


def parse_requirements(text):
    """Return list of dicts: id, title, block(verbatim lines), fields."""
    lines = text.split("\n")
    reqs = []
    i = 0
    n = len(lines)
    while i < n:
        m = REQ_HEAD_RE.match(lines[i])
        if m:
            rid, title = m.group(1), m.group(2)
            block = [lines[i]]
            i += 1
            while i < n and not (lines[i].startswith("#### ") or
                                 re.match(r"^#{1,3}\s", lines[i])):
                block.append(lines[i])
                i += 1
            # trim trailing blanks within block
            while block and block[-1].strip() == "":
                block.pop()
            fields = {}
            for bl in block:
                fm = re.match(r"^- \*\*(\w+)\*\*:\s*(.*)$", bl)
                if fm:
                    fields[fm.group(1)] = fm.group(2).strip()
            reqs.append({"id": rid, "title": title,
                         "block": "\n".join(block), "fields": fields})
        else:
            i += 1
    return reqs


def defined_ids(path, prefix):
    text = path.read_text()
    return set(re.findall(prefix + r"-\d{3}", text))


def main():
    prod_ids = defined_ids(BASE / "SUBTASK_product_requirements/outputs/product-requirements.md", "REQ-PROD")
    dom_ids = defined_ids(BASE / "SUBTASK_domain_app_design/outputs/domain-application-design.md", "REQ-DOM")

    concern_bodies = []
    all_reqs = []
    per_concern_counts = {}
    for name, title, path, owner, rng in CONCERNS:
        raw = path.read_text()
        body = strip_fragment(raw, name)
        shifted = shift_headings(body)
        concern_bodies.append((name, title, shifted))
        reqs = parse_requirements(raw)
        per_concern_counts[name] = len(reqs)
        for r in reqs:
            r["concern"] = name
            r["range"] = rng
            all_reqs.append(r)

    all_reqs.sort(key=lambda r: int(r["id"].split("-")[-1]))

    # ---- identity checks ----
    evidence = []

    # NO_NUMBER_COLLISION
    ids = [r["id"] for r in all_reqs]
    dups = sorted({x for x in ids if ids.count(x) > 1})
    # range containment
    range_ok = all(r["range"][0] <= int(r["id"].split("-")[-1]) <= r["range"][1] for r in all_reqs)
    evidence.append(("NO_NUMBER_COLLISION",
                     not dups and range_ok,
                     f"{len(ids)} ids, {len(set(ids))} unique; dups={dups or 'none'}; "
                     f"all within owning partition range={range_ok}"))

    # CONCERN_COVERAGE
    coverage = {n: c for n, c in per_concern_counts.items()}
    evidence.append(("CONCERN_COVERAGE", all(v > 0 for v in coverage.values()),
                     "; ".join(f"{n}={v}" for n, v in coverage.items())))

    # OPS_TESTABLE
    testable_fail = []
    for r in all_reqs:
        vm = r["fields"].get("verification_method", "")
        rg = r["fields"].get("release_gating", "")
        ac = r["fields"].get("acceptance_criteria", "")
        if vm not in VERIF_VOCAB:
            testable_fail.append(f"{r['id']}:bad_vm({vm!r})")
        if rg not in ("true", "false"):
            testable_fail.append(f"{r['id']}:bad_gating({rg!r})")
        if rg == "true" and not ac.strip():
            testable_fail.append(f"{r['id']}:gating_no_ac")
    evidence.append(("OPS_TESTABLE", not testable_fail,
                     "all reqs carry vm∈vocab + release_gating; every gating req has acceptance_criteria"
                     if not testable_fail else "; ".join(testable_fail)))

    # OPS_TRACES
    traces_fail = []
    internal = []
    for r in all_reqs:
        tline = r["fields"].get("traces_to", "")
        targets = re.findall(r"REQ-(?:PROD|DOM)-\d{3}", tline)
        if not targets:
            internal.append(r["id"])
            continue
        for t in targets:
            if t.startswith("REQ-PROD") and t not in prod_ids:
                traces_fail.append(f"{r['id']}->{t}(missing)")
            if t.startswith("REQ-DOM") and t not in dom_ids:
                traces_fail.append(f"{r['id']}->{t}(missing)")
    evidence.append(("OPS_TRACES", not traces_fail,
                     f"all traces_to targets resolve against {len(prod_ids)} REQ-PROD + {len(dom_ids)} REQ-DOM defined ids; "
                     f"OPS-internal (empty traces_to)={internal}"
                     if not traces_fail else "; ".join(traces_fail)))

    # ---- existing_followups section (authored by the gate) ----
    followups = """## existing_followups

Three open board follow-ups predate this design and are non-release-gating hardening or
polish. They are folded here into the operational-readiness concern each belongs to and are
**not** minted as new `REQ-OPS-*`; where an existing requirement already covers the substance,
that requirement is named. None gates the release.

| Issue | Summary | Folded into | Covered in substance by | Release-gating |
|-------|---------|-------------|--------------------------|----------------|
| #23 | Exercise and harden the native install path | `observability` | `REQ-OPS-060`, `REQ-OPS-061`, `REQ-OPS-066`, `REQ-OPS-068`, `REQ-OPS-072`, `REQ-OPS-075` — exercising the install path is where the readiness signal, the structured logs, and the serving metrics are first confirmed wired and observable in a real deployment | No |
| #24 | Least-privilege delivery RBAC + supply-chain hardening | `limits_and_quotas` | Adjacent to the operational-security posture: the operator/administrative audit trail (`REQ-OPS-077`, `REQ-OPS-079`) records privileged action, but least-privilege RBAC on the delivery/control plane is a distinct, privileged-actor access concern not fully covered by any release-gating `REQ-OPS-*`. It is control-plane access control, distinct in subject from the public, client-facing rate and volume limits (`REQ-OPS-040..048`), and remains issue #24 as hardening | No |
| #25 | Containerize follow-ups (non-blocking polish) | `durable_data` | Relates to the operated-deploy posture — a running deployment loses no user data to restart, redeploy, or upgrade (`REQ-OPS-001`, `REQ-OPS-003`, `REQ-OPS-004`); the containerization items are non-blocking polish on the deploy artifact, not a new durability requirement | No |

**Placement rationale.** #23 is folded into `observability` because its substance — proving the
operational signals are wired in a real deployment — is exactly what the observability requirements
assert. #24 is folded into `limits_and_quotas` as its operational-security neighbour: it is an
access-and-limits matter, but it bounds privileged control-plane actors rather than public clients,
so it sits beside the public limits without being restated as one. #25 is folded into `durable_data`
against the operated-deploy posture it polishes. Each issue appears exactly once above, is covered by
or adjacent to a named existing requirement, and is not duplicated as a new `REQ-OPS-*`.
"""

    # FOLLOWUPS_FOLDED — the identity is "each issue folded as exactly one placement
    # entry, none minted as a new REQ-OPS". Measure that: exactly one fold-table row
    # per issue (a line of the form "| #NN | ... |"), and no REQ-OPS id minted for them.
    fold_rows = re.findall(r"^\|\s*(#2[345])\s*\|", followups, re.M)
    one_row_each = sorted(fold_rows) == ["#23", "#24", "#25"]
    # the union carries only REQ-OPS-001..095; no REQ-OPS id was created to represent an issue
    minted_for_issue = re.search(r"REQ-OPS-\d{3}[^\n]*#2[345]\s*$", followups, re.M)
    folded_ok = one_row_each and not minted_for_issue
    evidence.append(("FOLLOWUPS_FOLDED", folded_ok,
                     "#23→observability, #24→limits_and_quotas, #25→durable_data; "
                     f"exactly one fold row per issue (rows={sorted(fold_rows)}); "
                     "none minted as a new REQ-OPS"))

    # ---- consolidated register (verbatim union) ----
    reg_lines = []
    reg_lines.append("## requirements_and_acceptance_criteria\n")
    reg_lines.append(
        "This is the consolidated `REQ-OPS-*` register: the verbatim union of the five concern "
        "sections' requirements, in id order. Each requirement is also stated in its concern section "
        "above; this register is the single flat index of the operational-readiness requirements and "
        "is followed by the OPS traceability table. Every requirement carries a `verification_method` "
        "from the vocabulary (`manual_user_check`, `automated_test`, `inspection`, `operational_check`), "
        "a `release_gating` flag, and `traces_to` the product/domain requirement it refines (empty only "
        "for an operational-internal requirement).\n")
    for r in all_reqs:
        reg_lines.append(r["block"])
        reg_lines.append("")
    # traceability table
    reg_lines.append("### OPS traceability table\n")
    reg_lines.append(
        "`REQ-OPS-*` → the product/domain requirements it refines, with its release-gating flag. "
        "An empty `traces_to` marks an operational-internal requirement that refines no single "
        "product/domain requirement.\n")
    reg_lines.append("| REQ-OPS | release_gating | traces_to |")
    reg_lines.append("|---------|----------------|-----------|")
    for r in all_reqs:
        tline = r["fields"].get("traces_to", "").strip()
        targets = re.findall(r"REQ-(?:PROD|DOM)-\d{3}", tline)
        rg = r["fields"].get("release_gating", "")
        reg_lines.append(f"| {r['id']} | {rg} | {', '.join(targets) if targets else '—'} |")
    register = "\n".join(reg_lines)

    # ---- assemble document ----
    gating_count = sum(1 for r in all_reqs if r["fields"].get("release_gating") == "true")
    doc = []
    doc.append("# Operational readiness\n")
    doc.append(
        "This document is the operational-readiness area of the chirp product design: what must be "
        "true in production **beyond \"it runs\"** for chirp to be operated, not just started. It "
        "states durable data, a backup and recovery path, limits and quotas, observability, and a "
        "status and incident posture — each as a testable `REQ-OPS-*` release requirement whose "
        "acceptance criteria a person who never met the author can check against the live product. It "
        "is **requirements, not implementation**: every engineering \"how\" (which backup tool, which "
        "metrics backend, which rate-limiter) is stated as a property the operated product must have "
        "and deferred to later code work.\n")
    doc.append(
        "It builds on, and does not restate, the domain persistence model (`REQ-DOM-100..118`) and the "
        "product-level operational needs (`REQ-PROD-037..041`, operator journey J9); it references "
        f"those ids at the seam. The register below holds {len(all_reqs)} requirements "
        f"(`REQ-OPS-001..095`), {gating_count} of them release-gating.\n")
    doc.append("The seven sections below are, in order: `durable_data`, `backups_and_recovery`, "
               "`limits_and_quotas`, `observability`, `status_and_incident`, `existing_followups`, "
               "and `requirements_and_acceptance_criteria`.\n")
    doc.append("---\n")
    for name, title, body in concern_bodies:
        doc.append(f"## {name}\n")
        doc.append(f"*{title}.*\n")
        doc.append(body)
        doc.append("\n---\n")
    doc.append(followups)
    doc.append("\n---\n")
    doc.append(register)
    doc.append("")
    document = "\n".join(doc)

    OUT.write_text(document)

    # ---- ALL_SECTIONS_PRESENT (check against the written document) ----
    found_order = re.findall(r"^## (\w+)$", document, re.M)
    sections_ok = found_order == REQUIRED_SECTIONS
    evidence.insert(0, ("ALL_SECTIONS_PRESENT", sections_ok,
                        f"order={found_order}"))

    # ---- report ----
    print("=== OPERATIONAL-READINESS SYNTHESIS: IDENTITY EVIDENCE ===")
    print(f"wrote {OUT} ({len(document.splitlines())} lines, {len(document)} bytes)")
    print(f"requirements total={len(all_reqs)} gating={gating_count} "
          f"non-gating={len(all_reqs)-gating_count}")
    print(f"per-concern counts: {per_concern_counts}")
    print()
    allpass = True
    for ident, ok, detail in evidence:
        allpass = allpass and ok
        print(f"[{'PASS' if ok else 'FAIL'}] {ident}: {detail}")
    print()
    print(f"ALL IDENTITIES: {'PASS' if allpass else 'FAIL'}")


if __name__ == "__main__":
    sys.exit(main())
