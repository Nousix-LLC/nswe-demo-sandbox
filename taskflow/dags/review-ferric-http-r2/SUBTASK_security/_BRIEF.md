# SUBTASK_security: Security / Information Hygiene Check

## Task Specification

**Slug**: SUBTASK_security  
**Task Kind**: standard  
**Depends on**: none  
**Status**: Pending

### Objective

Check that no sensitive or internal-infrastructure information has been committed into the repository through PR #210: specifically, no absolute host paths, private/internal network addresses, host runtime or taskflow directory references, SSH key paths, server hostnames, or other internal configuration details appear in CHANGELOG.md or the PR's commit messages.

### Context

This is a spoke task in review-ferric-http-r2. See `../_GLOBAL.md` for full background and subtree constraints.

**Depends on**: none — reads committed content directly  
**Dependents**: `SUBTASK_verdict` reads `security_findings.md`

---

## Input Specification

### Required Inputs

| Input | Source | Purpose |
|-------|--------|---------|
| Project context | `../_GLOBAL.md` | Review scope and constraints |
| Findings schema | `../contracts/findings_schema.yaml` | Required output structure |
| CHANGELOG.md | repo root | Primary surface for committed content inspection |
| Commit messages | `gh pr view 210 --repo Nousix-LLC/nswe-demo --json commits` | Commit message text for the PR's commits |
| PR description | `gh pr view 210 --repo Nousix-LLC/nswe-demo` | PR body for any path/hostname references |

---

## Process Specification

Read the content of CHANGELOG.md (focusing on the additions/changes in this PR) and the commit messages. Check for:

1. **Absolute filesystem paths** — any path starting with `/home/`, `/root/`, `/Users/`, `/var/`, `/opt/`, `/srv/`, or other absolute paths that reveal the build server's filesystem layout.

2. **IP addresses or private network hostnames** — any IP addresses (e.g., `192.168.x.x`, `10.x.x.x`, `172.16-31.x.x`, `100.x.x.x` Tailscale ranges), server hostnames, or internal network references.

3. **Taskflow/runtime directory references** — any references to `nousix-runtime`, `taskflow/`, `dags/`, `nswe-demo/`, or similar internal orchestration paths.

4. **SSH key paths or usernames** — any references to `~/.ssh/`, key file names, or server usernames embedded in content.

5. **API keys, tokens, or credentials** — any string that looks like a secret or credential embedded in the CHANGELOG text or commit messages.

6. **Internal tooling references** — references to internal build tooling, ArgoCD application names, internal Kubernetes cluster names, or other infrastructure-identifying strings beyond what a public library consumer would see.

Note: This check covers only the content COMMITTED INTO THE REPOSITORY (CHANGELOG.md entries, commit messages, PR description). It does not apply to review comments or SYNTHESIS.md, which are not committed. The CLAUDE.md project file explicitly states that server address, SSH key path, user name, and host paths must NOT appear in GitHub issues, PRs, comments, or committed files.

---

## Output Specification

**File**: `security_findings.md`  
**Location**: `SUBTASK_security/`  
**Schema**: `../contracts/findings_schema.yaml`

Required sections (per schema):
- `## Summary` — what was checked, overall result
- `## Findings` — per-finding. CLEAN finding explicitly states each category was checked and found clear.
- `## Verdict contribution` — APPROVE or REQUEST-CHANGES from this concern area

---

## Success Criteria

- [ ] All 6 categories of sensitive content checked in CHANGELOG.md additions
- [ ] Commit messages checked for the same categories
- [ ] PR description checked
- [ ] Each category recorded as CLEAN or as a specific finding with the offending text
- [ ] `security_findings.md` written following the schema

---

## Suggested Methodology Files

**Task-type row (from Domain Mapping):** "Security review" — Primary: Security; Supporting: Code Review

Suggested files:
- `security/Security_Secure_Coding_Methodology.md` — secure coding; output hygiene and what constitutes a sensitive information leak. Rationale: the whole task is about output hygiene in committed content.
- `security/BestPractices_Configuration_Management_Methodology.md` — configuration management; what configuration details should not be in source-controlled artifacts. Rationale: server addresses, paths, and credentials are configuration that must stay out of the repo.
- `code-review/CodeReview_Checklist_Methodology.md` — the security items in the review checklist. Rationale: provides the standard review framing for security concerns.

These are suggestions. Load fewer if some are clearly inapplicable.

## Inherited Constraints

- Repo: `Nousix-LLC/nswe-demo`
- Check only the content added/changed by PR #210 (focus on the diff)
- Output file must follow `../contracts/findings_schema.yaml`
- Do not expose server addresses, SSH key paths, or user names in the findings file itself

## Out-of-Scope Methodologies

- Rust/signature methodology — handled by SUBTASK_correctness
- Code quality / structure methodology — handled by SUBTASK_code_quality
