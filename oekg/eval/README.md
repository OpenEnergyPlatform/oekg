# `oekg/eval/` — the OEKG's competency questions

> **Status: CURRENT.** These are evaluation instruments for the OEKG. Nothing here is automated —
> no CI runs them, and running them is a manual step today.

## Contents

| Path | Contents |
|---|---|
| `competency_questions/cq_natural_language.txt` | the competency questions in prose — what the graph must be able to answer |
| `competency_questions/cq_sparql.txt` | the same questions as SPARQL queries |

The BA thesis reports **20** questions, of which **19** were answerable after its rework and 7 were
problematic before it. That result is the other half of the thesis's finding; the first half is the
SHACL improvement, `2695 → 55`. See
[`../archive/madbkr_ba/README.md`](../archive/madbkr_ba/README.md).

> These files have **not** been verified against the thesis's final versions the way the shapes
> were. Treat the count above as the thesis's claim rather than a checked fact.

## 🔀 The shapes moved out of this directory

This directory used to hold `oekg_shacl.txt`, the OEKG's SHACL shapes, described here as
"evaluation material… not a source of truth". That framing stopped being true once the shapes
became the graph's contract, and a `.txt` extension on a Turtle file did not help.

**They now live at [`../shapes/oekg_shapes.ttl`](../shapes/oekg_shapes.ttl)** — same content,
renamed and relocated. **Shapes work starts there, not here.** Read that directory's README first;
it explains which artifact is which and why, and it records a mistake worth not repeating.

The frozen thesis record of the same file remains at
`../archive/madbkr_ba/oekg_rework/shacl/oekg_shacl_new_graph.txt`, unchanged.

## What these can and cannot be run against

The SPARQL competency questions were written against the **live** OEKG in Fuseki. They cannot be
usefully run against [`../legacy/oekg.ttl`](../legacy/), which is a 2023 snapshot containing none
of the relevant class instances. See [`../README.md`](../README.md) for where the live graph
actually is.
