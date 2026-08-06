# `oekg/shapes/` — SHACL shapes for the OEKG

> **⚠️ These shapes validate no live graph.** Nothing in this repository is validated
> against them today, and no CI runs them. They are kept here as the **starting point for
> future SHACL work**, not as a working validation pipeline.

## What is here

`oekg_shapes.ttl` (350 lines) — the most developed SHACL artifact that exists for the OEKG
anywhere, in or out of this repository. Eight node shapes with `sh:closed`, 45
`sh:resultMessage`s and `sh:in` value enumerations, targeting `oeo:OEO_00010252`
(scenario_study) among others.

It is a **byte-identical copy** of
`../archive/madbkr_ba/oekg_rework/shacl/oekg_shacl_old_graph_txt`. The archive keeps its
original — that copy is the frozen thesis record; this one is the working starting point.

## What it was written against, and why that matters

It was authored during the BA thesis rework against `OEKG_Prep.ttl`, the **pre-rework**
graph, where it reports **2695 violations**. That graph lives in
`../archive/madbkr_ba/oekg_rework/`.

Two consequences, stated so nobody is misled by the directory's existence:

1. **It does not describe the live OEKG.** The live graph is populated by OEP factsheets
   over SPARQL into a Jena Fuseki dataset and never round-trips to this repository. See
   [`../README.md`](../README.md).
2. **It does not describe `../legacy/oekg.ttl` either.** That 2023 snapshot contains **zero**
   instances of the classes these shapes target, so running the shapes against it produces
   either nothing or a handful of trivial missing-`rdfs:label` reports.

## Known defect: namespaces

The file declares `@prefix oeo: <http://openenergy-platform.org/ontology/oeo/>` and
`@prefix oekg: <http://openenergy-platform.org/ontology/oekg/>` (hyphenated `http`), while
the graph it was written for uses `https://openenergyplatform.org/…`. Run as committed it
therefore reports **`Conforms: True` vacuously** — matching nothing. Normalising the
namespaces first is what reproduces its 2695-violation report.

Namespace drift across the OEKG's artifacts is not incidental: `oeplatform` itself binds two
inconsistent OEKG namespaces (`…/oekg/` and `…/ontology/oekg/`). Any future shapes work has
to settle this before it can settle anything else.

## Also SHACL, elsewhere in this repo

| Path | Lines | Job |
|---|---|---|
| `oekg/shapes/oekg_shapes.ttl` | 350 | *this file* — starting point for future work |
| `oekg/eval/oekg_shacl.txt` | 317 | evaluation material for the reworked graph (55 violations) |
| `oekg/archive/madbkr_ba/oekg_rework/shacl/oekg_shacl_old_graph_txt` | 350 | frozen thesis record of this file |
| `oekg/archive/madbkr_ba/oekg_rework/shacl/oekg_shacl_new_graph.txt` | 317 | frozen thesis record, byte-identical to `oekg/eval/oekg_shacl.txt` |

**None of them is a source of truth.** Which graph the OEKG's shapes should describe, and
whether the graph is generated from shapes at all, is model design and is decided elsewhere.
