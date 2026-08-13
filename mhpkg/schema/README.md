# The MHPKG data shape

**LinkML authors the data shape; MHPO owns the ontology.** This directory holds the LinkML schema
for MHPKG, the SHACL shapes generated from it, and worked examples that prove the shapes reject
what they should.

> **Status: first cut, one slice.** It covers a municipal heat plan, the target scenario inside it
> and one final energy consumption value — deep enough to be honest, small enough to finish. It is
> not the schema for the whole domain, and the [findings](#what-this-slice-established) below matter
> more than the coverage.
>
> **This directory's location is provisional.** **MH-03** decides the `mhpkg/` layout and may move
> it, as it may move [`../mhpo/`](../mhpo/).

## The two guardrails

Both were decided before this schema existed and neither is reopenable here.

1. **LinkML never mints domain terms.** Every class carries a `class_uri` and every slot a
   `slot_uri` pointing at a term MHPO or OEO already declares. A needed term that does not exist is
   an **MHPO term request**, not a new LinkML element — see [Term requests](#term-requests-open).
2. **`gen-owl` stays off.** MHPO owns the OWL rendering of this domain. A second one generated here
   would be two competing definitions of one domain, which is the duplication the single-T-Box
   decision exists to prevent.

## Files

| Path | What it is |
|---|---|
| [`mhpkg_target_scenario.yaml`](mhpkg_target_scenario.yaml) | the schema — **the only thing you edit** |
| [`generated/mhpkg_target_scenario.shacl.ttl`](generated/) | **generated.** Do not hand-edit |
| [`mhpkg_iri_policy.shacl.ttl`](mhpkg_iri_policy.shacl.ttl) | **hand-written.** The IRI policy as shapes — LinkML cannot express it |
| [`mint_slice.py`](mint_slice.py) | mints the example IRIs, so no UUID in this directory is hand-typed |
| [`validate.py`](validate.py) | validates both examples and **asserts the negative control catches every case** |
| [`examples/kassel_valid.ttl`](examples/kassel_valid.ttl) | a conformant instance |
| [`examples/kassel_invalid.ttl`](examples/kassel_invalid.ttl) | the negative control — every node wrong in a different way |

## Commands

```bash
uv sync --group schema --group graph        # linkml (88 pkgs) + pyshacl and rdflib (11)

# regenerate the shapes; commit the YAML and the generated file together
uv run gen-shacl --closed mhpkg/schema/mhpkg_target_scenario.yaml \
  > mhpkg/schema/generated/mhpkg_target_scenario.shacl.ttl

uv run python mhpkg/schema/mint_slice.py   # print the slice's IRIs and how they are derived
uv run python mhpkg/schema/validate.py     # validate; exit 0 only if the negative control holds
```

Verified with linkml 1.11.1, pyshacl 0.40.1, rdflib 7.6.0, against MHPO at pin
[`34776b6`](../mhpo/pin.txt) and OEO 2.13.0.

> ⚠️ **Do not validate with two `-s` flags.** `pyshacl` accepts repeated `-s` and **silently uses
> only the last one** — the earlier shapes graph is discarded with no warning. This was hit while
> building the slice: `pyshacl -s generated/… -s mhpkg_iri_policy.… kassel_valid.ttl` reported
> `Conforms: True` and exit 0 while consulting neither, and still reported conformance after a
> required label was deleted. `validate.py` merges the shapes into one graph, which is why it
> exists instead of a shell one-liner.

## What this slice established

The ticket's premise was that the LinkML-authors-SHACL decision was made on reasoning rather than
evidence. It holds — with two caveats that are load-bearing.

**✅ The mapping works, and the pivot is `class_uri`.** `gen-shacl` puts the `class_uri` straight
into `sh:targetClass`, so the generated shapes constrain **MHPO and OEO IRIs directly** rather than
some LinkML-shaped shadow of them. Nothing is minted and nothing is translated.

**✅ MHPO's reification is not the problem it looked like.** The worry was that BFO-style modelling
reifies what LinkML would express as a direct slot. In this slice it does not bite, because the two
halves reify the *same way*: OEO's `quantity value` already hangs the number and the unit off a
value node, which is exactly what LinkML would do. MHPO's heavy role reification —
`heat plan area` *bearer of* `heat plan area role` — is real but sits in the **area** subtree, and
this slice does not enter it. **That is a deferral, not a clearance:** the areas and roles are
three quarters of MHPO's 34 classes, and the first ticket that models them will meet it.

**✅ Enums are the pattern to reuse.** OEO models units, carriers and sectors as *classes*, but a
statistic is about the carrier *type*, so pointing at a class IRI is unavoidable punning. A LinkML
enum whose every `meaning:` is an OEO IRI generates `sh:in` — a real value-set constraint instead
of `sh:nodeKind sh:IRI`, which accepts any IRI including a carrier pasted into the sector slot.
This is not invented: `oekg/shapes/oekg_shapes.ttl` already enumerates ~120 OEO class IRIs by hand
for the same property. The enum reaches the same place from a generated source.

> ⚠️ Those OEKG shapes are otherwise unusable, and it is worth knowing why — though fixing them is
> out of scope, as the predecessor map settled. They declare `oeo` as
> `http://openenergy-platform.org/ontology/oeo/` (hyphenated, `http`) and use readable property
> names like `oeo:covers_energy_carrier` that OEO does not define. The namespace **does** resolve —
> 200, redirecting to the un-hyphenated host — but IRIs are *identity, not addresses*: OEO mints
> every term under `https://openenergyplatform.org/ontology/oeo/`, so the hyphenated string is a
> different term that happens to serve the same page. Resolving is not matching.
>
> `linkml-lint` warns that this schema's `oeo` prefix is not canonical and wants the hyphenated
> form. That is a **stale prefix-registry entry**, not a defect here. The warning is accepted rather
> than silenced, so `linkml-lint` on this schema reports one known problem.

**🔴 The IRI policy cannot be generated.** SHACL constrains a node's own IRI with `sh:pattern` at
**node** level, and LinkML has no way to emit that. Measured on linkml 1.11.1:

- a **type-level** `pattern` is dropped — silently when the type has a `uri:`; with a logged
  `ERROR: No URI for type X` **and exit code 0** when it does not;
- a **slot-level** `pattern` is emitted correctly;
- on an `identifier: true` slot it is emitted against `mhpkg_schema:id`, an invented property that
  appears in no instance triple — well-formed, and it can never fire.

So the machine-checkable half of the IRI policy that MH-02 delegated here lives in a hand-written
companion file. **This is direct input to MH-07: the generated-artifacts contract cannot say
"everything is generated".**

**🔴 Enum membership cannot be checked by anything in this repository.** OEO's `energy carrier` has
four asserted subclasses and all are abstract; `natural gas` is a subclass of `gas mixture` and
qualifies only *by inference*, through a disposition equivalence axiom. The OEKG's shape file admits
this in a comment — "energy carrier subclassed and as inferred". Confirming a candidate IRI really
is a carrier needs a reasoner, and this repository has `pyshacl` and `rdflib`, neither of which
reasons; MH-01 deliberately kept ROBOT, ODK and Docker out of the contributor setup. The enums are
hand-curated snapshots that can drift from OEO silently — the drift problem MH-01 solved for MHPO
terms, recurring one level down. **Input to MH-07 and MH-12.**

**🔴 Two decided policies collide over the municipality.** MH-02 §6 rules that
`Stadt Kassel, der Bürgermeister` is not a second entity and reuses `municipality/AGS_06611000`. But
the only class available for that IRI is `municipality area` — a spatial region, and a region cannot
commission a plan. There is no term anywhere in MHPO or OEO for the municipality as a legal body.
The IRI shapes make it concrete rather than arguable: the municipality shape requires
`.../municipality/AGS_<8 digits>` and the organisation shape requires `.../organisation/<UUIDv5>`,
so **one IRI cannot satisfy both**. Typing it as an organisation is a validation failure, not a
workaround — which leaves the planning authority absent from the example, and WPG §12 makes it a
statutory party. **This one needs a human.**

**⚠️ The publication date and three other slots borrow relations whose declared domain is wrong.**
`covers energy carrier` and `covers sector` declare domain `study`; `has scenario year value`
declares domain `scenario factsheet` *and* range `xsd:dateTime`; `has publication date` declares
domain `report`, and MHPO puts a heat plan under `plan specification`. OWL domains are inferential
rather than constraining, so nothing complains — a reasoner will quietly infer that **every MHPKG
consumption value is a study**, and SHACL cannot see this at all. Each is annotated at its slot and
folded into the term requests.

**⚠️ Closed shapes reject provenance.** `--closed` is what stops a pipeline inventing its own
predicates, and it also rejects *any* extra triple — including which PDF, which page, which model,
what confidence. Provenance modelling is already fog on the map; case 7 of the negative control is
where it turns from a modelling question into a validation failure.

**⚠️ German labels must be plain literals.** `range: string` generates `sh:datatype xsd:string`, and
a `"…"@de` literal has datatype `rdf:langString` — a different datatype, so it is **rejected**. The
obvious, correct-looking way to mark a German label as German fails. Worth knowing before a RAG
pipeline emits thousands of them; whether to widen the shape or forbid the tag is MH-07's.

**⚠️ Turtle cannot abbreviate these IRIs.** MH-02's IRIs carry path segments
(`.../heatplan/AGS_…`), and a Turtle prefixed name may not contain an unescaped `/`. So
`mhpkg:heatplan/AGS_06611000_2024-03-15` is a **syntax error**, and hand-written instance data must
use full angle-bracket IRIs. Cosmetic, but it bites immediately and silently looks like a typo.

## Term requests, open

None is worked around in the schema; each appears as a commented `TERM REQUEST` block in
[`mhpkg_target_scenario.yaml`](mhpkg_target_scenario.yaml) at the position it would occupy, so the
hole is visible in the artifact. They belong to MHPO's owners — filing is
[**MH-05**](../mhpo/README.md)'s neighbour, not this ticket's.

1. **Which area a plan is for.** Nothing relates a *plan* to the area it plans. Without it a heat
   plan cannot say where it applies.
2. **The municipality as a legal body**, distinct from its territory — the collision above.
3. **The role a body plays towards a plan.** Planning authority (statutory, WPG §12) versus
   contracted planner. `has organisation` collapses them into one relation.
4. **The AGS as data**, not only inside an IRI. A key recoverable by string surgery on an
   identifier cannot be queried or typed as a key. OEO's `unique individual identifier` is an
   *annotation* property, so it will not serve.
5. **Relations from a quantity value to its temporal region, energy carrier and sector** — or the
   existing `covers …` relations with domains widened past `study`.

## Deliberately not here

- **The rest of the domain.** One slice, done properly.
- **Which generators are authoritative and how output is published** — that is **MH-07**, and it is
  downstream of seeing one generator work. It now also inherits three constraints from above: the
  hand-written companion file, enum drift, and the `@de` question.
- **Loading anything into Fuseki** — **MH-11**. Nothing here has been near a triple store.
- **A validation CI job** — **MH-12**. `validate.py` exits non-zero on failure so that job has
  something to call, but wiring it into `checks.yml` is not this ticket's.
