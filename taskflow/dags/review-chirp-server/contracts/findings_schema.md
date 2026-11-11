# findings_schema.md — the shared finding-record shape (READ-ONLY contract)

Every review spoke emits exactly one findings file (name fixed per `_MANIFEST.yaml` ownership) that
conforms to this schema so the synthesis gate integrates all four mechanically.

## File header (each spoke)

```markdown
# Findings — <lens name> (SUBTASK_<slug>)
- PR: #19 (chirp-server), head 714d50f, reviewing main...HEAD
- Lens: <rust-soundness | architecture-contract | test-adequacy | code-review-quality>
- Acceptance criteria owned: <AC ids from _MANIFEST, or "cross-cutting">
- F1 sub-questions owned: <F1 ids from _MANIFEST, or "none">
- Overall lens disposition: <clean | findings-only-minor-or-nit | has-major | has-block>
```

## Finding record (repeat per finding)

Each finding is a markdown block with these fields. Keep it concrete and actionable — a reviewer's
finding, not a summary.

```markdown
### <FINDING-ID>  — <one-line title>
- **Severity**: <block | major | minor | nit>
- **AC / F1 ref**: <AC id(s) and/or F1 id(s) this bears on, or "general">
- **Location**: <path:line or path:symbol in crates/chirp-server/...>, or "(crate-wide)"
- **Observation**: <what the code does / fails to do — cite the diff or file>
- **Why it matters**: <impact: correctness / contract / soundness / maintainability / test gap>
- **Recommendation**: <the change the remediation DAG would make — do NOT make it here>
```

`<FINDING-ID>` convention: `<LENS>-NN` (e.g. `RUST-01`, `ARCH-02`, `TEST-01`, `CRQ-03`). Use a
stable, lens-prefixed id so the gate can reference it.

## Per-AC / per-F1 verdict ledger (mandatory, even when clean)

Each spoke MUST close with an explicit ledger for the AC/F1 items it owns — so "no finding" is an
affirmative statement, never silence the gate has to interpret:

```markdown
## Verdict ledger (owned items)
| AC / F1 id | Verdict | Evidence (file:line / test name / diff ref) | Finding id (if any) |
|------------|---------|----------------------------------------------|---------------------|
| AC3        | conforms | error.rs IntoResponse maps all 6 rows        | —                   |
| F1_2       | conforms | tests/api.rs::...invalid_dto...; grep: no 422 pin | —              |
```

## Severity vocabulary (fixed — the gate derives the verdict from these)

| Severity | Meaning | Effect on verdict |
|----------|---------|-------------------|
| `block`  | Must fix before land: correctness/contract/soundness defect that violates an acceptance criterion or the frozen wire contract, or a panic/unsafe on a request path | Any open `block` ⇒ `REQUEST-CHANGES` |
| `major`  | Significant quality/design problem that should be fixed but does not by itself violate the rubric | Gate decides (with reasoning) whether it forces `REQUEST-CHANGES` |
| `minor`  | Low-impact issue; land-then-fix acceptable, carry as tracked issue | Does not block |
| `nit`    | Style/taste; non-binding | Does not block |

## Discipline (binds every spoke)

- **Review only.** Do not edit source, do not push, do not relock/rebase, never touch `main`.
  Only `Nousix-LLC/nswe-demo`. Do NOT run `gh pr review` — the synthesis gate posts the single review.
- **Do NOT flag the CONFLICTING/DIRTY mergeability** — it is a known `Cargo.lock` restale, not a code defect.
- **Rely on the code DAG's cold machine gate** (`chirp-server/SYNTHESIS.md`) for build/test/fmt/clippy
  PASS; do not reproduce the full cold build. You MAY read files, run read-only `cargo`/`grep`
  inspection against the checkout to corroborate a specific finding, and read the diff via `gh pr diff 19`.
- **Cite evidence.** A finding without a `file:line` / test name / diff ref is not actionable.
