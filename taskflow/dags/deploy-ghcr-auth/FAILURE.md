# FAILURE.md — deploy-ghcr-auth (F1 of #29)

**Failure class:** blocked on a missing external capability (no GHCR `read:packages` credential and no
package-admin in this environment). Not a defect in analysis or resolution design. The acceptance
criteria require the deploy to be verified-reachable on the committed digest; that cannot be achieved
here. Reported `failed` so the overseer can re-fork with a packages-scoped credential.

The full verdict, live evidence, acceptance-criteria table, resolution + trade-off, and verification
runbook are in the sibling **`SYNTHESIS.md`** (overseer observation seam). Summary below.

## What was attempted

1. Verified live cluster state (ns `chirp`, ArgoCD `chirp` Application + AppProject) — all matches the
   brief: digest pod `ImagePullBackOff`, `ghcr-pull` Secret absent, stale `chirp:local` pod the sole
   endpoint, Application Synced@`22d2df6` but Health=Degraded, `Secret` not in the AppProject whitelist.
2. Attempted both candidate resolutions and every credential path to enable them.
3. Delivered the durable, landable half of the fix: **PR #30** (branch `work/deploy-ghcr-auth`, commit
   `18ab880`) strengthening the `deploy/chirp/README.md` pull-auth runbook (least-privilege requirement,
   selfHeal-survival rationale, live verification runbook, public-package trade-off). `main` not pushed.

## Ruled-out hypotheses (so the next attempt doesn't re-tread them)

- **`gh` OAuth token can pull GHCR** — NO. Scopes `gist, project, read:org, repo, workflow`; no
  `read:packages`. `docker pull <digest>` → **403**; token-exchange manifest fetch → **404**.
- **Stored `~/.docker/config.json` `ghcr.io` cred is different/stronger** — NO. Same `mattsmcknight`
  identity, same lack of package scope; manifest fetch → **404**.
- **Anonymous pull (package already public)** — NO. Anonymous GHCR fetch → **403** (private).
- **Flip package visibility via API** — NO. `GET /orgs/nousix-llc/packages/container/chirp-server` →
  **403 "need at least read:packages scope"**; the token has no package scope to change visibility.
- **Escalate token scope non-interactively** — NO. `gh auth refresh -s read:packages` is a device-flow
  (interactive); not viable headless.
- **Local `docker pull` + `k3d image import`** — NO. Can't pull the image without a credential; and an
  imported image would be undocumented, non-durable cluster state (fails the operability bar) anyway.
- **Org authority exists but token doesn't** — `mattsmcknight` is an org **admin** of `nousix-llc`, so a
  human/overseer with a properly scoped token CAN resolve this trivially; the sandbox token simply lacks
  the scope.

## What the overseer needs to do to unblock (one step, then re-fork/verify)

Provide a least-privilege `read:packages`-ONLY credential for `nousix-llc/chirp-server` and create the
Secret (or make the package public — a recorded supply-chain trade-off):

```sh
kubectl -n chirp create secret docker-registry ghcr-pull \
  --docker-server=ghcr.io --docker-username='<bot-or-user>' \
  --docker-password='<token with read:packages ONLY>'
```

ArgoCD selfHeal then rolls the committed digest to `1/1 Ready` and scales the stale `chirp:local`
ReplicaSet to 0; verify AC1–4 with the runbook in `deploy/chirp/README.md` (PR #30). Because `Secret` is
not in the AppProject `namespaceResourceWhitelist`, the out-of-band Secret survives selfHeal/prune.

## Constraints honored

No change to app code / image / digest; no deploy re-architecture; no `main` force-push or history
rewrite; no attribution trailers on the commit or PR; PR #30 does not carry `Closes #29` (#29 stays
open). A GitHub token value transiently echoed by a shell typo during investigation was **not** written
to any file, manifest, runbook, or terminal record.
