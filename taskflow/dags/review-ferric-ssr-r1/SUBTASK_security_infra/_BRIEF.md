# SUBTASK_security_infra — PR #228 Infrastructure Exposure and Supply-Chain Review

## Task Specification

**Slug**: SUBTASK_security_infra
**Task Kind**: standard
**Depends on**: none
**Status**: Pending

### Objective

Examine PR #228 (`work/ferric-ssr-r1`, repo `Nousix-LLC/nswe-demo`) for committed
host/infrastructure detail exposure and supply-chain risk. Specifically: check that no absolute host
paths, Tailscale/LAN IP addresses, internal server URLs, or host runtime/taskflow directory paths
appear in committed files; and check that any new dependencies are reasonable. This is a read-only
review; do not modify source code.

---

## Context

See `_GLOBAL.md` (parent workspace) for PR coordinates and cross-cutting constraints.

**Depends on**: none (independent spoke — runs in parallel with other spokes)
**Dependents**: SUBTASK_synthesis reads this output

---

## Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Shared context | `../_GLOBAL.md` | PR coordinates, constraint on host detail exposure |
| PR diff | `gh pr diff 228 --repo Nousix-LLC/nswe-demo` | The change under review (all files) |
| Cargo.toml / Cargo.lock changes | In the diff | New dependencies |

---

## Review Scope

This review is EXCLUSIVELY about infrastructure detail exposure and supply-chain risk in committed
files. It does not cover HTML escaping, correctness, or code quality (those are other spokes).

### A. Host path exposure

- Examine every added or modified file in the diff for:
  - Absolute host paths (e.g., `/home/user/...`, `/root/...`, `/workspaces/...`)
  - Taskflow/runtime internal paths (e.g., paths containing `nousix-runtime`, `taskflow/dags`,
    `nswe-demo/infrastructure`)
  - Any path that leaks the host machine's directory structure into committed content

### B. Network address exposure

- Search for IP addresses in the Tailscale range (100.x.x.x) or LAN ranges (192.168.x.x, 10.x.x.x)
  in any committed file
- Search for any internal server URLs (e.g., `http://100.x.x.x:xxxx`, `https://internal.xxx`)
- Check comments, documentation, test fixtures, configuration files, and embedded strings

### C. Credentials and secrets

- Are there any hardcoded API keys, tokens, passwords, or secrets in the committed files?
- Are there any test fixtures that look like real credentials?

### D. Supply-chain risk in new dependencies

- Does the diff add any new crates to `Cargo.toml`?
- For each new dependency:
  - Is it a well-known, widely-used crate with a public crates.io presence?
  - Are there any dependencies that seem unusual for SSR HTML rendering (e.g., network crates,
    file-system crates) that would warrant further investigation?
  - Are the version constraints appropriate (not overly broad)?

---

## Output Specification

| Attribute | Value |
|-----------|-------|
| File | `security_infra_findings.md` |
| Location | this workspace (`SUBTASK_security_infra/`) |

### Output Structure

```markdown
# PR #228 Infrastructure Exposure and Supply-Chain Findings

## Summary
<one-paragraph verdict: any infrastructure detail committed? Any dependency concerns?>

## Findings by Area

### A. Host path exposure
**Status**: CLEAN | FINDING (BLOCKER)
**What was checked**: ...
**Evidence** (file and line in repository if finding): ...
**Finding** (if any): ...

### B. Network address exposure
...

### C. Credentials and secrets
...

### D. Supply-chain risk (new dependencies)
<List each new dependency with a brief assessment>
**Status**: CLEAN | FINDING (BLOCKER) | FINDING (NON-BLOCKER)
...

## Verdict
PASS | FAIL (blocker exposure found) | PASS WITH NOTES
```

---

## Success Criteria

- All four areas examined with evidence-backed findings or clean verdicts
- Any committed host detail is flagged as a blocker with the specific file and line
- Any new dependency is accounted for with a brief risk assessment
- Output file exists at the declared path before this task reports completed

---

## Suggested Methodology Files

**Task-type row matched**: "Security review" → Primary: `Security`; Supporting: `Code Review`

Specific files:
- `security/Security_Dependency_Security_Methodology.md` — supply-chain risk, dependency review practices; directly applicable to new dependency assessment
- `security/BestPractices_Configuration_Management_Methodology.md` — covers what should and should not be committed; applicable to credentials/secrets and configuration exposure

These are the parent's flagged methodologies. Load fewer if some are clearly inapplicable; load more if the brief reveals additional surface.

## Inherited Constraints

- **Scope**: This task covers ONLY infrastructure exposure and supply-chain. HTML escaping is SUBTASK_security_xss.
- **Read-only**: Do not modify source code
- **Host detail exposure in committed files IS a blocker** — it must not appear in committed files, issues, PRs, or comments
- Findings citing found host details must cite the file and line in the repository, not reproduce the full detail in this output (avoid leaking the detail further)
