# Archive — BA thesis OEKG rework (`madbkr`)

> **Status: ARCHIVED. Closed sub-project. Nothing here is live.**
> This is the complete, finished artifact of a Bachelor's thesis that remodelled the OEKG
> against the Open Energy Ontology. It is kept intact for **provenance and completeness**.
> Do not build on it, do not import from it, and do not treat any script here as tooling.

## What this was

A rework of the OEKG's model: the April 2025 dump of the live graph was retargeted onto
current OEO classes and predicates through a three-step script pipeline, then validated
with SHACL. The headline result is the improvement in SHACL violations, **2695 → 55**:

| Shapes | Data graph | Violations |
|---|---|---|
| `oekg_rework/shacl/oekg_shacl_old_graph_txt` (350 lines) | `oekg_rework/OEKG_Prep.ttl` (pre-rework) | 2695 |
| `oekg_rework/shacl/oekg_shacl_new_graph.txt` (317 lines) | `oekg_rework/output_rework_oekg_final.ttl` (reworked) | 55 |

Both numbers were reproduced exactly with `pyshacl` against the archived reports in
`oekg_rework/shacl/`. **That improvement is the finding worth preserving.** The shapes are
the instrument, not the result.

## What is where

| Path | Contents |
|---|---|
| `scripts/` | the four rework scripts, their `README.md`, and `documentation.pdf` |
| `scripts/documentation.pdf` | **the predicate definitions** — every predicate with definition, domain and range. The most reusable document in this archive. |
| `oekg_rework/` | inputs, intermediates and outputs of the pipeline, plus `shacl/` (shapes and validation reports) |

The scripts ran in the order `reworkOeoBase.py` → `mainRemodel.py` → `labeler.py`.
`hierarchyEXTRA.py` **does not run at all** — see `scripts/README.md`.

## ⚠️ No reproducibility claim is made

Keeping this material is a **provenance** choice, not a reproducibility one. Concretely:

- **The repository pins no dependencies anywhere** — no `requirements.txt`,
  `pyproject.toml`, `setup.py`, `environment.yml` or `Pipfile`. The `owlready2` and
  `rdflib` versions the thesis ran against are unrecorded.
- `sync_reasoner()` additionally requires a **Java** toolchain that nothing here provides
  or documents.
- The shapes carry a **namespace defect**: `oekg_shacl_old_graph_txt` declares
  `http://openenergy-platform.org/…` while `OEKG_Prep.ttl` uses
  `https://openenergyplatform.org/…`, so running it as committed reports
  `Conforms: True` **vacuously**. Reproducing its 2695-violation report requires
  normalising the namespaces first.

All four scripts compile. None of that adds up to "the outputs can be regenerated".

## Replaceability

Retained deliberately, with the redundancy known and accepted: ~11.4M is kept here, of
which only ~1.2M is irreplaceable.

| Item | Size | Replaceable? |
|---|---|---|
| `oekg_rework/oeo-full.owl` | 3.6M | **yes** — vendored OEO v2.8.0, doubly redundant: published in the [`ontology`](https://github.com/OpenEnergyPlatform/ontology) repo, and `oeplatform` parses its own copy from `ONTOLOGY_ROOT` |
| `oekg_rework/OEO_Prep.owl` | 3.2M | yes — generated intermediate |
| `oekg_rework/shacl/Old_Graph_ValidationResults(2695).txt` | 900K | yes — generated report, reproduced exactly |
| `oekg_rework/OEKG_Prep.ttl` | 792K | yes — generated intermediate |
| `oekg_rework/output_rework_oekg_step1.ttl` / `…_step2.ttl` | 20K / 752K | yes — intermediate outputs |
| `oekg_rework/output_rework_oekg_final.ttl` | 776K | yes — final output of the scripts |
| **`oekg_rework/oekg_neu.ttl`** | 792K | **no — irreplaceable.** April 2025 dump of the *live* OEKG from the Fuseki endpoint. There is no other copy of the graph at that date. |
| shapes (350 + 317 lines), competency questions, `documentation.pdf`, the 4 scripts | ~460K | **no — irreplaceable** |

## Paths cited by the thesis

The thesis cites this material by repository path, for the validation reports it was too long to
include. **Those paths no longer exist**, and — contrary to what one might assume — the 2026-08
restructure did not break them: `d5d99fb` "clean repo" (2026-03-02) did, five months earlier. The
restructure only moved the material further, into this directory.

The repository state the thesis actually cites is tagged **`thesis-madbkr-2025`** (commit
`5ea4646`, 2025-06-04), so the cited tree stays reachable by name.

| Cited in the thesis | Where it is today |
|---|---|
| `oekg/oekg_rework/shacl` (footnotes 4 and 5, pp. 32 and 44) | `oekg/archive/madbkr_ba/oekg_rework/shacl` |
| `oekg/oekg_rework` | `oekg/archive/madbkr_ba/oekg_rework` |

Every other reference the thesis makes is stable: the issue links
([`ontology#2064`](https://github.com/OpenEnergyPlatform/ontology/issues/2064),
[`oeplatform#2008`](https://github.com/OpenEnergyPlatform/oeplatform/issues/2008)) and the OEO
modules wiki. `scripts/documentation.pdf` is cited only by name in prose, never by URL.

## Relation to the rest of `oekg/`

- **`oekg_rework/shacl/oekg_shacl_old_graph_txt` (350 lines) is now the ONLY copy** of the
  pre-rework instrument. Until 2026-08-13 a byte-identical copy sat in `oekg/shapes/` and was
  presented there as the current, forward-looking shapes — which it never was. It was removed;
  this copy stays, as the instrument that produced the 2695-violation baseline.
- `oekg_rework/shacl/oekg_shacl_new_graph.txt` (317 lines) is byte-identical to
  **`oekg/shapes/oekg_shapes.ttl`** (which until 2026-08-13 was `oekg/eval/oekg_shacl.txt`). The
  two copies have different jobs: this one is the frozen thesis record, the other is the graph's
  canonical working copy.
- `oekg/legacy/` is a *different* superseded pipeline — the original 2023 placeholder →
  notebook → Turtle route. It is not part of this thesis.
