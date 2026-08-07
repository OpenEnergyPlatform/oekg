
<a href="https://github.com/OpenEnergyPlatform/oekg/"><img align="right" width="100" height="100" src="https://raw.githubusercontent.com/OpenEnergyPlatform/organisation/master/logo/OpenEnergyFamily_Logo_OpenEnergyOntology_OEO.png" alt="Open Energy Knowledge Graph"></a>
<a href="https://openenergy-platform.org/"><img align="right" width="100" height="100" src="https://avatars2.githubusercontent.com/u/37101913?s=400&u=9b593cfdb6048a05ea6e72d333169a65e7c922be&v=4" alt="OpenEnergyPlatform"></a>

# Open Energy Family — Knowledge Graphs

📖 **Documentation: <https://openenergyplatform.github.io/oekg/>**

**This repository hosts two knowledge graphs.** They share a repository, not a model.

| Directory | Graph | Domain | Status |
|---|---|---|---|
| [`oekg/`](oekg/) | **OEKG** — Open Energy Knowledge Graph | energy studies and scenarios | live; the graph itself is served by the Open Energy Platform |
| [`mhpkg/`](mhpkg/) | **mhpkg** — Municipal Heat Planning KG ⚠️ *provisional name* | German *kommunale Wärmeplanung* | early draft |

They are kept side by side because they are developed by the same people, against overlapping
ontologies, for the same platform — and separated inside the repository because they are
genuinely different animals. The OEKG is populated from OEP factsheets and has three tiers of
history behind it; `mhpkg` is fed by a RAG pipeline over published heat plans and currently
consists of one OWL draft. Neither directory's layout is imposed on the other.

> ⚠️ **`mhpkg` is a provisional name.** Do not bake it into IRIs, namespace prefixes or
> published URLs without a rename path. See [`mhpkg/README.md`](mhpkg/README.md).

## What lives where

```text
.
├── docs/                  the documentation source (mkdocs; built by .github/workflows/gh-pages.yml)
│   └── oekg/
│       ├── fields.md      the OEKG's fields, as used by the OEP factsheets
│       └── provenance.md  how the OEKG is built now, and how it used to be
│
├── oekg/                  Open Energy Knowledge Graph — organised by STATUS, not file type
│   ├── shapes/            current, forward-looking: SHACL shapes (⚠️ validate no live graph)
│   ├── eval/              current: competency questions + evaluation shapes
│   ├── legacy/            superseded: the first population pipeline. Do not reuse.
│   └── archive/madbkr_ba/ archived: a finished BA thesis, intact
│
├── mhpkg/                 Municipal Heat Planning KG (provisional name)
│   └── model/             the first OWL draft of the model
│
├── CHANGELOG.md  CITATION.cff  CONTRIBUTING.md  CODE_OF_CONDUCT.md  LICENSE.txt
├── RELEASE_PROCEDURE.md   the family's release convention, adapted
├── USERS.cff              who uses these graphs
│
├── mkdocs.yml             the documentation site config
├── pyproject.toml         dependency groups (uv; this repo is not an installable package)
├── uv.lock                committed lockfile — CI installs exactly this
├── .python-version        the interpreter uv fetches; committed on purpose, see .gitignore
│
└── .github/               issue and PR templates, plus the docs-deploy workflow
                           (documentation is the ONLY thing with CI — no tests, no validation)

# there is no shared/ — see below, its absence is deliberate
```

Every directory above has its own README stating what is in it and **whether it is live**.
Read it before using anything in it. The single most important one:

