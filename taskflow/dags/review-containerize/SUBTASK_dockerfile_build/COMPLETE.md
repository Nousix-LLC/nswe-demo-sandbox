# COMPLETE — SUBTASK_dockerfile_build

**Task**: Reviewer's judgment over PR #22's build & image-composition story (concern 1, concern 2 layer/size face, concern 6 Dockerfile/shell idiom slice) → `findings.md`.

**Status**: completed (Atomic).

## What was done

Reviewed, read-only, the `Dockerfile` and `.dockerignore` of PR #22 at head `bc0c3c0d6380c9edd1b9433addc7fdcbffb55751` (`Nousix-LLC/nswe-demo`), corroborated against `Cargo.lock` and the code-DAG machine gate `taskflow/dags/containerize/SYNTHESIS.md`. Applied the containerization Docker-build and runtime methodologies plus the code-review checklist. Rendered a per-concern disposition for each owned concern and recorded severity-tagged findings per `../contracts/findings_schema.md`.

## Result summary

- **Concern 1 (build correctness & reproducibility): PASS.** Both the release `chirp-server` and the `wasm-bindgen --target web` SPA bundle are built; `--locked` on all three cargo invocations; both base images pinned by tag **and** `@sha256` digest; `ARG WASM_BINDGEN_VERSION=0.2.129` verified equal to the `wasm-bindgen` pin in `Cargo.lock`; the builder-1.88-vs-MSRV-1.82 bump is sound and justified; `.dockerignore` trims context without starving the build. Reproducibility/`--locked`/digest claims checked against the actual file, not the gate summary.
- **Concern 2 (layer composition + size): PASS.** Runtime carries only server binary + probe + SPA; no toolchain/source leakage; glibc 2.36 ABI match (bookworm ↔ cc-debian12); 41.7 MB breakdown holds, within the <50 MB target. Secret-leakage face cross-referenced to `SUBTASK_security_supplychain`, not re-filed (I2).
- **Concern 6 (Dockerfile/shell idiom slice): PASS.** Exec-form ENTRYPOINT/HEALTHCHECK, `set -eux`, syntax header for cache mounts, single cleaned apt layer, absolute WORKDIR, OCI labels, accurate comments.

**Findings filed**: `BUILD-1` (minor — unenforced `ARG`↔`Cargo.lock` version coupling), `BUILD-2` (nit — `.dockerignore` redundant entries). **No `block`/`major`** — the build is correct, reproducible, and the image minimal; severity discipline (I4) honored.

## Contract compliance

- Output `findings.md` conforms to `../contracts/findings_schema.md` (header, per-concern dispositions, findings table with the exact column set, `BUILD-` prefix).
- Read-only honored throughout (I5): no edit/commit/push/merge; no container rebuild (green gate relied upon).
- Only concerns owned by this spoke are filed; sibling territory cross-referenced by note only.

## Output

- `SUBTASK_dockerfile_build/findings.md`
