# _BRIEF.md — NSWE overseer iteration I60 (persona swe-lead) — BOARD hygiene: place #114, groom, reconcile
**Depends on**: I59

You are the **NSWE project overseer** (`swe-lead`) for `Nousix-LLC/nswe-demo`, continuing the chain
(… → I58 → I59 → **I60**). You are an event loop, **NOT** a code writer — **P1 holds; board work is not code
and needs no DAG.** Boot the kernel + the NSWE app-files, publish `thread_evaluation`, then Act.

**This turn's filesets: `BOARD` + `DELIVERABLES_GIT`.** This is an **action**: make the board say what is
true and place the new directive. No DAG this turn (no fork). Writes are on GitHub/the project board only
(`gh`), never to code (P1).

## What to do (write for the repository's readers; no host/system details)
1. **Place directive #114 as the Ferric-1.0 epic.** #114 ("design and build Ferric to a 1.0 framework, with
   server-side rendering", `human-directive`) says *"plan these under the Ferric epic and fold in the router
   and HTTP/JSON-client issues already on the board."* Ensure #114 is a **board item** on the `NSWE Delivery`
   project (project id `PVT_kwDOEB9jls4BlZH4` — confirm it is this repo's board before writing) with a status,
   grouped under / linked to the existing Ferric epic **#1**. Its concrete child issues come from the design
   DAG (scheduled as I61), not from your own reading — do not hand-write a Ferric backlog here.
2. **Reconcile repo issues against the board** (`BOARD`, "the board says what is true"). There are ~86 open
   issues, all owner-authored. List the open issues, find any that exist in the repo but were never added to
   the `NSWE Delivery` project (bare repo issues with no status), and add them — each with the status that
   matches the live world and grouped under its epic. Epics (#1/#2/#3/#34/#43/#44/#52/#53/#56/#72/#77/#83/#89/
   #90) and their child issues are reconciled alike. Ensure **PR #113 is on the board beside its persistence
   issue(s) (epic #56: #64–#67), In review, linked** (closing keyword as plain text in the PR body).
3. **Groom the backlog into order** (`BOARD`, "the backlog and its order"): place the language-sweep issues
   #109/#110/#111 and the design gap-review chores #99–#108 (`review`/`type:chore`) in order; link
   dependencies; close nothing unless its premise is gone (note why). Do not split issues to shrink a DAG and
   do not cut an epic into per-issue DAGs.
4. **Record** the hygiene pass in STATE and leave the board saying what is true.

Note: #110 ("revise in-repo written content") is a content change to the repo and is therefore a later **DAG**
goal (not board work) — place/order it here; launching a DAG for it is a later board check's decision, slots
permitting. #109/#111 (issue/board text) are board work and can be done as grooming.

## Schedule the successor
`I61` depends_on `I60` — **launch the Ferric 1.0 + SSR design DAG** from directive #114 (`PRODUCT_DESIGN`,
`swe-designer`). Write its brief fresh.

## Carried state (read first)
- `taskflow/overseer/I57/project_state.json` — STATE (design record; request sources; the series plan).
- `taskflow/overseer/I57/CONTINUE.md` — the I57 board-check findings + series plan.

## Gotchas / scope
- Every issue the project tracks is a board item with a status; a bare repo issue off the board is invisible
  to management. An epic grouping children does not put the children on the board — each needs its own item.
- Do NOT Exit. Only `Nousix-LLC/nswe-demo`. Never force-push `main`; **no attribution trailers**.
  **Nothing on GitHub carries host/system details** — translate host facts to repository identities.
