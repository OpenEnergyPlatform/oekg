# mhpkg — Municipal Heat Planning Knowledge Graph

> **Status: early draft.** This directory was created to give the first draft of the municipal
> heat planning knowledge graph a home with rules already attached, ahead of a wider
> restructure of this repository. That restructure has since landed. Nothing here is
> load-bearing yet.

This is the knowledge graph for German **kommunale Wärmeplanung** (KWP) — municipal heat
planning — built from the published municipal heat plans. It is developed **alongside, and
separately from, the OEKG**, which occupies [its own area](../oekg/) of this repository and
describes energy studies and scenarios. The two graphs share a repository, not a model. See the
[root README](../README.md) for how the repository is laid out and why there is no `shared/`.

## ✅ The name `mhpkg` is settled

It was provisional; it is now fixed, and it is **safe to bake in**. Instance data lives under
`https://openenergyplatform.org/id/mhpkg/` and named graphs under
`https://openenergyplatform.org/graph/mhpkg/`. No rename path is owed.

> ⚠️ **If you read an earlier version of this file**, it warned against putting `mhpkg` into IRIs,
> prefixes or published URLs. That warning is superseded — the schema in [`schema/`](schema/) now
> depends on exactly those namespaces.

## What belongs in here

- The knowledge graph itself and its schema/shapes.
- Its examples, and any queries that demonstrate or evaluate it.
- Documentation specific to this graph.

## Current layout

Three directories, each created when there was something to put in it:

| Path | Contents |
|---|---|
| [`schema/`](schema/) | **the data shape** — the LinkML schema, the SHACL generated from it, the hand-written IRI-policy shapes, and worked examples. Start here |
| [`mhpo/`](mhpo/) | the pinned MHPO term list — which terms this graph may cite, and the commit they came from |
| [`model/`](model/) | the Termboard exports (JSON and OWL, by date), the **mapping** from Termboard names to the schema, and `termboard_delta.py`, which compares a new export with the schema. **Start here when a new export arrives** |

`model/` holds the model as it is drawn, and `schema/` holds it as it is enforced. The shapes live
in [`schema/generated/`](schema/generated/) and are generated rather than hand-written.

> ⚠️ **Termboard output never reaches the schema or the graph without a human decision.** The OWL
> export is not even valid RDF/XML, declares everything as `owl:Class` and strips umlauts from IRI
> local names — so `Kassel Wärme Ingenieurbüro` becomes `Kassel_Wrme_Ingenieurbro`, which the IRI
> policy mints as a **different** entity with no error. The JSON export is clean enough to be
> *compared* against the schema, and [`model/termboard_delta.py`](model/) does exactly that; every
> resulting change is still made by hand and recorded in `model/termboard_mapping.yaml`. See
> [`model/README.md`](model/README.md).

⚠️ These directory names and this layout are **provisional** — see open question 3 below.

Directory names are shared with the OEKG's area *where both graphs genuinely have the same
thing* — `shapes/`, `eval/`, `examples/` are the agreed vocabulary. No parallel structure is
invented ahead of content: **create a directory when there is something to put in it**, not
before. Empty directories that exist get filled with the wrong things.

> ✅ **The drafts' vendor base IRI** (`https://termboard.com/ontology/…`) no longer matters: no
> Termboard IRI is ever used. The tool matches Termboard names, and instance IRIs come from the IRI
> policy in `https://openenergyplatform.org/id/mhpkg/`.

## What does *not* belong in here

- **Anything belonging to the OEKG.** It has its own area.
- **The RAG pipeline** — that lives in
  [municipal-heat-planning-pdf-processing](https://github.com/OpenEnergyPlatform/municipal-heat-planning-pdf-processing).
- **The MHPO ontology** — that lives in
  [municipal-heat-planning-ontology](https://github.com/OpenEnergyPlatform/municipal-heat-planning-ontology).
  This graph *uses* MHPO; it does not define it.
- **Bulk tabular data extracted from the heat plans.** ⚠️ See the open question below —
  large tabular extractions may be better served by a table on the Open Energy Platform
  than by triples in the graph. Until that boundary is decided, **flag such data rather
  than committing it**, so the decision is made deliberately and not by accident.
- **Source PDFs of the heat plans.** They are published elsewhere; reference them, do not
  vendor them.

## How this graph relates to its neighbours

```text
published Wärmeplan PDFs
        │
        ▼
municipal-heat-planning-pdf-processing   (RAG pipeline: vocabulary + content extraction)
        │
        ▼
municipal-heat-planning-ontology (MHPO)  ──uses──▶  Open Energy Ontology (OEO)
        │
        ▼
   mhpkg  (this directory)  ──loaded into──▶  Jena Fuseki dataset `mhpkg`
```

The Open Energy Platform already serves the OEKG from a Jena Fuseki store over SPARQL. MHPKG gets
**its own dataset beside it**, holding one named graph per heat plan, so re-loading a plan is an
atomic whole-graph replace and a re-run updates rather than duplicates. ⚠️ **The dataset does not
exist yet** — the layout is decided, not provisioned.

## Open questions this scaffold deliberately does not answer

These are being worked separately. Please do not settle them by implication —
if a change forces a position on one, say so rather than letting the commit decide it.

1. ✅ ~~**The model source of truth.**~~ **Decided.** [LinkML](https://linkml.io/) authors the data
   shape and generates the SHACL; MHPO remains the only source of *terms*. See
   [`schema/`](schema/) for the schema and for what the first slice established — including where
   the approach has known limits.
2. **The KG / table boundary.** Which extracted data belongs in the graph as triples versus
   in a table on the Open Energy Platform.
3. ⚠️ **This directory's internal layout** — the names `schema/`, `mhpo/` and `model/`, and where the
   IRI-policy document finally lives. The *graph's* name is settled (`mhpkg`); only the layout is
   open.

Previously listed here and now answered: **the Fuseki dataset** — MHPKG gets its own, as described
above.

## Licence

This repository is licensed under Creative Commons Zero v1.0 Universal — see
[LICENSE.txt](../LICENSE.txt). Anything committed here is published under CC0, so only
commit content that may be redistributed on those terms.
