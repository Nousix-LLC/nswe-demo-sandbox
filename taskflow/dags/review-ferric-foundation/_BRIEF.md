# _BRIEF.md — Code review DAG: ferric-foundation / PR #14 (issue #4)

You are a **swe-coder** code-writing **DAG** node. The NSWE project overseer (`swe-lead`) forked you to perform the **code review** of an already-opened PR — the human-requested "code review is a DAG" step of the work-item turn. Boot the kernel first (your standing contract), run the atomic-vs-decompose evaluation on THIS brief (a focused review of a ~3k-line additive diff is almost certainly **Atomic** — do not over-decompose), do the review, post it to GitHub, write your `SYNTHESIS.md` review verdict, and stop on your one terminal `report_status`.

## What you are reviewing
- Repo: `Nousix-LLC/nswe-demo` (GitHub; `gh` authenticated on this host; `git`, `cargo`, `rustup` available).
- **PR #14** — `ferric-foundation: workspace + ferric core`, base `main` ← head `work/ferric-foundation`, `Closes #4`. URL: https://github.com/Nousix-LLC/nswe-demo/pull/14
- The machine gate already **PASSED** (the code-writing DAG's own `SYNTHESIS.md` at `/home/user/nousix-runtime/nswe-demo/taskflow/dags/ferric-foundation/SYNTHESIS.md`: workspace+wasm build OK, 36 unit + 6 doctests OK, fmt/clippy clean). Your job is the **human-review-equivalent judgment layer** on top of that machine verdict — not to re-run the build (read the machine verdict for build/test facts).

## Your task
1. **Get the diff.** Clone into your own workspace (e.g. `gh repo clone Nousix-LLC/nswe-demo checkout` under `/home/user/nousix-runtime/nswe-demo/taskflow/dags/review-ferric-foundation/`), check out `work/ferric-foundation`, and read the per-file diff vs `main` (`git diff main...work/ferric-foundation`). Do NOT reuse another process's clone. Do NOT modify any source — you review, you do not edit (a reviewer DAG writes a verdict + PR review, not code).
2. **Review against the acceptance criteria of issue #4** (the bar that was set): (1) virtual workspace + `crates/ferric`; (2) sound reactive signals with computed + batching, no stale-subscriber leaks; (3) component model + `mount`; (4) DOM rendering via wasm-bindgen/web-sys with keyed diff + click/input events; (5) wasm build + counter example; (6) native tests (wasm-bindgen-test optional if no headless browser); (7) fmt/clippy clean, rustdoc, README.
3. **Review against the methodologies** your brief names (load on-demand): `code-review` (the review discipline + finding severities), `rust` (ownership/borrowing soundness of the signal graph, trait design, `RefCell`/`Rc` discipline, no panics across signal reads), `core` (coding standards, error handling). Focus a principal-level read on: reactive-core soundness (stale subscriber leaks, borrow held across a signal read, batching correctness), the keyed-diff/patch correctness, the public API surface ergonomics/stability (it is a long-lived surface a Twitter-style SPA must be buildable on later), and any unsafe/panic/`unwrap` hazards.
4. **Post the review to GitHub.** `gh pr review 14 -R Nousix-LLC/nswe-demo` with either `--approve` (no block/major findings) or `--request-changes` (one or more block/major findings), and a review body that lists your findings with file:line and severity. Inline comments are welcome but the summary body is required. Be specific and fair; minor/nit findings do not block.
5. **Write `SYNTHESIS.md`** (your terminal fold/verdict record) in your workspace with a prominent **review verdict: APPROVE | REQUEST-CHANGES**, the findings table (severity x location x statement), which acceptance criteria are met/unmet, which methodologies you applied, and the `gh pr review` URL/outcome. Make the verdict the first line so the overseer can gate without re-reading the diff.

## Decision rule (what the overseer will read)
- **APPROVE** => no block- or major-severity findings; acceptance criteria substantively met; the machine gate is green. The overseer will then LAND (merge PR #14 squash into `main`, closing #4).
- **REQUEST-CHANGES** => at least one block/major finding, or an unmet acceptance criterion. The overseer will REMEDIATE (fork a fresh code-writing DAG carrying your findings) — it will NOT merge.
Report honestly: an approve that waves through a real defect is worse than a request-changes with evidence.

## Methodology bundles (named by the overseer; load on-demand)
`code-review` (primary), `rust`, `core`. You are the final judge of what you load.

## Terminal
Follow the kernel: author `SYNTHESIS.md` (your review verdict) + `COMPLETE.md` (atomic), then one terminal `report_status`. Make the **APPROVE/REQUEST-CHANGES verdict** and the **`gh pr review` outcome** prominent so the overseer can gate without re-reviewing.
