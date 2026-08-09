# Phase 0 — Project Foundation & Professional Development Workflow

> NoteKeeper API — Production-grade backend project

This phase establishes the engineering foundation of the project before implementing the actual API.

The goal is not to build application functionality yet.

The goal is to create a professional development environment with:

- Python project management
- reproducible dependencies
- code quality tools
- automated local checks
- testing infrastructure
- Git version control
- GitHub repository
- feature branch workflow
- Pull Requests
- GitHub Actions CI

---

# 1. Phase 0 Goals

By the end of Phase 0, the project should have:

```text
Python 3.12
        ↓
uv project management
        ↓
pyproject.toml
        ↓
uv.lock
        ↓
virtual environment
        ↓
Ruff
        ↓
Pytest
        ↓
pre-commit
        ↓
Git
        ↓
GitHub
        ↓
feature branches
        ↓
Pull Requests
        ↓
GitHub Actions CI
```

The final development workflow becomes:

```text
Create feature branch
        ↓
Develop
        ↓
Run tests
        ↓
Run Ruff
        ↓
pre-commit
        ↓
git add
        ↓
git commit
        ↓
git push
        ↓
Pull Request
        ↓
GitHub Actions
        ↓
Review
        ↓
Merge into main
        ↓
Delete feature branch
```

---

# 2. Project Initialization

## Python

The project uses:

```text
Python 3.12.x
```

The exact environment currently uses:

```text
Python 3.12.10
```

Python version is recorded in:

```text
.python-version
```

This helps keep local development and CI consistent.

---

# 3. uv

## What is uv?

`uv` is a fast Python package and project manager.

We use it for:

- project initialization
- virtual environments
- dependency installation
- dependency locking
- running commands
- reproducible development environments

Instead of manually managing:

```text
python
pip
venv
requirements.txt
```

we use a project-oriented workflow around:

```text
pyproject.toml
uv.lock
```

---

# 4. uv Project Initialization

The project was initialized with:

```text
uv init
```

This initially created a structure similar to:

```text
notekeeper-api/
├── src/
│   └── notekeeper_api/
│       └── __init__.py
├── .python-version
├── pyproject.toml
└── README.md
```

The project will later evolve into the backend architecture defined for NoteKeeper.

---

# 5. pyproject.toml

`pyproject.toml` is the central configuration file for the Python project.

It contains information such as:

- project name
- project version
- Python requirements
- dependencies
- development dependencies
- build configuration
- tool configuration

Example project metadata:

```toml
[project]
name = "notekeeper-api"
version = "0.1.0"
requires-python = ">=3.11"
```

The project currently uses Python 3.12.

---

# 6. Virtual Environment

uv manages the project's virtual environment.

The environment is:

```text
.venv/
```

We do NOT commit `.venv/` to Git.

Why?

Because the virtual environment contains:

- installed packages
- executables
- platform-specific files

Another developer should be able to clone the repository and recreate the environment.

The environment is recreated from:

```text
pyproject.toml
uv.lock
```

---

# 7. uv run

Instead of relying on globally installed Python tools, we use:

```text
uv run <command>
```

Examples:

```text
uv run python --version

uv run pytest

uv run ruff check .

uv run ruff format --check .

uv run pre-commit run --all-files
```

This ensures the command runs in the project's managed environment.

---

# 8. uv tree

To inspect installed dependencies:

```text
uv tree
```

This displays the project's dependency tree.

For example:

```text
notekeeper-api
├── fastapi
├── uvicorn
├── pytest
├── ruff
└── pre-commit
```

This is useful when debugging dependency problems.

---

# 9. uv.lock

`uv.lock` records the resolved dependency versions.

The purpose is reproducibility.

Conceptually:

```text
pyproject.toml
      +
   uv.lock
      ↓
same dependency environment
```

The lock file should normally be committed to Git.

---

# 10. Ruff

## What is Ruff?

Ruff is a Python linting and formatting tool.

We use it for:

```text
ruff check
```

and:

```text
ruff format
```

The project currently uses:

```text
Ruff 0.16.2
```

---

# 11. Ruff Linting

Run:

```text
uv run ruff check .
```

Linting checks the code for issues such as:

- unused imports
- undefined names
- problematic patterns
- style problems
- common Python mistakes

