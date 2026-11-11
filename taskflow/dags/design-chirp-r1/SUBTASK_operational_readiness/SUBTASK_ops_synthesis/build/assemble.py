#!/usr/bin/env python3
"""Deterministically assemble design/operational-readiness.md from the five concern
fragments plus the two authored cross-cutting sections. Carries fragment content
verbatim (requirements never rewritten); strips only the environment/scaffolding
trailers that are taskflow/process artifacts, not repository design content; and
generates the consolidated register + traceability table from the fragments."""
import re, sys

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_operational_readiness"
BUILD = BASE + "/SUBTASK_ops_synthesis/build"
OUT = BASE + "/SUBTASK_ops_synthesis/outputs/operational-readiness.md"

# (section_key, readable title, fragment path) in design_artifact_map order
FRAGS = [
    ("durable_data", "durable_data — Durable data in production",
     BASE + "/SUBTASK_ops_durable_data/outputs/durable-data.md"),
    ("backups_and_recovery", "backups_and_recovery — Backups and recovery",
     BASE + "/SUBTASK_ops_backups_recovery/outputs/backups-recovery.md"),
    ("limits_and_quotas", "limits_and_quotas — Limits and quotas",
     BASE + "/SUBTASK_ops_limits_quotas/outputs/limits-quotas.md"),
    ("observability", "observability — Observability",
     BASE + "/SUBTASK_ops_observability/outputs/observability.md"),
    ("status_and_incident", "status_and_incident — Status and incident",
     BASE + "/SUBTASK_ops_status_incident/outputs/status-incident.md"),
]

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def strip_methodology_note(text):
    # Remove the "## Methodology note (environment)" trailer to EOF (taskflow/engine detail).
    return re.split(r'\n#+ Methodology note \(environment\)', text, maxsplit=1)[0].rstrip()

def strip_fold_note_blockquote(text):
    # Remove the observability "> Note for the synthesis fold (issue #23): ..." blockquote
    # (contiguous '>' lines) plus one adjacent blank line. Process scaffolding, not repo content.
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        if lines[i].startswith("> ") and "Note for the synthesis fold" in lines[i]:
            while i < len(lines) and lines[i].startswith(">"):
                i += 1
            # swallow one trailing blank line; keep the single leading blank already
            # emitted so exactly one blank line separates the prior paragraph from the
            # following heading.
            if i < len(lines) and lines[i].strip() == "":
                i += 1
            continue
        out.append(lines[i]); i += 1
    return "\n".join(out)

def drop_title_line(text):
    # Remove the fragment's own leading H1/H2 title line (first heading encountered).
    lines = text.split("\n")
    for idx, ln in enumerate(lines):
        if re.match(r'^#{1,2} \S', ln):
            del lines[idx]
            # also drop an immediately-following blank line
            if idx < len(lines) and lines[idx].strip() == "":
                del lines[idx]
            break
    return "\n".join(lines).lstrip("\n")

def relevel_narrative(text):
    # Narrative headings (# / ## / ###) -> ### ; requirement headings (#### REQ-OPS) stay ####.
    out = []
    for ln in text.split("\n"):
        m = re.match(r'^(#{1,3}) (?!#)', ln)
        if m and not ln.startswith("####"):
            ln = "### " + ln[m.end():]
        out.append(ln)
    return "\n".join(out)

REQ_HEAD = re.compile(r'^#### (REQ-OPS-\d{3}) ')

def extract_req_blocks(text):
    """Return list of (id, block_text, release_gating, traces_list) for each #### REQ-OPS block,
    verbatim (heading + following lines up to the next #### or ### heading or EOF)."""
    lines = text.split("\n")
    blocks, i = [], 0
    while i < len(lines):
        m = REQ_HEAD.match(lines[i])
        if not m:
            i += 1; continue
        rid = m.group(1)
        blk = [lines[i]]; i += 1
        while i < len(lines) and not lines[i].startswith("#### ") and not re.match(r'^#{1,3} (?!#)', lines[i]):
            blk.append(lines[i]); i += 1
        btext = "\n".join(blk).rstrip()
        gating = "true" if re.search(r'\*\*release_gating\*\*:\s*true', btext) else "false"
        tm = re.search(r'\*\*traces_to\*\*:\s*(.*)', btext)
        traces = []
        if tm:
            traces = re.findall(r'REQ-(?:PROD|DOM)-\d{3}', tm.group(1))
        blocks.append((rid, btext, gating, traces))
    return blocks

# ---- assemble ----
parts = [read(BUILD + "/preamble.md").rstrip(), ""]

all_blocks = []
for key, title, path in FRAGS:
    raw = read(path)
    body = strip_methodology_note(raw)
    if key == "observability":
        body = strip_fold_note_blockquote(body)
    # collect verbatim requirement blocks BEFORE re-leveling (keeps #### intact)
    all_blocks.extend(extract_req_blocks(body))
    body = drop_title_line(body)
    body = relevel_narrative(body)
    parts.append("## " + title)
    parts.append("")
    parts.append(body.strip())
    parts.append("")

# existing_followups (authored)
parts.append(read(BUILD + "/existing_followups.md").strip())
parts.append("")

# requirements_and_acceptance_criteria (authored intro + verbatim union + traceability table)
parts.append(read(BUILD + "/register_intro.md").strip())
parts.append("")

# sanity: ids must be globally sorted and unique
ids = [b[0] for b in all_blocks]
assert ids == sorted(ids), "register not in id order"
assert len(ids) == len(set(ids)), "duplicate REQ-OPS id in union"

for rid, btext, gating, traces in all_blocks:
    parts.append(btext)
    parts.append("")

# traceability table
parts.append("### OPS traceability table")
parts.append("")
parts.append("Every `REQ-OPS-*`, its release-gating flag, and the product/domain requirement(s) it refines. "
             "A requirement with no trace is operational-internal (it refines no single `REQ-PROD-*`/`REQ-DOM-*`).")
parts.append("")
parts.append("| REQ-OPS | release_gating | traces_to |")
parts.append("|---------|----------------|-----------|")
for rid, btext, gating, traces in all_blocks:
    tcell = ", ".join(traces) if traces else "—"
    parts.append(f"| {rid} | {gating} | {tcell} |")
parts.append("")

doc = "\n".join(parts).rstrip() + "\n"
with open(OUT, "w", encoding="utf-8") as f:
    f.write(doc)

print(f"wrote {OUT}")
print(f"requirements in union: {len(all_blocks)}")
print(f"id range: {ids[0]}..{ids[-1]}  unique={len(set(ids))}")
print(f"release_gating true={sum(1 for b in all_blocks if b[2]=='true')} "
      f"false={sum(1 for b in all_blocks if b[2]=='false')}")
print(f"with-trace={sum(1 for b in all_blocks if b[3])} "
      f"internal(no-trace)={sum(1 for b in all_blocks if not b[3])}")
