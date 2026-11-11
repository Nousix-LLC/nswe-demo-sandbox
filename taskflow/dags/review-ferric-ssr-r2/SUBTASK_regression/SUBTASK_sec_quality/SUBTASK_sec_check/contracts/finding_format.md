# Per-Concern Finding Format

Each spoke task MUST produce a file containing exactly one subsection conforming to this format. The subsection is pasted verbatim by SUBTASK_synthesis under the `## Security Findings` header.

---

## Required Format

```markdown
### <Concern Name>

**Result**: Clean | Finding
**Evidence**: `<filename>:L<start>-L<end>` at commit `75c1eef` — <what specifically was read and checked>
**Finding** *(only when Result is Finding)*:
- **Severity**: Blocker | Non-blocker | Note
- **Description**: <concrete description of the security issue>
- **Resolution**: <what would satisfy a reviewer blocking on this>
```

---

## Required Concern Names (verbatim — must match exactly)

- `HTML Injection in ssr.rs`
- `DOM Spoofing in app.rs`
- `Test Injection Safety in hydrate_wasm.rs`

---

## Field Rules

- **Result**: exactly `Clean` or `Finding` — no other values
- **Evidence**: MUST cite specific file and line number(s) at commit `75c1eef`; a range (e.g. `ssr.rs:L12-L45`) is acceptable; multiple ranges acceptable when multiple relevant locations exist
- **Finding**: MUST be omitted entirely when Result is Clean — do not write "N/A", "none", or leave it blank
- **Threat-model reasoning**: for DOM Spoofing, the Evidence field or Finding field MUST address whether the attack is realistic for a Rust WASM library crate distributed as a dependency (not a served page controlled by an attacker)