Linting is about code quality and correctness.

---

# 12. Ruff Formatting

To format code:

```text
uv run ruff format .
```

To check formatting without modifying files:

```text
uv run ruff format --check .
```

The distinction is important.

Local development:

```text
ruff format .
```

means:

> Fix formatting.

CI:

```text
ruff format --check .
```

means:

> Verify that formatting is already correct.

CI should generally verify rather than silently modify the code.

---

# 13. Ruff Configuration

Ruff configuration is stored in:

```text
pyproject.toml
```

Keeping tool configuration in the project makes the setup reproducible.

---

# 14. Pytest

## What is Pytest?

Pytest is the testing framework used by the project.

Run:

```text
uv run pytest
```

Tests will eventually cover:

- API endpoints
- authentication
- authorization
- services
- repositories
- database behavior
- validation
- error handling

At Phase 0, the testing infrastructure is only being established.

The serious test suite will be built as the application is implemented.

---

# 15. pre-commit

## What is pre-commit?

`pre-commit` is a framework for Git hooks.

It allows automated checks to run before a Git commit is created.

Conceptually:

```text
git commit
     ↓
pre-commit
     ↓
quality checks
     ↓
everything passes?
   /        \
 YES        NO
  ↓          ↓
commit     blocked
```

This provides local protection against committing bad code.

---

# 16. pre-commit Configuration

Configuration is stored in:

```text
.pre-commit-config.yaml
```

The project uses Ruff through pre-commit.

The hooks include:

```text
ruff-check
ruff-format
```

The Ruff version is pinned to the project's Ruff version.

This helps avoid situations where:

```text
local Ruff version
        ≠
pre-commit Ruff version
```

Reproducibility matters.

---

# 17. Installing pre-commit Hooks

Install the Git hooks with:

```text
uv run pre-commit install
```

This installs the hook into:

```text
.git/hooks/
```

The `.git` directory itself is internal Git metadata and is not committed.

---

# 18. Running pre-commit Manually

Run against all files:

```text
uv run pre-commit run --all-files
```

This is useful when:

- setting up the project
- adding new hooks
- changing configuration
- debugging CI failures

---

# 19. pre-commit vs CI

These are related but different.

## pre-commit

Runs locally:

```text
Developer
    ↓
git commit
    ↓
pre-commit
    ↓
checks
```

## GitHub Actions

Runs remotely:

```text
git push / Pull Request
        ↓
GitHub Actions
        ↓
checks
```

Why use both?

Because pre-commit provides fast local feedback, while CI provides an independent verification environment.

---

# 20. .gitignore

A `.gitignore` file tells Git which files should not be tracked.

Important ignored files/directories include:

```text
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
.env
.env.*
.vscode/
.idea/
dist/
build/
*.egg-info/
```

---

# 21. Why .venv is ignored

The virtual environment is machine-specific.

We do not commit:

```text
.venv/
```

Instead, another developer can recreate it using the project's dependency configuration.

Conceptually:

```text
Git repository
      ↓
clone
      ↓
uv sync
      ↓
new .venv
```

---

# 22. Environment Variables

Sensitive configuration should not be committed.

For example:

```text
.env
```

should remain local.

We will later use environment variables for things such as:

```text
DATABASE_URL
SECRET_KEY
JWT configuration
```

A safe pattern is:

```text
.env
```

for local secrets, and:

```text
.env.example
```

for documenting required variables without exposing secrets.

---

# 23. Git

## What is Git?

Git is a distributed version control system.

It tracks:

- changes
- commits
- branches
- history

Git answers questions such as:

```text
What changed?
Who changed it?
When did it change?
Can I go back?
What was the project like previously?
```

---

# 24. Git's Four Important Areas

A useful mental model is:

```text
Working directory
       │
       │ git add
       ▼
Staging area
       │
       │ git commit
       ▼
Local repository
       │
       │ git push
       ▼
GitHub
```

---

# 25. Working Directory

The working directory contains the files currently being edited.

Example:

```text
app/main.py
README.md
pyproject.toml
```

When you modify them, Git can detect those changes.

---

# 26. Staging Area

The staging area contains changes selected for the next commit.

Stage a file:

```text
git add <file>
```

Stage everything:

```text
git add .
```

Important:

`git add` does NOT create a commit.

