# Completion Record — SUBTASK_spec-deviation

## Task

Verify client-server type consistency for the `before` pagination cursor and assess whether the
documented deviation from the external spec (ISO 8601 vs milliseconds) is a blocker.
Pinned commit: `decb6196c2c1e6ed421d393a642f0c844cc333ba`.

## Work Done

Read `crates/chirp-types/src/api.rs` lines 142–159 and `crates/chirp-frontend/src/api.rs` lines
214–260 at the pinned commit. Traced callers of `public_timeline` and `public_user_profile` across
`crates/chirp-frontend/src/landing.rs` and `crates/chirp-frontend/src/public_profile.rs`.

## Result

The runtime type contract is consistent: both callers extract `i64` millisecond timestamps from
response items and convert with `.to_string()`, producing decimal integer strings that the server
parses as `i64` without error. No live type mismatch exists and the spec deviation itself is not a
blocker.

One non-blocking finding: the `public_timeline` doc comment at `crates/chirp-frontend/src/api.rs`
line 217 claims "ISO 8601 cursor" for the `before` parameter, which contradicts the actual wire
format and would cause a 422 for any future caller following the doc. The same wrong claim appears
in module-level docs in `landing.rs:19` and `public_profile.rs:15`.

## Output

- `FINDINGS.md` — concern 4 findings per `../../contracts/findings_schema.md`
