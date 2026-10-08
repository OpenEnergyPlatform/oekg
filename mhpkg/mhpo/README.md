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

MHPO **has released** — `v0.1.0` on 2026-09-30, its first — but **none of its published IRIs
resolve**. Term IRIs (`…/ontology/MHPO_00020003`) return 404, and so do the release's own ontology
and version IRIs, which v0.1.0 writes as `https://purl.org/mhpo//mhpo-base.owl` and
`…//releases/2026-09-29/…` (double slash, and a date where the tag says `0.1.0`).
`https://purl.org/mhpo/ontology/mhpo.owl` does resolve, but to `mhpo-edit.owl` on the moving
`production` branch, not to a release. So the only reliably consumable artifact is still
`src/ontology/mhpo-edit.owl` at a commit. **The pin is the commit a release tag points at** — a tag
names it, but a tag can be moved and a SHA cannot.

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

To take an MHPO update: run `--latest` to see what moved, edit `commit:` (and `tag:`) in
`pin.txt`, re-run without flags, and commit `pin.txt` and `terms.csv` in the same change. Prefer a
release commit over a `develop` HEAD. Then re-run the schema checks in `../schema/README.md` —
nothing in this directory checks the schema's IRIs against the list.

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
LinkML schema's `slot_uri` values point at RO and BFO relations, not at MHPO. At the current pin
(v0.1.0):

| Source | Terms | |
|---|---|---|
| `mhpo` | 40 | 39 classes and its **first own relation**, `represents heat supply area` |
| `iao` | 7 | the new parents — `plan specification`, `objective specification`, … — and three annotation properties |
| `oeo` | 5 | `region of relevance`, `quantity value`, `has spatial region`, `quantity value of`, and an annotation property |
| `bfo` | 4 | including `BFO_0000050/51` (part of / has part) |
| `ro` | 2 | `RO_0000052` (characteristic of), `RO_0000053` (has characteristic) |
| `cco` | 2 | still cited although CCO is no longer imported — see below |

> ℹ️ **18 external labels are `unresolved`, and that is recorded rather than guessed.** MHPO's
> imports are not resolved in the editors' file, so labels for BFO, RO, IAO, CCO and OEO terms
> simply are not present in it. Resolving them needs ROBOT and the ODK toolchain, which this
> repository deliberately does not require. The IRIs — the part the schema needs — are complete.

> ✅ **Every cited term is now declared in the editors' file.** Before v0.1.0, MHPO used
> `RO_0000052`, `RO_0000053` and `RO_0000087` in axioms without declaring or importing them. v0.1.0
> declares the two it still uses and replaced *has role* (`RO_0000087`) by *has characteristic*
> (`RO_0000053`) throughout. RO is still not imported; MHPO tracks that in its own issue #38.

> ⚠️ **v0.1.0 dropped its CCO import but still cites two CCO terms.** `ont00001808` (CCO
> *is about*) appears in axioms on `initial suitability assessment` and `shortened heat planning`,
> and `ont00001754` is used as an annotation property. Both are declared locally, so nothing
> dangles, but their meaning now comes from nowhere MHPO imports. IAO, which MHPO does import, has
> its own `is about` (`IAO_0000136`).

## Provisional

This directory's location is provisional: **MH-03** decides the `mhpkg/` layout and may move it.
