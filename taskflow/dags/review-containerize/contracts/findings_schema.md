# Findings Schema (contract artifact — READ-ONLY)

This is the shared structural declaration every analysis spoke composes against.
A spoke writes its `findings.md` to its OWN workspace in exactly this shape so the
synthesis gate can mechanically aggregate findings and render one verdict. Do not
redefine this schema; import it by conforming to it.

## Each spoke's `findings.md` MUST contain

### 1. Header
- **Spoke**: the SUBTASK slug.
- **Concerns owned**: the concern numbers from `_MANIFEST.yaml` this spoke owns (and any declared concern-6 / concern-2 slice).
- **Diff reviewed**: PR #22 head commit `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751` of `Nousix-LLC/nswe-demo`.

### 2. Per-concern disposition block
For EACH concern the spoke owns, a short block stating:
- **Concern N — <title>**: `PASS` | `PASS-WITH-NOTES` | `FAIL`
- A 2–5 sentence justification grounded in the actual diff (quote the line/section).
- `FAIL` is used when the concern has at least one OPEN `block` finding; `PASS-WITH-NOTES` when only `major`/`minor`/`nit` findings exist; `PASS` when clean.

### 3. Findings table
One row per finding, using this exact column set:

| Finding ID | Concern | Severity | Location | Evidence | Remediation |
|---|---|---|---|---|---|

- **Finding ID**: `<PREFIX>-<n>` using the spoke's `finding_id_prefix` from `_MANIFEST.yaml` (e.g. `BUILD-1`, `SEC-2`).
- **Concern**: the brief concern number this finding belongs to.
- **Severity**: one of `block` | `major` | `minor` | `nit` (see rubric below).
- **Location**: concrete — `path/to/file:line` or `path/to/file §section` or the artifact name. A finding with no location is not actionable.
- **Evidence**: what in the diff (or its absence) substantiates the finding — quote or cite precisely.
- **Remediation**: REQUIRED for `block` and `major` — a concrete, landable fix. Optional for `minor`/`nit`.

If the spoke finds nothing to report for a concern, it still emits the per-concern disposition (`PASS`) and writes "No findings." in the table region.

## Severity rubric (authoritative taxonomy)

| Severity | Meaning | Gate effect |
|---|---|---|
| `block` | A concrete, landable defect that is wrong and must be fixed before this PR should merge (e.g. the build cannot reproduce, a secret is baked into a layer, the SIGTERM code is incorrect, a claimed behavior is false). | Any OPEN `block` forces **REQUEST-CHANGES**. |
| `major` | A significant, concrete defect that is real and fixable but arguably non-merge-blocking. | Requires an explicit synthesis disposition; does not by itself force REQUEST-CHANGES. |
| `minor` | A concrete, non-blocking improvement. | Recorded; advisory. |
| `nit` | Stylistic / cosmetic. | Recorded; advisory. |

**Severity discipline (identity I4).** A `block` or `major` MUST name a concrete landable defect — a specific thing that is wrong in THIS diff and can be fixed. A hardening *wish*, a posture preference, or a "would-be-nice" is NOT a block/major regardless of how good the idea is; file it as `minor` or `nit`. When in doubt between major and minor, ask: "is there a concrete defect, or do I just want more?" Only the former is major.

## What a spoke MUST NOT do
- MUST NOT edit/stage/commit/push/rebase/relock/merge anything, or touch `main` / `work/containerize` (identity I5). Reviews read and report; they do not fix.
- MUST NOT re-run the container build to reconfirm the machine gate — rely on `taskflow/dags/containerize/SYNTHESIS.md` for build/run facts; judge the diff.
- MUST NOT file a finding for a concern it does not own; cross-reference a sibling's territory by note, do not re-file it.
- MUST NOT post anything to GitHub — the single posted review is the synthesis gate's job alone.
