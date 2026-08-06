---
hide:
  - footer
---

# Municipal Heat Planning Knowledge Graph

A knowledge graph for German **kommunale Wärmeplanung** (municipal heat planning), built from the
heat plans that municipalities publish under the Wärmeplanungsgesetz.

The goal is to extract as much as possible from those plans **in structured form**, so that real
values for specific attributes can be queried across all of them at once — rather than being
locked inside several hundred PDFs. There is substantial interest in this from energy research,
because planning and modelling work can build directly on such a dataset.

!!! warning "Provisional name"

    `mhpkg` is a **working name** for both the directory and the graph, and it may change. Nothing
    should bake it into IRIs, namespace prefixes or published URLs without a rename path.

## Status: early draft

Being honest about maturity, because the ambition above is much larger than what exists today:

| | |
|---|---|
| **Model** | one draft, `mhpkg/model/mhpkg_model_first_draft.owl` |
| **Size** | 350 lines of RDF/XML — 21 classes, 16 object properties, no datatype properties |
| **Origin** | exported from [Termboard](https://termboard.com/), a visual knowledge-modelling tool |
| **SHACL shapes** | none yet — the draft contains zero `sh:NodeShape` |
| **Extracted data** | none yet in the graph |
| **Store** | not yet decided |

Two things about the draft that are known and unresolved:

- Its **base IRI is a vendor namespace** — `https://termboard.com/ontology/…` — because it came
  out of the modelling tool that way. It needs rebasing onto a namespace this project controls.
- Its `dc:title` is still `"Imported Document"`.

Neither is an oversight to be fixed casually: choosing the namespace is a modelling decision, and
it is recorded rather than quietly patched.

## How the data gets here

The pipeline spans four repositories and is documented on its own page:
**[Workflow](../workflow.md)**.

In short: published PDFs → a RAG pipeline → the MHPO ontology → this graph → a Fuseki dataset.
Note that the RAG pipeline currently identifies **vocabulary**, not values; value extraction is
the planned next step.

## What belongs here, and what does not

`mhpkg/` holds the graph and its schema, its examples, and its own documentation. It does **not**
hold:

| Not here | Where instead |
|---|---|
| The RAG pipeline | [municipal-heat-planning-pdf-processing](https://github.com/OpenEnergyPlatform/municipal-heat-planning-pdf-processing) |
| The MHPO ontology | [municipal-heat-planning-ontology](https://github.com/OpenEnergyPlatform/municipal-heat-planning-ontology) |
| Source heat-plan PDFs | published by the municipalities; referenced, not vendored |
| Bulk tabular extractions | ⚠️ undecided — see below |
| Anything belonging to the OEKG | [`oekg/`](../oekg/index.md) |

### The graph / table boundary is open

Not everything worth extracting from a heat plan belongs in a graph. Long runs of figures — per
municipality, per year, per technology — are naturally tabular, and the Open Energy Platform
already serves tables well.

**Where that line falls has not been decided.** Until it is, bulk tabular data is *flagged* rather
than committed, so the decision is made deliberately instead of being settled by whatever happened
to get committed first.

## Relationship to the OEKG

The two graphs share this repository, a tech stack and a platform. They **do not share a model**,
and there is deliberately no `shared/` directory holding common semantics — see the repository
README for the reasoning. Both draw on the Open Energy Ontology, but independently.
