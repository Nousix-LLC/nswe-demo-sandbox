# SUBTASK_synthesis

## Objective
Assemble the completed feature branch into a pull request against `main` on `Nousix-LLC/ferric`,
verify all wiring, and close issues #130, #143, #144, #145. This is the synthesis gate: it runs
only after all three feature spokes complete.

## Inputs
- Repository: `Nousix-LLC/ferric`, branch `work/ferric-async-forms-r1`
- COMPLETE.md from SUBTASK_walking_skeleton — contains actual GitHub issue numbers assigned
- COMPLETE.md from SUBTASK_async_resource — confirms async_resource.rs implementation is done
- COMPLETE.md from SUBTASK_dom_events — confirms dom.rs event binding is done
- COMPLETE.md from SUBTASK_form_binding — confirms form.rs form binding is done
- Hub context: `../_GLOBAL.md`
- Contracts: `../contracts/module_interfaces.md` and `../contracts/event_kind_contract.md`

## Declared Outputs
1. Pull request on `Nousix-LLC/ferric` base `main` ← `work/ferric-async-forms-r1`:
   - Title: "feat: async resources, full DOM events, and two-way form binding (Ferric 1.0 #130)"
   - Body includes: summary of three features, test plan, closes #130 #143 #144 #145
2. All three features verified present on the branch before PR creation:
   - `async_resource.rs` exports `ResourceState`, `Resource`, `suspense`
   - `dom.rs` handles all EventKind variants exhaustively
   - `form.rs` exports `FormField<T>` and `Bind<T>`
   - `lib.rs` re-exports the new types in its prelude
3. `cargo check --target wasm32-unknown-unknown` confirmed passing on the branch
4. SYNTHESIS.md authored at `../SYNTHESIS.md` (the observation seam) recording: PR URL, issue numbers closed, final branch commit SHA
5. Issues #130, #143, #144, #145 marked as closed via the PR (the "closes #N" lines in the PR body handle this on merge)

## Success Criteria
- PR exists, is open, targets `main`, and body contains "Closes #N" for all four issue numbers
- PR description is complete: feature summary, what each module adds, test plan checklist
- `cargo check --target wasm32-unknown-unknown` passes on the branch at PR creation time
- SYNTHESIS.md is authored with PR URL, issue numbers, and final commit SHA
- No secrets, tokens, or credentials in any committed file or PR body

## Constraints
- Do not merge the PR — merging is the owner's decision.
- Do not publish to crates.io — that is the owner's decision.
- Do not force-push to main.
- Do not touch namespaces or infrastructure outside the ferric repository.
- If `lib.rs` does not yet re-export the new types in the prelude, add those re-exports as a
  final commit on the branch before creating the PR (this is a minor additive change to `lib.rs`
  that synthesis owns as a gate task).
- Security: never commit credentials or tokens; the repo is public.
- End the PR description with:
  🤖 Generated with [Claude Code](https://claude.com/claude-code)
