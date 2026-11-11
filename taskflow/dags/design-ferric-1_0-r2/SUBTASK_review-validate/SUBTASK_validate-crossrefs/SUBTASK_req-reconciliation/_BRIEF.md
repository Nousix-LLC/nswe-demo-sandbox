# Task: REQ Register Reconciliation

## Task Specification

**Slug**: SUBTASK_req-reconciliation
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-designer

### Objective

Read the nine concern-findings.md files, build the full REQ-* id inventory, and perform
three reconciliation checks: duplicate id detection, orphaned cross-reference spot-checking,
and BAR-FERRIC-* coverage verification. Produce `req-reconciliation.md` conforming to
`../contracts/_MANIFEST.yaml` §req_reconciliation_schema.

### Context

Part of the SUBTASK_validate-crossrefs subtree (see `_GLOBAL.md` in the parent workspace).
This task runs after all nine per-concern validators complete; it does not re-validate the
design documents from scratch. It builds the inventory from the req_ids_found lists in the
concern findings, then does targeted spot-checks against the design documents only to confirm
or deny specific cross-reference citations.

**Dependencies**: none (all nine concern-findings.md are already present)  
**Dependents**: SUBTASK_synthesis-crossrefs

---

## Inputs

| Input | Location | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Context and input paths |
| Contract | `../contracts/_MANIFEST.yaml` | Output schema |
| Parent contract | `../../contracts/_MANIFEST.yaml` | Concern-findings schema reference |
| Scope findings | `../../SUBTASK_validate-scope/concern-findings.md` | REQ-FW-* ids |
| SSR findings | `../../SUBTASK_validate-ssr/concern-findings.md` | REQ-SSR-* ids |
| Authoring findings | `../../SUBTASK_validate-authoring/concern-findings.md` | REQ-API-* ids |
| Async findings | `../../SUBTASK_validate-async/concern-findings.md` | REQ-ASYNC-* ids |
| Router findings | `../../SUBTASK_validate-router/concern-findings.md` | REQ-RT-* and REQ-HTTP-* ids |
| Docs findings | `../../SUBTASK_validate-docs/concern-findings.md` | REQ-DX-* ids |
| Release findings | `../../SUBTASK_validate-release/concern-findings.md` | REQ-REL-* ids |
| Perf findings | `../../SUBTASK_validate-perf/concern-findings.md` | REQ-PERF-* ids |
| Plan findings | `../../SUBTASK_validate-plan/concern-findings.md` | BAR-FERRIC-* → REQ-* citations |
| Design documents | branch `work/design-ferric-1_0` at `/home/user/nswe-demo` | Targeted spot-checks only |

For design documents: `git -C /home/user/nswe-demo show work/design-ferric-1_0:design/ferric/<file>`

---

## What to Produce

### Full REQ Inventory

Extract all `req_ids_found` lists from the nine concern-findings.md files and merge them into
a single inventory grouped by prefix. Record the source document for each id.

### Duplicate ID Check

Any REQ-* id that appears in the req_ids_found list of more than one concern-findings.md
is a duplicate. Flag each with both source locations.

### Orphaned Cross-Reference Check

Look for REQ-* ids that are cited in a document's body as cross-references (i.e., they appear
in the document text but are not in that document's own REQ register). For each such citation,
confirm the cited id exists in the owning document's req_ids_found list. Use targeted re-reads
of the relevant design document sections to verify, not a full re-read.

Note: cross-references between documents (e.g., ssr-hydration.md citing REQ-API-003) are
expected; the check is whether the cited id actually exists in the owning document's register.

### BAR-FERRIC Coverage Check

Read the release-bar concern findings for the list of BAR-FERRIC-* criteria and their REQ-*
citations. For each BAR-FERRIC-* criterion, confirm that every REQ-* id it cites appears in
the full inventory built above. Flag any BAR criterion citing a REQ-* id not present in the
inventory.

---

## Output

| Attribute | Value |
|---|---|
| Filename | `req-reconciliation.md` |
| Location | `SUBTASK_req-reconciliation/` (this workspace) |
| Format | Markdown, per `../contracts/_MANIFEST.yaml` §req_reconciliation_schema |

Required sections: full_req_inventory, duplicate_ids, orphaned_references, bar_without_req,
reconciliation_status.

---

## Success Criteria

- [ ] All nine concern-findings.md read and merged into full REQ inventory
- [ ] Duplicate id check complete (clean or flagged)
- [ ] Orphaned cross-reference check complete with spot-checks performed
- [ ] BAR-FERRIC coverage check complete
- [ ] `req-reconciliation.md` written with all required sections and a reconciliation_status