It only prepares changes for the next commit.

---

# 27. Local Repository

A commit records a snapshot of staged changes.

Create a commit:

```text
git commit -m "message"
```

The commit is stored locally.

It does not automatically appear on GitHub.

---

# 28. Git Status

Check repository state:

```text
git status
```

This is one of the most important Git commands.

It tells you:

- current branch
- modified files
- staged files
- untracked files
- whether the working tree is clean

Professional habit:

```text
git status
```

before making important Git decisions.

---

# 29. Git Diff

View unstaged changes:

```text
git diff
```

This answers:

> What changed in my working directory?

---

# 30. Staged Diff

View changes currently staged for commit:

```text
git diff --cached
```

This answers:

> What exactly am I about to commit?

A useful workflow is:

```text
git status
      ↓
git diff
      ↓
git add
      ↓
git diff --cached
      ↓
git commit
```

---

# 31. Git Commit

Create a commit:

```text
git commit -m "message"
```

Commit messages should describe the change.

Examples:

```text
chore: initialize project

docs: add phase 1 learning notes

ci: add GitHub Actions pipeline

feat: add note creation endpoint

fix: validate note ownership
```

---

# 32. Conventional Commit Style

We are using a simplified Conventional Commit style.

Common prefixes:

```text
feat:
fix:
docs:
test:
refactor:
chore:
ci:
```

Examples:

```text
feat: add note CRUD endpoints

fix: prevent access to another user's notes

test: add authentication tests

docs: update API documentation

refactor: separate repository logic

chore: update dependencies

ci: add GitHub Actions pipeline
```

The prefix makes project history easier to understand.

---

# 33. Git Log

View commit history:

```text
git log --oneline
```

More useful graph:

```text
git log --oneline --decorate --graph --all
```

This helps visualize branches and commits.

---

# 34. Git Branches

Branches allow development to happen independently.

The project uses:

```text
main
```

as the stable/default branch.

New work happens on feature or task branches.

Example:

```text
main
  │
  └── feature/notes-crud
```

---

# 35. Creating a Branch

Create and switch to a new branch:

```text
git switch -c feature/notes-crud
```

This does two things:

```text
create branch
    +
switch to branch
```

---

# 36. Switching Branches

Switch to an existing branch:

```text
git switch main
```

Check branches:

```text
git branch
```

The `*` shows the current branch.

Example:

```text
* feature/notes-crud
  main
```

---

# 37. Branch Naming

We use descriptive branch names.

Examples:

```text
feature/notes-crud
feature/authentication
feature/tags
feature/postgres

fix/note-ownership

test/authentication

docs/api-documentation

chore/docker

ci/github-actions
```

The branch name should communicate what the work is about.

---

# 38. Why Not Develop Directly on main?

`main` should represent a reasonably stable version of the project.

Instead:

```text
main
  ↓
create feature branch
  ↓
develop
  ↓
test
  ↓
Pull Request
  ↓
CI
  ↓
merge
```

This reduces the risk of breaking the main branch.

---

# 39. GitHub

GitHub is a platform for hosting Git repositories and collaborating around them.

It provides:

- remote repositories
- branches
- Pull Requests
- code review
- GitHub Actions
- issues
- project management
- security features

Git itself is the version control system.

GitHub is a platform built around Git.

---

# 40. Remote Repository

The GitHub repository is the remote repository.

Our local repository is:

```text
C:\Users\scofi\Desktop\Projects\notekeeper-api
```

The GitHub repository is the remote.

---

# 41. origin

Git normally uses:

```text
origin
```

as the conventional name for the main remote.

Add a remote:

```text
git remote add origin <URL>
```

Check remotes:

```text
git remote -v
```

Typical output:

```text
origin  <repository-url> (fetch)
origin  <repository-url> (push)
```

`origin` is just a name.

It is not a special Git server.

---

# 42. Local Branch vs Remote Branch

These are different concepts.

Local:

```text
main
feature/notes-crud
```

Remote:

```text
origin/main
origin/feature/notes-crud
```

A local branch does not automatically exist on GitHub.

You have to push it.

---

# 43. First Push

Push a new branch:

```text
git push -u origin <branch>
```

Example:

```text
git push -u origin feature/notes-crud
```

The `-u` establishes upstream tracking.

