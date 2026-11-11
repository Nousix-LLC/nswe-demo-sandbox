# Security / Information Hygiene Findings — PR #210

## Summary

Checked three surfaces committed to the repository in PR #210 — the `crates/ferric-http/CHANGELOG.md`
additions (160 lines, new file), commit messages for both commits (`d6a9b6e`, `0436218`), and the PR
description — against six categories of sensitive/internal-infrastructure content. Five of the six
categories are entirely clean. One ADVISORY finding: the commit message for commit `0436218` names
the internal review workflow run (`review-ferric-http-r1`) both in the headline and body. This is an
internal orchestration artifact name, not a server address, credential, or filesystem path; it does
not constitute a security blocker.

Overall result: **1 ADVISORY finding; no BLOCKERs; no SHOULD_FIX items.**

---

## Findings

**[CLEAN] Category 1 — Absolute filesystem paths**: No absolute host paths starting with `/home/`,
`/root/`, `/Users/`, `/var/`, `/opt/`, `/srv/`, or any other absolute filesystem prefix appear in
CHANGELOG.md, the two commit messages, or the PR description. The file reference
`chirp-frontend/src/api.rs` that appears in CHANGELOG.md (acceptance-criteria table, REQ-HTTP-011
row) and in the PR description is a project-relative source path, not a host path, and is appropriate
for public documentation of a library consumer.

**[CLEAN] Category 2 — IP addresses or private network hostnames**: No IPv4 addresses (private
ranges `10.x.x.x`, `172.16–31.x.x`, `192.168.x.x`) and no Tailscale `100.x.x.x` addresses appear
in any committed content. No internal server hostnames or private DNS names present.

**[ADVISORY] Category 3 — Taskflow / runtime directory references**:
- File: `crates/ferric-http/CHANGELOG.md` (not in this file; see commit message below)
- Surface: Commit message headline and body for commit `0436218`
- Principle: Committed content in a public repository should not reveal internal orchestration
  tooling names; CLAUDE.md explicitly states that server address, SSH key path, user name, and host
  paths must not appear in GitHub issues, PRs, comments, or committed files.
- Evidence: The headline reads "fix(ferric-http): correct API signatures in CHANGELOG.md
  (review-ferric-http-r1 blockers)" and the body reads "Fixes two blocker findings from
  review-ferric-http-r1 and addresses three should-fix items while editing:". The token
  `review-ferric-http-r1` is the name of the internal taskflow DAG run from which the prior review
  findings originated.
- Severity rationale: This is ADVISORY, not BLOCKER or SHOULD_FIX. The string reveals that an
  internal review orchestration system exists and uses this naming convention, but it exposes no
  server address, file-system path, SSH key, credential, or network topology. The commit is already
  merged; the information is in the git log and cannot be removed without rewriting history. For
  future commits, using a human-readable descriptor ("prior review round" or "r1 review findings")
  instead of the DAG run ID would avoid leaking internal workflow naming conventions.
- Resolution: No change required for merge. For future practice, strip internal DAG run IDs from
  commit messages; use project-visible language ("prior review round" or reference the GitHub PR
  that carried those findings).

**[CLEAN] Category 4 — SSH key paths or usernames**: No references to `~/.ssh/`, SSH key file
names, or server usernames appear in any committed content. The Co-Authored-By attribution
(`dev@example.com`, `noreply@anthropic.com`) in commit trailers is standard git attribution
using public email addresses, not internal server credentials.

**[CLEAN] Category 5 — API keys, tokens, or credentials**: No strings resembling API keys, bearer
tokens, secrets, or credentials appear in CHANGELOG.md, either commit message, or the PR
description. The CI-gate table in the PR description records command invocations and pass/fail
status; it contains no secret material.

**[CLEAN] Category 6 — Internal tooling references (ArgoCD apps, Kubernetes cluster names, build
infrastructure)**: No ArgoCD application names, Kubernetes cluster identifiers (such as `k3d-nswe`),
internal namespace names, or other Kubernetes/cluster infrastructure-identifying strings appear in
any committed content. The cargo commands in the CI table (`cargo fmt`, `cargo clippy`, `cargo test`,
`cargo build`, `cargo doc`) are public-facing standard toolchain invocations, not internal
infrastructure identifiers. (The DAG run name covered in Category 3 is the only internal tooling
reference found.)

---

## Verdict contribution

**APPROVE** — No blockers found in this concern area. The single ADVISORY (internal DAG run name
in a commit message) does not prevent merge; it is a future-practice note.
