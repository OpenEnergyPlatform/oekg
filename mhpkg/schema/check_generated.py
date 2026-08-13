#!/usr/bin/env python3
"""Check that the committed SHACL still matches the schema it was generated from.

The drift check for `generated/`, in the spirit of `mhpkg/mhpo/extract_terms.py --check`: regenerate
from the source and compare. Someone editing `mhpkg_target_scenario.yaml` and forgetting to re-run
`gen-shacl` is the failure this catches.

WHY IT CANNOT BE A BYTE DIFF, which is the obvious way to write it and is wrong here:

    `gen-shacl` output is NOT byte-stable across runs. Every `sh:property` is a blank node, and
    rdflib mints fresh blank-node ids per process, so the property blocks come out in a different
    order every time. Measured: three consecutive runs of the same schema produced three different
    SHA-256 sums. `PYTHONHASHSEED=0` does NOT fix it — three more runs, three more sums — so this is
    blank-node id generation, not dict-ordering.

    A `diff`-based check would therefore fail on every single run while nothing was wrong, which is
    worse than no check: it trains people to ignore it.

So the comparison is GRAPH-ISOMORPHIC — `rdflib.compare.to_isomorphic`, which canonicalises blank
node labels and compares the graphs as graphs. Two serialisations of the same shapes compare equal;
a genuine change to a constraint does not.

⚠️ This needs the `schema` dependency group (it runs the generator), whereas `validate.py` needs only
`graph`. That split is deliberate and comes from MH-04: `linkml` is 88 of the 95 packages, and a job
that only validates data has no reason to install a generator. Keep the two scripts separate for
that reason — do not fold this into `validate.py`.

The generator runs IN-PROCESS rather than as a subprocess. Two reasons: the `gen-shacl` console
script is not always on `PATH` even when `linkml` is installed, and running in-process lets this
script capture the generator's log records directly — which matters, because that is the only way to
see the failures it reports without failing.

Usage:
    uv run --group schema python mhpkg/schema/check_generated.py
Exit codes:
    0  the committed file is graph-isomorphic to a fresh generation
    1  it has drifted, or the generator logged an error — re-run gen-shacl and commit the result
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from linkml.generators.shaclgen import ShaclGenerator
from rdflib import BNode, Graph
from rdflib.compare import to_isomorphic

HERE = Path(__file__).parent
SCHEMA = HERE / "mhpkg_target_scenario.yaml"
COMMITTED = HERE / "generated" / "mhpkg_target_scenario.shacl.ttl"

# `closed=True` must match the `--closed` flag in the README command. It is a deliberate choice
# rather than a default: closed shapes are what stop a pipeline inventing its own predicates.
CLOSED = True


class ErrorCatcher(logging.Handler):
    """Collect ERROR-or-worse records emitted while generating.

    `gen-shacl` reports real failures through the logger and STILL SUCCEEDS — a dropped type-level
    `pattern` logs `No URI for type X` and the process exits 0. So the absence of an exception is not
    evidence that generation worked, and the log has to be treated as part of the result.
    """

    def __init__(self) -> None:
        super().__init__(level=logging.ERROR)
        self.records: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.records.append(record.getMessage())


def main() -> int:
    catcher = ErrorCatcher()
    logging.getLogger().addHandler(catcher)
    try:
        turtle = ShaclGenerator(str(SCHEMA), closed=CLOSED).serialize()
    except Exception as exc:  # noqa: BLE001 — any generator failure is a check failure
        print(f"generation failed: {type(exc).__name__}: {exc}")
        return 1
    finally:
        logging.getLogger().removeHandler(catcher)

    if catcher.records:
        print("the generator logged errors while still succeeding, which it does silently:")
        for msg in catcher.records:
            print(f"  {msg}")
        return 1

    fresh = to_isomorphic(Graph().parse(data=turtle, format="turtle"))
    committed = to_isomorphic(Graph().parse(COMMITTED, format="turtle"))

    if fresh == committed:
        print(f"OK — {COMMITTED.relative_to(HERE.parent.parent)} matches the schema "
              f"({len(committed)} triples, compared as graphs rather than bytes)")
        return 0

    print(f"DRIFT — {COMMITTED.relative_to(HERE.parent.parent)} does not match {SCHEMA.name}")
    print(f"  committed: {len(committed)} triples")
    print(f"  generated: {len(fresh)} triples")

    # Report the CONCRETE differences, not the raw set difference. Canonicalisation relabels every
    # blank node, so subtracting the isomorphic graphs reports almost the whole file as "changed"
    # and names nothing a human can act on. Every constraint that matters is a (predicate, object)
    # pair with a non-blank object — `sh:minInclusive 2024`, `sh:path oeo:OEO_00140178` — so compare
    # those and let the blank-node scaffolding fall away.
    def constraints(g: Graph) -> set[tuple[str, str]]:
        return {
            (str(p), str(o))
            for _, p, o in g
            if not isinstance(o, BNode)
        }

    c_committed, c_fresh = constraints(committed), constraints(fresh)
    pairs = (
        ("in the committed file but not regenerated", sorted(c_committed - c_fresh)),
        ("regenerated but not in the committed file", sorted(c_fresh - c_committed)),
    )
    if any(diff for _, diff in pairs):
        for label, diff in pairs:
            if diff:
                print(f"\n  {label}:")
                for p, o in diff:
                    print(f"    {p} {o}")
    else:
        print("\n  No constraint differs. The graphs differ only in blank-node structure —")
        print("  e.g. the same constraints attached to a different number of property shapes.")

    print("\nRe-run the gen-shacl command in mhpkg/schema/README.md and commit the result.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
