# COMPLETE — SUBTASK_security_supplychain

**Task**: Security reviewer's judgment over PR #22's container security posture, supply-chain /
dependency trust boundary, and the secret/credential-leakage face of concern 2. Output: `findings.md`
in the `contracts/findings_schema.md` shape.

## What was done

Read the `Dockerfile`, `.dockerignore`, `deploy/README.md`, and the `main.rs`/`healthcheck.rs` context
from the PR #22 diff at head `bc0c3c0d` (read-only via `gh pr diff`), plus the hub, contract manifest,
findings schema, and the code-DAG machine gate (`taskflow/dags/containerize/SYNTHESIS.md`). Grounded the
judgment in the `security` bundle (Secure-Coding least-privilege + Dependency-Security supply-chain/lock
discipline). Verified each posture/supply-chain claim against the actual file content rather than taking
the diff's prose at face value, and against the machine gate for runtime facts.

## Result (dispositions)

- **Concern 3 — container security posture**: `PASS-WITH-NOTES`. Non-root `USER 65532:65532` (gate-confirmed
  live PID-1 uid), exec-form `ENTRYPOINT`/`HEALTHCHECK`, distroless minimal surface, no baked secrets,
  documented read-only/cap-drop/no-new-privileges run. One minor least-privilege note (SEC-1).
- **Concern 3 — supply-chain / dependency trust boundary**: `PASS`. Both base images tag+`@sha256` digest
  pinned (match the gate); `--locked` on the CLI install and both cargo builds; `wasm-bindgen-cli` from
  crates.io, version-pinned, `--locked`, deliberately chosen over a prebuilt binary.
- **Concern 2 (secret/credential-leakage face only)**: `PASS`. No credential `ARG`/`ENV`/`COPY`;
  `.dockerignore` excludes `.env*`/`.git`; runtime image carries only binaries + static bundle.

## Findings

- **SEC-1 (minor, Concern 3)** — `COPY --chown=65532:65532 /out/static /srv/chirp` makes the served SPA
  writable by the serving process; remediation: drop `--chown` so assets are root-owned read-only.
- **SEC-2 (nit, Concern 3)** — `.dockerignore` is a denylist; optional defensive key-material globs.

No `block` or `major` findings. Severity discipline (I4) applied: the one concrete item is a non-blocking
improvement, not a significant defect.

## Contract conformance

- `findings.md` conforms to `contracts/findings_schema.md` (header + per-concern disposition + findings
  table with the exact column set + `SEC` finding-ID prefix per `_MANIFEST.yaml`).
- Identities honored on this spoke's side: I1 (each owned concern carries an explicit disposition),
  I2 (layer/size face of concern 2 and Dockerfile idiom cross-referenced, not re-filed), I4 (no inflated
  block/major), I5 (read-only; nothing written to GitHub).

## Output

- `SUBTASK_security_supplychain/findings.md`

Feeds `SUBTASK_verdict_synthesis`.
