<!--SPDX-License-Identifier: MIT-->
<!--Version: v1.0.0-->

# Collaborative Development

## Prerequisites
- [Git](https://git-scm.com/)
- [GitHub](https://github.com/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — **only if you are editing the
  documentation.** You do *not* need Python installed; uv fetches its own.

## Local setup

> This section is specific to this repository and is **not** part of the family CONTRIBUTING
> template. Keep it when the template is next updated.

**The only installable toolchain here is the documentation build.** That is not an oversight, it is
the current truth of the repository: neither knowledge graph's data lives in these files, there is
no test suite, and there is no validation pipeline yet. If you came to work on the graphs
themselves, you need an editor — not an environment.

```bash
git clone https://github.com/OpenEnergyPlatform/oekg.git
cd oekg
uv sync --group docs
uv run mkdocs serve
```

Then open **<http://127.0.0.1:8000/oekg/>** — note the `/oekg/` suffix, see the traps below.

Three commands is the whole of it:

| Command | What it does |
|---|---|
| `uv sync --group docs` | creates `.venv/` and installs the locked documentation toolchain |
| `uv run mkdocs serve` | live-reloading local preview |
| `uv run mkdocs build --strict` | **exactly** what CI runs — run it before you push |

Verified from a clean clone on a machine whose system Python was 3.10: the first run takes about
**7 seconds**, including downloading CPython 3.13 and all 30 packages. Afterwards it is instant.
uv reads the committed `.python-version` and provisions the interpreter itself, so no contributor
needs a particular Python.

### Traps worth knowing before your first pull request

1. **`mkdocs serve` does not serve the site at `/`.** `mkdocs.yml` sets a `site_url` with a path, so
   the dev server mounts everything under **`/oekg/`**. `http://127.0.0.1:8000/` redirects there, but
   a hand-typed deep link will not: the tech-stack page is `/oekg/tech-stack/`, not `/tech-stack/`.
   OEKG pages carry the prefix **twice** — `/oekg/oekg/fields/` — because the site lives at `/oekg/`
   and the page itself is `docs/oekg/fields.md`. Confusing, correct, and worth reading twice.
2. **`strict: true` makes every warning a build failure**, broken `#anchors` included. A
   documentation edit that looks fine in the browser can still fail CI, so run
   `uv run mkdocs build --strict` before pushing rather than discovering it in a red pipeline.
3. **The default branch is `production`** — not `main`, not `develop`. See the note under
   *Permanent branches* below.
4. **`mhpkg` is a provisional name.** Do not bake it into IRIs, prefixes or published URLs without
   a rename path.
5. **Never hand-edit `uv.lock`.** Change `pyproject.toml`, run `uv lock`, and commit both in the
   same commit. CI installs with `--frozen`, which *fails* rather than silently re-resolving when
   the two disagree.
6. **Do not relax the `mkdocs~=1.6` pin to allow 2.0.** The reason is documented on the
   [tech stack page](docs/tech-stack.md) and it is not a stylistic preference.

## Types of interaction
This repository is following the [Contributor Covenant Code of Conduct](./CODE_OF_CONDUCT.md). <br>
Please be self-reflective and always maintain a good culture of discussion and active participation.

### A. Use
Since the open license allows free use, no notification is required. 
However, for the authors it is valuable information who uses the software for what purpose. 
Indicators are `Watch`, `Fork` and `Starred` of the repository. 
If you are a user, please add your name and details in USERS.cff

### B. Comment
You can give ideas, hints or report bugs in issues, in PR, at meetings or other channels. 
This is no development but can be considered a notable contribution. 
If you wish, add your name and details to `CITATION.cff`.

### C. Contribute and Review
You add code and become an author of the repository. 
You must follow the workflow!

### D. Mantain and Release
You contribute and take care of the repository. 
You review and answer questions. 
You coordinate and carry out the release.

## Workflow
The workflow for contributing to this project has been inspired by the workflow described by [Vincent Driessen](https://nvie.com/posts/a-successful-git-branching-model/).

### 1. Describe the issue on GitHub
Create [an issue](https://help.github.com/en/articles/creating-an-issue)
in the GitHub repository. 
The `issue title` describes the problem you will address.  <br>
This is an important step as it forces one to think about the "issue".
Make a checklist for all needed steps if possible.

### 2. Solve the issue locally

#### 2.0. Get the latest version of the default branch
Load the `production` branch:
```bash
git checkout production
```

Update with the latest version:
```bash
git pull
```

##### Permanent branches
* production - the default branch, and the only permanent one

> ⚠️ **This repository has one permanent branch, not two.** The family template describes a
> `production` + `develop` pair. A `develop` branch existed here early on (last seen in PR #16)
> and was abandoned; it does not exist today, so `git checkout develop` will fail. Feature
> branches are branched from and merged back into **`production`** directly — that is what recent
> pull requests actually did. `production` is also the branch the documentation deploy triggers on.

#### 2.1. Create a new (local) branch
Create a new feature branch:
```bash
git checkout -b feature-1314-my-feature
```

Naming convention for branches: `type`-`issue-nr`-`short-description`

##### `type`
* feature - includes the feature that will be implemented
* hotfix - includes small improvements before an release, should be branched from a release branch
* release - includes the current version to be released

The majority of the development will be done in `feature` branches.

##### `issue-nr`
The `issueNumber` should be taken from Step 1. Do not use the "#". 

##### `short-description`
Describe shortly what the branch is about. 
Avoid long and short descriptive names for branches, 2-4 words are optimal.

##### Other hints
- Separate words with `-` (minus)
- Avoid using capital letters
- Do not put your name to the branch name, it's a collaborative project
- Branch names should be precise and informative

Examples of branch names: `feature-42-add-new-ontology-class`, `feature-911-branch-naming-convention`, `hotfix-404-update-api`, `release-v0.10.0`

#### 2.2. Start editing the files
- Divide your feature into small logical units
- Start to write the documentation or a docstring
- Don't rush, have the commit messages in mind
- Add your changes to the CHANGELOG.md

On first commit to the repo:
- Add your name and details to CITATION.cff

Check branch status:
```bash
git status
```

#### 2.3. Commit your changes 
If the file does not exist on the remote server yet, use:
```bash
git add filename.md
```

Then commit regularly with:
```bash
git commit filename.md
```

Write a good `commit message`:
- "If applied, this commit will ..."
- Follow [existing conventions for commit messages](https://chris.beams.io/posts/git-commit)
- Keep the subject line [shorter than 50 characters](https://chris.beams.io/posts/git-commit/#limit-50)
- Do not commit more than a few changes at the time: [atomic commits](https://en.wikipedia.org/wiki/Atomic_commit)
- Use [imperative](https://chris.beams.io/posts/git-commit/#imperative)
- Do not end the commit message with a [period](https://chris.beams.io/posts/git-commit/#end) ~~.~~ 
- Allways end the commit message with the `issueNumber` including the "#"

Examples of commit message: `Added function with some method #42` or `Update documentation for commit messages #1`

#### 2.4 Fix your latest commit message
Do you want to improve your latest commit message? <br>
Is your latest commit not pushed yet? <br>
Edit the commit message of your latest commit:
```bash
git commit --amend
```

### 3. Push your commits
Push your `local` branch on the remote server `origin`. <br>
If your branch does not exist on the remote server yet, use:
```bash
git push --set-upstream origin feature-1314-my-feature
```

Then push regularly with:
```bash
git push
```

### 4. Submit a pull request (PR)
Follow the GitHub guide [creating-a-pull-request](https://help.github.com/en/articles/creating-a-pull-request). <br>
The PR should be directed: `base: production` <- `compare: feature-1-collaboration`. <br>
Note the base is `production`, per *Permanent branches* above — merging there publishes the
documentation site, so make sure `uv run mkdocs build --strict` passes first. <br>
Add the line `Close #<issue-number>` in the description of your PR.
When it is merged, it [automatically closes](https://help.github.com/en/github/managing-your-work-on-github/closing-issues-using-keywords) the issue. <br>
Assign a reviewer and get in contact.

#### 4.0. Let someone else review your PR
Follow the GitHub guide [approving a pull request with required reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/approving-a-pull-request-with-required-reviews). <br>
Assign one reviewer or a user group and get into contact.

If you are the reviewer:
- Check the changes in all corresponding files.
- Checkout the branch and run code.
- Comment if you would like to change something (Use `Request changes`)
- If all tests pass and all changes are good, `Approve` the PR. 
- Leave a comment and some nice words!

#### 4.1. Merge the PR
Follow the GitHub guide [merging a pull request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request).

#### 4.2. Delete the feature branch
Follow the GitHub guide [deleting a branch](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-and-deleting-branches-within-your-repository#deleting-a-branch).

### 5. Close the issue
Document the result in a few sentences and close the issue. <br>
Check that all steps have been documented:

- Issue title describes the problem you solved?
- All commit messages are linked in the issue?
- The branch was deleted?
- Entry in CHANGELOG.md?
- PR is closed?
- Issue is closed?
