# `oekg/` — Open Energy Knowledge Graph

The OEKG describes energy studies and scenarios in RDF, using the
[Open Energy Ontology (OEO)](https://github.com/OpenEnergyPlatform/ontology) as its schema.

## 🔴 The live graph is not in this directory

**The OEKG lives in a [Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) dataset,
not in this repository.** The Open Energy Platform's scenario-bundle factsheets populate it by
writing triples over SPARQL, through an `rdflib` `SPARQLUpdateStore` pointed at the endpoint;
querying is likewise over SPARQL. The graph never round-trips to a file here.

So nothing in this directory is the OEKG, and **moving files here cannot affect the
platform**. The endpoint is **Django configuration** in
[`oeplatform`](https://github.com/OpenEnergyPlatform/oeplatform) (`rdfdb` settings), not a
constant, and certainly not something this repository fixes. Historically the deployed dataset
has been `oekg_main` on a Fuseki instance at OVGU; treat any host you find written down as *a
deployment detail*, not as canonical, and get the current one from the platform.

What this directory holds is the OEKG's **shapes, evaluation instruments and history**.

## Organised by status, not by file type

That is deliberate, and it is the single thing to understand about this layout. Most of what
this repository has ever contained for the OEKG is *superseded*, so filing it by file type
would put live and dead material side by side with nothing to tell them apart.

| Directory | Status | What it is |
|---|---|---|
| [`shapes/`](shapes/) | **current**, canonical | `oekg_shapes.ttl` — the OEKG's SHACL shapes, from the BA thesis. Validated against the live graph 2026-08-13: **135 violations, 133 of them upstream `oeplatform` data bugs**. No CI runs them yet. |
| [`eval/`](eval/) | **current** | the competency questions (prose + SPARQL). The shapes **moved out** of here to `shapes/` on 2026-08-13. |
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
| to work on shapes | [`shapes/`](shapes/) — and read its README first; it records which artifact is which, and why |
| the actual graph data | the SPARQL endpoint, not this repository |

## No CI validates any of this

`.github/workflows/checks.yml` runs pull-request checks, but it deliberately validates **no graph
data**: no shapes are run and no queries are executed. Adding SHACL validation to CI is an obvious
win, but it needs a decision about *what is validated against what* first — and that is model
design. The 2026-08-13 validation makes the shape of that decision concrete: of the 135 violations
the live graph produces, **133 are `oeplatform` data bugs that no pull request to this repository
can fix**, so a blocking check against the live graph would be permanently red.
