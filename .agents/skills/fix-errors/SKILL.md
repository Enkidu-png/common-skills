---
name: fix-errors
description: Fix build errors, type errors, lint issues, guard (check:*) failures, and test failures in the bazarty TypeScript codebase (TanStack Start, React 19, Supabase, Deno edge functions). Covers the validation gate (npm run bramka), running specific checks and tests, and Deno-specific errors. Use when the user hits build or typecheck errors, check:* guard failures, test failures, or needs to run or interpret the gate before a PR.
---

# fix-errors

Fix build errors, type errors, lint issues, guard failures, and test failures in the bazarty TypeScript codebase.

## Overview

This skill helps resolve common issues encountered during development, including:
- Type errors (`tsc`), unused imports, wrong prop types
- Build failures (`vite build` and its post-build checks)
- Repo guards (`npm run check:*`: typography, tokens, scope, secrets, migrations, context)
- Deno-specific errors in Supabase edge functions
- Test failures (unit scripts, Deno tests, Playwright e2e)

Fix the reported failure with the narrowest useful command. Do not turn a targeted repair into repeated full-gate validation.

## Full Gate

Run the full gate only when the user, task, or approved spec explicitly requires it:

```bash
npm run bramka
```

This runs every command listed in the gate config in order and stops at the first non-zero exit (`npm run bramka -- --lista` prints the list without running it). Exit codes: `0` green, `1` red, `2` NOT CHECKED (report it with the reason, never treat it as green). It is intentionally broader and more expensive than the default implementation workflow; CI (`.github/workflows/warp-ci.yml`) runs it for every PR.

### Individual Checks

Run checks separately when debugging specific issues:

**Types:**
```bash
npm run typecheck
```

**Build (includes source-map and build-version checks):**
```bash
npm run build
```

**Repo guards (each is a separate script under `scripts/`):**
```bash
npm run check:typo      # forbidden glyphs in user-facing text
npm run check:tokeny    # palette copies vs src/styles.css
npm run check:zakres    # diff scope (Scope-Files) and shadcn duplicates
npm run check:kontekst  # dead .md links, skill frontmatter, AGENTS.md size
npm run check:secrets
npm run check:migracje  # supabase/migrations vs migration registry
```

**Hooks lint (part of the gate; `npm run lint` is not):**
```bash
npm run check:hooki
```

**Unit tests:**
```bash
npm run test:jednostkowe
```

**Deno edge functions:**
```bash
npm run test:deno
```

**End-to-end (Playwright):**
```bash
npm run test:e2e:smoke
```

## Running Specific Tests

**Single Playwright file:**
```bash
npx playwright test tests/e2e/<obszar>/<plik>.spec.ts
```

**Filter by test title:**
```bash
npx playwright test -g "<substring>"
```

**Single Deno test file:**
```bash
deno test --allow-env --allow-net --allow-read supabase/functions/<nazwa>/<plik>.deno-test.ts
```

**Single unit script:**
```bash
node scripts/<test-skrypt>.mjs
```

## Common Error Types

### Unused Imports
Remove unused `import` statements identified by the compiler or lint.

### Unused Constants
Remove constants that are defined but never used.

### Unknown Imports
Add the correct `import` for undefined identifiers. Search the codebase to find the correct module path (aliases such as `@/` resolve to `src/`).

### Type Mismatches
Update calls to pass arguments of the correct type. Common fixes:
- Narrow `string | null` before use instead of asserting with `!`
- Use the generated Supabase row types instead of hand-written shapes
- Convert at the boundary (`Number(...)`, `String(...)`) rather than widening a type to `any`

### Object Shape Changes
When a type adds/removes fields, update all places where it's constructed or destructured:
- Object literals and default values
- Destructuring in components and hooks
- Mappers between database rows and UI types

### Function Signature Changes
When a function adds a new parameter, update all call sites to provide the new argument:
- For `boolean` params: pass `true` or `false` based on context
- For optional params: pass `undefined` as default or the value if needed

### Union and Enum Changes
When adding a new member to a union or enum, update exhaustive `switch` statements and lookup maps:
- Add a new case with appropriate handling
- Mirror the implementation pattern of similar members

### Incorrect Interface Implementation
Fix implementations that return the wrong type or don't satisfy the declared interface.

### Deno-Specific Errors

Supabase edge functions (`supabase/functions/**`) run on Deno, not Node. They are typechecked by `deno check`, not by the app's `tsc`.

**Common Deno errors:**
- Node-only imports (`node:fs`, npm packages without an `npm:` specifier) in an edge function
- Imports from `src/` that pull browser or Vite-only code into a function
- Missing environment variables in tests (`Deno.env.get` returns `undefined`)

**Fixes:**
- Import through `npm:` or `jsr:` specifiers, or move shared code to `supabase/functions/_shared/`
- Keep error details server-side: the client gets a code and `request_id`, never the exception text

Deno errors are discovered by running:

```bash
npm run test:deno
```

## Best Practices

**Before fixing:**
- Read the full error message to understand the root cause
- Check if multiple errors are related (fixing one may resolve others)
- For type errors, verify you understand the expected vs actual types
- For edge function errors, check whether the code runs on Deno or in the app

**When fixing:**
- Fix one error type at a time when there are multiple issues
- Run the smallest applicable check (`npm run typecheck`, one `check:*`) when it helps resolve errors; do not repeat broad checks without a relevant code change
- For Deno errors, run `npm run test:deno` to verify the fix
- For complex changes, run relevant tests after fixing

**After fixing:**
- Run the relevant tests and fix the code until they pass
- Run `npm run typecheck` and the guards related to the change, and fix their findings; return to affected tests only when a fix materially changes behavior
- Run the formatter (`npx prettier --write <changed files>`) once after all other code changes are complete
- Do not rerun tests or checks after formatting, and do not add a full gate run, unless explicitly required
- If you only fixed a formatting failure and made no behavioral code change, rerun only the formatter