After that:

```text
git push
```

is usually enough.

---

# 44. Fetch

Download information from the remote repository:

```text
git fetch
```

Important:

`git fetch` does not automatically integrate the changes into your current branch.

Think:

```text
git fetch
=
"Tell me what changed on the remote."
```

---

# 45. Pull

Pull remote changes:

```text
git pull
```

Conceptually:

```text
git pull
≈
git fetch
+
integrate changes
```

We also used:

```text
git pull --ff-only
```

This asks Git to update the branch only when the update can be performed as a fast-forward.

This helps avoid unexpected merge commits on branches such as `main`.

---

# 46. Pull Requests

A Pull Request proposes merging changes from one branch into another.

Example:

```text
base: main
compare: feature/notes-crud
```

Meaning:

```text
feature/notes-crud
        ↓
       PR
        ↓
      main
```

A Pull Request is more than a merge button.

It provides:

- code review
- discussion
- CI checks
- change history
- a controlled integration point

Even when working alone, PRs are useful practice and provide a quality gate.

---

# 47. Pull Request Workflow

Professional workflow:

```text
main
  ↓
create branch
  ↓
develop
  ↓
commit
  ↓
push
  ↓
open Pull Request
  ↓
CI
  ↓
review
  ↓
merge
  ↓
main
```

---

# 48. Important PR Direction

When creating a PR:

```text
base: main
compare: feature/...
```

The meaning is:

> Take the changes from the feature branch and merge them into main.

Do not accidentally reverse the branches.

---

# 49. Default Branch

The GitHub repository has a **default branch**.

For NoteKeeper:

```text
main
```

should be the default branch.

Important distinction:

```text
Git branch
    ≠
GitHub default-branch setting
```

GitHub can have several branches while one branch is designated as the default.

---

# 50. Branch Cleanup

After a feature branch is merged, it should normally be deleted.

Example:

```text
feature/notes-crud
        ↓
merged into main
        ↓
delete feature/notes-crud
```

This keeps the repository clean.

The branch can still be recovered from Git history if necessary.

---

# 51. GitHub Actions

## What is GitHub Actions?

GitHub Actions is GitHub's automation and CI/CD system.

It can automatically:

- run tests
- run linters
- build applications
- build Docker images
- deploy applications
- perform scheduled tasks

---

# 52. Workflow Files

GitHub Actions workflows live in:

```text
.github/workflows/
```

Our workflow:

```text
.github/workflows/ci.yml
```

---

# 53. CI

CI means:

```text
Continuous Integration
```

The purpose is to automatically verify changes.

Our current CI pipeline is:

```text
Push / Pull Request
        ↓
GitHub Actions
        ↓
Checkout repository
        ↓
Setup Python
        ↓
Install uv
        ↓
Install dependencies
        ↓
Ruff lint
        ↓
Ruff format check
        ↓
Pytest
```

---

# 54. CI Jobs

Our workflow contains two jobs:

```text
CI
├── lint
└── test
```

The jobs can execute independently.

---

# 55. GitHub Runner

A GitHub Actions runner is the machine that executes a workflow.

Our workflow uses:

```text
ubuntu-latest
```

Therefore:

```text
Local development
    Windows 11

CI
    Ubuntu Linux
```

This is normal in professional software development.

---

# 56. Checkout Action

The workflow uses:

```text
actions/checkout
```

This retrieves the repository contents onto the GitHub Actions runner.

Conceptually:

```text
GitHub repository
        ↓
GitHub runner
        ↓
project files
```

---

# 57. Python Setup in CI

CI reads:

```text
.python-version
```

to determine the Python version.

This helps keep:

```text
local Python
        ≈
CI Python
```

consistent.

---

# 58. uv in CI

GitHub Actions installs uv using the official uv setup action.

The purpose is to reproduce our local Python environment.

The workflow runs:

```text
uv sync --locked --dev
```

---

# 59. Why --locked?

CI should not silently modify the lock file.

Using:

```text
uv sync --locked
```

means:

> Use the existing lock file and fail if the project configuration and lock file are inconsistent.

This protects reproducibility.

---

# 60. Why --dev?

Development dependencies include tools such as:

```text
pytest
ruff
pre-commit
```

CI needs these tools.

Therefore:

```text
uv sync --locked --dev
```

