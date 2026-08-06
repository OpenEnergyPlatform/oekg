---
hide:
  - footer
---

# How the OEKG is built — and how it used to be

This page exists because the OEKG's part of this repository is organised **by status**, and
that only makes sense if you know which pipeline produced what. It has two subjects: the
pipeline that is live, and the one that is not.

## The live graph is not in this repository

The OEKG is populated by the **Open Energy Platform's scenario-bundle factsheets**. When
someone creates or edits a factsheet on the platform, the platform writes the resulting
triples over **SPARQL** into a **Jena Fuseki** dataset, through an `rdflib`
`SPARQLUpdateStore` pointed at the endpoint. Reading the graph works the same way, by SPARQL
query. There is no export step and no file in this repository in that path.

```text
OEP scenario-bundle factsheet
        │  SPARQL update (rdflib SPARQLUpdateStore)
        ▼
Jena Fuseki dataset  ◀── SPARQL query ──  consumers
```

Two consequences worth stating plainly:

- **The platform does not read any file from this repository.** The only ontology file the
  factsheet code parses is `oeo-full.owl`, and it takes that from the platform's own
  `ONTOLOGY_ROOT`, not from here.
- **There is therefore no file in this repository that *is* the OEKG**, and no file here that
  the shapes in `oekg/shapes/` can be meaningfully run against.

The endpoint itself is Django configuration in
[`oeplatform`](https://github.com/OpenEnergyPlatform/oeplatform) (`rdfdb` settings), not a
constant. The deployed value at the time of writing is a Fuseki dataset hosted at OVGU. If you
need to query the OEKG, that endpoint — not this repository — is the thing to ask for.

## The superseded pipeline

Before the factsheets existed, the OEKG was assembled by hand from published study reports, in
three steps:

```text
published study report (PDF)
        │  read by a human
        ▼
placeholder JSON        one file per study, a deliberately simple structure
        │  Google Colab notebook, rdflib
        ▼
a single Turtle file    committed to this repository
```

The **placeholders** were the interesting idea: rather than asking energy experts to write RDF,
they wrote flat JSON with a shape that mapped onto the OEO's conceptualisation, and a notebook
did the conversion with [`rdflib`](https://github.com/RDFLib/rdflib). The notebook doubled as a
tutorial — the intent was that anyone could follow it to turn a study into a graph. Writing
Turtle directly was always the alternative for anyone who preferred it; the placeholders
existed to lower the barrier, not to be a required format.

All three stages are preserved in `oekg/legacy/`:

| Path | What it is |
|---|---|
| `oekg/legacy/placeholder/` | the 7 placeholder JSON files |
| `oekg/legacy/notebook/oekg_tutorial.ipynb` | the Colab notebook that converted them |
| `oekg/legacy/oekg.ttl` | what came out — a 2023 snapshot |

### Why it was superseded

Hand-maintaining placeholders does not scale, and it puts the graph a manual step away from the
people who actually have the information. The factsheets moved authorship onto the platform,
where the data is entered once and lands in the graph directly.

### ⚠️ Do not mistake `oekg/legacy/oekg.ttl` for the OEKG

It is a 2023 snapshot, byte-identical to its 2023-08-31 state — never edited since, only moved.
It contains **zero** instances of the classes the OEKG is now about: scenario_study, scenario
bundle, scenario / model / framework factsheet, study report. Its dominant class is
`IAO_0000100` (data set). No SHACL file in or out of this repository describes it.

## The model rework, and where the definitions live

Between those two pipelines, a Bachelor's thesis remodelled the graph against a current OEO
release, retargeting classes and predicates and validating the result with SHACL. Its headline
result is the drop in SHACL violations, **2695 → 55**.

That work is archived intact at `oekg/archive/madbkr_ba/` — inputs, intermediates, outputs,
shapes, validation reports and the four scripts. It is closed; nothing there is live tooling,
and the archive's README makes no reproducibility claim, because the repository pins no
dependencies.

The single most useful document to come out of it is
**`oekg/archive/madbkr_ba/scripts/documentation.pdf`**, which gives **every predicate with its
definition, domain and range**. If you are looking for what an OEKG predicate means, that is
where to look.

One irreplaceable file sits in that archive: `oekg_rework/oekg_neu.ttl`, an **April 2025 dump
of the live graph** from the Fuseki endpoint. It is the only copy of the OEKG at that date
anywhere in this repository.

## Summary

| Question | Answer |
|---|---|
| Where is the OEKG? | a Jena Fuseki dataset, reached over SPARQL. Not in this repository. |
| Who writes it? | the OEP's scenario-bundle factsheets. |
| What are the Turtle files here, then? | history — a 2023 snapshot, and the thesis rework's inputs and outputs. |
| Where are the predicates defined? | `oekg/archive/madbkr_ba/scripts/documentation.pdf`. |
| Where are the fields listed? | [`fields.md`](fields.md). |
