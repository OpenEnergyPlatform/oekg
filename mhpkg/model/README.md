# The Termboard model, and how a new export reaches the schema

MHPKG is modelled in [Termboard](https://termboard.com/), by two people, and exported here every few
weeks. This directory holds those exports and the one tool that compares an export with the
[LinkML schema](../schema/).

**The tool compares; it never converts.** Termboard does not know which box is a class, which is an
individual and which is a literal. `2030`, `MWh`, `Kassel` and `municipal heat plan` are all just
boxes. So the step from a sketch to a schema stays a human decision. What the tool does is
make that step fast: it lists everything the new export says that the schema does not, and
everything the schema has that the export no longer says.

## Files

| Path | What it is |
|---|---|
| `schema_<YYYYMMDD>.json` | **a Termboard JSON export: the one the tool reads.** Export it from Termboard as JSON and name it by date |
| `mhpkg_model_draft_<YYYYMMDD>.owl` | the Termboard OWL export of the same board. Kept for people, **not readable by machines** — see below |
| `mhpkg_model_first_draft.owl` | the August 2026 first draft, OWL only. Historical |
| [`termboard_mapping.yaml`](termboard_mapping.yaml) | **the decisions**: for every Termboard name, what it is in the schema, or why it is not there |
| [`termboard_delta.py`](termboard_delta.py) | the comparison. Needs the `schema` group |

## The loop

```bash
# 1. export the board from Termboard as JSON and save it here as schema_<YYYYMMDD>.json
#    (the OWL export may sit next to it for people to read)

# 2. see what changed. The newest schema_*.json is used by default.
uv run --group schema python mhpkg/model/termboard_delta.py

# 3. for each finding, decide, then record the decision:
#      a new name that the schema already covers      -> add it to termboard_mapping.yaml
#      a new name that the schema must grow to cover  -> edit ../schema/mhpkg_target_scenario.yaml,
#                                                        then map it
#      a new name that OEO and MHPO have no term for  -> a TERM REQUEST block in the schema,
#                                                        `term_request: <n>` in the mapping
#      a name that is not ready                       -> `deferred:` or `open:`, with the reason

# 4. regenerate, then check everything
uv run gen-shacl --closed mhpkg/schema/mhpkg_target_scenario.yaml \
  > mhpkg/schema/generated/mhpkg_target_scenario.shacl.ttl
uv run --group schema python mhpkg/schema/check_generated.py
uv run --group graph  python mhpkg/schema/validate.py
uv run --group schema python mhpkg/model/termboard_delta.py --check   # exit 0 = nothing unaccounted
```

`--check` exits 1 while anything is unaccounted for. Names that are marked `term_request`, `deferred`
or `open` are listed as known and do not count as failures. They are holes that someone recorded on
purpose.

### What the report checks

1. **Unmapped terms and relations**: new in Termboard, and no decision recorded yet.
2. **Mapped names no longer in the export**: removed or renamed in Termboard. A rename shows up
   twice, once here and once in 1.
3. **Mapping targets not in the schema**: the mapping points at a class, slot or enum value
   that does not exist.
4. **Typed edges that the schema does not realise.** Termboard draws `A —refers to sector→ sector`,
   and the schema must let class A carry `covers_sector` with a sector range. Termboard's `part of`
   is checked as the inverse of `has part`.
5. **Untyped `related to` edges with no typed counterpart**: two boxes connected by a relation that
   nobody has named yet.

Terms are matched **by name**, not by Termboard id. An id identifies a *box on the board*: the
2026-09-15 draft has four `year` boxes with four ids, and they are one concept.

## Why the JSON export, and not the OWL one

The OWL export was the reason for the earlier rule that Termboard output is never machine-consumed.
Its defects are real, and all of them were verified:

- **It is not valid RDF/XML.** It nests an `owl:Restriction` node inside `rdfs:subClassOf
  rdf:parseType="Resource"`, where only property elements are allowed. rdflib rejects both
  `mhpkg_model_first_draft.owl` and `mhpkg_model_draft_20260915.owl` at the first `subClassOf`.
- **Everything is an `owl:Class`**: values, units, datatypes and individuals included.
- **Umlauts are stripped from IRIs**: `Kassel Wärme Ingenieurbüro` becomes `…#Kassel_Wrme_Ingenieurbro`.
  Fed through the [IRI policy](../schema/mint_slice.py), that silently mints a *different*
  organisation.

The JSON export has none of these defects. Names keep their umlauts, relations are typed
(`Composition`, `Attributive`, `Other`) and named, and nothing claims to be OWL. That is enough
to **compare** against, but not enough to **generate** from, because the class/individual/literal
question is still unanswered. The rule therefore stands, with one exception: the JSON export may be
read *as input to a check*, and nothing from Termboard reaches the schema or the graph without a
human decision recorded in the mapping.

## Status of the 2026-09-15 draft

Carried into the schema in full. `--check` passes, with these recorded holes:

| Termboard | Disposition |
|---|---|
| `is about municipality` | TERM REQUEST 1: nothing relates a plan to the area it plans |
| `on behalf of` | TERM REQUEST 3: the planning authority's role; also MH-15 |
| `part of convoi` | TERM REQUEST 6: joint planning by several municipalities |
| `has numerator`, `has denominator` | TERM REQUEST 7: what a share is a share of |
| `has uuid`, `UUID` | open: the IRI already is the identity (MH-02, #61) |
| `aggregated potential analysis` | deferred: the draft gives it no content |
| an unnamed self-edge on `final energy consumption value` | open: most likely a stray drag on the board |

For the people drafting the model, three small fixes at the source would make the next export
cleaner: fix the typo `tartget scenario indicators`, delete the unnamed self-edge, and remove the
`related to` edges that duplicate a typed one. The tool accepts all three, but each one is noise.
