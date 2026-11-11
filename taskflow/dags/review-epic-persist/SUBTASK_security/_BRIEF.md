# Task: Security and trust boundaries — PR #113

## Task Specification

**Slug**: SUBTASK_security
**Task Kind**: standard
**Status**: Pending

### Objective

Judge the change's security posture at the store boundary and in the deployment surface: credentials,
injection, migration safety, admission policy, and anything the diff pulls in.

### Context

Part of the PR #113 review DAG (see `../_GLOBAL.md`). Read-only; write a findings document only.

## Inputs

| Input | Source | Purpose |
|---|---|---|
| Subtree hub | `../_GLOBAL.md` | Pinned commit, target, constraints |
| Contract | `../contracts/finding_schema.md`, `../contracts/_MANIFEST.yaml` | Findings format + rubric |
| PR #113 diff @ `09fa453` | `gh pr diff 113` / `git` (read-only) | Store boundary, manifests, deps, lockfile |

## The bar (what blocks)

An exposure, or a committed/loggable secret, is a **blocking** finding. Examine at least:

- Credential handling for `CHIRP_DATABASE_URL`: supplied out of band, the `Secret` excluded from the ArgoCD
  AppProject, **nothing committed** and nothing logged (check source, manifests, and any log lines that could
  print the URL).
- SQL / injection and input handling at the store boundary (parameterized queries vs string building).
- Migration safety (can a migration run destructively or without control?).
- Pod Security `restricted` admission — does the StatefulSet/Pod spec satisfy it?
- Anything the diff pulls in: new dependencies / features, and their trust implications (scan the lockfile
  delta).

**Note:** when you quote evidence, never reproduce a real secret value or any host/cluster credential — point
at the file and line, describe the exposure, and keep the value out of the findings.

## Output

`SUBTASK_security/outputs/findings.md`, conforming to `../contracts/finding_schema.md` (prefix `SEC`).

## Success criteria

- [ ] Credentials, injection, migration safety, admission policy, and dependency pull-ins all assessed.
- [ ] "What I checked" / "what I found clean" both specific.
- [ ] Findings pinned, severities + `blocks_landing` honest, each with "what would satisfy me"; sub-verdict.

## Constraints

Read-only on the repo; no GitHub writes. No host/cluster/SSH/credential details or DAG internals, and **no
secret values**, in the findings. Plain voice.
