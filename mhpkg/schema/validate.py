#!/usr/bin/env python3
"""Validate the example instances against the MHPKG shapes.

WHY THIS EXISTS RATHER THAN A `pyshacl` COMMAND LINE. The shapes come in two files — the generated
`generated/mhpkg_target_scenario.shacl.ttl` and the hand-written `mhpkg_iri_policy.shacl.ttl` — and
`pyshacl` accepts repeated `-s` flags while SILENTLY USING ONLY THE LAST ONE. Two `-s` flags do not
merge; the first shapes graph is discarded without a warning.

That is not a theoretical hazard. It was hit while building this slice: the first run of the valid
example reported `Conforms: True` with exit 0 against both files, and the generated shapes had not
been consulted at all. Deleting a required label still reported conformance. The same invocation
would have made a broken pipeline look healthy in CI.

So the shapes are merged into one graph here, and the merge is not optional. Same class of trap as
`uv sync --frozen` in MH-04 and `gen-shacl`'s exit-0-on-error: a check that reports success by
doing nothing.

The negative control is asserted, not merely run. `kassel_invalid.ttl` must fail, and it must fail
for each of the reasons it is annotated with — a negative control that stopped catching four of its
six cases would otherwise still be "failing" and still look fine.

Usage:
    python mhpkg/schema/validate.py
Exit codes:
    0  the valid example conforms AND every expected violation was found
    1  otherwise
"""

from __future__ import annotations

import sys
from pathlib import Path

from pyshacl import validate
from rdflib import Graph

HERE = Path(__file__).parent
SHAPE_FILES = [
    HERE / "generated" / "mhpkg_target_scenario.shacl.ttl",
    HERE / "mhpkg_iri_policy.shacl.ttl",
]
VALID = HERE / "examples" / "kassel_valid.ttl"
INVALID = HERE / "examples" / "kassel_invalid.ttl"

# Each expected violation, as (label, constraint component, focus-node fragment, discriminator).
#
# The discriminator is load-bearing, not decoration. Cases 6b and 6c are both `In` violations on
# one focus node, and 6a and 6d are both `MinInclusive` on that same node — so an expectation
# written as (component, focus) alone would be satisfied by a SINGLE violation and would print
# four ticks for two catches. Pinning a third field makes each line an independent assertion.
#
# It is a `Result Path:` line for property-level constraints, and a `Source Shape:` line for
# node-level `sh:pattern`, which reports no path at all.
EXPECTED = [
    ("1  Tier-1 AGS missing its leading zero",
     "Pattern", "municipality/AGS_6611000", "Source Shape: mhpkg_shapes:MunicipalityAreaIri"),
    ("2  Tier-3 UUIDv4 where the policy requires v5",
     "Pattern", "9f1e2d3c-4b5a-4c7d", "Source Shape: mhpkg_shapes:OrganisationIri"),
    ("3a non-ASCII instance IRI",
     "Pattern", "Kassel-W", "Source Shape: mhpkg_shapes:NoNonAsciiInstanceIri"),
    ("3b …which is also not a UUID, so it fails the Tier-3 shape too",
     "Pattern", "Kassel-W", "Source Shape: mhpkg_shapes:OrganisationIri"),
    ("4a missing publication date",
     "MinCount", "heatplan/AGS_06611000_2024-03-15", "Result Path: oeo:OEO_00390096"),
    ("4b German label as @de instead of a plain literal",
     "Datatype", "heatplan/AGS_06611000_2024-03-15", "Result Path: rdfs:label"),
    ("5  Tier-2 IRI missing its date discriminator",
     "Pattern", "targetscenario/AGS_06611000>", "Source Shape: mhpkg_shapes:TargetScenarioIri"),
    ("6a negative energy consumption",
     "MinInclusive", "a878a3a1-b856-5aaf", "Result Path: oeo:OEO_00140178"),
    ("6b energy carrier outside the controlled vocabulary",
     "In", "a878a3a1-b856-5aaf", "Result Path: oeo:OEO_00000523"),
    ("6c sector slot holding an energy carrier",
     "In", "a878a3a1-b856-5aaf", "Result Path: oeo:OEO_00000505"),
    ("6d target year before the WPG existed",
     "MinInclusive", "a878a3a1-b856-5aaf", "Result Path: oeo:OEO_00020440"),
    ("7  undeclared property on a closed shape",
     "Closed", "b1c2d3e4-f5a6", "Result Path: rdfs:seeAlso"),
]

# Consequences of the cases above rather than cases in their own right, listed so the report
# accounts for every violation instead of quietly leaving two unexplained. The broken plan node in
# case 4 points at a target scenario and an organisation that the invalid file does not define, so
# `sh:class` cannot confirm their type. Real failures, just not designed ones.
EXPECTED_CASCADES = [
    ("dangling target scenario reference from case 4",
     "Class", "heatplan/AGS_06611000_2024-03-15", "Result Path: obo:BFO_0000051"),
    ("dangling organisation reference from case 4",
     "Class", "heatplan/AGS_06611000_2024-03-15", "Result Path: oeo:OEO_00000510"),
]


def shapes_graph() -> Graph:
    """Merge every shapes file into ONE graph. See the module docstring for why this matters."""
    g = Graph()
    for f in SHAPE_FILES:
        g.parse(f, format="turtle")
    return g


def run(data: Path, shapes: Graph) -> tuple[bool, str]:
    conforms, _, text = validate(
        Graph().parse(data, format="turtle"),
        shacl_graph=shapes,
        advanced=True,
    )
    return conforms, text


def main() -> int:
    shapes = shapes_graph()
    print(f"shapes: {len(shapes)} triples from {len(SHAPE_FILES)} files (merged, not stacked)")
    ok = True

    # --- The positive case ---
    conforms, text = run(VALID, shapes)
    print(f"\n{VALID.name}: {'CONFORMS' if conforms else 'FAILED'}")
    if not conforms:
        ok = False
        print(text)

    # --- The negative control ---
    conforms, text = run(INVALID, shapes)
    print(f"\n{INVALID.name}: {'conforms — WRONG, this must fail' if conforms else 'non-conforming, as intended'}")
    if conforms:
        return 1

    blocks = text.split("Constraint Violation")[1:]

    def caught(component: str, focus: str, discriminator: str) -> bool:
        return any(
            component in b and focus in b and discriminator in b
            for b in blocks
        )

    print("\nexpected violations:")
    for label, component, focus, discriminator in EXPECTED:
        hit = caught(component, focus, discriminator)
        print(f"  {'✅' if hit else '❌ NOT CAUGHT'}  {label}")
        ok = ok and hit

    print("\nexpected cascades (consequences, not designed cases):")
    for label, component, focus, discriminator in EXPECTED_CASCADES:
        hit = caught(component, focus, discriminator)
        print(f"  {'✅' if hit else '❌ NOT CAUGHT'}  {label}")
        ok = ok and hit

    total = len(EXPECTED) + len(EXPECTED_CASCADES)
    print(f"\n{len(blocks)} violations reported, {total} accounted for")
    if len(blocks) != total:
        print("  ⚠️ unexplained violations — the report above is incomplete")
        ok = False

    print("\nOK" if ok else "\nFAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
