---
name: create-pr
description: Create a pull request in the bazarty repository for the current branch. Use when the user mentions opening a PR, creating a pull request, submitting changes for review, or preparing code for merge.
---

# create-pr

## Overview

This guide covers best practices for creating pull requests in the bazarty repository, including merging the base branch, validating changes efficiently, linking GitHub issues, ensuring appropriate test coverage, and structuring your PR for effective review.

## Related Skills

- `write-pr-description` - Write the PR body itself: template sections, prose, and reviewer guidance
- `fix-errors` - Fix targeted type, build, guard, test, lint, or formatting failures before opening a PR
- `testy-e2e` - Add or update Playwright coverage for user-visible flows, regressions, and P0 use cases
- `testy-jednostkowe` - Add unit tests for non-trivial logic

## Pre-PR Checklist

### 1. Merge the base branch into your feature branch

**Always merge the base branch into your feature branch before starting the review process.** The base branch is `dev` (the default branch: integration, the friends' test site, the DEV database). Work on the agent-system transition targets `warp/przejscie`. `main` is production: a PR goes to `main` only as a release (`dev` to `main`) or an urgent fix, both by the procedure in `.ai/docs/RUNBOOK-WYDANIE.md` and only after the owner agrees. Never push to `main` or `dev` directly.

```bash
git fetch origin
git merge origin/<base-branch>
```

Resolve any merge conflicts locally before opening the PR.

### 2. Review your changes

Before creating a PR, review what changes you're about to submit:

```bash
# View commits in your branch (comparing against base branch)
git --no-pager log <base-branch>..HEAD --oneline

# View file statistics for changes
git --no-pager diff <base-branch>...HEAD --stat

# View full diff
git --no-pager diff <base-branch>...HEAD
```

This helps you:
- Verify all intended changes are included
- Catch unintended changes before review
- Write an accurate PR description
- Ensure you're comparing against the correct base branch
- **Tests:** Include tests when required - bug fixes (regression test), algorithmic code (unit tests), UI changes (visual proof), P0 use cases (Playwright e2e test). See Testing Requirements below.

### 3. Respect implementation agent validation

PR creation is not a validation boundary. If the implementation workflow already completed its tests, lint checks, and final formatting pass and the candidate has not changed, do not rerun them.

If merging the base branch or preparing the PR changed source, tests, manifests, generated code, or configuration, validate the new candidate in this order:

1. Run the relevant tests and fix the code until they pass.
2. Run `npm run typecheck` and the `npm run check:*` guards related to the change, and fix their findings. Return to affected tests only when a fix materially changes behavior.
3. Run the formatter (`npx prettier --write <changed files>`) once after all other code changes are complete.

Do not rerun tests or checks after formatting, and do not run the full gate (`npm run bramka`), unless the user, task, or approved spec explicitly requires it. CI (`.github/workflows/warp-ci.yml`) runs the full gate and owns uncommon failures outside targeted local coverage. Documentation-only changes do not require tests or formatting; run only the guards that read documents (`npm run check:kontekst`, `npm run check:typo`).

### 4. Link to the GitHub issue

PRs should be associated with a GitHub issue in `Enkidu-png/bazarty-platforma` (the single task tracker). Find it with `gh issue list --search "<keywords>"`.

**Branch naming convention:**
Use a short descriptive branch name with a type prefix (e.g., `fix/koszyk-suma`, `feat/oferta-ceny`); agent-system transition work uses `warp/<slug>`.

**How to link PRs to issues:**
Put the issue number in the PR title (e.g., `Poprawka sumy koszyka (#1234)`) and a closing keyword in the body (`Fixes #1234`). GitHub closes the issue only when the PR merges into the default branch (`dev`); for a PR into `warp/**` the orchestrator closes the issue explicitly. Add `Refs #1234` when the PR only touches the issue: the `szybkie` fast path counts one PR per issue by this reference.

**Scope trailer:**
The first commit of the task carries `Scope-Files: <glob>[, <glob>...]` in its message body. Without it the diff-scope guard (`npm run check:zakres`) checks nothing.

### 5. Open the PR

Use the PR template at `.github/pull_request_template.md` when opening PRs. Write the PR title and body in Polish (the owner reads them).

Add changelog entries when appropriate using the format at the bottom of the PR template (the `changelog` skill reads them at release time). Some examples:
- Feature: "Negocjacja ceny w czacie: kupujący proponuje cenę, twórca akceptuje albo odrzuca."
- Improvement: "Szybsze ładowanie feedu na telefonie."
- Bug fix: "Naprawiona suma w koszyku przy dwóch pracach od jednego twórcy." 

**CLI workflow:**

- **Check if PR exists** for current branch:
  ```bash
  gh pr view --json number,url
  ```
  Exit code 0 if PR exists, 1 if not.

- **Create a new PR:**
  ```bash
  # With title and body
  gh pr create --base dev --title "Title" --body "Description" --draft

  # Auto-fill from commits
  gh pr create --base dev --fill --draft

  # Use PR template file
  gh pr create --base dev --body-file .github/pull_request_template.md --title "Title" --draft
  ```
  Key flags: `--draft` / `-d`, `--fill` / `-f`, `--body-file` / `-F`, `--web` / `-w`

- **Update an existing PR:**
  ```bash
  gh pr edit --title "New title" --body "New body"
  gh pr edit --add-reviewer username --add-label bug
  ```

- **Mark PR ready for review:**
  ```bash
  gh pr ready
  ```

### 6. Include co-author attribution

When committing changes, include the agent attribution trailers your session provides at the end of the commit message, and never add a second co-author trailer if the commit already has one. Commits and pushes go out only as the `Enkidu-png` GitHub account (`npm run check:autorzy` enforces it).

## Testing Requirements

### Bug fixes require regression tests

**All bug fixes should be accompanied by a regression test.** This helps prevent re-breaking something that was already broken once.

The test should:
- Reproduce the original bug (would fail before the fix)
- Pass after the fix is applied
- Be clearly named to indicate what bug it's preventing

### Algorithmic code requires unit tests

Code with non-trivial logic should have unit tests to validate functionality:

**Examples of what needs unit tests:**
- Money math (prices, fees, offers, payouts) and shipping quotes
- Search, filtering, and facet logic that should return expected results for a given query
- Parsers, formatters, and mappers between database rows and UI types
- Any algorithmic or computational logic

**Not required for:**
- Sufficiently-simple functions
- Trivial getters/setters

Follow the `testy-jednostkowe` skill for guidance on writing unit tests.

### UI changes need visual proof

**Every user-visible change is verified on the running app**, not in code. Attach a screenshot (saved under `screenshots/`, which is gitignored) or a short video to the PR, and list anything you did not check together with the command that would check it. Follow the `ui-guidelines` skill for what to look at.

### Ask before skipping integration coverage

If the PR changes a user-visible flow, fixes an end-to-end regression, or otherwise looks like it would benefit from integration coverage, use the `AskUserQuestion` tool before creating or updating the PR to ask whether the user wants an integration test added as part of the work.

Prefer a direct choice such as:

- `Yes, add an integration test before creating the PR`
- `No, continue without an integration test`

If the user chooses to add one, use the `testy-e2e` skill.

### P0 use cases require integration tests

**All "P0 use cases" require an integration test** that covers the behavior/flow in question.

**A "P0 use case" is defined as:** Any behavior of the application that, if broken, warrants an out-of-band release.

Integration tests should:
- Exercise the full user-facing flow
- Validate end-to-end functionality
- Be placed in the matching `tests/e2e/<obszar>/` directory

Use the `testy-e2e` skill for implementation details, directory choice, and validation workflow.

## PR Description Guidelines

Use the `write-pr-description` skill for the body itself. It covers following the
repository's template, the prose baseline, and when to add a reading order and focus
areas for the reviewer.

## After Opening the PR

1. **Monitor CI checks** - Ensure all automated checks pass
2. **Respond to review comments** - Address feedback promptly
3. **Keep the PR up to date** - Merge the base branch if conflicts arise (see `resolve-merge-conflicts`)
4. **Validate changed candidates** - After code changes from review feedback, run affected tests, then the related checks, then the formatter once. Do not repeat validation for PR metadata or an unchanged candidate.

## Best Practices

- **Keep PRs focused** - One logical change per PR when possible
- **Write clear commit messages** - Explain what and why, not just what
- **Self-review first** - Review your own diff before requesting review
- **Update tests** - Ensure test coverage reflects your changes
- **Document breaking changes** - Call out any API changes or breaking modifications
- **Use existing switches** - Gate risky changes behind an existing configuration switch (for example `sprzedaz_wlaczona`) when appropriate
