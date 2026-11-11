# Security Scan — PR #209 (`deploy/chirp/10-deployment.yaml`)

## Verdict

PASS

## Evidence

**Scan scope**: Full content of `deploy/chirp/10-deployment.yaml` as it appears on the
`deploy/update-chirp-server-digest-d8230fea` branch (not only the diff lines), plus the diff
itself. The brief requires scanning the whole file because a changed file ships as-is.

**Method**: Retrieved the full file via `gh api` with `?ref=<branch>` and the diff via
`gh pr diff 209 --repo Nousix-LLC/nswe-demo`. Checked every line against the six forbidden
categories.

**Category-by-category results**:

| Category | Patterns searched for | Result |
|---|---|---|
| Absolute host paths | `/home/`, `/root/`, `/home/<user>/` | **None found.** Only container-internal paths present: `/tmp` (emptyDir mount), `/srv/chirp` (read-only container root reference), `/healthz`, `/readyz` (HTTP probe paths). |
| Tailnet / LAN IP addresses | `100.x.x.x` and other IP patterns | **None found.** No IP addresses appear anywhere in the file. |
| Internal / non-public server URLs | Hostnames or URLs outside public registries and GitHub | **None found.** The only URL-class value is `ghcr.io/nousix-llc/chirp-server@sha256:…`, which is GitHub Container Registry — a public registry address. |
| SSH key paths or key material | `.ssh/`, `.pem`, `.key`, PEM-block headers | **None found.** |
| Secrets, passwords, tokens, credentials | Literal credential values, connection strings with embedded passwords | **None found.** `CHIRP_DATABASE_URL` is consumed via `secretKeyRef` from the out-of-band Secret `chirp-db-credentials`; no literal value is present. `ghcr-pull` is a reference to an imagePullSecret resource, not a credential. Both references are explicitly documented in comments as "NOT committed to git." |
| Internal infrastructure details | Server hostnames, cluster addresses, node names | **None found.** Kubernetes resource names (`chirp-db-credentials`, `ghcr-pull`, namespace `chirp`) are application-layer manifest identifiers; they do not expose server hostnames, IP addresses, cluster API endpoints, or node names. |

**Diff-specific check**: The diff modifies only the image digest comment (CI run reference,
commit hash, and issue number) and the image tag line. All new values are:
- `d8230fea` — a public git commit hash
- `41803200262` — a public GitHub Actions run ID
- `ghcr.io/nousix-llc/chirp-server@sha256:f845ca8c29408fd27d0fc3a6ff3f0f0d661d17ffd63b6427dcceb5b6845f044f` — a public registry reference

None introduce any forbidden content.

## Findings

None.
