# `oekg/shapes/` — SHACL shapes for the OEKG

> **Status: CURRENT and canonical.** `oekg_shapes.ttl` is the OEKG's shapes file. It was validated
> against the live graph on 2026-08-13 and it binds — see [Validation status](#validation-status).
> No CI runs it yet; wiring that up is tracked work.

## What is here

`oekg_shapes.ttl` (317 lines) — eight node shapes over the **reworked** OEKG model, produced by the
BA thesis *"Qualitätsverbesserung eines Knowledge Graphen mit Hilfe von SHACL und
Kompetenzfragen"* (Madeleine Breitkreutz, OVGU, submitted 2025-08-04). It targets `scenario bundle`
(`OEO_00020227`), `study report`, `scenario factsheet`, `framework factsheet`, `model factsheet`,
and the objects of fourteen predicates. It declares the current
`https://openenergyplatform.org/ontology/…` namespaces.

It is **byte-identical** to `../archive/madbkr_ba/oekg_rework/shacl/oekg_shacl_new_graph.txt`
(`md5 d5ab525e8316cb99abf2551949722414`). The archived copy is the frozen thesis record; this one
is the working copy and may be revised. Two copies, deliberately — and never a third.

## ⚠️ Read this before "correcting" the shapes

**This directory previously held a different, superseded file, and that mistake cost a reviewer
real time.** Until 2026-08-13, `oekg/shapes/oekg_shapes.ttl` was the thesis's **pre-rework**
instrument — 350 lines, targeting `scenario_study` (`OEO_00010252`), using `oekg:has_publication`
and `RO_0002233/4`, declaring the old `http://openenergy-platform.org/…` namespace. It was
surfaced here because it is *longer*, on the reasoning that 350 lines beat 317.

That reasoning was wrong. The thesis **folded** five shapes (Author, Institution, ContactPerson,
FundingSource, Technology) into `CommonShape`; the shorter file is the *successor*, not the lesser
one.

The consequence was concrete. The thesis supervisor, reviewing what this repository offered as its
current shapes, reported three defects as things the student *"noch korrigiert haben sollte"*:

| | old 350-line file | `oekg_shapes.ttl` today |
|---|---|---|
| line 19 | `sh:path oeo:has_study_keyword` | `sh:path oeo:OEO_00390071` — has study descriptor tag |
| line 55 | `sh:path oeo:OEO_00000505` — covers sector | *(folded; now `OEO_00020439` covers sector (shortcut))* |
| line 62 | `sh:path oeo:OEO_00000522` — covers | *(folded; now `OEO_00020438` covers technology (shortcut))* |

All three were **already correct** in this file. The old README compounded it by instructing
readers that *"rebasing this file onto the current namespace is the first thing any future shapes
work should do"* — pointing effort at an artifact no graph uses.

**Verified 2026-08-13:** all **21 rows** of the thesis's Tabelle 1 (the old→new entity mapping) are
applied in this file, with no old form remaining. Its 31-term `has study descriptor tag`
enumeration matches the thesis appendix exactly. Nothing newer exists anywhere — the only other
candidate, on the unmerged branch `feature-add-shacl-file`, is from **December 2024**, six months
*older* than this.

The superseded file has been removed from this directory. Its byte-identical original remains at
`../archive/madbkr_ba/oekg_rework/shacl/oekg_shacl_old_graph_txt`, where it belongs — as the
instrument that produced the thesis's 2695-violation baseline.

## Validation status

Validated **2026-08-13** with `pyshacl` 0.40.1 / `rdflib` 7.6.0 against a snapshot of the live
graph (13,700 triples, 55 scenario bundles):

| | |
|---|---|
| Result | `Conforms: False` — **135 violations**, 0.99% of triples |
| Thesis baseline | 55 violations / 11,056 triples (0.5%) on the reworked graph |
| Non-vacuity | **1,499 focus nodes bound across all eight shapes** — namespaces match the live graph |

That last row is the one that matters: the shapes **bind**. A shapes file whose namespaces do not
match its data reports `Conforms: True` by matching nothing, and this one does not do that.

**133 of the 135 violations are `oeplatform` data bugs that cannot be fixed in this repository** —
78 unfilled mandatory fields (which the thesis predicted, §8.4), 17 missing OEO term labels, and
five writer regressions that appeared after the rework landed. Only **2** are the shapes' own
(enumeration drift: one new OEO term missing, one term wrongly dropped). The upstream work is
tracked separately; ask a maintainer for the OEKG data-quality backlog.

Validation was run against a dump, not the SPARQL endpoint — the endpoint remains the source of
truth and the dump-vs-live gap is unmeasured.

## Why these shapes are hand-written Turtle

The MHPKG graph in this repository authors its shapes in **LinkML** and generates SHACL with
`gen-shacl` (see [`../../mhpkg/schema/`](../../mhpkg/schema/)). The OEKG deliberately does **not**,
and the asymmetry is a decision rather than an oversight — please do not "unify" it without
reading this.

`gen-shacl` never emits `sh:targetObjectsOf`, `sh:message`/`sh:resultMessage`, or node-level
`sh:pattern`. **Three of these eight shapes have no `sh:targetClass` at all** — `DatasetShape`,
`RegionShape`, and `CommonShape`, the largest of the eight with 773 focus nodes and ten
`sh:targetObjectsOf`. `CommonShape` exists precisely to constrain whatever sits at the end of ten
predicates *regardless of its class*, which is not a LinkML class and therefore cannot be a
generated shape. Generating the five class-based shapes and hand-writing the other three was
considered and rejected: it splits the shapes across files for no gain and still discards all 38
`sh:resultMessage` strings, which the thesis wrote deliberately because a readable validation
report was part of its method.

MHPKG reached the same limit from the other side: its `mhpkg_iri_policy.shacl.ttl` is hand-written
because LinkML silently drops the patterns it needs.

## Known work in flight

- **The six `sh:in` enumerations — 382 OEO terms — are still hand-maintained**, and that is the
  source of the 2 shape-side violations above. They are to become **generated from the OEO** and
  checked for currency in CI, so that the shapes and the platform's dropdowns (which already derive
  the same lists dynamically from OEO annotations) cannot disagree. Not implemented yet.
- **No CI validates this file.** Adding that needs a decision about what is validated against what,
  which is tracked separately.

## Running the shapes

```bash
uv sync --group graph
uv run python -c "
from pyshacl import validate
from rdflib import Graph
shapes = Graph().parse('oekg/shapes/oekg_shapes.ttl', format='turtle')
data = Graph().parse('<your-dump>.ttl', format='turtle')
conforms, _, text = validate(data_graph=data, shacl_graph=shapes, advanced=True)
print(conforms); print(text[:4000])
"
```

> ⚠️ **Never pass `pyshacl` two `-s` flags.** It accepts them and **silently uses only the last**,
> discarding the earlier shapes graph without warning — reporting `Conforms: True` with exit 0
> while consulting neither. See [`../../mhpkg/schema/validate.py`](../../mhpkg/schema/validate.py),
> which merges shapes in code for exactly this reason.

## Related

| Path | What it is |
|---|---|
| [`../eval/`](../eval/) | the competency questions — the graph's other evaluation instrument |
| [`../archive/madbkr_ba/`](../archive/madbkr_ba/) | the finished BA thesis: both frozen shapes records, the graphs, the scripts, and `documentation.pdf` with the predicate definitions |
| [`../legacy/`](../legacy/) | the superseded 2023 population pipeline. Do not reuse. |
| [`../README.md`](../README.md) | where the live graph actually is (a Fuseki dataset, not this repository) |
