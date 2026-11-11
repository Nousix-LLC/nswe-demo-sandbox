# SYNTHESIS — SUBTASK_code-quality

## Verdict

gate: FAIL
round: 1

---

## Checks

| Check | Result | Mechanical evidence | Notes |
|---|---|---|---|
| coverage | pass | Both spoke files present; each contains all five required dimensions | app-rs-notes.md: 5/5. hydrate-wasm-notes.md: 5/5. |
| format conformance | pass | Severity label + evidence citation present in all ten findings | Minor: test structure evidence cites function name rather than line number; file is named. Insufficient to block. |
| verdict consistency | fail | Blocker finding present in hydrate-wasm-notes.md → overall verdict must be FAIL | hydrate_wasm.rs:62, 113, 174 (hardcoded strings without SSR sentinels). code-quality.md correctly records FAIL. |
| prose quality | pass | No AI-tell patterns found in either spoke file or in the assembled code-quality.md | Both spoke files are factual, evidence-cited, plain voice. |

---

## Findings

- [F1] severity=block check=verdict-consistency
       location=`crates/ferric/tests/hydrate_wasm.rs:62, 113, 174`
       statement=All three tests inject HTML without TEXT_OPEN_MARKER/TEXT_CLOSE_MARKER sentinels; sentinel-handling code paths in hydrate.rs are never exercised; adopt-walk coverage is false against production SSR output.
       mechanical=LLM-judged (spoke reviewer read hydrate.rs and ssr.rs; sentinel constants verified absent from import block)

---

## Coverage assertion

Coverage assertion is NOT present on a FAIL verdict. The gate found a block-severity finding; the finding is recorded above. The assembled `code-quality.md` carries the FAIL verdict and states the specific finding and remediation requirement.

**What was checked:**
- ownership coverage: each artifact produced by its declared owner ✓ (app-rs-notes.md by SUBTASK_app-rs-quality; hydrate-wasm-notes.md by SUBTASK_hydrate-wasm-quality; code-quality.md by this task)
- coverage: all five quality dimensions present in each spoke file ✓
- format identities: severity label + evidence citation in each finding ✓ (minor deviation noted, not blocking)
- verdict consistency: Blocker finding present → FAIL verdict required and recorded ✗ (this is the failing identity — not a contract violation by the synthesis task; it reflects the actual state of the code under review)
- prose quality: plain voice, no AI-tell patterns ✓

The failing identity (verdict-consistency) records a code quality problem in the reviewed commits, not a decomposition or synthesis defect. The gate result is correct: the spoke found a blocker; the synthesis records it as FAIL; no silent plug was inserted.
