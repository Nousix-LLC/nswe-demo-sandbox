# SUSPENSION.md — deploy-ghcr-auth

**Status:** suspended (Atomic — external-input wait)
**Evaluation:** Atomic (one remediation responsibility)

## Why suspended

The resolution of F1 of #29 is fully determined and its durable documentation is landed as PR #30,
but the **live** fix cannot be completed in this environment. Making the committed private-GHCR digest
`@sha256:054af27…` pullable requires either (a) a `read:packages` credential for
`nousix-llc/chirp-server` to create the out-of-band `ghcr-pull` Secret in ns `chirp`, or (b) an
org-admin flip of the package to public. The only GitHub token available here is scoped
`gist, project, read:org, repo, workflow` — **no package scopes** — verified by `docker pull` → 403 and
packages API → 403. Non-interactive scope escalation is not possible headless. This is a blocked-on-
external-input condition, not a defect in the work.

Full evidence, acceptance-criteria results, resolution rationale, and verification runbook are in the
sibling `SYNTHESIS.md` (the overseer's observation seam).

## Resumption condition

A least-privilege GHCR pull credential (a `read:packages`-ONLY token for `nousix-llc/chirp-server`) is
made available so the `ghcr-pull` Secret can be created in namespace `chirp` — **or** an org admin makes
the `chirp-server` GHCR package public. On that input, re-dispatch to run the one-step fix and verify
AC1–4 live:

```sh
kubectl -n chirp create secret docker-registry ghcr-pull \
  --docker-server=ghcr.io --docker-username='<bot-or-user>' \
  --docker-password='<token with read:packages ONLY>'
```

ArgoCD selfHeal then rolls the committed digest to `1/1 Ready` and scales the stale `chirp:local`
ReplicaSet to 0.

## Work preserved

- Branch `work/deploy-ghcr-auth` (commit `18ab880`) pushed; **PR #30** → `main` open (not merged).
- Repo manifests and the committed digest are unchanged; `main` not pushed.
