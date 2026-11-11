# format_review_partial.md

## Concerns Covered

- Concern 1 (structural coherence): section hierarchy, version-entry format, ordering, and separator consistency across the new CHANGELOG; comparison against the established `ferric-router/CHANGELOG.md` pattern
- Concern 4 (formatting consistency): code-fence style, inline code, em-dash usage, type-header pattern, and doc-comment coverage within the new file

---

## Summary

PR #210 introduces a single new file, `crates/ferric-http/CHANGELOG.md` (160 lines). No existing CHANGELOG.md exists at the repo root; the only pre-existing reference is `crates/ferric-router/CHANGELOG.md`. Structural coherence was assessed against that file's established conventions and against standard CHANGELOG layout principles. Formatting consistency was assessed internally (within the new file) and against `ferric-router`. The file is structurally sound: heading levels are correct and consistent, sections are ordered in reverse-chronological order, horizontal-rule separators are applied uniformly, and the preamble matches the repo's established boilerplate exactly. No blockers or SHOULD_FIX items were found. Four ADVISORYs are recorded: two about structural choices that diverge from the `ferric-router` pattern (H3 subsection naming and cross-entry depth asymmetry), and two about minor formatting inconsistencies within the code blocks (uneven doc-comment coverage and a stray C-style comment).

---

## Findings

**[CLEAN] Version-section heading level**: Both `## Unreleased — usable_early surface (#148)` and `## Initial implementation (#6)` use H2, the correct level for CHANGELOG version entries.
- Principle: Version sections at H2, subsections at H3+, is the conventional CHANGELOG hierarchy.
- Evidence: Lines 9 and 152 of the diff both open with `## `.
- Resolution: N/A — sound.

**[CLEAN] Reverse-chronological ordering**: Unreleased appears before the initial implementation entry.
- Principle: CHANGELOG convention places newer entries above older ones.
- Evidence: `## Unreleased` (line 9) precedes `## Initial implementation (#6)` (line 152 in the diff).
- Resolution: N/A — sound.

**[CLEAN] Section separators**: `---` horizontal rules are used as delimiters before each H2 section and in the preamble.
- Principle: Consistent visual separation between entries improves scannability.
- Evidence: `---` appears after the preamble (line 8) and before the second version section (line 151); no separator appears mid-section.
- Resolution: N/A — sound.

**[CLEAN] Preamble boilerplate**: First three lines match `ferric-router/CHANGELOG.md` word-for-word (`# Changelog — <crate>`, `All notable changes to \`<crate>\` are documented here.`, `Versioning follows the workspace \`version.workspace = true\` setting.`).
- Principle: Repo-wide consistency in CHANGELOG boilerplate reduces cognitive overhead.
- Evidence: Diff lines 1–5 reproduce the established ferric-router preamble with only the crate name changed.
- Resolution: N/A — sound.

**[CLEAN] Code-fence language tag**: All code blocks throughout the file use `` ```rust ``.
- Principle: Consistent language tags enable syntax highlighting and signal the code's nature.
- Evidence: `` ```rust `` opens each of the six type-signature blocks (Client, ClientBuilder, RequestBuilder, Response, Error, Method) in the Unreleased section.
- Resolution: N/A — sound.

**[CLEAN] Inline backtick usage**: Type names, method names, and file paths are wrapped in inline backticks throughout both sections.
- Principle: Consistent inline-code formatting distinguishes identifiers from prose.
- Evidence: Consistently applied — `` `Client` ``, `` `RequestBuilder::json()` ``, `` `src/error.rs` ``, etc. in both sections.
- Resolution: N/A — sound.

**[CLEAN] Type-header pattern**: Each named type in the Unreleased section uses the same `**\`TypeName\`** — description.` structure for its header line.
- Principle: Uniform item-header format allows readers to scan the API surface quickly.
- Evidence: All six type headers (`Client`, `ClientBuilder`, `RequestBuilder`, `Response`, `Error`, `Method`) follow the pattern. The `Result<T>` type alias uses a slightly different form (the full definition is in the backtick span rather than a name + description), but that is structurally appropriate because it is not a named type.
- Resolution: N/A — sound.

**[CLEAN] Struct-body placeholder**: All `struct` declarations use `{ ... }` uniformly.
- Principle: Consistent placeholder style keeps code blocks readable.
- Evidence: `pub struct Client { ... }`, `pub struct ClientBuilder { ... }`, `pub struct RequestBuilder { ... }`, `pub struct Response { ... }` — all four structs use the same form.
- Resolution: N/A — sound.

---

**[ADVISORY] H3 subsection naming diverges from ferric-router pattern**: The Unreleased section opens with `### Verification: all usable_early acceptance criteria met`, not a keepachangelog-style `### Added` / `### Changed` subsection.
- Principle: `ferric-router/CHANGELOG.md` establishes `### Added` (and similar keepachangelog categories) as the repo convention for CHANGELOG subsections.
- Evidence: `ferric-router` lines such as `### Added` → `#### \`navigate_replace(path: &str)\`...`; `ferric-http` uses `### Verification: all usable_early acceptance criteria met` → `#### Public API surface (frozen at usable_early)`.
- Resolution: The deviation is content-appropriate — this entry records a scope-closure and verification record, not an incremental feature list — but it establishes a divergent pattern for a second crate. Consider either noting this as an intentional exception in the CHANGELOG preamble or aligning the H3 to `### Added` with the API surface list nested under it and the acceptance-criteria table as a separate `### Verified` or prose subsection. No action required if the team accepts per-crate structural latitude.

**[ADVISORY] Structural asymmetry between the two version sections**: The Unreleased section carries H3 and H4 subsections with tables and code blocks; the Initial implementation section is flat (prose + bullet list, no sub-headings).
- Principle: Parallel structure between version entries makes navigation predictable.
- Evidence: `## Unreleased` contains `###` and `####` headers; `## Initial implementation (#6)` has none — it goes directly from the H2 heading to prose and bullets.
- Resolution: The asymmetry is proportionate to the content — the initial implementation entry is a brief inventory, the unreleased entry is a detailed surface declaration — so this is cosmetic rather than structural. No change required, but worth flagging in case a reviewer expects a `### Added` heading in the initial section.

**[ADVISORY] Uneven doc-comment coverage in code blocks**: `RequestBuilder` and `Method` include `///` doc comments on individual methods; `Client`, `ClientBuilder`, `Response`, and `Error` carry no inline comments.
- Principle: For a frozen public API declaration the documentation depth should be uniform across type blocks so readers can rely on the same level of inline annotation.
- Evidence: `RequestBuilder` block has `/// Append query-string parameters...` and three other `///` comments. `Method` has `/// The uppercase HTTP token...` on `as_str()`. All other type blocks (Client: 8 methods, ClientBuilder: 3 methods, Response: 10 methods, Error: 3 methods, 5 enum variants) carry no inline comments.
- Resolution: Either add brief `///` comments to the methods in the other type blocks, or remove the `///` comments from `RequestBuilder` and `Method` and document the non-obvious behavior in prose below each code block. Either direction removes the inconsistency.

**[ADVISORY] C-style comment in `Method` block**: `impl std::fmt::Display for Method { /* delegates to as_str() */ }` uses a C-style block comment while the rest of the code blocks that carry comments use `///`.
- Principle: Consistent comment syntax within code blocks is a minor but visible formatting inconsistency.
- Evidence: `Method` block, last line: `impl std::fmt::Display for Method { /* delegates to as_str() */ }`.
- Resolution: Replace with `// delegates to as_str()` (line comment) or a `///` doc comment on the impl block, consistent with the doc-comment style used elsewhere.