installs the project's development environment.

---

# 61. CI Lint Job

The lint job runs:

```text
uv run ruff check .
```

and:

```text
uv run ruff format --check .
```

The CI job does not modify source files.

It verifies them.

---

# 62. CI Test Job

The test job runs:

```text
uv run pytest
```

As the application grows, this will execute tests for:

```text
authentication
authorization
notes
tags
database
repositories
services
API endpoints
validation
security
```

---

# 63. CI vs pre-commit

Important distinction:

```text
pre-commit
    Local
    Runs before commit
    Fast developer feedback

GitHub Actions
    Remote
    Runs after push / PR
    Independent verification
```

Both are useful.

---

# 64. Complete Development Workflow

The complete workflow is:

```text
1. Start from main

       ↓

2. Update local main

    git switch main
    git pull --ff-only

       ↓

3. Create feature branch

    git switch -c feature/my-feature

       ↓

4. Develop

       ↓

5. Run tests

    uv run pytest

       ↓

6. Run Ruff

    uv run ruff check .
    uv run ruff format .

       ↓

7. Run pre-commit

    uv run pre-commit run --all-files

       ↓

8. Check Git

    git status
    git diff

       ↓

9. Stage changes

    git add <files>

       ↓

10. Inspect staged changes

    git diff --cached

       ↓

11. Commit

    git commit -m "feat: ..."

       ↓

12. Push

    git push

       ↓

13. Open Pull Request

    feature → main

       ↓

14. GitHub Actions

    lint
    format
    test

       ↓

15. Review

       ↓

16. Merge

       ↓

17. Delete feature branch

       ↓

18. Update local main

    git switch main
    git pull --ff-only
```

---

# 65. Git Cheat Sheet

## Repository state

```text
git status
```

What is happening?

---

## See unstaged changes

```text
git diff
```

What changed but isn't staged?

---

## Stage a file

```text
git add <file>
```

---

## Stage everything

```text
git add .
```

---

## See staged changes

```text
git diff --cached
```

What will be included in my next commit?

---

## Commit

```text
git commit -m "message"
```

---

## History

```text
git log --oneline
```

---

## Detailed history graph

```text
git log --oneline --decorate --graph --all
```

---

## List branches

```text
git branch
```

---

## Current branch

```text
git branch --show-current
```

---

## Create + switch branch

```text
git switch -c feature/example
```

---

## Switch branch

```text
git switch main
```

---

## Add remote

```text
git remote add origin <URL>
```

---

## Check remotes

```text
git remote -v
```

---

## Push new branch

```text
git push -u origin feature/example
```

---

## Push existing tracked branch

```text
git push
```

---

## Fetch remote information

```text
git fetch
```

---

## Pull changes

```text
git pull
```

---

## Safe update of main

```text
git pull --ff-only
```

---

# 66. Git Mental Model

The most important model to remember:

```text
WORKING DIRECTORY
        │
        │ git add
        ▼
STAGING AREA
        │
        │ git commit
        ▼
LOCAL REPOSITORY
        │
        │ git push
        ▼
GITHUB
        │
        │ Pull Request
        ▼
CI / REVIEW
        │
        │ merge
        ▼
MAIN
```

---

# 67. Git Vocabulary

## Repository

A project tracked by Git.

---

## Commit

A snapshot of staged changes.

---

## Branch

An independent line of development.

---

## Remote

Another Git repository, usually hosted somewhere such as GitHub.

---

## origin

The conventional name for the primary remote.

---

## HEAD

The commit/branch currently checked out.

Example:

```text
HEAD -> main
```

means HEAD currently points to the `main` branch.

---

## Staging area

The set of changes selected for the next commit.

---

## Working tree

The current files on disk.

---

## Pull Request

A proposal to merge changes from one branch into another.

---

## CI

Continuous Integration.

Automated verification of code changes.

---

## CD

Continuous Delivery / Continuous Deployment.

Automated delivery or deployment of software.

---

# 68. Professional Python Tooling Summary

Our Phase 0 Python tooling:

```text
Python
    Language/runtime

uv
    Project + dependency management

pyproject.toml
    Project/tool configuration

uv.lock
    Dependency lock file

Ruff
    Linting + formatting

Pytest
    Testing

pre-commit
    Local automated Git hooks
```

