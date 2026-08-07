#!/usr/bin/env python3
"""Regenerate the vendored MHPO term list from the pinned commit.

This repository does not vendor MHPO itself. It vendors a *term list* — every term MHPO
declares or uses — because that is the whole of what the LinkML schema needs: an IRI to put
in `class_uri` / `slot_uri`, and a label so a human can tell which term that is.

Why a list and not the ontology:

* MHPO has **no releases and no tags**, and `purl.org/mhpo` redirects to the repository's
  GitHub page rather than to an ontology. The only consumable artifact is `mhpo-edit.owl` on
  a branch, so whatever we take has to be pinned to a commit by hand.
* A list diffs one readable line per term. A 57 KB OWL functional-syntax file does not.
* It needs no ODK, no Docker and no ROBOT, which keeps the contributor setup to `uv`.

Deliberately stdlib-only: nothing here may add a dependency, because the dependency set for
graph work is decided in MH-04 and this must not front-run it.

Usage:
    python extract_terms.py            # regenerate terms.csv from the pinned commit
    python extract_terms.py --check    # exit 1 if terms.csv differs from the pin (for CI)
    python extract_terms.py --latest   # report drift between the pin and MHPO's develop HEAD
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
PIN = HERE / "pin.txt"
OUT = HERE / "terms.csv"

REPO = "OpenEnergyPlatform/municipal-heat-planning-ontology"
EDIT_PATH = "src/ontology/mhpo-edit.owl"
BRANCH = "develop"  # MHPO's default branch; it has no `main`, despite its ODK config

# IRI prefix -> short source name. Order matters: first match wins.
SOURCES = [
    ("https://purl.org/mhpo/ontology/", "mhpo"),
    ("http://purl.obolibrary.org/obo/BFO_", "bfo"),
    ("http://purl.obolibrary.org/obo/IAO_", "iao"),
    ("http://purl.obolibrary.org/obo/RO_", "ro"),
    ("http://purl.obolibrary.org/obo/", "obo"),
    ("https://www.commoncoreontologies.org/", "cco"),
    ("https://openenergyplatform.org/ontology/oeo/", "oeo"),
]

# Vocabulary terms that are never citable as domain terms. Excluded from the list entirely
# so that "is this IRI in terms.csv?" is a usable check rather than one with caveats.
INFRASTRUCTURE = (
    "http://www.w3.org/2002/07/owl#",
    "http://www.w3.org/2000/01/rdf-schema#",
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "http://www.w3.org/2001/XMLSchema#",
    "http://purl.org/dc/elements/1.1/",
    "http://purl.org/dc/terms/",
)

REPLACED_BY = "http://purl.obolibrary.org/obo/IAO_0100001"

RE_DECL = re.compile(r"Declaration\((\w+)\(<([^>]+)>\)\)")
RE_LABEL = re.compile(r'AnnotationAssertion\(rdfs:label <([^>]+)> "((?:[^"\\]|\\.)*)"')
RE_DEPRECATED = re.compile(r'AnnotationAssertion\(owl:deprecated <([^>]+)> "true"')
RE_REPLACED = re.compile(rf"AnnotationAssertion\(<{re.escape(REPLACED_BY)}> <([^>]+)> <([^>]+)>")
RE_OBJPROP_USE = re.compile(r"Object(?:Some|All)ValuesFrom\(<([^>]+)>")
RE_IRI = re.compile(r"<([^>]+)>")

AXIOM_PREFIXES = (
    "SubClassOf(", "EquivalentClasses(", "DisjointClasses(", "SubObjectPropertyOf(",
    "ObjectPropertyDomain(", "ObjectPropertyRange(", "ClassAssertion(",
)


def read_pin() -> str:
    for line in PIN.read_text(encoding="utf-8").splitlines():
        if line.startswith("commit:"):
            return line.split(":", 1)[1].strip()
    sys.exit(f"no 'commit:' line in {PIN}")


def fetch(ref: str) -> str:
    url = f"https://raw.githubusercontent.com/{REPO}/{ref}/{EDIT_PATH}"
    with urllib.request.urlopen(url, timeout=60) as r:  # noqa: S310 - fixed https host
        return r.read().decode("utf-8")


def source_of(iri: str) -> str:
    for prefix, name in SOURCES:
        if iri.startswith(prefix):
            return name
    return "other"


def curie(iri: str) -> str:
    return iri.rsplit("/", 1)[-1].split("#")[-1]


def parse(text: str) -> list[dict]:
    declared: dict[str, str] = {}
    for kind, iri in RE_DECL.findall(text):
        declared[iri] = kind

    labels = {iri: lbl for iri, lbl in RE_LABEL.findall(text)}
    deprecated = set(RE_DEPRECATED.findall(text))
    replaced = dict(RE_REPLACED.findall(text))

    # Terms used in logical axioms, even when MHPO never declares them. MHPO cites several
    # RO_* relations it neither declares nor imports; they must still be citable, so they
    # belong in the list — flagged, not silently dropped.
    used: set[str] = set()
    objprops_used: set[str] = set()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(AXIOM_PREFIXES):
            used.update(RE_IRI.findall(stripped))
            objprops_used.update(RE_OBJPROP_USE.findall(stripped))

    rows = []
    for iri in sorted(set(declared) | used):
        if iri.startswith(INFRASTRUCTURE):
            continue
        kind = declared.get(iri)
        if kind is None:
            kind = "ObjectProperty" if iri in objprops_used else "Class"
        label = labels.get(iri, "")
        rows.append(
            {
                "curie": curie(iri),
                "label": label,
                "type": {"Class": "class", "ObjectProperty": "objectProperty",
                         "AnnotationProperty": "annotationProperty",
                         "DataProperty": "dataProperty"}.get(kind, kind.lower()),
                "source": source_of(iri),
                "declared_in_mhpo": "yes" if iri in declared else "no",
                # Imports are unresolved in the editors' file, so external labels are simply
                # not present. Recorded honestly rather than guessed; resolving them needs
                # ROBOT and the ODK toolchain this repository deliberately does not require.
                "label_status": "from_mhpo" if label else "unresolved",
                "deprecated": "yes" if iri in deprecated else "no",
                "replaced_by": curie(replaced[iri]) if iri in replaced else "",
                "iri": iri,
            }
        )
    return rows


FIELDS = ["curie", "label", "type", "source", "declared_in_mhpo",
          "label_status", "deprecated", "replaced_by", "iri"]


def render(rows: list[dict]) -> str:
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=FIELDS, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="regenerate from the pin and fail if terms.csv differs")
    ap.add_argument("--latest", action="store_true",
                    help="report drift between the pin and MHPO's develop HEAD")
    args = ap.parse_args()

    if args.latest:
        pin = read_pin()
        url = f"https://api.github.com/repos/{REPO}/commits/{BRANCH}"
        with urllib.request.urlopen(url, timeout=60) as r:  # noqa: S310
            head = json.load(r)["sha"]
        if head == pin:
            print(f"up to date: pin == {BRANCH} HEAD ({pin[:7]})")
            return 0
        old = {r["iri"] for r in parse(fetch(pin))}
        new_rows = parse(fetch(head))
        new = {r["iri"] for r in new_rows}
        print(f"MHPO moved: pin {pin[:7]} -> {BRANCH} HEAD {head[:7]}")
        print(f"  +{len(new - old)} terms, -{len(old - new)} terms")
        for iri in sorted(new - old):
            lbl = next((r["label"] for r in new_rows if r["iri"] == iri), "")
            print(f"  + {curie(iri):18} {lbl}")
        for iri in sorted(old - new):
            print(f"  - {curie(iri)}")
        # Drift is information, not a failure: MHPO is owned by other people and moves often.
        return 0

    rendered = render(parse(fetch(read_pin())))

    if args.check:
        if not OUT.exists():
            print(f"{OUT.name} is missing", file=sys.stderr)
            return 1
        if OUT.read_text(encoding="utf-8") != rendered:
            print(f"{OUT.name} does not match the pinned MHPO commit.\n"
                  f"Run: python {Path(__file__).name}", file=sys.stderr)
            return 1
        print(f"{OUT.name} matches the pin")
        return 0

    OUT.write_text(rendered, encoding="utf-8")
    print(f"wrote {OUT.name}: {rendered.count(chr(10)) - 1} terms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
