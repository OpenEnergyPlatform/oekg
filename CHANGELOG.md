# Changelog

All notable changes to this project will be documented in this file.

The format is inspired from [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and the versioning aims to respect [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

Here is a template for new release sections:
```
## [v0.0.0] Release - Name of Release - 20YY-MM-DD

### Added
- [#](https://github.com/OpenEnergyPlatform/oekg/pull/)
### Changed
- [#](https://github.com/OpenEnergyPlatform/oekg/pull/)
### Removed
- `oekg/shapes/oekg_shapes.ttl` in its **pre-rework** form (350 lines, old
  `http://openenergy-platform.org/…` namespace, targeting `scenario_study`). Nothing was lost: a
  byte-identical copy is retained as the frozen thesis record at
  `oekg/archive/madbkr_ba/oekg_rework/shacl/oekg_shacl_old_graph_txt`
- [#](https://github.com/OpenEnergyPlatform/oekg/pull/)
```


## Current

### Added
- [LICENSE.txt](https://github.com/OpenEnergyPlatform/oekg/blob/main/LICENSE)
- README.md [#2](https://github.com/OpenEnergyPlatform/oekg/pull/2)
- CONTRIBUTING.md [#2](https://github.com/OpenEnergyPlatform/oekg/pull/2)
- CHANGELOG.md [#2](https://github.com/OpenEnergyPlatform/oekg/pull/2)
- CODE_OF_CONDUCT.md [#3](https://github.com/OpenEnergyPlatform/oekg/pull/3)
- CITATION.cff [#2](https://github.com/OpenEnergyPlatform/oekg/pull/2)
- oekg rework files [[#50](https://github.com/OpenEnergyPlatform/oekg/pull/50)]
- Documentation site (mkdocs-material, deployed to GitHub Pages) [[#51](https://github.com/OpenEnergyPlatform/oekg/pull/51)]
- `mhpkg/` for the Municipal Heat Planning KG — provisional name [[#51](https://github.com/OpenEnergyPlatform/oekg/pull/51)]
- Dependency management with uv: `pyproject.toml`, `uv.lock`, `.python-version` [[#51](https://github.com/OpenEnergyPlatform/oekg/pull/51)]
- Contributor setup instructions in CONTRIBUTING.md
- `mhpkg/schema/`: first cut of the MHPKG data shape — a LinkML schema for one slice (a municipal
  heat plan, its target scenario and one final energy consumption value), the SHACL shapes generated
  from it, a hand-written companion file enforcing the IRI policy, and a passing plus a deliberately
  failing example instance [[#54](https://github.com/OpenEnergyPlatform/oekg/pull/54)]

### Changed
- Repository restructured around two knowledge graphs; OEKG files grouped by status
  (`shapes/`, `eval/`, `legacy/`, `archive/`) under `oekg/` [[#51](https://github.com/OpenEnergyPlatform/oekg/pull/51)]
- CONTRIBUTING.md now documents `production` as the only permanent branch, matching the
  repository's actual practice
- **The OEKG's canonical SHACL shapes are now `oekg/shapes/oekg_shapes.ttl`**, moved from
  `oekg/eval/oekg_shacl.txt` (same content, `.txt` → `.ttl`). The file previously at that path was
  the thesis's *pre-rework* instrument and had been surfaced as "the most developed" shapes purely
  because it was longer — but the thesis had **folded** five shapes into `CommonShape`, so the
  shorter file is the successor. A reviewer had already been misled by this and reported
  already-fixed defects as open ones.
- `oekg/eval/` now holds only the competency questions; shapes work starts in `oekg/shapes/`
- The OEKG shapes were **validated against the live graph for the first time since the rework**
  (2026-08-13): they bind 1,499 focus nodes across all eight shapes and report 135 violations
  (0.99% of triples), **133 of which are `oeplatform` data bugs** rather than shape defects.
  Documentation that claimed no SHACL file here describes the live graph was corrected accordingly
  (`docs/oekg/index.md`, `docs/oekg/endpoint.md`, `docs/tech-stack.md`)

### Removed
- `requirements-docs.txt`, superseded by `pyproject.toml` and `uv.lock` [[#51](https://github.com/OpenEnergyPlatform/oekg/pull/51)]
