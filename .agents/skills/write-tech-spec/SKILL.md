---
name: write-tech-spec
description: Write a TECH.md spec for a significant bazarty feature after researching the current codebase and implementation constraints. Use when the user asks for a technical spec, implementation plan, or architecture doc tied to a product spec.
---

# write-tech-spec

Write a `TECH.md` spec for a significant feature in bazarty (TanStack Start + React 19, Supabase Postgres with RLS, Deno edge functions, Stripe Connect, Furgonetka).

## Overview

The tech spec should translate product intent into an implementation plan that fits the existing codebase, documents architectural choices, and makes the work easier for agents to execute and reviewers to evaluate.

Write specs to one of two places (the repo's `specs/README.md` is the source of truth for both templates):

- a new feature tied to a GitHub issue: `specs/GH<n>/tech.md` (e.g. `specs/GH1234/tech.md`), next to `specs/GH<n>/product.md`
- a large, long-lived area (payments, shipping, chat, catalog, profile, ...): `specs/<obszar>/TECH.md`, with decisions in the Decisions section of its TECH.md

Match the directory used by the sibling `product.md` / `PRODUCT.md` when one exists. `specs/` should contain only `GH<n>` or area-named directories as direct children.

The tracker is GitHub Issues (`gh` CLI). If there is no issue yet, ask the user whether to file one or which area directory to use. Only create a new GitHub issue when the user explicitly asks for one.

## When to use

Use this skill when the implementation spans multiple modules, has meaningful architectural tradeoffs, or when reviewers will benefit from seeing the plan before or alongside the code. For pure UI changes or straightforward fixes, a tech spec is often unnecessary.

Prefer to have a `PRODUCT.md` first so the technical plan is anchored to agreed behavior. If the implementation is still too uncertain, build an e2e prototype first and then write the tech spec from what was learned.

## Research before writing

Before drafting, read the product spec (if any), inspect the relevant code, and identify the main files, types, data flow, and ownership boundaries. Do not guess about current architecture when the code can be inspected directly.
When referencing relevant code chunks in the spec, prefer commit-pinned references so future readers can inspect the exact code you researched. Capture the current commit SHA for each repository you inspected (for example, `git rev-parse HEAD`) and, when possible, make file references Markdown links to the corresponding GitHub `blob/<sha>/...#Lx-Ly` URL. Use the linked text to keep the path readable in the spec.

## Structure

Required sections:

1. **Context** — What's being built, how the current system works in the area being changed, and the most relevant files with line references. Combine the "problem," "current state," and "relevant code" into one grounded section. Example references:
   - [`src/routes/zamowienie.tsx:42 @ <commit-sha>`](https://github.com/Enkidu-png/bazarty-platforma/blob/<commit-sha>/src/routes/zamowienie.tsx#L42) - entry point for the user flow
   - [`supabase/functions/order-action/index.ts (120-220) @ <commit-sha>`](https://github.com/Enkidu-png/bazarty-platforma/blob/<commit-sha>/supabase/functions/order-action/index.ts#L120-L220) - edge function logic that will likely change
   Reference `PRODUCT.md` for user-visible behavior rather than restating it.
2. **Proposed changes** - The implementation plan: which modules change, new types/APIs/state being introduced, data flow, ownership boundaries, and how the design follows existing patterns. Call out tradeoffs when there is more than one reasonable path. In bazarty this section is where architectural decisions live (the ADR register is frozen; no new ADRs): name the chosen path, the rejected alternatives and why. Schema changes go through forward-only migrations in `supabase/migrations/` with RLS policies spelled out; error codes returned to clients by edge functions are listed in `docs/DOKUMENTACJA-EDGE-FUNCTIONS.md` (exception text never reaches the client, only a code and `request_id`).
3. **Testing and validation** - How the implementation will be verified against the product behavior. Owns everything about proving the feature works: unit tests (`npm run test:jednostkowe`, Deno tests for edge functions via `npm run test:deno`), Playwright e2e tests under `tests/e2e/<area>/`, targeted guards (`npm run typecheck`, `npm run check:*`), the full gate (`npm run bramka`, run by CI), manual steps on the running app, screenshots, videos, and any other verification. Reference the numbered Behavior invariants from `PRODUCT.md` directly rather than restating them; each important invariant should map to a concrete test or verification step. This section is where validation lives - `PRODUCT.md` intentionally does not have a Validation section.
4. **Parallelization** - Actively evaluate whether parallel sub-agents (launched with the `Agent` tool, each in its own git worktree, coordinated by the `orkiestrator-warp` plugin) would meaningfully reduce wall-clock time or isolate work. `run_agents` / Oz cloud agents are not available in this repo. When the spec proposes using sub-agents, include for each proposed agent:
   - A short name/role and the subtask it owns.
   - The git worktree it should use (one agent = one issue = one worktree), so parallel agents do not collide on the same checkout or files.
   - Branch and PR strategy: which branch each agent works on, the worktree path each agent will use, and how their work lands (one PR per agent, a single combined PR, etc.).
   - Coordination boundaries: which files/services each agent owns and how it syncs with sibling agents (messaging, merge points, validation ownership).

   Distinguish which steps can run in parallel and which must run sequentially. When the dependency graph is non-trivial, consider a short Mermaid diagram (`graph TD` or `flowchart LR`) so the reader can see fan-out and merge points at a glance.

   When parallelization is NOT proposed, briefly note why it isn't beneficial (e.g. the task is small, or subtasks are tightly coupled) so reviewers can challenge that judgment.

   Propose concrete defaults for worktrees, branch names, and execution mode rather than leaving them open-ended.

Optional sections — include only when they add signal. Omit the heading entirely if empty; do not write "None" as a placeholder.

- **End-to-end flow** — Include only when tracing the path through the system tells you something the Proposed changes list doesn't.
- **Diagram** — Include a Mermaid diagram only when a visual will explain the design faster than prose (data flow, state transitions, sequence across layers). Prefer one or two focused diagrams over decorative ones.
- **Risks and mitigations** — Include when there are real failure modes, regressions, migration concerns, or rollout hazards worth calling out.
- **Follow-ups** — Include when there is deferred cleanup or future work worth naming.

## Length heuristic

Right-size the spec to the feature:

- Single-file change with clear approach: skip the tech spec or keep it under ~40 lines.
- Multi-module change with some ambiguity: target ~80-150 lines.
- Large cross-cutting or architecturally novel change: longer is fine when every section earns its place.

If Context and Proposed changes end up describing the same files and state from different angles, collapse them.

## Writing guidance

- Ground the plan in actual codebase structure and patterns.
- Pin important code references to a commit SHA and link them to the corresponding GitHub lines when the repository has an accessible remote.
- Prefer concrete implementation guidance over generic architecture language.
- Explain why the proposed design fits this repo.
- Reference `PRODUCT.md` for behavior instead of restating it.
- Each section should earn its place — if a section would repeat another or contain only boilerplate, omit it.

## Keep the spec current

Approved specs may ship in the same PR as the implementation. Update `TECH.md` in the same PR when module boundaries, implementation sequencing, risks, validation strategy, or rollout assumptions change. The checked-in spec should describe the implementation that actually ships.

For large features, the implementer may optionally keep a `DECISIONS.md` file summarizing concrete decisions. Offer it when it would help future agents; otherwise skip it. By default decisions stay in `tech.md` (Proposed changes for `specs/GH<n>/`, the Decisions section for `specs/<obszar>/`).

## Related Skills

- `implement-specs`
- `write-product-spec`
- `spec-driven-implementation`