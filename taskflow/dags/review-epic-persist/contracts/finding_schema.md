# Finding Schema (contract — READ-ONLY)

Every concern spoke in this review DAG emits exactly one `outputs/findings.md` with the structure below. The
synthesis gate reads all seven and folds them into one verdict. Do not invent a different shape; compose
against this one. All locations pin to commit **`09fa453c3c40e39a9b4647e0de6e00dcf50ecb21`** on PR
`Nousix-LLC/nswe-demo#113`.

## `findings.md` document structure

```markdown
# Findings — <concern name> — PR #113 @ 09fa453

## What I checked
- <enumerated list of what this concern examined: files, criteria, behaviors, manifests, CI jobs, cluster
  state — specific enough that a reader knows the surface covered>

## What I found clean
- <specific things examined and judged sound — a well-chosen boundary, a real edge case covered, an
  assertion that would actually fail if the behavior broke. "No findings" means something only next to this.>

## Findings
<zero or more findings, each in the per-finding block below; if none, say so explicitly>

## Concern sub-verdict
- one of: CLEAN | NON-BLOCKING-ONLY | HAS-BLOCKERS
- one-line justification tied to the concern's bar
```

## Per-finding block

```markdown
### <FINDING-ID>  — <short title>
- **severity**: blocker | major | minor | nit
- **blocks_landing**: true | false     # true iff severity == blocker
- **location**: `path/relative/to/repo/file.rs:L120-L138` @ 09fa453   # or: "whole-PR" / "design-level" + why
- **acceptance-criterion / design ref**: #65 | #66 | #67 | #64 | BAR-xxx | durable-persistence requirement | n/a
- **principle**: <the rule or criterion at stake — one line>
- **why it matters here**: <the concrete consequence in THIS system>
- **confidence**: verified | suspected   # "verified" = I confirmed it; "suspected" = framed as the question
                                          # that would settle it, not asserted as fact
- **what would satisfy me**: <the concrete change / test / proof that clears this finding>
```

## Finding-ID convention

`<CONCERN-PREFIX>-NN`, zero-padded two digits, unique within the spoke. Prefixes:

| Concern | Prefix |
|---|---|
| Correctness vs acceptance criteria & design | `COR` |
| Durability proof / test depth | `DUR` |
| Code quality, design & Rust idiom | `CQ` |
| Architecture / contract stability | `ARC` |
| Security & trust boundaries | `SEC` |
| Operational readiness | `OPS` |
| CI `doc` check diagnosis | `CI` |

## Rules every spoke honors

1. **Evidence over assertion.** A finding a reader cannot verify from the location + principle is an opinion,
   not a finding. When unsure, set `confidence: suspected` and phrase "what would satisfy me" as the question
   that settles it.
2. **Severity is honest.** `blocker` ⟺ `blocks_landing: true`. Never downgrade a blocker to backlog to make
   approval easier; never inflate a preference to a blocker. "I would have done it differently" is not a
   finding on its own.
3. **Pin to the commit.** Give `file:line @ 09fa453`. A finding with no verifiable location must say why
   (whole-PR or design-level) rather than omit it.
4. **Read tests as closely as code.** For the durability-proof concern especially: would each assertion fail
   if the behavior it guards broke? Does a double stand in for a boundary or for the logic under test?
5. **Patterns over instances.** Ten copies of one mistake are one finding that names the pattern and where it
   recurs, not ten findings.
6. **No host/system details, ever.** Nothing in a findings.md that will be surfaced to repo readers may carry
   host paths, cluster/SSH/credential details, or DAG internals. Point at repo files, lines, issues, and
   design paths.
7. **Plain voice.** Hold the prose to the plain-voice bar: no moral adjectives ("honest"/"genuine"/"real")
   glued to things that cannot hold them, no narrated candor, no template filler, no inflated
   seamless/robust/comprehensive/leverage. Judge by cluster and density.
