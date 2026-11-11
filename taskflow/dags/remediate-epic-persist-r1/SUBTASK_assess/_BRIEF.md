# Task: Diagnose the PR #113 `doc` hazards — produce the correction inventory

## Task Specification

**Slug**: SUBTASK_assess
**Task Kind**: standard
**Status**: Pending

### Objective

Survey the `Nousix-LLC/nswe-demo` branch `work/epic-persist` at its pinned head and produce a **complete, precise
correction inventory** of every documentation hazard that keeps the required `doc` CI check red under `-D warnings`,
plus the connected #118 hazards — so the remediation step can apply fixes mechanically and nothing resurfaces on the
`doc` re-run.

### Context

Part of the PR #113 doc-blocker remediation (see `../_GLOBAL.md`). The `doc` job fails because a public doc comment
links into a private module under `RUSTDOCFLAGS: -D warnings`. rustdoc reports only the **first** failing crate, so a
partial inventory is a trap: a second public→private or ungated→gated link left undiagnosed will fail the check again
after the first is fixed. The inventory you produce is the seam the whole pipeline composes against.

**Dependencies**: none.
**Dependents**: `SUBTASK_apply_fixes` consumes your inventory; `SUBTASK_synthesis` asserts coverage against it.

### Distinct concerns to diagnose (each is a hazard class the inventory must cover)

- **Public→private intra-doc links** — the known **CI-01** case is `export_user_data` at
  `crates/chirp-server/src/repository/in_memory.rs` (~L787) linking `` [`ExportDocument`](super::export::ExportDocument) ``
  into a `pub(crate)` item in the private `export` module. Find this **and any other** public item whose doc links
  into a `pub(crate)`/private item in the changed crate.
- **Ungated→gated doc links** — the known case is `crates/chirp-server/src/repository/export.rs` (~L7): an
  always-compiled reference linking into the `postgres`-feature-gated module. Find this and any other always-compiled
  doc that links into a feature-gated item.
- **Stale scaffold / placeholder docs** — public doc comments on the persistence layer that still describe
  now-implemented methods as unimplemented stubs/placeholders.
- **Internal build-breakdown vocabulary** — workstream/scaffold vocabulary that leaked into shipped public comments.

## Input Specification

| Input | Source (repository identity) | Purpose |
|-------|------------------------------|---------|
| Project context | `../_GLOBAL.md` | Constraints, scope, success criteria |
| Correction schema | `../contracts/inventory.schema.yaml` (read-only) | The record shape your inventory MUST conform to |
| Branch under remediation | `Nousix-LLC/nswe-demo` `work/epic-persist`, PR #113, head `09fa453c3c40e39a9b4647e0de6e00dcf50ecb21` | The code to survey |
| Review verdict / issue #118 | PR #113 review (CI-01 finding); issue #118 acceptance criteria | What "resolved" means for each hazard |

## Output Specification

**Primary output**: `INVENTORY.md` in this task's workspace — a list of correction records, each conforming to
`../contracts/inventory.schema.yaml` (`id`, `file`, `anchor`, `hazard_kind`, `current`, `rework`, `criterion`). Each
record names the exact current text and the exact docs-only rework. The inventory must be complete enough that
applying every record leaves `cargo doc` green under `-D warnings`.

## Success Criteria

- [ ] Every hazard across the four classes above is captured as a schema-conforming record (CI-01 included).
- [ ] Each record's `rework` is a concrete, docs-only replacement (plain code span, reworded sentence, accurate
      prose, or a doc feature-gate attribute) — never a change to store logic, schema, migrations, or wiring.
- [ ] The inventory distinguishes `CI-01` from `#118` records via the `criterion` field.
- [ ] `INVENTORY.md` is self-contained: a reader can apply each fix from the record alone.

## Constraints

- Documentation / doc-feature-gating findings only; propose no logic/schema/migration/wiring change.
- Read-only task: do not edit repository source or push anything. Diagnosis only.
- Output hygiene: `INVENTORY.md` names everything by repository identity (repo-relative paths, symbols, issue/PR
  numbers) — no host/cluster/SSH/credential/taskflow details.
