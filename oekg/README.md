# `oekg/` — Open Energy Knowledge Graph

The OEKG describes energy studies and scenarios in RDF, using the
[Open Energy Ontology (OEO)](https://github.com/OpenEnergyPlatform/ontology) as its schema.

## 🔴 The live graph is not in this directory

**The OEKG lives in a [Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) dataset,
not in this repository.** The Open Energy Platform's scenario-bundle factsheets populate it by
writing triples over SPARQL, through an `rdflib` `SPARQLUpdateStore` pointed at the endpoint;
querying is likewise over SPARQL. The graph never round-trips to a file here.

So nothing in this directory is the OEKG, and **moving files here cannot affect the
platform**. The endpoint is Django configuration in
[`oeplatform`](https://github.com/OpenEnergyPlatform/oeplatform), not a constant in this repo.
The deployed value at the time of writing is a Fuseki dataset at OVGU
(`oekb.iks.cs.ovgu.de:3443/oekg_main`); treat that as *the deployed value*, not as canonical.

What this directory holds is the OEKG's **shapes, evaluation instruments and history**.

## Organised by status, not by file type

That is deliberate, and it is the single thing to understand about this layout. Most of what
this repository has ever contained for the OEKG is *superseded*, so filing it by file type
would put live and dead material side by side with nothing to tell them apart.

| Directory | Status | What it is |
|---|---|---|
| [`shapes/`](shapes/) | **current**, forward-looking | the most developed SHACL shapes for the OEKG. ⚠️ They validate **no live graph** — a starting point, not a pipeline. |
| [`eval/`](eval/) | **current** | the graph's evaluation instruments: competency questions (prose + SPARQL) and the 317-line evaluation shapes. |
| [`legacy/`](legacy/) | **superseded**, kept for provenance | the first population pipeline: hand-built placeholder JSON → Colab notebook → a 2023 Turtle snapshot. **Do not reuse.** |
| [`archive/madbkr_ba/`](archive/madbkr_ba/) | **archived**, closed | a finished BA thesis that remodelled the graph against the OEO. Intact, nothing deleted. Its `documentation.pdf` holds the predicate definitions. |

Each of those has its own README stating what it is and whether it is live. Read it before
using anything in it.

## Where to start

| If you want… | Go to |
|---|---|
| what the OEKG's fields are | [`../docs/oekg/fields.md`](../docs/oekg/fields.md) |
| how the graph used to be built, and how it is built now | [`../docs/oekg/provenance.md`](../docs/oekg/provenance.md) |
| the predicate definitions | `archive/madbkr_ba/scripts/documentation.pdf` |
| to work on shapes | [`shapes/`](shapes/) — and read its README first |
| the actual graph data | the SPARQL endpoint, not this repository |

## No CI validates any of this

There is no `.github/workflows/` in this repository. No shapes are run, no queries are
executed, nothing is checked. Adding SHACL validation to CI is an obvious win, but it needs a
decision about *what is validated against what* first — and that is model design.
