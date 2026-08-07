# The MHPO pin

**MHPO is the T-Box.** All classes and properties for municipal heat planning live in
[`municipal-heat-planning-ontology`](https://github.com/OpenEnergyPlatform/municipal-heat-planning-ontology).
This repository does not define domain terms — it **cites** them, and this directory is the
record of which terms may be cited.

| File | What it is |
|---|---|
| [`pin.txt`](pin.txt) | the MHPO commit this list was generated from |
| [`terms.csv`](terms.csv) | **generated** — every term MHPO declares or uses |
| [`extract_terms.py`](extract_terms.py) | regenerates `terms.csv` from the pin; stdlib only |

> ⚠️ **`terms.csv` is generated. Do not edit it by hand.** Change `pin.txt`, re-run the script,
> and commit both together.

## Why a term list and not the ontology

MHPO has **no releases and no tags**, and `https://purl.org/mhpo` redirects to the repository's
GitHub page rather than to an ontology — individual term IRIs return 404. The only consumable
artifact is `src/ontology/mhpo-edit.owl` on a branch, so any pin is a commit SHA by hand.

Given that, a list beats a copy: it is what the LinkML schema actually needs (an IRI to cite and
a label to recognise it by), it diffs one readable line per term instead of 57 KB of OWL
functional syntax, and it requires no ODK, Docker or ROBOT — so working on this graph stays a
`uv sync` away.

## Usage

```bash
python mhpkg/mhpo/extract_terms.py           # regenerate terms.csv from the pin
python mhpkg/mhpo/extract_terms.py --check   # fail if terms.csv drifts from the pin  (CI)
python mhpkg/mhpo/extract_terms.py --latest  # report what changed on MHPO's develop  (report only)
```

To take an MHPO update: run `--latest` to see what moved, edit `commit:` in `pin.txt`,
re-run without flags, and commit `pin.txt` and `terms.csv` in the same change.

## The two checks, and why they are separate

- **Consistency** (`--check`, on pull requests): regenerating from **the pinned commit** must
  reproduce `terms.csv` exactly. This catches hand-edits and stale regeneration, and it can
  **never fail because MHPO moved** — the pin is the input.
- **Freshness** (`--latest`, on a schedule): compares the pin against MHPO's `develop` HEAD and
  **reports**. It never fails a build. MHPO is owned by other people and has several branches in
  flight; a pull request here should not turn red because a co-worker committed there.

## Deprecated terms fail loudly

`terms.csv` carries `deprecated` and `replaced_by` columns. When a cited term is deprecated
upstream, the check **fails and names the successor** — it never rewrites automatically. A
replacement can be narrower, broader or a split, so it is a semantic change that deserves a human.
As of the current pin, **no MHPO term is deprecated**, so this path is untested in anger.

## What the list contains, and one honest gap

The list covers every term MHPO **declares or uses** — not just its own namespace — because the
LinkML schema's `slot_uri` values point at RO and BFO relations, not at MHPO. At the current pin:

| Source | Terms | |
|---|---|---|
| `mhpo` | 34 | all classes; MHPO mints **no relations of its own**, which is correct OBO practice |
| `cco` | 4 | the parents MHPO subclasses under |
| `bfo` | 3 | including `BFO_0000050/51` (part of / has part) |
| `ro` | 3 | `RO_0000052`, `RO_0000053`, `RO_0000087` |
| `iao` | 3 | two are annotation properties (`definition`, `alternative label`) |
| `oeo` | 1 | `OEO_00360020` — the OEO alignment is real but currently minimal |

> ℹ️ **12 external labels are `unresolved`, and that is recorded rather than guessed.** MHPO's
> imports are not resolved in the editors' file, so labels for BFO, RO, CCO and OEO terms simply
> are not present in it. Resolving them needs ROBOT and the ODK toolchain, which this repository
> deliberately does not require. The IRIs — the part the schema needs — are complete.

> 🔴 **MHPO cites `RO_*` relations it neither declares nor imports.** Its import products are BFO,
> IAO, OEO and CCO; the only `ObjectProperty` declaration in the editors' file is `BFO_0000051`.
> `RO_0000052`, `RO_0000053` and `RO_0000087` are used in axioms but dangle. They resolve at ODK
> build time or not at all. Worth raising with MHPO's maintainers — it is their repository.

## Provisional

This directory's location is provisional: **MH-03** decides the `mhpkg/` layout and may move it.
