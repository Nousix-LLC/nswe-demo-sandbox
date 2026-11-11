# PR #228 Infrastructure Exposure and Supply-Chain Findings

## Summary

PR #228 (`work/ferric-ssr-r1`) adds server-side rendering (SSR) support across two crates:
a new `ssr.rs` and `hydrate.rs` in `crates/ferric/`, and a new `ssr.rs` handler module in
`crates/chirp-server/`. The diff was examined across all four security areas. No host paths,
Tailscale or LAN IP addresses, internal server URLs, secrets, or external supply-chain
additions were found in any committed file. The only Cargo change is a workspace-local path
dependency on a sibling crate — no external packages enter the dependency graph.

---

## Findings by Area

### A. Host path exposure

**Status**: CLEAN

**What was checked**: Every added line in all eight changed files was searched for the
following patterns: `/home/`, `/root/`, `/workspaces/`, `nousix-runtime`, `taskflow/dags`,
`nswe-demo/infrastructure`. All URL-shaped strings in the diff were inspected individually.
The documentation comment in `crates/chirp-server/src/ssr.rs` that references
`design/ferric/ssr-hydration.md §2.1` is a repository-relative Markdown path in a Rust
doc comment — it names a file in the project repository, not a host filesystem path.

**Evidence**: No matches returned. Zero host filesystem paths appear in any added line.

**Finding**: None.

---

### B. Network address exposure

**Status**: CLEAN

**What was checked**: Every added line was searched for Tailscale address prefixes
(`100.`), LAN prefixes (`192.168.`, `10.`), and patterns matching `internal.` or
`https?://[0-9]` (bare IP URL forms). URL strings present in the diff (`/pkg/chirp.js`,
`/`, `/healthz`) are HTTP path components, not full URLs with host addresses.

**Evidence**: No matches returned. Zero IP addresses or internal service URLs appear in
any added line.

**Finding**: None.

---

### C. Credentials and secrets

**Status**: CLEAN

**What was checked**: Every added line was searched for the following patterns:
`api_key`, `api-key`, `token`, `secret`, `password`, `credential`, `Bearer`, `sk-`,
`-----BEGIN`, SSH key markers. The test code in `crates/ferric/src/ssr.rs` and
`crates/chirp-server/src/ssr.rs` was read in full; no test fixtures contain
real-looking credentials or opaque strings resembling tokens.

The word "secret" does not appear anywhere in the diff. The HTML document the SSR handler
produces (`assemble_document`) contains no embedded values beyond a trusted URL path
(`/pkg/chirp.js`) and static markup.

**Evidence**: No matches returned on any credential-pattern search. No test fixtures
raise concern.

**Finding**: None.

---

### D. Supply-chain risk (new dependencies)

**Status**: CLEAN

**What was checked**: The `Cargo.lock` diff and the `crates/chirp-server/Cargo.toml` diff.

**New dependency entry in `Cargo.toml`**:

```toml
ferric = { path = "../ferric" }
```

This is a **workspace-local path dependency**. The crate is a sibling member of the same
Cargo workspace (`crates/ferric/`), already present in the repository. No crates.io version
constraint, no git URL, no registry fetch. The `Cargo.lock` change is exactly one line —
`"ferric"` added to `chirp-server`'s `dependencies` list — confirming the workspace
resolver recorded this relationship.

No new external packages enter the dependency graph. The supply-chain surface is unchanged.

**Assessment of the dependency**:
- **Source**: Workspace-local (`path = "../ferric"`); not fetched from any external registry.
- **Risk**: Zero external supply-chain exposure. The code is committed in this same PR and
  reviewed elsewhere (SUBTASK_security_xss and other spokes).
- **Version constraint**: Not applicable — path dependencies carry no version range.

**Finding**: None.

---

## Verdict

**PASS**

All four areas are clean. No host paths, IP addresses, or credentials appear in any committed
file. The only dependency change is a workspace-local path dependency on a sibling crate, which
introduces zero external supply-chain exposure.