> 🔴 **Neither graph's data lives in this repository.** The OEKG is served from a
> [Jena Fuseki](https://jena.apache.org/documentation/fuseki2/) dataset that the Open Energy
> Platform writes into over SPARQL; it never round-trips to a file here. See
> [`oekg/README.md`](oekg/README.md) and [`docs/oekg/provenance.md`](docs/oekg/provenance.md).

## Why there is a top-level `oekg/` again

This directory existed until March 2026, when the commits `clean repo` and `clean hierarchy`
deliberately **flattened it**, hoisting its contents to the repository root.

**That was the right call at the time and it is being reversed on purpose.** With one
knowledge graph in the repository, an `oekg/` prefix on every path carried no information —
everything was the OEKG, so the prefix was noise. With a second graph arriving, the prefix is
the only thing that says which graph a file belongs to. It earns its place now; it did not
then.

**Please do not "clean" it away again** without first establishing that this repository is back
down to one graph.

## `shared/`

There is no `shared/` directory. Its absence is deliberate, and this is the rule that governs
it:

> **`shared/`** holds only what is **proven** to serve **both** knowledge graphs, and only
> **infrastructure** — tooling, CI helpers, build scripts. It never holds semantic content:
> no shapes, no vocabulary, no term mappings, no namespace decisions. Nothing enters on the
> expectation of being shared; it enters once both graphs demonstrably use it. If something
> in `shared/` later turns out to serve only one graph, it moves back into that graph's
> directory. **`shared/` does not exist until something earns it — its absence is
> deliberate.**

Nothing qualifies today: `mhpkg` has no shapes and no tooling, so there is no second consumer
for anything. Two candidates were considered and **excluded on principle**, not for lack of a
second consumer:

- **OEO term handling** — the strongest candidate and the most dangerous, because it is
  *semantic*. A shared OEO extraction shaped by the OEKG's needs would silently constrain how
  `mhpkg` models things.
- **Prefixes and namespaces** — three are in play across the two graphs, and the OEKG's own
  artifacts straddle a namespace migration (`http://openenergy-platform.org/ontology/…` →
  `https://openenergyplatform.org/ontology/…`) that this repository has not finished. The MHP
  draft independently carries a vendor namespace from the tool that exported it. A shared
  prefix file would have to assert which of these is canonical, which is a decision neither
  graph's directory layout gets to make.

To admit something, name the two consumers in the pull request and update this section in the
same change.

## Documentation

📖 **<https://openenergyplatform.github.io/oekg/>**

The documentation source is in [`docs/`](docs/), built with
[mkdocs-material](https://squidfunk.github.io/mkdocs-material/) from [`mkdocs.yml`](mkdocs.yml)
and deployed to GitHub Pages by [`.github/workflows/gh-pages.yml`](.github/workflows/gh-pages.yml)
on every push to `production`. The nav mirrors the tree above: shared pages (tech stack,
workflow) on top, then one section per knowledge graph.

To build it locally:

```bash
uv sync --group docs
uv run mkdocs serve
```

Then open **<http://127.0.0.1:8000/oekg/>** — not `/`. See
[CONTRIBUTING.md](./CONTRIBUTING.md#local-setup) for the full setup, including the traps.

## The OEKG in one paragraph

The Open Energy Knowledge Graph is a knowledge graph based on the
[Open Energy Ontology (OEO)](https://github.com/OpenEnergyPlatform/ontology) with the aim of

- representing and describing energy studies and scenarios in a structured, unified and
  flexible, as well as machine readable way
- allowing semi-automated qualitative and (partially) quantitative comparisons of studies and
  scenario projections

It contains a network of entities, their semantic types, properties, and relationships for the
energy system analysis domain. It is based on the [RDF standard](https://www.w3.org/RDF/) and
uses the [Turtle format](https://www.w3.org/TR/turtle/). It is populated through the study and
scenario factsheets on the [OEP](https://github.com/OpenEnergyPlatform/oeplatform), and queried
over a SPARQL endpoint.

## License / Copyright

This repository is licensed under
[Creative Commons Zero v1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).<br>
See [LICENSE.txt](./LICENSE.txt). Everything committed here is published under CC0, so only
commit content that may be redistributed on those terms.

## Contributing

For further contributing infos and conventions see: [CONTRIBUTING.md](./CONTRIBUTING.md)
