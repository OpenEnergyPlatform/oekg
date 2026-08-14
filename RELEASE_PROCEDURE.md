<!--
SPDX-FileCopyrightText: 2026 Open Energy Family <https://github.com/OpenEnergyPlatform>
SPDX-FileCopyrightText: super-repo v0.5.0 <https://github.com/rl-institut/super-repo>
SPDX-License-Identifier: MIT
-->

# Release Procedure

The release procedure is a process in which different parts of the repository are involved.<br>
These symbols help with orientation:

- 🐙 GitHub
- 💠 git (Bash)
- 📝 File
- 💻 Command Line (CMD)

Adapted for `oekg` from the Open Energy Family's convention (`rl-institut/super-repo` v0.5.0,
as carried by [`oemetadata`](https://github.com/OpenEnergyPlatform/oemetadata)). Two
family-standard sections are **deliberately absent** because they do not apply here: this
repository ships **no Python package**, so there is no PyPI or Test-PyPI release and no
`pyproject.toml` / `uv.lock` / `python -m build` step; and it has **no `develop` branch**, so
release branches are cut from and merged back into `production` directly.

## ⚠️ Read this before the first release

Two things are unsettled, and this document must not be read as having settled them:

1. **This repository has never been released.** `CHANGELOG.md` contains no release sections at
   all, and `CITATION.cff` still says `version: 0.0.0`, `date-released: 2022-06-23`, with no
   DOI and without every contributor listed. The first release therefore includes fixing those,
   not just bumping them.
2. **This repository holds two knowledge graphs** — the OEKG and `mhpkg` — and the procedure
   below, inherited from the family, assumes **exactly one release artifact**: one changelog,
   one `CITATION.cff` version, one SemVer line, one tag namespace. Whether the two graphs
   release together or independently (and if independently, with what tag prefixes, e.g.
   `oekg-v…` / `mhpkg-v…`) is **not decided**. It needs the graphs' authors in the room, not a
   template. Until it is decided, treat every `v0.1.0` below as a placeholder for whatever
   scheme is chosen.

## Version Numbers

Software in this repository follows [Semantic Versioning (SemVer)](https://semver.org/).<br>
It always has the format `MAJOR.MINOR.PATCH`, for example `1.5.0`.

**The knowledge graphs are data and follow [Calendar Versioning (CalVer)](https://calver.org/)**,
format `YYYY-MM-DD`, for example `2026-05-16`. This distinction is the most directly useful idea
in the family's procedure and it matters here: almost everything this repository releases is
data, not software.

## Citable references

**Publications citing this repository must cite a tag or a commit SHA, never `/tree/<branch>/…`.**
Branch paths move, and a citation in a submitted thesis cannot be corrected afterwards.

This is not hypothetical here. The 2025 BA thesis cites
`github.com/OpenEnergyPlatform/oekg/tree/production/oekg/oekg_rework/shacl` twice for validation
reports it was too long to print; the directory was reorganised in 2026 and those footnotes now
404. The cited state is preserved as the annotated tag `thesis-madbkr-2025`, and
`oekg/archive/madbkr_ba/README.md` maps the old paths to the current ones.

For a thesis or paper, **set the tag when the work is submitted**, pattern
`thesis-<initials>-<year>`. These provenance tags are deliberately outside whatever release tag
scheme is eventually chosen above — they name a cited state, not a release.

## GitHub Release

Following Semantic Versioning, different workflows for Major, Minor, or Patch releases are
possible.<br>
For Major and Minor releases, follow the complete workflow.<br>
For a **Patch Release** (Hotfix), start at
[section 4](https://github.com/OpenEnergyPlatform/oekg/blob/production/RELEASE_PROCEDURE.md#4--create-a-draft-github-release).

### 1. 🐙 Create a `GitHub Project`

- Create a [new project](https://github.com/OpenEnergyPlatform/oekg/projects)
- Named `oekg-v0.1.0`
- Add a meaningful description
- Track project progress

▶️ It gives an overview of open and finished issues and Pull Requests!

### 2. 🐙 Finish all planned Developments

- Some days before the release, inform all developers
- Merge the open Pull Requests
- On release day, start the release early to ensure sufficient time for reviews
- Merge everything on the `production` branch

▶️ Completion of the preparation of the planned release!

### 3. 🐙 Create a `GitHub Issue`

- Use the [issue templates](https://github.com/OpenEnergyPlatform/oekg/issues/new/choose)
- Name `Release - Minor Version - 0.1.0`
- Complete the necessary details

▶️ This issue documents the status of the release!

### 4. 🐙 Create a `Draft GitHub Release`

- Start here for a **Patch Release** (Hotfix)
- [Draft a new release](https://github.com/OpenEnergyPlatform/oekg/releases/new)
- Enter the release version number `0.1.0` as title
- Summarize key changes from the changelog in the description
- State **which graph or graphs** the release covers

```text
## [0.1.0] Minor Release - Name - Date
### Added
### Changed
### Removed

**Complete changelog:** [CHANGELOG.md](https://github.com/OpenEnergyPlatform/oekg/blob/production/CHANGELOG.md)
**Compare versions:** [0.1.0 - 0.2.0](https://github.com/OpenEnergyPlatform/oekg/compare/v0.1.0...v0.2.0)
**Main developers:** @…
```

- Save draft

### 5. 💠 Create a `release` branch

- Change to `production` branch: 💠`git checkout production`
- Update with online version: 💠`git pull`
- Create branch: 💠`git checkout -b release-v0.1.0`
- Push branch: 💠`git push --set-upstream origin release-v0.1.0`

### 6. 📝 Update the version files

- `📝CITATION.cff`
  - Update `version`
  - Update `date-released`
  - Check that **every** contributor is listed, including contributors to the archived
    material under `oekg/archive/`
  - Add a DOI if one exists
- `📝USERS.cff`
  - Add any new users, research projects or institutions
- Update the `📝CHANGELOG.md`
  - Check that all Pull Requests are included
  - Rename the `Unreleased` section with the release title from the issue
  - Follow `[0.0.0] Minor Release - Name of Release - 20YY-MM-DD`

▶️ Increase version numbers!

### 7. 🐙 Create a Release Pull Request

- Merge `release` into `production` branch
- Assign two reviewers to check the release
- Wait for reviews
- Merge Pull Request and delete the `release` branch

▶️ Merge code on `production` branch!

### 8. 💠 Set the `Git Tag`

- Change to `production` branch: 💠`git checkout production`
- Update with online version: 💠`git pull`
- Check existing tags: 💠`git tag -n`
- Create new tag: 💠`git tag -a v0.1.0 -m "oekg Minor Release v0.1.0"`
- This commit will be the final version for the release, breathe three times and check again
- Push tag: 💠`git push --tags`

If you messed up, remove tags and start again

- Delete local tag: 💠`git tag -d v0.1.0`
- Delete remote tag: 💠`git push --delete origin v0.1.0`

▶️ Git Tag for GitHub Release!

### 9. 🐙 Publish `GitHub Release`

- Navigate to releases and open the draft release
- Choose the correct `Git Tag`
- Choose the `production` branch
- Select `Set as the latest release`
- Select `Create a discussion for this release` in category `Announcements`
- **Publish release**

▶️ 🎉 Release on GitHub! 🚀

### 10. 💻 Update the documentation

- Change to `production` branch: 💠`git checkout production`
- Update with online version: 💠`git pull`
- Check that the documentation build has published the new state

> **Note on `mike`.** The family's procedure uses [`mike`](https://github.com/jimporter/mike)
> for **versioned** mkdocs deployment (`mike deploy --push --update-aliases 0.1 latest`).
> `mike` is **deliberately deferred** for this repository: the site does not exist yet, and
> versioned docs are not worth their complexity before there is a first version. Adopt it when
> there is more than one version of the documentation worth keeping online.

▶️ Update the documentation!

### 11. 🐙 Set up new development

- Create a new **Unreleased** section in the `📝CHANGELOG.md`

```text
## [Unreleased]

### Added

### Changed

### Removed
```

- Close all solved issues and PRs and set labels and status
- Create a new [GitHub Project](https://github.com/OpenEnergyPlatform/oekg/projects) by cloning
  the latest project

▶️ Continue the developments 🛠

## Sources

- <https://github.com/rl-institut/super-repo> (v0.5.0)
- <https://github.com/OpenEnergyPlatform/oemetadata/blob/production/RELEASE_PROCEDURE.md>
- <https://raw.githubusercontent.com/folio-org/stripes/master/doc/release-procedure.md>

!!! note "Used Icons"
    🐙 GitHub | 💠 git | 📝 File | 💻 Command Line
