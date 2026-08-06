# `oekg/legacy/` — the first OEKG population pipeline

> **Status: SUPERSEDED. Kept for provenance. Do not reuse.**
> This is how the OEKG *used to* be built, in 2023. It is not how it is built now, and none
> of these files participates in the live graph. Nothing here should be copied as a pattern
> for either knowledge graph in this repository.

## What this was

The OEKG's first population route, in three steps:

```text
placeholder/*.json            hand-written JSON, one per study
        │
        ▼
notebook/oekg_tutorial.ipynb  Google Colab notebook: reads the placeholders with rdflib,
        │                     serialises the result
        ▼
oekg.ttl                      the graph as a file in this repository
```

| Path | Contents |
|---|---|
| `placeholder/` | 7 placeholder JSON files (`bdi`, `esbbb`, `example`, `ksz2050`, `ps8`, `trafo`, `zukunft`) — the intermediate hand-built structures |
| `notebook/oekg_tutorial.ipynb` | the Colab notebook that turned placeholders into RDF |
| `oekg.ttl` | 2150 lines of Turtle — a **2023 snapshot**, not the live graph |

## Why it is superseded

The OEKG is now populated by the Open Energy Platform's factsheets, which write directly over
SPARQL into a Jena Fuseki dataset. There is no placeholder step, no notebook, and no file in
this repository in that path. See [`../README.md`](../README.md) and
[`../../docs/oekg/provenance.md`](../../docs/oekg/provenance.md).

## 🔴 `oekg.ttl` is **not** the OEKG

Read this before using the file for anything:

- It is **byte-identical to the 2023-08-31 merge-base** copy. It has never been edited; later
  commits only moved it.
- It contains **zero** instances of the classes the OEKG is actually about — scenario_study
  (`OEO_00010252`), scenario bundle (`OEO_00020227`), scenario / model / framework factsheet,
  study report. Its dominant class is `IAO_0000100` (data set, 242 instances).
- **No SHACL file in or out of this repository describes it.** All the shapes were authored
  against Fuseki dumps of the live graph.

It is retained as the record of what the first pipeline produced. Treat it as a 2023
historical artifact, not as data.

## The notebook does not run as-is

`notebook/oekg_tutorial.ipynb` was written for Google Colab and reads literal paths of the
form `"a/path/in/your/google/drive/…"`. It serialises to `OEKG_V1.ttl`. It is kept as the
prose record of the conversion logic, not as a runnable tool.
