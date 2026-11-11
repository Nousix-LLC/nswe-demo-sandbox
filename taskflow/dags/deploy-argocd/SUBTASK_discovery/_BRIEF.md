# Task: Resolve ground-truth facts for the chirp deploy

## Task Specification

**Slug**: SUBTASK_discovery
**Task Kind**: standard
**Status**: Pending

### Objective

Establish the authoritative facts the manifest-authoring spokes and the synthesis gate need, and
record them in one file, so no downstream task has to re-derive them (and so two spokes cannot
diverge on them).

### Context

Part of the deploy-argocd subtree (NSWE #13) — see `../_GLOBAL.md` and `../contracts/`. This is the
serialized precursor: its output `outputs/ground_truth.md` is a declared dependency of both authoring
spokes and of the synthesis gate.

**Dependencies**: none (Group 0).
**Dependents**: `SUBTASK_app_manifests`, `SUBTASK_argocd_gitops`, `SUBTASK_synthesis`.

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Subtree hub | `../_GLOBAL.md` | Scope, constraints, chosen decomposition |
| Contract | `../contracts/_MANIFEST.yaml`, `../contracts/deploy_contract.yaml` | The fields to resolve (see `derived_facts`) and identities to ground |

### Facts to resolve (the output must answer each)

- **Repo checkout**: the absolute path of the working git checkout of `Nousix-LLC/nswe-demo` at
  `origin/main @ ada3aa9` (clone via `gh`/`git` if none exists; record the path). This is where the
  authoring spokes will write `deploy/chirp/` and `deploy/argocd/`.
- **Image digest**: the ACTUAL published `ghcr.io/nousix-llc/chirp-server` image digest
  (`@sha256:...`) from the #11 CI pipeline's GHCR package — the immutable digest to pin, not a tag.
  Record how it was obtained (e.g. `gh api` / registry manifest / `crane`/`docker buildx imagetools`).
- **Health surface**: the container's real listen port and health path, read from the root
  `Dockerfile` (EXPOSE/CMD) and `deploy/docker/healthcheck.rs` — distinguish SPA root vs an API
  health endpoint so probes target the real surface.
- **Cluster facts** (read-only inspection of the live k3d `nswe` / k3s v1.35.5+k3s1 cluster): the
  ingress class (k3s Traefik), the ArgoCD version and the `Application`/`AppProject` `apiVersion`,
  any relevant storage/namespace facts, and whether the GHCR package is private (→ imagePullSecret
  need). Do NOT mutate the cluster.

### Input Verification
- [ ] `../_GLOBAL.md` and `../contracts/` readable.

---

## Process Specification

Approach: resolve each fact from an authoritative source and record it with provenance (the command
or file it came from) so the synthesis gate can trust and re-check it. Treat cluster access as
strictly read-only. If a fact cannot be resolved (e.g. the image is not yet published), record that
explicitly with the blocking reason rather than guessing — a wrong digest or port poisons both spokes.

### Methodology
Apply the suggested bundles below for registry/image-digest resolution, k3s/Traefik ingress facts,
and ArgoCD CRD-surface inspection.

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| Filename | `ground_truth.md` |
| Location | `outputs/` (under this task's workspace) |

The output MUST record, with provenance for each: `repo_checkout_path`, `image_digest`,
`container_listen_port`, `health_path`, `ingress_class`, `argocd_application_apiversion`,
`appproject_apiversion`, `ghcr_package_private`, and any `storage_notes`. Match the field names in
`../contracts/_MANIFEST.yaml` `derived_facts` so downstream tasks can consume them unambiguously.

---

## Success Criteria

- [ ] Every `derived_facts` field in the contract manifest is resolved and recorded with provenance,
      OR explicitly marked unresolved with the blocking reason.
- [ ] The image digest is a real published `@sha256:` digest (not a placeholder/tag).
- [ ] Cluster inspection was read-only (no mutations).
- [ ] `outputs/ground_truth.md` exists and is self-contained.

---

## Suggested Methodology Files

The parent's Domain-Mapping reading for this child (SUGGESTIONS — load as a starting point; you are
the final judge; load fewer if clearly inapplicable, more if your reading reveals additional surface):

- Task-type rows: *"Kubernetes networking & service connectivity"* (primary `kubernetes`), *"Image
  signing & admission-time verification"* / supply-chain (`kubernetes-security`), *"Container
  deployment / production ops"* (`containerization`), *"GitOps repository topology & app composition"*
  (`gitops`).
- Bundle IDs to load via `engine_load_methodology`: `kubernetes` (networking/ingress facts),
  `kubernetes-security` (`K8sSecurity_Supply_Chain_Security_Methodology.md` — resolving/verifying an
  immutable image digest), `containerization` (`Containerization_Docker_Build_Methodology.md`,
  `Containerization_Runtime_Methodology.md` — reading the Dockerfile for port/health), `gitops`
  (ArgoCD Application/AppProject surface), `operations` (gh CLI / registry access).
- Rationale: this task's whole job is grounding facts from the registry, the Dockerfile/healthcheck,
  and the live cluster — the above bundles cover exactly those sources.
- These are the parent's flagged methodologies based on task type. Load them as a starting point but
  you are the final judge of what your work requires.

## Inherited Constraints

- Cluster access is **read-only** here. Target only the k3d `nswe` cluster.
- Repo scope `Nousix-LLC/nswe-demo`; base `origin/main @ ada3aa9`.
- Record the ACTUAL digest; never substitute a movable tag or a placeholder.
- No secrets written to the tree or to the output file.

## Out-of-Scope Methodologies

- Authoring manifests, RBAC/AppProject design, or deploying — those belong to the sibling authoring
  spokes and the synthesis gate, not here. Do not write any `deploy/` manifest.
