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

!!! info "The name is settled"

    `mhpkg` was a working name and is now **fixed**. It is safe in IRIs, prefixes and published
    URLs — instance data lives under `https://openenergyplatform.org/id/mhpkg/` and named graphs
    under `https://openenergyplatform.org/graph/mhpkg/`. No rename path is owed.

## Status: early, but no longer only a sketch

Being honest about maturity, because the ambition above is much larger than what exists today:

| | |
|---|---|
| **Data shape** | one slice authored in [LinkML](https://linkml.io/) — `mhpkg/schema/` |
| **Coverage** | a municipal heat plan, its inventory analysis and target scenario, and their final energy consumption, greenhouse gas emission and share values |
| **SHACL shapes** | **generated** from the LinkML schema, plus two hand-written files: the IRI policy, and rules that depend on where a node sits |
| **Terms** | cited from MHPO and OEO, never minted here — pinned term list in `mhpkg/mhpo/` |
| **Examples** | one conformant instance and one deliberately failing one |
| **Termboard model** | exported to `mhpkg/model/` by date (latest: 2026-09-15), and compared with the schema by a delta tool |
| **Extracted data** | none yet in the graph |
| **Store** | decided — its own Fuseki dataset, one named graph per heat plan. Not yet provisioned |

The two graphs are authored differently on purpose, and the split is the thing to understand:

- **MHPO owns the vocabulary.** Every class and slot in the LinkML schema carries a `class_uri` or
  `slot_uri` pointing at a term MHPO or OEO already declares. A term that does not exist becomes an
  **MHPO term request**, not a new element here — so this repository never becomes a second,
  competing definition of the same domain.
- **LinkML owns the shape.** Required fields, cardinality, value ranges and controlled vocabularies
  are data constraints, and an ontology does not assert them: OWL is open-world. Generating the
  shapes from MHPO instead was tried on paper and rejected for exactly that reason — the result
  would validate very little.

### Where to look in the repository

[`mhpkg/schema/`](https://github.com/OpenEnergyPlatform/oekg/tree/production/mhpkg/schema) — its
README carries the commands, the tool versions, and a frank account of what the first slice
established *and where the approach has limits*. Read that before extending the schema; two of the
limits change how the generated artifacts can be checked.

[`mhpkg/mhpo/`](https://github.com/OpenEnergyPlatform/oekg/tree/production/mhpkg/mhpo) — the pinned
MHPO term list, and the script that regenerates it. MHPO has no releases or tags, so the pin is a
commit SHA.

[`mhpkg/model/`](https://github.com/OpenEnergyPlatform/oekg/tree/production/mhpkg/model) — the
Termboard exports and the loop that carries a new one into the schema.

### About the Termboard model

The model is drawn in Termboard and exported here, but **nothing from Termboard reaches the schema or
the graph without a human decision**. Termboard cannot say which box is a class, which is an
individual and which is a literal: `2030`, `MWh` and `municipal heat plan` are all boxes. Its OWL
export is also not valid RDF/XML, and it strips umlauts from IRI local names, so
`Kassel Wärme Ingenieurbüro` becomes `Kassel_Wrme_Ingenieurbro`. Fed through the IRI policy, that
mints a **different** entity without raising an error.

The JSON export is clean enough to **compare** against. `mhpkg/model/termboard_delta.py` reads it,
together with a committed mapping of Termboard names to schema elements, and lists what is new,
what is gone, and which drawn relations the schema cannot yet express. The schema change itself is
made by hand. Terms that neither OEO nor MHPO has become term requests.

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
