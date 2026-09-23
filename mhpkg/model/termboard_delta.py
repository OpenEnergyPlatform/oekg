#!/usr/bin/env python3
"""Report what a Termboard export says that the LinkML schema does not — and the reverse.

WHY THIS EXISTS. MHPKG is modelled in Termboard by two people, and every few weeks a new export
lands in `mhpkg/model/`. Carrying it into `../schema/` is deliberately done by hand: Termboard does
not know which node is a class, which is an individual and which is a literal, so no converter can
decide that. What *can* be automated is the comparison — the slow, error-prone part of "what is new
since the schema was last touched, and what does the schema still not express?".

This tool never writes the schema. It reads a Termboard **JSON** export plus the committed mapping
file `termboard_mapping.yaml`, in which a human has recorded what each Termboard name *is* in the
schema — or why it is not there — and reports every place the three disagree.

WHY THE JSON EXPORT AND NOT THE OWL ONE. Termboard's OWL export is not valid RDF/XML: it puts an
`owl:Restriction` node element inside `rdfs:subClassOf rdf:parseType="Resource"`, where only
property elements are allowed, and rdflib rejects it (both `mhpkg_model_first_draft.owl` and
`mhpkg_model_draft_20260915.owl`). It also declares every node an `owl:Class` and strips umlauts
from IRI local names. The JSON export has none of these problems: it carries term names with
umlauts intact and typed, named relations.

WHAT IS COMPARED, BY NAME. Termboard ids identify *boxes on the board*, not concepts — the
2026-09-15 draft has four separate `year` boxes with four different ids. So terms are matched by
name, and relations by (source name, relation name, target name).

Reported, in order:

  1. unmapped terms and relations        — new in Termboard, no decision recorded yet
  2. mapped names absent from the export — removed or renamed in Termboard
  3. mapping targets absent from the schema — the mapping points at nothing
  4. typed edges the schema does not realise — the sketch says A -rel-> B, the schema cannot
  5. untyped `related to` edges with no typed counterpart — a relation nobody has named yet

Items the mapping marks `term_request`, `deferred` or `open` are listed as known and do not fail.

Usage (needs the `schema` group, for LinkML's SchemaView):
    uv run --group schema python mhpkg/model/termboard_delta.py            # newest schema_*.json
    uv run --group schema python mhpkg/model/termboard_delta.py EXPORT.json
    uv run --group schema python mhpkg/model/termboard_delta.py --check    # exit 1 on any finding

Exit codes:
    0  no findings (or findings without --check)
    1  --check and at least one finding in sections 1-5
    2  usage error: missing export, unreadable mapping
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml
from linkml_runtime.utils.schemaview import SchemaView

HERE = Path(__file__).parent
MAPPING = HERE / "termboard_mapping.yaml"

# Dispositions a mapping entry may carry. Exactly one per entry.
TERM_KINDS = {"class", "enum", "value", "datatype", "example", "term_request", "deferred", "open"}
RELATION_KINDS = {"slot", "inverse", "literal", "sketch", "term_request", "deferred", "open"}
# Known holes: recorded on purpose, listed in the report, never a failure.
KNOWN = {"term_request", "deferred", "open"}


def kind_of(entry: dict, allowed: set[str], where: str) -> str:
    kinds = [k for k in entry if k in allowed]
    if len(kinds) != 1:
        raise SystemExit(f"mapping: {where!r} needs exactly one of {sorted(allowed)}, has {kinds}")
    return kinds[0]


def load_export(path: Path) -> tuple[set[str], list[tuple[str, str, str]]]:
    data = json.loads(path.read_text(encoding="utf-8"))["data"]
    names = {t["name"].strip() for t in data["terms"]}
    by_id = {t["id"]: t["name"].strip() for t in data["terms"]}
    edges = [
        (by_id[r["sourceId"]], (r.get("name") or "").strip(), by_id[r["targetId"]])
        for r in data["relations"]
    ]
    return names, edges


def newest_export() -> Path:
    exports = sorted(HERE.glob("schema_*.json"))
    if not exports:
        raise SystemExit(f"no schema_*.json export in {HERE}")
    return exports[-1]


class Delta:
    def __init__(self, export: Path, mapping: dict):
        self.export = export
        self.names, self.edges = load_export(export)
        self.terms: dict[str, dict] = {str(k): v for k, v in (mapping.get("terms") or {}).items()}
        self.relations: dict[str, dict] = {
            str(k): v for k, v in (mapping.get("relations") or {}).items()
        }
        self.sv = SchemaView(str((HERE / mapping["schema"]).resolve()))
        self.findings: dict[str, list[str]] = defaultdict(list)
        self.known: list[str] = []

    # --- helpers ---------------------------------------------------------------------

    def term_kind(self, name: str) -> str | None:
        e = self.terms.get(name)
        return kind_of(e, TERM_KINDS, name) if e else None

    def rel_kind(self, name: str) -> str | None:
        e = self.relations.get(name)
        return kind_of(e, RELATION_KINDS, name) if e else None

    def slot_for(self, rel: str, target: str) -> str | None:
        """The schema slot a relation maps to, honouring a per-target-class override."""
        e = self.relations[rel]
        target_class = (self.terms.get(target) or {}).get("class")
        return (e.get("by_target") or {}).get(target_class, e["slot"])

    def ranges(self, cls: str, slot: str) -> set[str]:
        """Every range the slot may take on this class, `any_of` included."""
        s = self.sv.induced_slot(slot, cls)
        out = {s.range} if s.range else set()
        out |= {x.range for x in (s.any_of or []) if x.range}
        return out

    # --- the five checks -------------------------------------------------------------

    def unmapped(self) -> None:
        for n in sorted(self.names - self.terms.keys()):
            self.findings["1 unmapped term"].append(repr(n))
        for r in sorted({e[1] for e in self.edges} - self.relations.keys()):
            self.findings["1 unmapped relation"].append(repr(r))

    def removed(self) -> None:
        for n in sorted(self.terms.keys() - self.names):
            self.findings["2 term no longer in export"].append(repr(n))
        for r in sorted(self.relations.keys() - {e[1] for e in self.edges}):
            self.findings["2 relation no longer in export"].append(repr(r))

    def dangling_targets(self) -> None:
        classes, slots, enums = self.sv.all_classes(), self.sv.all_slots(), self.sv.all_enums()
        types = self.sv.all_types()
        for name, e in sorted(self.terms.items()):
            k = kind_of(e, TERM_KINDS, name)
            if k == "class" and e[k] not in classes:
                self.findings["3 no such class"].append(f"{name!r} -> {e[k]}")
            elif k == "enum" and e[k] not in enums:
                self.findings["3 no such enum"].append(f"{name!r} -> {e[k]}")
            elif k == "value":
                enum, _, pv = e[k].partition(".")
                if enum not in enums or pv not in (enums[enum].permissible_values or {}):
                    self.findings["3 no such enum value"].append(f"{name!r} -> {e[k]}")
            elif k == "datatype" and e[k] not in types:
                self.findings["3 no such type"].append(f"{name!r} -> {e[k]}")
            elif k in KNOWN:
                self.known.append(f"term     {name!r}: {k} {e[k]}")
        for name, e in sorted(self.relations.items()):
            k = kind_of(e, RELATION_KINDS, name)
            if k == "slot":
                for s in {e[k], *(e.get("by_target") or {}).values()}:
                    if s not in slots:
                        self.findings["3 no such slot"].append(f"{name!r} -> {s}")
            elif k == "inverse" and e[k] not in self.relations:
                self.findings["3 inverse of an unmapped relation"].append(f"{name!r} -> {e[k]!r}")
            elif k in KNOWN:
                self.known.append(f"relation {name!r}: {k} {e[k]}")

    def unrealised_edges(self) -> None:
        seen = set()
        for s, rel, t in self.edges:
            if self.rel_kind(rel) == "inverse":
                s, rel, t = t, self.relations[rel]["inverse"], s
            if (s, rel, t) in seen or self.rel_kind(rel) != "slot":
                continue
            seen.add((s, rel, t))
            if self.term_kind(s) != "class":
                continue  # the subject is an example, a term request, … — nothing to realise
            cls, slot = self.terms[s]["class"], self.slot_for(rel, t)
            if cls not in self.sv.all_classes() or slot not in self.sv.all_slots():
                continue  # already reported by dangling_targets(); nothing to compare against
            edge = f"{s!r} -{rel}-> {t!r}"
            if slot not in self.sv.class_slots(cls):
                self.findings["4 slot not on class"].append(f"{edge}   ({cls} has no {slot})")
                continue
            want = self.target_range(t)
            if want and want not in self.ranges(cls, slot):
                have = ", ".join(sorted(self.ranges(cls, slot))) or "—"
                self.findings["4 target outside slot range"].append(
                    f"{edge}   ({cls}.{slot} takes {have}, not {want})"
                )

    def target_range(self, t: str) -> str | None:
        e = self.terms.get(t) or {}
        k = kind_of(e, TERM_KINDS, t) if e else None
        if k in ("class", "enum", "datatype"):
            return e[k]
        if k == "value":
            return e[k].partition(".")[0]
        return None  # example / term request / unmapped: no range to compare

    def unexplained_untyped(self) -> None:
        typed = set()
        for s, rel, t in self.edges:
            if self.rel_kind(rel) not in (None, "sketch"):
                typed |= {(s, t), (t, s)}
        for s, rel, t in sorted(set(self.edges)):
            if self.rel_kind(rel) == "sketch" and (s, t) not in typed:
                self.findings["5 untyped edge, no typed counterpart"].append(
                    f"{s!r} -{rel or '∅'}-> {t!r}"
                )

    # --- report ----------------------------------------------------------------------

    def run(self) -> int:
        self.unmapped()
        self.removed()
        self.dangling_targets()
        self.unrealised_edges()
        self.unexplained_untyped()
        return sum(len(v) for v in self.findings.values())

    def report(self) -> str:
        n_terms, n_edges = len(self.names), len(self.edges)
        lines = [
            f"export : {self.export.name}  ({n_terms} distinct term names, {n_edges} relations)",
            f"schema : {self.sv.schema.name}",
            "",
        ]
        if not self.findings:
            lines.append("no findings — the schema and the mapping account for every name and edge")
        for section in sorted(self.findings):
            items = sorted(set(self.findings[section]))
            lines.append(f"{section}  ({len(items)})")
            lines += [f"    {i}" for i in items]
            lines.append("")
        if self.known:
            lines.append(f"known and recorded, not failures  ({len(self.known)})")
            lines += [f"    {i}" for i in sorted(self.known)]
        return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument(
        "export", nargs="?", type=Path,
        help="Termboard JSON export (default: the newest schema_*.json next to this script)",
    )
    ap.add_argument("--mapping", type=Path, default=MAPPING)
    ap.add_argument("--check", action="store_true", help="exit 1 if there is any finding")
    args = ap.parse_args()

    export = args.export or newest_export()
    if not export.is_file():
        print(f"no such export: {export}", file=sys.stderr)
        return 2
    try:
        mapping = yaml.safe_load(args.mapping.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        print(f"cannot read mapping {args.mapping}: {exc}", file=sys.stderr)
        return 2

    delta = Delta(export, mapping)
    n = delta.run()
    print(delta.report(), end="")
    return 1 if (args.check and n) else 0


if __name__ == "__main__":
    sys.exit(main())
