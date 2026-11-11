# COMPLETE — SUBTASK_discovery (deploy-argocd, NSWE #13)

**Status**: completed (Atomic). **Date**: 2026-10-08.

## What this task did

Resolved the authoritative ground-truth facts the two authoring spokes and the synthesis gate need,
and recorded them — each with provenance — in `outputs/ground_truth.md`, so no downstream task
re-derives them and the two spokes cannot diverge on them. Cluster access was strictly read-only;
the repo checkout and GHCR package were inspected read-only (no mutations).

## Output

- `outputs/ground_truth.md` — self-contained facts record, field-aligned to
  `../contracts/_MANIFEST.yaml` `derived_facts`.

## Resolved facts (all `derived_facts` fields; none unresolved)

| Field | Value |
|---|---|
| `repo_checkout_path` | `/home/user/nswe-demo` (⚠ working tree at `25e90c0`, **5 behind** base `ada3aa9`; Dockerfile + `deploy/` exist only at `ada3aa9` — spokes MUST `checkout -B work/deploy-argocd ada3aa9` before authoring) |
| `image_digest` | `ghcr.io/nousix-llc/chirp-server@sha256:054af27f588c13aeebd8698dbddf690e15bf75cd36c9a087b38763fd0902abe3` (published manifest-list digest; from #11 CI run `37805862710` on `main`@`ada3aa9`) |
| `container_listen_port` | `8080` (Dockerfile `EXPOSE`/`CHIRP_BIND_ADDR=0.0.0.0:8080`) |
| `health_path` | `/healthz` (API health, HTTP 200 `{"status":"ok"}`; SPA at `/`) |
| `ingress_class` | `traefik` (k3s built-in; serverlb `localhost:8081 -> 80`) |
| `argocd_application_apiversion` | `argoproj.io/v1alpha1` (ArgoCD v3.5.4) |
| `appproject_apiversion` | `argoproj.io/v1alpha1` |
| `ghcr_package_private` | `true` — imagePullSecret required (or make package public); inferred from anonymous GHCR token `401` |
| `storage_notes` | none needed (stateless, in-memory repo); default SC `local-path` available |

## Key provenance

- Image digest: GitHub Actions run `37805862710` (the sole successful `ci.yml` push run on `main` @
  `ada3aa97eb2…`), corroborated by the `Summarize published image` step (`build.outputs.digest`), the
  `exporting manifest list sha256:054af27…` line, and both `pushing manifest … @sha256:054af27…` lines.
- Health surface: root `Dockerfile` and `deploy/docker/healthcheck.rs` read from the `ada3aa9` git
  objects (`git show ada3aa9:<path>`) since the current checkout tree predates #11.
- Cluster facts: read-only `kubectl get ingressclass/storageclass/ns/crd` and `kubectl -n argocd get
  deploy` against context `k3d-nswe` (k3s v1.35.5+k3s1).

## Notable / downstream-relevant findings

1. **Stale checkout** — the single biggest non-obvious fact: the checkout's `main` is 5 commits
   behind `ada3aa9` and lacks the Dockerfile and `deploy/` path. The authoring spokes MUST base
   `work/deploy-argocd` on `ada3aa9` (== current `origin/main`), not on the local `HEAD`.
2. **GHCR package is private** → the deploy will `ImagePullBackOff` without an imagePullSecret in
   namespace `chirp` (or making the package public). Flagged so a spoke/gate handles it deliberately.
3. **Namespace `chirp` does not exist yet** — needs a Namespace manifest and/or Application
   `CreateNamespace=true`.

## Environmental limitation (disclosed, non-blocking)

The environment `gh` token lacks `read:packages`, so the GHCR Packages API and authenticated registry
inspection were unavailable. The image digest was still resolved authoritatively from the Actions
publish log; the package-private flag was resolved via the anonymous-`401` discriminator rather than
the direct visibility field. Details in `outputs/ground_truth.md` §8.
