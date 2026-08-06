# `oekg/eval/` — the OEKG's evaluation instruments

> **Status: CURRENT.** These are the instruments used to evaluate the OEKG. Nothing here is
> automated — no CI runs them, and running them is a manual step today.

Both kinds of material in this directory are evaluation instruments, which is why they sit
together rather than being split by file type.

## Contents

| Path | Contents |
|---|---|
| `competency_questions/cq_natural_language.txt` | the competency questions in prose — what the graph must be able to answer |
| `competency_questions/cq_sparql.txt` | the same questions as SPARQL queries |
| `oekg_shacl.txt` | 317 lines of SHACL, the evaluation shapes for the **reworked** graph |

## `oekg_shacl.txt`

These shapes target `oeo:OEO_00020227` (scenario bundle) and report **55 violations** against
`../archive/madbkr_ba/oekg_rework/output_rework_oekg_final.ttl`. That 55 is one half of the BA
thesis's headline `2695 → 55` result; see
[`../archive/madbkr_ba/README.md`](../archive/madbkr_ba/README.md).

The file is **byte-identical** to
`../archive/madbkr_ba/oekg_rework/shacl/oekg_shacl_new_graph.txt`
(`md5 d5ab525e8316cb99abf2551949722414`). Both copies are kept deliberately and they have
different jobs: the archived copy is the frozen thesis record, this one is the graph's
evaluation material and may be revised. Neither is a source of truth.

Forward-looking shapes work starts from [`../shapes/`](../shapes/), not from here.

## What these can and cannot be run against

The SPARQL competency questions were written against the **live** OEKG in Fuseki, and the
shapes against a dump of it. Neither can be usefully run against `../legacy/oekg.ttl`, which
is a 2023 snapshot with none of the relevant class instances. See
[`../README.md`](../README.md) for where the live graph actually is.