---

# 69. Quality Pipeline

Our quality process is:

```text
Developer
    ↓
Ruff
    ↓
Pytest
    ↓
pre-commit
    ↓
Git commit
    ↓
Push
    ↓
GitHub Actions
    ↓
Ruff
    ↓
Pytest
    ↓
Pull Request
    ↓
Merge
```

The same basic quality expectations exist locally and remotely.

---

# 70. Why We Built This Before the Backend

The NoteKeeper project is intended to become a foundation for a future RAG system.

Therefore, we don't want to start with:

```text
"Let's make some endpoints."
```

and later discover that:

- dependencies aren't reproducible
- code isn't tested
- Git history is messy
- CI doesn't exist
- deployment is difficult
- secrets are committed
- branches are unmanaged

Instead, we establish engineering practices first.

The actual application can now be built on top of this foundation.

---

# 71. Phase 0 Final Architecture

Current repository foundation:

```text
notekeeper-api/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .venv/
│   └── ignored by Git
│
├── .gitignore
│
├── .pre-commit-config.yaml
│
├── .python-version
│
├── pyproject.toml
│
├── uv.lock
│
├── README.md
│
└── tests/
```

The application architecture will be introduced in Phase 1.

---

# 72. Phase 0 Lessons Learned

## Lesson 1

Don't treat Git as:

```text
git add .
git commit
git push
```

as three commands to memorize.

Understand the state transitions:

```text
working directory
        ↓
staging
        ↓
commit
        ↓
remote
```

---

## Lesson 2

Always understand what you're committing.

Useful sequence:

```text
git status
git diff
git add
git diff --cached
git commit
```

---

## Lesson 3

Local and remote branches are different.

```text
local:

main

remote:

origin/main
```

They must be synchronized intentionally.

---

## Lesson 4

A Pull Request is a controlled integration point.

It is not just:

```text
"another way to merge."
```

It provides:

```text
review
+
CI
+
discussion
+
history
```

---

## Lesson 5

pre-commit and CI solve different problems.

```text
pre-commit
    local protection

CI
    remote protection
```

---

## Lesson 6

Lock dependencies for reproducibility.

```text
pyproject.toml
        +
uv.lock
```

should describe the expected environment.

---

## Lesson 7

Don't commit machine-specific or sensitive files.

Examples:

```text
.venv/
.env
__pycache__/
.pytest_cache/
.ruff_cache/
```

---

# 73. Phase 0 Completion Checklist

```text
[✓] Python 3.12 configured
[✓] uv installed
[✓] uv project initialized
[✓] pyproject.toml created
[✓] uv.lock created
[✓] virtual environment created
[✓] FastAPI installed
[✓] Uvicorn installed
[✓] Ruff installed
[✓] Pytest installed
[✓] pre-commit installed
[✓] Ruff configured
[✓] pre-commit configured
[✓] .gitignore created
[✓] Git repository initialized
[✓] main branch created
[✓] feature branch created
[✓] initial commit created
[✓] feature changes committed
[✓] GitHub repository connected
[✓] main pushed to GitHub
[✓] feature branch pushed
[✓] Pull Request created
[✓] GitHub Actions CI created
[✓] lint CI configured
[✓] format CI configured
[✓] test CI configured
[✓] CI passed
[✓] Pull Request merged
[✓] feature branch removed
[✓] main set as GitHub default branch
[✓] local main synchronized
```

---

# 74. Phase 0 Final Mental Model

If you remember only one thing from this phase, remember this:

```text
                    DEVELOPMENT

                        main
                         │
                         │
                  create branch
                         │
                         ▼
                  feature branch
                         │
                    write code
                         │
              ┌──────────┴──────────┐
              │                     │
            Ruff                  Pytest
              │                     │
              └──────────┬──────────┘
                         │
                    pre-commit
                         │
                      commit
                         │
                       push
                         │
                         ▼
                      GitHub
                         │
                   Pull Request
                         │
                         ▼
                 GitHub Actions
                         │
                 ┌───────┴───────┐
                 │               │
               Lint            Tests
                 │               │
                 └───────┬───────┘
                         │
                       Review
                         │
                       Merge
                         │
                         ▼
                        main
```

This workflow will remain the foundation of NoteKeeper throughout the rest of the project.