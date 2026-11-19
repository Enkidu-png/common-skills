---
name: reproduce-bug-report
description: Launch subagents (Agent tool) driving a local Playwright browser to reproduce UI-focused bug reports, capture visual evidence (a screen recording by default), and report reproduction findings. Use when investigating a specific interactive or visual bug from an issue, ticket, support report, or prompt.
---

# Reproduce bug report

Use this skill when the current context is a GitHub issue, support report, tester report, or user prompt describing a specific bug that may be reproduced through visible application behavior. It is primarily for UI, rendering, layout, forms, checkout, chat, onboarding, or other interactive bugs where a screen recording (or screenshots) makes the result more actionable.

The parent agent should not try to manually reproduce the UI bug itself unless the user explicitly asks. Launch one or more subagents with the Agent tool (Oz cloud agents and `run_agents` are not available here); each child drives a Playwright browser against the app, interacts with it, and captures visual evidence. When children need a dev server or code changes, give each its own worktree (`isolation: "worktree"`).

## Parent workflow

1. Read the bug report carefully and extract:
   - reported behavior
   - expected behavior
   - reproduction steps, if provided
   - device and browser (phone or desktop width), app instance (local dev, the testers' instance, production), account role (buyer, creator, admin), or other environment constraints when relevant
   - attached screenshots, videos, logs, or comments that narrow the repro path
2. Decide whether this skill applies:
   - Use it for UI-visible bugs, interaction bugs, rendering/layout bugs, onboarding bugs, and bugs where a screen recording (or screenshots) would be useful.
   - Do not use it for purely backend, CI, build, dependency, or text-only code issues unless the prompt specifically asks for visual reproduction.
   - If the report requires credentials, private account state, or another capability not available to the repro environment, report that constraint clearly instead of guessing.
3. If the reproduction path is straightforward, launch one subagent.
4. If there are multiple plausible repro paths, launch several subagents in a single message so they run in parallel. Give each child a distinct hypothesis or environment variant, such as:
   - phone width vs desktop width, Chromium vs WebKit
   - logged out vs logged in, buyer vs creator account
   - fresh account vs an account with existing orders, boards, or chats
   - local dev server vs the testers' instance
   - different data states (empty list, one item, many items)
5. If steps are incomplete, use codebase knowledge to propose likely app states and assign children to investigate those states. Do not invent facts about the original reporter's environment.
6. Wait for all children to report before summarizing. Distinguish confirmed reproduction, partial reproduction, non-reproduction, blockers, and untested hypotheses.

## Version and app setup

- Prefer reproducing against the same app instance and commit the reporter used (the testers' instance runs a known deployment; production is `main`).
- Do not silently substitute a different branch or instance when a closer reporter-matched one is available.
- Prefer a local dev server on the matching commit when the repro needs code inspection or must not touch shared data; prefer the deployed instance when the bug may depend on the deployment.
- If the exact deployment or commit cannot be determined, report that clearly, explain what was attempted, and use the closest justified fallback only when it is useful for continuing the investigation.
- Record the reporter's instance and commit, the tested instance and commit, and any fallback decision in the manifest and final report.

## Repository-specific guidance

The consuming repository may ship a companion `reproduce-bug-report-local` skill. When that companion is available or referenced in the prompt, read it and apply its repository-specific scope, app setup, environment, and workflow guidance as supplemental instructions. The local companion may narrow scope or specialize setup, but it should not redefine the evidence, artifact, reporting, or safety expectations in this core skill.

Launch the children with the Agent tool, one call per child in a single message, shaped like this:

```text
Agent(description: "repro-primary", prompt: <shared child prompt> + <primary repro prompt>)
Agent(description: "repro-variant", prompt: <shared child prompt> + <variant prompt>, isolation: "worktree")
```

Omit extra children when they would duplicate the same steps. Omit `model` unless the user requested a specific model. For a long multi-child investigation, track children through the `boss` plugin.

## Shared child prompt

Give every child agent these shared instructions, then append the child-specific repro path or hypothesis.

```text
You are trying to reproduce a reported UI bug by driving a Playwright browser.

Goal:
- Reproduce the reported behavior as faithfully as possible.
- Capture a screen recording of the reproduction by default; most UI bugs involve motion, a transition, or a multi-step interaction, so a clip is stronger proof than stills. Capture screenshots as a supplement, or as the primary artifact only for a genuinely static render.
- If the provided steps are unclear or incomplete, use codebase and product knowledge to identify plausible app states that could produce the reported behavior, then test the assigned hypothesis.
- Report clear reproduction evidence, not just opinions.

Inputs:
- Bug report context: <paste or summarize the issue body, comments, screenshots/video descriptions, labels, and relevant metadata>
- Assigned repro path or hypothesis: <specific steps, environment, app state, settings, feature flags, or code path to test>
- Reporter app instance/commit: <exact value from the report, or unknown>
- App target: <URL or local dev server on a given commit, or the justified fallback if the exact one is unavailable>

Safety and privacy:
- Do not ask the public reporter for credentials, tokens, private repos, private workspace names, or private account identifiers.
- Do not include secrets, auth tokens, private URLs, Authorization headers, refresh tokens, or other private account details in recordings, screenshots, logs, manifests, or final reports.
- Do not create or sign into an account unless the prompt and repository-specific guidance explicitly authorize a safe test-auth workflow (for example the documented test accounts).
- If the assigned report cannot be exercised within the allowed auth/state constraints, stop and report the blocker.
- Do not post comments to GitHub or external services unless explicitly instructed. When the prompt names a GitHub issue to report back to, post the reproduction summary as a comment on that issue only; do not post anywhere else.
- Avoid destructive actions. Shared databases hold real testers' data: never reset a database or delete data you did not create. If a repro requires deleting app state, delete only test state you created for this repro and report exactly what was reset.

Artifact workflow:
- Create a dedicated artifact directory named for your variant, such as `screenshots/bug-repro-primary/`.
- Record a video of the reproduction by default (Playwright `recordVideo` on the browser context, or a trace with screenshots) and save it in the artifact directory with a descriptive name such as `repro.webm`.
- Capture screenshots as a supplement (or as the primary artifact only for a genuinely static render) with ordered filenames, such as `01-initial-state.png`, `02-before-click-settings.png`, and `03-after-click-settings.png`.
- Maintain a short manifest in the artifact directory with:
  - recording or screenshot filename
  - timestamp
  - visible app state
  - action just taken or about to be taken
  - whether the screenshot shows the reported bug
- If the harness supports built-in screenshot or artifact upload, use it. Otherwise leave artifacts in the directory and report the paths.

Reproduction workflow:
1. Confirm the environment you are testing: browser and viewport, app URL, which database the app talks to, and the commit if visible.
2. Identify the exact reporter instance/commit from the report when available, then use the closest repository-approved target.
3. If no exact reporter instance is available, record that it is unknown and choose the most defensible target for the report; state the fallback explicitly.
4. Start from the cleanest state that matches the report. Do not reset app state if the bug depends on existing settings or persisted local state.
5. Reach the baseline app state required by the report before attempting the bug-specific reproduction.
6. Start the video recording and capture a baseline screenshot before attempting the bug-specific reproduction.
7. Follow the exact provided bug reproduction steps first, when available.
8. If exact steps do not reproduce, test the assigned hypothesis and document where it diverges from the report.
9. If the bug appears, stop changing variables and capture enough evidence to make the reproduction actionable.
10. If the bug does not appear, make at most two targeted variations that are directly supported by the report or code-path hypothesis.
11. If the app crashes, hangs, or blocks progress, capture a screenshot and collect non-sensitive logs or terminal output that explain the blocker.

Code-path investigation for unclear steps:
- Search the codebase for UI strings, labels, feature names, route names, edge function names, and components mentioned in the report.
- Identify the likely component, query, RLS policy, edge function, or state transition that could produce the reported behavior.
- Use that investigation to choose targeted UI actions rather than broad exploratory clicking.
- Report the files or symbols that informed your hypothesis, but keep the final report focused on reproduction evidence.

Report back:
- A brief bug summary before the verdict, including the issue/report identifier if available, the reported behavior, and the expected behavior.
- Reproduction status: confirmed, partially confirmed, not reproduced, or blocked.
- The exact steps you performed.
- Environment and app/build information.
- Reporter instance/commit, tested instance/commit, and the fallback explanation if they differ.
- Whether the observed behavior matched the report, and how closely.
- The screen recording (and any supplementary screenshots) with short descriptions and artifact paths or attachment names.
- Any logs, crash output, or diagnostics collected, with secrets redacted.
- The most likely code path or state involved, if investigated.
- Suggested next debugging step or follow-up question, only if it would materially change the next action.
```

## Child prompt patterns

### Primary repro child

Use this for a report with clear steps:

```text
You own the primary reproduction attempt.

Follow the bug report's steps exactly before trying variants. Prioritize matching the reporter's device width, browser, account role, and data state. If those details are missing, choose the most common path and explicitly list assumptions.
```

### Variant child

Use this when there is a specific alternate condition worth testing:

```text
You own this reproduction variant: <variant name>.

Test only this variant's assigned environment or state. Do not duplicate the primary child's full search space. Report whether this variant changes the outcome and include screenshots for any difference.
```

### Code-path hypothesis child

Use this when repro steps are missing or ambiguous:

```text
You own code-path-guided reproduction.

Start by tracing likely code paths from strings, UI labels, settings names, feature names, or screenshots in the report. Then choose a targeted UI path that should exercise the suspected state. Report the code paths you used to form the hypothesis and the visual result of testing it.
```

## Success criteria

A successful use of this skill produces:

- A confirmed reproduction with a screen recording (and screenshots where useful) and exact steps, or a well-scoped non-reproduction with tested assumptions.
- Clear artifact paths or attachments for visual evidence.
- A concise summary of which variants were tested and which were not.
- Enough environment detail for an engineer to repeat the test.
- No leaked secrets, credentials, private account details, or unnecessary public comments.

## Summary format

When the children finish, summarize in this structure:

```text
Bug summary:
- Issue/report: <identifier or source>
- Reported behavior: <what bug the child attempted to reproduce>
- Expected behavior: <what should have happened instead>
Reproduction status: <confirmed | partially confirmed | not reproduced | blocked>

What was tested:
- <variant/child>: <steps and environment>

Evidence:
- <screenshot/artifact path>: <what it shows>

Findings:
- <observed behavior vs reported behavior>
- <likely state/code path, if known>

Next step:
- <one concrete debugging action or follow-up question>
```
