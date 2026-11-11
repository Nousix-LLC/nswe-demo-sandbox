# Remediation Synthesis — design-ferric-1_0-r1

**Verdict: APPROVE**

All 5 BLOCKING findings from the design-ferric-1_0-r3 review (Concern 2: release bar testability)
have been remediated in `design/ferric/release-bar.md` on branch `work/design-ferric-1_0`.

Commit: `ade5bdd` — "design(ferric): remediate 5 blocking release-bar testability findings"

---

## Per-criterion remediation record

### BAR-FERRIC-001 — Backward compatibility (ferric core) ✓ RESOLVED

**Finding:** "The baseline prelude" named no specific version, git tag, or commit. An outside
reviewer could not identify which API surface to compile against.

**Fix applied:**
> "An app written against the **`ferric` prelude at the `v0.1.0-usable_early` git tag** compiles
> at 1.0 without modification to **any item exported at that tag**."

The baseline is now the named `v0.1.0-usable_early` milestone tag (the first publish in the
`usable_early` stage). A reviewer can `git checkout v0.1.0-usable_early`, compile their app
against that surface, then recompile against 1.0 to verify no previously exported item is gone.

---

### BAR-FERRIC-003 — HTML sanitization ✓ RESOLVED

**Finding:** "A standard HTML sanitizer" named no specific sanitizer and stated no assertion.
A reviewer could not determine which sanitizer to run or what pass/fail means.

**Fix applied:**
> "the produced HTML is unchanged by the **`ammonia` HTML sanitizer** — specifically,
> **`assert_eq!(html, ammonia::clean(&html))`** holds for the rendered test component."

The sanitizer is now named (`ammonia` crate) and the exact assertion is stated. The automated
test must include `assert_eq!(html, ammonia::clean(&html))`; a reviewer can read the test and
confirm that assertion is present and passes in CI.

---

### BAR-FERRIC-006 — Hydration mismatch detection ✓ RESOLVED

**Finding:** "Detects the mismatch and recovers without a silent fault" specified no observable
outcome. A reviewer inducing a deliberate mismatch could not tell whether detection occurred.

**Fix applied:**
> "in **development builds**, Ferric emits a **`console.warn` message to the browser console
> identifying the mismatched node**; in **production builds**, Ferric performs a **full
> client-side re-render of the affected subtree**."

The observable outcome is now stated for both build configurations. A reviewer can induce a
deliberate mismatch in a dev build and observe the named `console.warn` output; in a production
build they can observe the subtree re-render in lieu of a partial update.

---

### BAR-FERRIC-015 — Backward compatibility (ferric-router) ✓ RESOLVED

**Finding:** "The baseline router prelude" named no version anchor. Same issue as BAR-FERRIC-001.

**Fix applied:**
> "The `ferric-router` prelude surfaces present at the **`v0.1.0-usable_early` git tag** are
> present at 1.0; no **item exported at that tag** is removed or redefined."

The fix is parallel to BAR-FERRIC-001. The anchor is the `v0.1.0-usable_early` tag applied
consistently across all three crate compatibility criteria.

---

### BAR-FERRIC-017 — Backward compatibility (ferric-http) ✓ RESOLVED

**Finding:** "The baseline HTTP client prelude" named no version anchor. Same issue as
BAR-FERRIC-001.

**Fix applied:**
> "The `ferric-http` prelude surfaces present at the **`v0.1.0-usable_early` git tag** are
> present at 1.0 without removal or redefinition."

Same anchor as BAR-FERRIC-001 and BAR-FERRIC-015, applied to `ferric-http`.

---

## Scope confirmation

**In scope (all addressed):** The 5 BLOCKING findings in Concern 2 (release bar testability).

**Out of scope (unchanged):** Non-blocking findings #165–#179, which are on the board as Todo
per the design-ferric-1_0-r3 review. No documents other than `design/ferric/release-bar.md`
were modified; no structural design changes were made.

---

## Change summary

| BAR criterion | Finding type | Anchor/assertion added |
|---|---|---|
| BAR-FERRIC-001 | No version anchor | `v0.1.0-usable_early` git tag |
| BAR-FERRIC-003 | No sanitizer named, no assertion | `ammonia::clean` + `assert_eq!` |
| BAR-FERRIC-006 | No observable mismatch outcome | `console.warn` (dev), re-render (prod) |
| BAR-FERRIC-015 | No version anchor | `v0.1.0-usable_early` git tag |
| BAR-FERRIC-017 | No version anchor | `v0.1.0-usable_early` git tag |

All five changes are targeted text substitutions within the blocking statements only. No
`BAR-FERRIC-*` ids, references, verification methods, or stages were altered.
