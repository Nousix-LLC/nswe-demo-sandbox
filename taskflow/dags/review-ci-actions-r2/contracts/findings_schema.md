# Findings Schema (contract kind: taxonomy) — READ-ONLY

This is the frozen seam for the review DAG. Every spoke MUST emit its findings in this record shape
with this severity vocabulary, so the synthesis gate can mechanically aggregate counts and apply the
verdict rule. Do not redefine or extend this schema in a spoke; if it is inadequate, request a plan
amendment (additive only).

## Severity taxonomy (closed enum)

| Severity | Meaning | Gate effect |
|----------|---------|-------------|
| `block`  | Defect that must be fixed before this PR can land (breaks a stated acceptance criterion, breaks the workflow, or introduces a correctness/security defect that would fire on `main`). | Forces `REQUEST-CHANGES`. |
| `major`  | Significant problem that should be fixed before landing (unsound mechanics, real drift/misfire risk, materially wrong behavior) but is not a hard breakage. | Forces `REQUEST-CHANGES`. |
| `minor`  | Worth fixing; does not block landing (quality, clarity, non-critical robustness). | Advisory; does not change the verdict. |
| `nit`    | Cosmetic / stylistic / optional. | Advisory; does not change the verdict. |

## Verdict rule (asserted by the synthesis gate)

```
APPROVE            iff  total(block) == 0  AND  total(major) == 0
REQUEST-CHANGES    otherwise   (list the specific required changes = every block + major required_change)
```

## Per-finding record (required fields)

Each finding is one entry with these fields:

| Field | Required | Content |
|-------|----------|---------|
| `id` | yes | `<PREFIX>-<n>`, prefix per the spoke's ownership row (`WF-`, `SEC-`, `IMG-`, `DOC-`). Unique within the spoke. |
| `severity` | yes | One of `block` / `major` / `minor` / `nit`. |
| `concern` | yes | Which brief concern(s) this finding addresses (1–6). |
| `location` | yes | `path:line` where possible; otherwise `path` + the `ci.yml` job/step or diff hunk the finding is about. Use the PR-head path. |
| `finding` | yes | What is wrong or notable, stated factually. |
| `rationale` | yes | Why it matters / the evidence supporting the severity. |
| `required_change` | required iff `severity` ∈ {`block`,`major`} | The specific change that would clear the finding. Omit for `minor`/`nit` (a suggestion MAY still be given). |

## Findings-file shape (what each spoke writes)

Each spoke writes `findings.md` in its own workspace with:

1. A header line stating the spoke, the concern(s) covered, and **the PR head reviewed (`c8123376`)**.
2. A **findings table or list** of the records above (may be empty if the spoke finds nothing — state "no findings" explicitly).
3. A short **concern-coverage note**: for each concern the spoke owns, one line on what was examined and the local conclusion (clean / has findings).
4. A one-line **spoke roll-up**: counts of block / major / minor / nit this spoke raised.

A spoke that finds nothing blocking still emits a conformant `findings.md` (empty findings table +
coverage note + zero roll-up). "No findings" is a valid, required output — not a missing file.

## Gate consumption (informative)

The synthesis gate reads all four `findings.md`, verifies conformance to this schema, de-duplicates
findings that two spokes raised about the same `location`, aggregates the roll-ups, maps issue-#11
acceptance criteria to the findings, applies the verdict rule above, and writes the root
`SYNTHESIS.md`. The gate MUST NOT silently plug a failed identity (e.g. a non-conformant or missing
findings file) — it reports it.
