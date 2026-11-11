# Task: Secrets and Infrastructure Data Scan

## Task Specification

**Slug**: SUBTASK_sec_secrets
**Task Kind**: standard
**Depends on**: none
**Status**: Pending
**Assigned To**: swe-reviewer

### Objective

Scan the diff for the three remediation commits to identify any hardcoded IP addresses, hostnames, credentials, auth tokens, SSH keys, real server addresses in test files, or other sensitive infrastructure data committed into the repository.

---

## Context

This task is part of the security review subtree for PR #193. See `../_GLOBAL.md` for full scope and constraints.

**Files changed by the remediation commits:**
- `crates/ferric/src/async_resource.rs` — B1
- `crates/ferric/src/vdom.rs` — B2
- `crates/ferric/src/dom.rs` — B2
- `crates/ferric/src/form.rs` — B3 (includes new WASM test)

---

## Input Specification

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Scope and constraints |
| PR diff | `gh pr diff 193 --repo Nousix-LLC/nswe-demo` | Changed lines to scan |

The diff is the primary source for this concern — if the data is not in the diff, it was not introduced by these commits.

---

## Review Questions

1. Does the diff contain any hardcoded IP addresses, hostnames, credentials, auth tokens, SSH keys, or similar infrastructure details?
2. Do the new test files or test helpers contain any real server addresses, real credentials, or other sensitive data?

---

## Output Specification

**Primary Output:** `finding.md` at this task's workspace root (`SUBTASK_sec_secrets/finding.md`)

The finding file MUST follow the schema in `../_GLOBAL.md` §Contract:

```markdown
## Finding

- **severity**: blocker | non-blocker | clean
- **concern**: Secrets and infrastructure data
- **location**: crates/ferric/src/file.rs:LINE (or N/A)
- **description**: [what was found or verified clean]

## What was examined
[Files, diff sections reviewed, and which sub-questions above were answered]
```

---

## Suggested Methodology Files

Task type row (Domain Mapping): **Security review** → Primary: `security`

- `security/Security_Secure_Coding_Methodology.md` — credential handling and sensitive data sections; use the secrets-management and credential-exposure checklist items
- `security/BestPractices_Configuration_Management_Methodology.md` — environment-variable and secrets hygiene principles to apply when evaluating what should/should not appear in source

These are SUGGESTIONS. The agent is the final judge of what its work requires — load fewer if inapplicable.

## Inherited Constraints

- Repository-relative paths only in all findings
- Focused pass on the three remediation commits only
- Severity `blocker` only for concrete security vulnerability (leaked credential, real server address) introduced by this PR

## Success Criteria

- [ ] Both review questions answered with evidence from the diff
- [ ] `finding.md` produced with `severity` assigned
