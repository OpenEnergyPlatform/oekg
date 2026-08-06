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

## ⚠️ `mhpkg` is a provisional name

The directory name and the short name `mhpkg` are **provisional** and may change.

**Do not bake `mhpkg` into anything expensive to change** — in particular not IRIs, not
namespace prefixes, and not published URLs. If you need a prefix while working on the
draft, use a clearly temporary one and keep it in a single place so a rename is one edit.

## What belongs in here

- The knowledge graph itself and its schema/shapes.
- Its examples, and any queries that demonstrate or evaluate it.
- Documentation specific to this graph.

## Current layout

Only one directory exists, because there is only one thing to put anywhere:

| Path | Contents |
|---|---|
| `mhpkg/model/mhpkg_model_first_draft.owl` | the first draft of the model — 350 lines of RDF/XML exported from [Termboard](https://termboard.com/): 21 `owl:Class`, 16 `owl:ObjectProperty`, no `owl:DatatypeProperty`, no `sh:NodeShape` |

`model/` rather than `shapes/` because the draft is **OWL, not SHACL** — it contains zero
`sh:NodeShape`, so the shapes-first intent is not yet reflected in it. The name is
**provisional** and may be revised when the model source of truth is decided (see the open
questions below).

Directory names are shared with the OEKG's area *where both graphs genuinely have the same
thing* — `shapes/`, `eval/`, `examples/` are the agreed vocabulary. No parallel structure is
invented ahead of content: **create a directory when there is something to put in it**, not
before. Empty directories that exist get filled with the wrong things.

> ⚠️ **The draft's base IRI is a vendor namespace** —
> `https://termboard.com/ontology/d0425b2d-…`, and its `dc:title` is still
> "Imported Document". It **needs rebasing onto a namespace this project controls**, and this
> is exactly the "don't bake in IRIs" hazard arriving through a tool rather than a decision.
> Deliberately **not** done during the repository restructure: rebasing an ontology's IRIs is
> model design. Recorded here so it is not lost.

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
   mhpkg  (this directory)  ──loaded into──▶  Jena Fuseki dataset  ◀── which dataset: open
```

The Open Energy Platform already serves the OEKG from a Jena Fuseki store over SPARQL.
Whether `mhpkg` becomes a second dataset in that same store or gets its own instance is
**not yet decided**.

## Open questions this scaffold deliberately does not answer

These are being worked separately. Please do not settle them by implication in the draft —
if the draft forces a position on one, say so rather than letting the commit decide it.

1. **The model source of truth.** SHACL-shapes-first is the intended direction, and LinkML
   is under consideration as the authoring layer to generate from. Not yet decided.
2. **The KG / table boundary.** Which extracted data belongs in the graph as triples versus
   in a table on the Open Energy Platform.
3. **The Fuseki dataset** that will host this graph.
4. **This directory's final name and internal layout.**

## Licence

This repository is licensed under Creative Commons Zero v1.0 Universal — see
[LICENSE.txt](../LICENSE.txt). Anything committed here is published under CC0, so only
commit content that may be redistributed on those terms.
