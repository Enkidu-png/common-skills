---
name: diagnose-ci-failures
description: Diagnose CI failures for a PR using the GitHub CLI, extract error logs, and generate a plan to fix them. Use when the user asks to check CI status, pull CI issues, triage test failures, or investigate PR build failures.
---

# diagnose-ci-failures

Programmatically diagnose CI failures for a PR and generate a plan to fix them.

## Overview

This skill provides a deterministic workflow to check CI status for a PR, extract failure logs, analyze errors, and create a plan (not code changes) to resolve issues. The output is always a plan document that can be reviewed before execution.

## Workflow

### 1. Verify PR exists for current branch

Get the current branch and check if a PR exists:

```bash
# Get current branch
git branch --show-current

# Check for PR
GH_PAGER=cat gh pr view <branch-name> --json number,title,url,state
```

If no PR exists, inform the user and offer to create one using the `create-pr` skill.

### 2. Check CI status

Fetch the status of all CI checks:

```bash
GH_PAGER=cat gh pr view <branch-name> --json statusCheckRollup
```

Parse the output to identify:
- Completed checks vs. in-progress checks
- Successful checks
- Failed checks with their names and details URLs

If CI is still running, inform the user which checks have already failed or passed, highlight the checks that are still running, and suggest waiting for completion before diagnosis.

### 3. Extract failure logs

For each failed check, pull the logs using the run ID from the status check:

```bash
GH_PAGER=cat gh run view <run-id> --log-failed
```

Focus on extracting:
- Error messages and their locations (file paths, line numbers)
- Compilation errors (unused imports, type mismatches, etc.)
- Lint and guard errors with the rule or guard name
- Test failure messages and stack traces
- Build failures and their root causes

### 4. Categorize errors

Group errors by type:
- **Guard failures**: `npm run check:*` (typography, tokens, scope, secrets, migrations, context) with the guard name and the offending file:line
- **Linting issues**: `npm run check:hooki` (ESLint hooks rules) findings
- **Type and build errors**: `tsc` errors, `vite build` failures, missing imports, signature mismatches
- **Test failures**: Failing unit, Deno or Playwright tests with their names and failure reasons
- **Gate verdict NOT CHECKED (exit 2)**: a check could not run (missing stack, missing env); this is not a code error and must be reported as unchecked
- **Runner issues**: self-hosted `mac-mini` runner offline, job skipped, or timeout

### 5. Generate fix plan

Create a plan document (in plan mode, or as a written plan in your reply) with:
- **Problem Statement**: Summary of failing checks
- **Current State**: What errors were found and where
- **Proposed Changes**: Specific fixes needed for each error category
- **Validation Steps**: The narrowest commands that verify each fix (one `check:*`, `npm run typecheck`, one test file); the full gate runs again in CI after push

The plan should reference the `fix-errors` skill for detailed guidance on resolving specific error types.

## Important Notes

- **GitHub CLI paging**: Set `GH_PAGER=cat` on every `gh` invocation. The GitHub CLI does not support `--no-pager` as a global option; `GH_PAGER` and `PAGER` are its documented paging controls
- **Always create a plan first**: Never make code changes directly. Generate a plan for user review
- **Check test status in CI**: Even if tests fail locally, verify they passed in CI before flagging as issues
- **Unrelated test failures**: If tests passed in CI but fail locally, they may be environment-specific or flaky
- **Multiple error types**: Fix one category at a time (e.g., all type errors before tests)
- **The gate stops at the first failure**: `npm run bramka` exits on the first non-zero command, so later commands in the list were not checked; say so in the plan
- **Cross-reference fix-errors skill**: For detailed error resolution strategies, use the `fix-errors` skill

## Common CI Check Names

Workflow `warp-ci` (`.github/workflows/warp-ci.yml`, self-hosted runner `mac-mini`):
- `zakres` - decides what changed; a docs-only change skips the gate (`kod=false`), which is a skip, not a pass
- `ci` - runs `npm run bramka` (the full gate); the failing step log names the first red command

Check the latest run for a branch with `gh run list --branch <branch> --workflow warp-ci.yml --limit 1`.

## Example Commands

**Get PR status with details:**
```bash
GH_PAGER=cat gh pr view --json number,title,state,statusCheckRollup
```

**Get logs from specific failed run:**
```bash
GH_PAGER=cat gh run view 12345678 --log-failed
```

**Check for specific error in logs:**
```bash
GH_PAGER=cat gh run view 12345678 --log-failed 2>&1 | grep -A 5 "error:"
```
