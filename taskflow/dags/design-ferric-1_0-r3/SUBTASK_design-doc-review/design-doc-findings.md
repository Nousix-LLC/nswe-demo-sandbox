spoke: design-doc-review
concern_ids: [1, 2, 3]

# Merged findings from the design-doc-review subtree.
# Produced by SUBTASK_findings-synthesis.
#
# Identity assertions (all PASSED):
#   I-1: Each spoke's concern_ids names exactly its assigned concern.
#        completeness-review: [1], release-bar-quality: [2], traceability-review: [3].
#        No overlap; together they cover [1, 2, 3].
#   I-2: Every finding has severity, concern, location, statement, recommendation.
#        All 17 findings (DDR-C-001..003, DDR-B-001..011, DDR-T-001..003) have all required fields.
#   I-3: Merged output contains every finding from every spoke.
#        3 from completeness-review + 11 from release-bar-quality + 3 from traceability-review = 17.
#   I-4: summary.blocking_count equals count of severity==BLOCKING findings.
#        BLOCKING: DDR-B-001, DDR-B-002, DDR-B-003, DDR-B-004, DDR-B-005 = 5.
#        summary.blocking_count: 5.

findings:

  # ── Concern 1: Completeness against directive #114 ──────────────────────────
  # Source: SUBTASK_completeness-review/completeness-findings.yaml
  # 3 findings; 0 BLOCKING.

  - id: DDR-C-001
    severity: non-blocking
    concern: 1
    location: "docs-and-dx.md (REQ-DX-001..010 — no testing-guidance requirement); release-bar.md §5 (gap finding: testing story)"
    statement: >
      No REQ-DX-* or REQ-FW-* requires the 1.0 documentation to cover how app authors test
      Ferric components, routes, or async flows. REQ-FW-021 (component testing utilities) is
      explicitly deferred to post-1.0. The design provides no fallback: there is no requirement
      for a testing-guidance section in the guide or tutorial that tells authors what they can
      do at 1.0 with cargo test and wasm-bindgen-test, what requires manual DOM setup, and
      what framework-provided support arrives post-1.0. The release-bar.md §5 identifies this
      as a known gap and defers the decision to the release plan, but the release plan
      (release-plan.md) does not add a testing-guidance work item to Docs and DX (epic #134).
    recommendation: >
      Add an acceptance criterion to REQ-DX-001 (conceptual guide) or as a new REQ-DX-011
      that the 1.0 docs include a testing section covering: what app-author tests are practical
      at 1.0 using cargo test and wasm-bindgen-test, the manual setup required to mount a
      component in a test environment, and a pointer to the post-1.0 testing utilities that
      will remove that overhead. This closes the gap without requiring REQ-FW-021 to move
      into 1.0 scope.

  - id: DDR-C-002
    severity: non-blocking
    concern: 1
    location: "scope-and-requirements.md §REQ-FW-019 (post_one_oh deferral); docs-and-dx.md (REQ-DX-001, REQ-DX-009 — no accessibility posture requirement); release-bar.md §5 (gap finding: accessibility of framework output)"
    statement: >
      REQ-FW-019 (framework-level accessibility contract) is explicitly deferred to post-1.0.
      No DX requirement requires the 1.0 documentation to state what accessibility the framework
      provides or does not provide at 1.0. The only accessibility requirements in the design
      are REQ-RT-004 (Link component is keyboard-focusable and announced by AT) and REQ-RT-007
      (aria-current="page" on the active Link). For a 1.0 framework whose reference consumer
      (chirp) is a public-facing web app, this leaves authors without a posture statement:
      does the view! macro pass ARIA attributes through to the DOM? Does the framework generate
      semantic HTML for common elements? What are authors responsible for? The release-bar.md §5
      identifies this as a gap and defers the decision to the release plan, but the release plan
      does not add an accessibility-posture work item to Docs and DX (epic #134) or to
      Release and Distribution (epic #136).
    recommendation: >
      Add an acceptance criterion to REQ-DX-009 (accurate README/landing) or REQ-DX-001
      (conceptual guide) that the 1.0 docs include an accessibility posture statement covering:
      the view! macro passes standard HTML attributes including ARIA attributes to the DOM
      without filtering; app authors are responsible for writing accessible markup; the
      framework's only framework-level ARIA guarantee at 1.0 is the Link component
      (keyboard focus, aria-current). This documents the known 1.0 limitation without
      requiring REQ-FW-019 to move into 1.0 scope.

  - id: DDR-C-003
    severity: non-blocking
    concern: 1
    location: "docs-and-dx.md (REQ-DX-007, REQ-DX-009 — no browser-support requirement); scope-and-requirements.md §REQ-FW-003 (stable Rust + WASM toolchain, no browser version stated)"
    statement: >
      No requirement in any design document states which browser versions or WebAssembly
      baseline Ferric supports at 1.0. REQ-FW-003 requires stable Rust and the standard
      WASM toolchain. REQ-DX-007 requires build and toolchain documentation. Neither
      mandates a browser support statement. An author evaluating Ferric for a production
      project needs to know the minimum browser requirement — whether the framework relies
      only on the WebAssembly MVP (Baseline 2023, all modern browsers), or whether it uses
      later Web APIs (SIMD, threads, component model) that narrow the supported set.
      The BAR-FERRIC-022 README requirement names what the README must contain but does
      not list a browser support matrix.
    recommendation: >
      Add an acceptance criterion to REQ-DX-007 (build/toolchain docs) or REQ-DX-009
      (accurate README) that the 1.0 docs state Ferric's minimum browser requirement:
      specifically, whether the only dependency is the WebAssembly MVP (which covers all
      modern browsers since 2017), or whether any framework API relies on a later
      WebAssembly feature that narrows the supported set. If the answer is the MVP baseline,
      a one-sentence note in the README resolves the gap.

  # ── Concern 2: Release bar quality (BAR-FERRIC-* testability) ───────────────
  # Source: SUBTASK_release-bar-quality/release-bar-findings.yaml
  # 11 findings; 5 BLOCKING.

  - id: DDR-B-001
    severity: BLOCKING
    concern: 2
    location: "release-bar.md §BAR-FERRIC-001"
    statement: >
      The criterion requires that "An app written against the baseline `ferric` prelude compiles at 1.0
      without modification to any previously exported item," but the document defines no specific version,
      git tag, or commit that constitutes "the baseline." An outside reviewer cannot determine which
      pre-1.0 API surface to compile against to check backward compatibility.
    recommendation: >
      Anchor the baseline to a specific, named reference — for example a git tag such as
      `v0.1.0-usable_early` or the earliest published crates.io version — so a reviewer knows exactly
      which API surface the 1.0 release must remain compatible with. Alternatively, list the frozen
      prelude items explicitly in the compatibility policy (BAR-FERRIC-029), and cross-reference that
      list here.

  - id: DDR-B-002
    severity: BLOCKING
    concern: 2
    location: "release-bar.md §BAR-FERRIC-003"
    statement: >
      The criterion states "the produced HTML passes a standard HTML sanitizer without injected markup"
      but names no specific sanitizer (e.g. `ammonia`, DOMPurify, `sanitize-html`). The verification
      clause — "A test produces the HTML string for a representative component and checks its content
      without running a browser" — does not specify what the test checks for or how the sanitizer result
      is evaluated. An outside reviewer cannot determine which sanitizer to run, what its pass/fail
      threshold is, or whether the existing test satisfies the sanitizer claim.
    recommendation: >
      Name the specific sanitizer (e.g. the Rust `ammonia` crate) and the exact check — for example
      "output is unchanged after passing through `ammonia::clean`" or "output contains no `<script>`
      tags or `on*` event-attribute values." Add this as a named assertion in the automated test so the
      verification is directly observable.

  - id: DDR-B-003
    severity: BLOCKING
    concern: 2
    location: "release-bar.md §BAR-FERRIC-006"
    statement: >
      The criterion states "Ferric detects the mismatch and recovers without a silent fault" when
      client-rendered structure diverges from server HTML, but specifies no observable outcome for
      detection or recovery — no mention of a console warning, a panic, a logged error, a dev-mode-only
      diagnostic, or a re-render. An outside reviewer inducing a deliberate hydration mismatch has no
      basis for determining whether the framework "detected" it, and no way to distinguish a genuine
      detection from a silent failure.
    recommendation: >
      Specify the observable outcome: for example "in development builds, Ferric logs a warning to the
      browser console identifying the mismatched node; in production builds, the mismatch triggers a
      full client-side re-render of the affected subtree." The example_build verification should include
      a step that deliberately introduces a mismatch and names the expected observable result.

  - id: DDR-B-004
    severity: BLOCKING
    concern: 2
    location: "release-bar.md §BAR-FERRIC-015"
    statement: >
      The criterion requires "The `ferric-router` prelude surfaces present at the baseline are present
      at 1.0; no previously exported item is removed or redefined," but the document provides no version
      anchor for "the baseline." An outside reviewer cannot identify which pre-1.0 router API surface
      to check compatibility against.
    recommendation: >
      Same fix as DDR-B-001: anchor the baseline to a named git tag or the earliest published
      crates.io version for `ferric-router`, or enumerate the frozen router prelude items in the
      compatibility policy and cross-reference them here.

  - id: DDR-B-005
    severity: BLOCKING
    concern: 2
    location: "release-bar.md §BAR-FERRIC-017"
    statement: >
      The criterion requires "The `ferric-http` prelude surfaces present at the baseline are present at
      1.0 without removal or redefinition," but the document provides no version anchor for "the
      baseline." An outside reviewer cannot identify which pre-1.0 HTTP client API surface to check
      compatibility against.
    recommendation: >
      Same fix as DDR-B-001: anchor the baseline to a named git tag or the earliest published
      crates.io version for `ferric-http`, or enumerate the frozen HTTP prelude items in the
      compatibility policy and cross-reference them here.

  - id: DDR-B-006
    severity: non-blocking
    concern: 2
    location: "release-bar.md §BAR-FERRIC-008"
    statement: >
      The criterion requires each diagnostic to "name the problem in terms of the author's code rather
      than macro internals." trybuild tests capture and fix the exact error text, which helps, but the
      quality standard — what makes a message "in author terms" vs. "in macro internals" — is not
      defined. Two reviewers reading captured trybuild output could disagree on whether a given message
      meets the standard without a more concrete definition.
    recommendation: >
      Add a short definition or examples: for example "the error message names the specific attribute or
      element the author wrote, not an internal type or span within the macro expansion." If any
      trybuild expected-output file contains a message citing a framework-internal type name, revise the
      message and update the expectation file.

  - id: DDR-B-007
    severity: non-blocking
    concern: 2
    location: "release-bar.md §BAR-FERRIC-010"
    statement: >
      The criterion requires each component type error to "name the problem at the call site rather than
      inside framework internals." The same issue as DDR-B-006 applies: the quality standard is not
      defined, and trybuild tests are only as good as the expected output they capture.
    recommendation: >
      Same fix as DDR-B-006: add a concrete definition — e.g. "the error message cites the prop name
      and the component name as the author wrote them" — and audit the trybuild expected outputs against
      that definition.

  - id: DDR-B-008
    severity: non-blocking
    concern: 2
    location: "release-bar.md §BAR-FERRIC-019"
    statement: >
      The criterion requires a conceptual guide that explains Ferric's reactive model, component
      system, and data-loading pattern "in terms an author unfamiliar with the framework can read." The
      quality standard — what makes a guide sufficient for an unfamiliar author — is not defined. The
      tutorial half of the criterion is verifiable ("a reviewer can follow the tutorial steps exactly
      and reach the stated end state"), but the guide quality is aspirational without a threshold.
    recommendation: >
      Add a concrete minimum bar for the guide — for example "an author with no prior exposure to
      Ferric can, after reading the guide, correctly predict the render output of a component with a
      signal and a memo without looking at framework source." Alternatively, separate the verifiable
      structural claim (the guide covers these three topics) from the quality aspiration and move the
      latter to a non-bar note.

  - id: DDR-B-009
    severity: non-blocking
    concern: 2
    location: "release-bar.md §BAR-FERRIC-021"
    statement: >
      The criterion requires the new-user path to be completable "without reverse-engineering toolchain
      details." The boundary between documented expected toolchain knowledge (e.g. `rustup` is
      installed) and knowledge that requires reverse-engineering (e.g. resolving an undocumented linker
      flag) is not defined. Different reviewers would draw this line differently based on their
      background.
    recommendation: >
      State the assumed prior knowledge explicitly — for example "the user has `rustup` and the stable
      Rust toolchain installed; no other setup is assumed" — and list each additional toolchain step the
      documented path requires (e.g. adding `wasm32-unknown-unknown`, installing `wasm-pack` or
      `cargo-generate`). The criterion passes if every required step is documented; it fails if any
      required step is absent from the docs.

  - id: DDR-B-010
    severity: non-blocking
    concern: 2
    location: "release-bar.md §BAR-FERRIC-027"
    statement: >
      The criterion states "No heavy general-purpose runtime is introduced" but does not define
      "heavy." An outside reviewer cannot make a binary pass/fail determination without a size or
      category threshold. In the WASM context, including a full server-side async runtime would
      obviously fail; a reviewer evaluating a borderline dependency (e.g. a feature-flagged pull of
      `futures`) has no defined rule to apply.
    recommendation: >
      Replace the phrase with a specific constraint, such as "no dependency adds more than N KB to the
      optimized WASM bundle relative to the baseline footprint" or "the dependency set consists solely
      of: `wasm-bindgen`, `web-sys`, `js-sys`, `serde`, `wasm-bindgen-futures`, and any crate listed
      and justified in the footprint document." The benchmark numbers document the actual footprint;
      this criterion should state the rule for what fails it.

  - id: DDR-B-011
    severity: non-blocking
    concern: 2
    location: "release-bar.md §BAR-FERRIC-029"
    statement: >
      The criterion requires a written compatibility policy "discoverable from the repository root" but
      does not define what "discoverable" means — a link in the README, a named file at the root, a
      section in CONTRIBUTING.md, or simply any file in the repo. A reviewer looking for this policy
      could disagree with another reviewer on whether it is "discoverable" if it is buried in a
      subfolder or linked only from an intermediate document.
    recommendation: >
      Name the specific location: for example "a `COMPATIBILITY.md` file at the repository root" or "a
      `## Compatibility Policy` section in the README." If it will live in a subfolder (e.g.
      `docs/compatibility.md`), require that the README link to it by name.

  # ── Concern 3: Internal coherence and traceability ──────────────────────────
  # Source: SUBTASK_traceability-review/traceability-findings.yaml
  # 3 findings; 0 BLOCKING.

  - id: DDR-T-001
    severity: non-blocking
    concern: 3
    location: >-
      design/ferric/contracts/design_artifact_map.yaml (file header vs. hub document descriptions);
      taskflow/dags/design-ferric-1_0-r3/SUBTASK_design-doc-review/_GLOBAL.md (Design document
      inventory table, row "contracts/design_artifact_map.yaml")
    statement: >-
      The hub documents describe design_artifact_map.yaml as "Maps REQ-* to design artifacts and
      issues." The actual file maps design document filenames to their owning subtasks and repository
      paths; its own header says "where each owned design doc lands in the repository." No REQ-* IDs
      appear anywhere in the file. The stated cross-reference function — looking up which design
      artifact or issue corresponds to a given REQ-* ID — cannot be performed using the artifact map.

      As a result, the first audit check from the traceability review brief ("Does every REQ-* ID
      declared in scope-and-requirements.md appear in the artifact map?") returns no matches for any
      of the 21 REQ-FW-* IDs, not because of a coverage gap but because the map does not have REQ-*
      entries. The traceability chain (REQ-* → BAR-FERRIC-* → issues) is intact through direct
      citations in issues #137–#164; this mislabeling does not break that chain.
    recommendation: >-
      Either (a) update the hub document descriptions to accurately reflect that
      design_artifact_map.yaml is a document-placement map, not a REQ-* cross-reference — changing
      "Maps REQ-* to design artifacts and issues" to "Maps design document filenames to their owning
      subtasks and repository paths" — or (b) add a separate contract file (e.g.,
      contracts/req_to_bar_map.yaml) that records each REQ-* ID, the BAR-FERRIC-* criterion it
      is enforced by, and the issue number that implements it, so the cross-reference function the hub
      documents describe actually exists in the system.

  - id: DDR-T-002
    severity: non-blocking
    concern: 3
    location: >-
      Issues #129–#136 (all 8 epic issues), "**BAR-FERRIC covered:**" field in each body
    statement: >-
      All 8 epic issues (#129–#136) use the abbreviated ID format "BAR-NNN" (e.g., "BAR-001,
      BAR-002") in their "BAR-FERRIC covered" field. The id_and_traceability_schema.yaml defines
      the canonical pattern as "BAR-FERRIC-<NNN>" (e.g., "BAR-FERRIC-001"). The 28 feature issues
      (#137–#164) all use the canonical format correctly. A reviewer searching for "BAR-FERRIC-001"
      in the issue register finds it in #137 (feature) but not in #129 (the owning epic), because
      #129 uses "BAR-001." The numeric cross-reference is still intelligible, but the format
      divergence makes the issue register non-conformant with the id_schema pattern and would
      cause a substring search for "BAR-FERRIC" to miss the epic bodies.
    recommendation: >-
      Update the "BAR-FERRIC covered" field in all 8 epic issues to use the canonical
      "BAR-FERRIC-NNN" format. Specifically: #129 uses BAR-001 through BAR-011 (where referenced),
      #130 uses BAR-012–014, #131 uses BAR-015–016, #132 uses BAR-017–018, #133 uses BAR-003–006,
      #134 uses BAR-019–022, #135 uses BAR-026–028, #136 uses BAR-023–025 and BAR-029. Replace
      each with the "BAR-FERRIC-NNN" form. This is a batch edit with no design change.

  - id: DDR-T-003
    severity: non-blocking
    concern: 3
    location: >-
      Issues #129, #131, #132, #133, #134, #135, #136 (7 of 8 epic issues); id_and_traceability_schema.yaml §epic.fields
    statement: >-
      Seven of the eight epic issues do not directly cite any REQ-* IDs in their bodies. They
      reference design area files (e.g., "design/ferric/authoring-model.md") and BAR-FERRIC-*
      criteria, but not specific requirement IDs. Issue #130 is the exception: it cites
      REQ-ASYNC-012 and REQ-ASYNC-013 in a note. The id_and_traceability_schema.yaml does not
      require direct REQ-* citations in epics — it requires "design_refs" (design-doc area references)
      for epics and REQ-*/BAR-FERRIC-* citations for work items. The epics are therefore
      schema-compliant. However, the traceability audit question ("Does every epic and feature issue
      trace to at least one REQ-* ID?") cannot be answered "yes" for 7 epics without following the
      indirect chain: epic → BAR-FERRIC-* → feature issue → REQ-*. A reviewer performing a direct
      traceability check on epic bodies would find no REQ-* and incorrectly conclude a gap exists.
    recommendation: >-
      Consider adding a "Key requirements:" field to each epic body that lists the primary REQ-*
      IDs from the cited design area — one or two representative IDs per epic is sufficient to
      establish direct traceability without duplicating the full feature-issue listings. Alternatively,
      update the id_and_traceability_schema.yaml to clarify that REQ-* traceability for epics is
      indirect (via BAR-FERRIC-* and the feature issues under the epic) and that this is by design,
      so future reviewers understand the intended structure.

summary:
  blocking_count: 5
  non_blocking_count: 12
  notes: >
    Merges all findings from three spokes: SUBTASK_completeness-review (concern 1, 3 findings,
    0 BLOCKING), SUBTASK_release-bar-quality (concern 2, 11 findings, 5 BLOCKING), and
    SUBTASK_traceability-review (concern 3, 3 findings, 0 BLOCKING).
    Total: 17 findings; 5 BLOCKING (all in concern 2, all on release-bar testability); 12 non-blocking.

    The 5 BLOCKING findings share two root causes: three (DDR-B-001, DDR-B-004, DDR-B-005) have no
    version anchor for the "baseline" API surface in the backward-compatibility criteria;
    one (DDR-B-002) names no specific sanitizer and leaves its verification test unspecified;
    one (DDR-B-003) omits the observable outcome for hydration mismatch detection.

    Concern 1 (completeness): all directive #114 must-haves are covered. The three non-blocking gaps
    are documentation omissions — testing guidance, accessibility posture, and browser support
    statement — each resolvable by adding acceptance criteria to existing requirements.

    Concern 3 (traceability): the primary REQ-* → BAR-FERRIC-* → issue chain is intact for all
    release-gating REQ-FW-001..014. The three non-blocking findings are labeling and format
    inconsistencies with no effect on what gets built.
