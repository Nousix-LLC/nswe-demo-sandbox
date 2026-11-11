# SUSPENSION.md — security-persist-r1

**Status**: Suspended — NeedsDecompose  
**Decomposition**: security-persist-r1 decomposes into three sequential child tasks

## Decomposition Summary

Two distinct security concerns from issue #120 (PR #113 review) triggered decomposition by the
enumerated-concerns rule: the brief explicitly names two concerns that span different file trees,
different specializations (Rust crypto code vs. Kubernetes manifest), and can be verified
independently. A synthesis task was added to gate the combined output and open the PR.

### Children materialized

| Task id | Depends on | Responsibility |
|---------|------------|----------------|
| `SUBTASK_credential_hashing` | none | argon2id KDF + constant-time verify in Rust; creates branch |
| `SUBTASK_ssl_manifest` | `SUBTASK_credential_hashing` | `PGSSLMODE: require` in CronJob manifest |
| `SUBTASK_synthesis` | `SUBTASK_ssl_manifest` | Four-check verification gate + PR creation |

## Resumption Condition

This task resumes (folds SUSPENDED → COMPLETED) when the `SUBTASK_synthesis` child authors
`SYNTHESIS.md` at this workspace (`security-persist-r1/SYNTHESIS.md`) and calls
`engine_resume_suspended`. That happens after all three children reach COMPLETED.

## Workspace

`/home/user/nousix-runtime/nswe-demo/taskflow/dags/security-persist-r1/`

## Authored state files

- `_GLOBAL.md` — subtree hub (project context, repository facts, constraints)
- `contracts/_MANIFEST.yaml` — minimal seam contract (ownership, identity assertions)
- `SUBTASK_credential_hashing/_BRIEF.md` — credential hashing task brief
- `SUBTASK_ssl_manifest/_BRIEF.md` — SSL manifest task brief
- `SUBTASK_synthesis/_BRIEF.md` — synthesis gate task brief
