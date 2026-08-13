#!/usr/bin/env python3
"""Mint the instance IRIs used by this slice's example data.

The IRI policy (MH-02) is a PURE FUNCTION of the data: two independent runs over the same heat
plan must produce byte-identical IRIs. This script is how the example instances get their IRIs,
so that `examples/kassel_valid.ttl` can be regenerated rather than hand-maintained — a hand-typed
UUID is a hand-typed UUID whatever the policy says.

Deliberately stdlib-only, and deliberately a copy of the policy's own `mint.py` rather than an
import of it: `pyproject.toml` sets `package = false`, so there is nothing here to import from.
That duplication is a known, recorded limit of the policy, not an oversight.

Usage:
    python mhpkg/schema/mint_slice.py
"""

from __future__ import annotations

import re
import unicodedata
import uuid

BASE = "https://openenergyplatform.org/id/mhpkg/"
GRAPH = "https://openenergyplatform.org/graph/mhpkg/"

# Namespace UUIDs are DERIVED, not magic constants: anyone can recompute them.
NS_MHPKG = uuid.uuid5(uuid.NAMESPACE_URL, BASE)

LEGAL = r"(gmbh\s*&\s*co\.?\s*kg|gmbh|mbh|ag|kg|ohg|e\.?\s*v\.?|gbr|se|ug)"


def ns(collection: str) -> uuid.UUID:
    return uuid.uuid5(NS_MHPKG, collection)


def normalise(label: str) -> str:
    """The umlaut rule, applied in order. Versioned: changing a step re-mints every Tier-3 IRI."""
    s = unicodedata.normalize("NFC", label)  # 1 canonical composition
    s = s.casefold()  # 2 case-insensitive (ß → ss)
    s = re.sub(r"[^\w\s]", " ", s, flags=re.U)  # 3 punctuation → space
    s = re.sub(r"\s+", " ", s).strip()  # 4 collapse + trim
    s = re.sub(rf"\s+{LEGAL}$", "", s)  # 5 strip trailing legal form
    return s.strip()


def mint(collection: str, name: str) -> str:
    """Tier 3: UUIDv5 over the identifying name. Never v4 — v4 is random."""
    return f"{BASE}{collection}/{uuid.uuid5(ns(collection), name)}"


# --- The slice: Kassel's 2024 heat plan, one target-scenario indicator ------------------

AGS = "06611000"  # Kassel. 06 Hessen · 6 RB Kassel · 11 Stadt Kassel · 000 kreisfrei.
PUBLISHED = "2024-03-15"

MUNICIPALITY = f"{BASE}municipality/AGS_{AGS}"  # Tier 1: public register key
HEATPLAN = f"{BASE}heatplan/AGS_{AGS}_{PUBLISHED}"  # Tier 2: key + discriminator
TARGET_SCENARIO = f"{BASE}targetscenario/AGS_{AGS}_{PUBLISHED}"  # Tier 2

# Tier 3. Value identity is its COORDINATES, never its magnitude — so correcting 241 to 2410
# updates this node instead of orphaning it.
INDICATOR = "https://openenergyplatform.org/ontology/oeo/OEO_00050016"  # final energy consumption
ENERGY_CARRIER = "https://openenergyplatform.org/ontology/oeo/OEO_00000292"  # natural gas
YEAR = "2030"
AGGREGATION = "https://openenergyplatform.org/ontology/oeo/OEO_00140070"  # integral

VALUE_TUPLE = "|".join([HEATPLAN, INDICATOR, ENERGY_CARRIER, YEAR, AGGREGATION])
VALUE = mint("value", VALUE_TUPLE)

# The contracted planner has no public register key, so Tier 3 over its normalised label.
PLANNER_LABEL = "Kassel Wärme Ingenieurbüro"
PLANNER = mint("organisation", normalise(PLANNER_LABEL))

if __name__ == "__main__":
    print(f"NS_MHPKG          = {NS_MHPKG}")
    for coll in ("value", "organisation"):
        print(f"NS[{coll:12}] = {ns(coll)}")
    print()
    print(f"municipality      {MUNICIPALITY}")
    print(f"heat plan         {HEATPLAN}")
    print(f"target scenario   {TARGET_SCENARIO}")
    print(f"organisation      {PLANNER}")
    print(f"   from label     {PLANNER_LABEL!r} -> {normalise(PLANNER_LABEL)!r}")
    print()
    print(f"value tuple       {VALUE_TUPLE}")
    print(f"value             {VALUE}")
    print()
    print(f"data graph        {GRAPH}plan/AGS_{AGS}_{PUBLISHED}")
    print(f"shapes graph      {GRAPH}shapes")
    print()
    # The trap the policy calls out, reproduced here so it stays visible: umlaut-stripped input
    # does not error, it mints a DIFFERENT organisation. Concrete support for never
    # machine-consuming Termboard output, which strips umlauts from IRI local names.
    stripped = "Kassel Warme Ingenieurburo"
    print(f"umlaut-stripped   {mint('organisation', normalise(stripped))}")
    print("                  ^ a different organisation, silently. Not an error.")
