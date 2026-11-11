# COMPLETE — SUBTASK_supply_chain_security (concern 3)

**Task**: Security review of `.github/workflows/ci.yml` at PR #21 head `c8123376` — least-privilege
permissions, secret handling, third-party-action supply-chain pinning. Read-only review.
**Decompose evaluation**: Atomic (single-responsibility security review of one artifact → one findings file).
**Status**: completed.

## What was done

- Fetched `ci.yml` at head `c8123376` via `gh api ... -q .content | base64 -d` (read-only; nothing pushed).
- Loaded the suggested security methodologies (`security/Security_Dependency_Security_Methodology.md`,
  `security/Security_Secure_Coding_Methodology.md`) for grounding on supply-chain pinning and least-privilege/secret handling.
- Assessed all three concern-3 facets:
  - **Top-level permissions** → `contents: read` (least-privilege default): clean.
  - **`image` job `packages: write` scoping** → job-level block replaces top-level set; write scope confined to the one job: clean.
  - **Secrets** → `GITHUB_TOKEN`-only, no PATs/external secrets; write path gated to `push`→`main` (not PRs); no expression-injection sink: clean.
  - **Third-party action pinning** → enumerated all 7 external actions; all mutable-tag-pinned, none SHA-pinned: findings raised.
- Emitted findings in the frozen schema (`../contracts/findings_schema.md`), id prefix `SEC-`.

## Findings summary (full detail in `findings.md`)

| id | severity | summary |
|----|----------|---------|
| SEC-1 | minor | All third-party actions tag/branch-pinned, not SHA-pinned; `image`-job `docker/*` actions are the higher-impact (write-token) slice; calibrated against owned hardening issue #24. |
| SEC-2 | nit | No build provenance/attestation/SBOM on the published GHCR image (#24-adjacent hardening). |

**Roll-up: block 0 · major 0 · minor 1 · nit 1** — no finding from this spoke forces `REQUEST-CHANGES`.

## Severity justification (issue #24 calibration)

Tag-pinning is a real, unmitigated supply-chain exposure, but severity was held at `minor` (not `major`/`block`)
because: (a) hardening is an explicitly owned separate track — issue #24 — so blocking this CI-standup PR on it
would reflexively block what #24 owns (the brief's inherited constraint); (b) all refs are reputable publishers;
(c) the write-scoped actions fire only on post-merge `main` pushes, never on PR triggers. The exposure is recorded
regardless, with SHA-pinning prioritization guidance aimed at the write-token slice.

## Scope boundary honored

Judged only the *security* of the `image` job's permissions/auth; its *functional* correctness is
`SUBTASK_image_job`, and workflow correctness/caching/toolchain-redundancy is `SUBTASK_workflow_correctness` —
cross-referenced in `findings.md`, not duplicated.

## Output

- `SUBTASK_supply_chain_security/findings.md` — schema-conformant findings (header states head `c8123376`; `SEC-` ids; roll-up present).

## Composition with parent

The synthesis gate (`SUBTASK_synthesis`) consumes this `findings.md` directly, aggregates the roll-up into the
verdict, and maps any issue-#11 acceptance criteria. This spoke contributes 0 block + 0 major, so it does not,
by itself, drive the verdict away from `APPROVE`.
