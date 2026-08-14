---
hide:
  - footer
---

# Querying the OEKG — the SPARQL endpoint

The OEKG is served from a **Jena Fuseki** dataset over SPARQL. That endpoint, not this
repository, is where the graph actually is.

!!! warning "This page is not authoritative"

    The endpoint is **deployment configuration**, not a property of this repository. It is set in
    [`oeplatform`](https://github.com/OpenEnergyPlatform/oeplatform)'s Django settings (the
    `rdfdb` entry) and can change without any commit here. The value below is what is deployed at
    the time of writing.

    If it does not work, ask the Open Energy Platform maintainers rather than assuming the graph
    is gone.

## The deployed endpoint

| | |
|---|---|
| **Query** | `https://oekb.iks.cs.ovgu.de:3443/oekg_main/query` |
| **Update** | `https://oekb.iks.cs.ovgu.de:3443/oekg_main/update` |
| **Host** | Otto-von-Guericke-Universität Magdeburg |
| **Software** | Apache Jena Fuseki |

The update endpoint is how the platform's factsheets write to the graph. Ordinary consumers want
the query endpoint.

## Querying it

Any SPARQL client works. With Python:

```python
from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("https://oekb.iks.cs.ovgu.de:3443/oekg_main/query")
sparql.setReturnFormat(JSON)
sparql.setQuery("""
    SELECT ?s ?p ?o
    WHERE { ?s ?p ?o }
    LIMIT 10
""")

for row in sparql.queryAndConvert()["results"]["bindings"]:
    print(row)
```

`rdflib` with a `SPARQLStore`, Apache Jena's own tooling, or plain HTTP all work equally well —
there is nothing OEKG-specific about the protocol.

## Prefixes

⚠️ **Check which namespace form the graph is using before writing queries against it.** The
project has migrated from `http://openenergy-platform.org/…` to
`https://openenergyplatform.org/…`, and the live graph has been updated — but **some files in this
repository have not**, including the competency-question SPARQL in `oekg/eval/` and the shapes in
`oekg/shapes/`.

A query copied from those files may return zero results against the live graph, and a
zero-result SPARQL query looks identical to a correct query about absent data. If a query
mysteriously returns nothing, suspect the namespace first.

## Ready-made queries

`oekg/eval/competency_questions/` holds the graph's **competency questions** — the questions the
OEKG was built to be able to answer — in both natural language and SPARQL. They are the fastest
way to see what the graph can do, subject to the namespace caveat above.

## What you cannot do here

- **You cannot get the graph as a file from this repository.** See
  [provenance](provenance.md).
- **You can validate the live graph with the shapes in `oekg/shapes/`, but not from here.** As of
  2026-08-13 those shapes do describe the deployed model — they were run against a dump of it and
  bound 1,499 focus nodes. What this repository cannot give you is the data: you supply a dump or
  point `pyshacl` at the endpoint yourself. See
  [the OEKG overview](index.md#the-shapes-describe-the-live-graph-as-of-2026-08-13).
