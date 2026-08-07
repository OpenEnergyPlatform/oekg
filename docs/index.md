---
hide:
  - footer
---

# Open Energy Family — Knowledge Graphs

This site documents **two knowledge graphs** developed in one repository. They share a
repository, a tech stack and a platform. They do **not** share a model.

<div class="grid cards" markdown>

- **[OEKG — Open Energy Knowledge Graph](oekg/index.md)**

    Energy studies and scenarios, described against the
    [Open Energy Ontology](https://github.com/OpenEnergyPlatform/ontology). Live: populated by
    the Open Energy Platform's scenario-bundle factsheets and served from a SPARQL endpoint.

- **[Municipal Heat Planning KG](mhpkg/index.md)**

    German *kommunale Wärmeplanung* — structured data extracted from published municipal heat
    plans. Early draft. The name `mhpkg` is provisional.

</div>

## Start here

| If you want to… | Go to |
|---|---|
| query the OEKG | [SPARQL endpoint](oekg/endpoint.md) |
| know what fields a study or scenario has | [Factsheet fields](oekg/fields.md) |
| understand how heat-plan data is produced | [Workflow](workflow.md) |
| know what tools and formats are used | [Tech stack](tech-stack.md) |
| understand why this repository looks the way it does | [OEKG provenance](oekg/provenance.md) |

## One thing worth knowing immediately

**Neither graph lives in this repository as a file you can download and be done with.** The
OEKG is served from a Jena Fuseki dataset and is written to by the platform, not by commits
here; the Turtle files in `oekg/` are historical. The heat-planning graph is still a draft.

If you came looking for "the graph", the [SPARQL endpoint](oekg/endpoint.md) is what you want,
and [OEKG provenance](oekg/provenance.md) explains why the repository is arranged the way it is.

## Status, honestly

| | OEKG | Municipal Heat Planning KG |
|---|---|---|
| **Model** | Open Energy Ontology (OEO) | [MHPO](https://github.com/OpenEnergyPlatform/municipal-heat-planning-ontology), which draws on OEO |
| **How it is populated** | OEP scenario-bundle factsheets, over SPARQL | RAG pipeline over published heat plans |
| **Where the data lives** | Jena Fuseki dataset | not yet decided |
| **Maturity** | live, in use | one OWL draft, 21 classes |
| **Validation** | shapes exist but validate no live graph | none yet |

That last row is not an oversight. See [Tech stack](tech-stack.md) for what is settled and what
is still open — including the model source of truth, which is genuinely undecided.
