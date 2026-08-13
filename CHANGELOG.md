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

### Removed
- `requirements-docs.txt`, superseded by `pyproject.toml` and `uv.lock` [[#51](https://github.com/OpenEnergyPlatform/oekg/pull/51)]
