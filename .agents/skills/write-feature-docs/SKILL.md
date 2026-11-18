---
name: write-feature-docs
description: Draft a complete Polish documentation page (Markdown in `docs/`) for a shipped bazarty feature from its product.md and/or tech.md spec. Use at release time, when a feature has shipped and needs a human-facing doc, when the owner asks to write docs for a feature, draft a docs page, or convert a spec into documentation. Also handles features without specs by researching the codebase first. Requires an interactive session with the owner present - it confirms a content design plan, then an outline, before drafting, and cannot run unattended.
---

# write-feature-docs

Draft a complete documentation page for a shipped bazarty feature. You read the feature's spec, verify technical claims by researching the codebase yourself, confirm the content design plan and then the outline with the owner, and only then produce a complete Markdown draft in `docs/` and open a PR in this repo with the owner as the reviewer.

Docs in `docs/` are for humans (the owner, testers, future collaborators), so they are written **in Polish**. The repo's split applies: `docs/` belongs to humans, `.ai/` and `specs/` to agents. Docs are written **at release time** for features that have shipped, not when a spec merges.

The owner's job is to confirm what you couldn't verify from the spec and code - not to do a full accuracy review, not to polish prose, not to know docs conventions.

## The workflow

1. Find and read the spec files
2. Research the codebase to verify technical claims - minimize what the owner needs to check
3. Present the content design plan and wait for confirmation - who the page is for
4. Present the outline and wait for confirmation - what the page will contain
5. Generate the complete Markdown draft
5.5. Attempt screenshot capture on the running app (if a browser tool is available)
6. Open a PR in this repo and request the owner's review

Steps 3 and 4 are **two separate confirmations, in that order.** The outline is derived from the plan - the plan picks the content type, and the content type determines what sections the outline has. Presenting them together would show the owner an outline built on an audience they have not agreed to yet, and they would anchor on the concrete outline instead of reconsidering the question above it. Settle who the page is for, then decide what goes in it.

---

## Step 1: Find and read the spec

Ask the owner for the issue number or area if they haven't provided it. Specs live in one of two places (see `specs/README.md`):
- a feature tied to a GitHub issue: `specs/GH<n>/product.md` and `specs/GH<n>/tech.md`
- a large area: `specs/<obszar>/PRODUCT.md`, `TECH.md`, `DECISIONS.md`

`product.md` / `PRODUCT.md` is the primary source: user-facing behavior, what and why. `tech.md` / `TECH.md` is the secondary source: implementation, data model. Read both if both exist. The product spec is the primary driver for the docs content.

**When reading the tech spec:** Before incorporating anything from it, identify content that looks like internal implementation detail - database schema and RLS policies, edge function names, Supabase project refs, secrets and env var names, Stripe or Furgonetka account details, internal endpoints. Present these flagged items to the owner and ask them to confirm what's safe to include and what should stay internal. Do not include anything marked confidential in the draft. Never copy secrets, keys, test account passwords or project refs into `docs/`.

This confirmation is why the skill requires a present owner. There is no unattended path: without someone to say what is safe to publish, tech spec content cannot be drafted at all.

If neither file exists, skip to [No-spec fallback](#no-spec-fallback).

---

## Step 2: Research the codebase

Before presenting the plan or the outline, verify as much technical content as possible yourself from the local checkout (and `gh` for issues and PRs) - reducing what the owner needs to confirm to only what you genuinely cannot determine from the code.

Things to verify from code:
- **Feature switches**: flags and settings that gate the feature (for example `sprzedaz_wlaczona`, env switches like `BAZARTY_ENV`), searched in `src/`, `supabase/functions/` and `supabase/migrations/`.
- **UI strings**: user-visible button labels, menu item names, page titles referenced in the spec (`src/routes/`, `src/components/`).
- **Routes and navigation paths**: confirm exact paths and how the user reaches them (e.g. **Panel twórcy** > **Zamówienia**, route `/dashboard/...`).
- **Error codes and messages** the user can see: check `docs/DOKUMENTACJA-EDGE-FUNCTIONS.md` and the edge function code.
- **Related features**: identify other docs in `docs/` that cross-reference this one for "Powiązane".

For each claim you verify from code, mark it confirmed. For claims you can't verify (UI behavior not in code, product intent, behavior of unreleased features), flag them as `[UNVERIFIED]` in the outline - those are the only things the owner needs to focus on.

---

## Step 3: Present the content design plan and wait

**This is the first of two confirmations, and it comes before the outline.** Settle who the page is for before deciding what goes in it.

Fill in this plan (short answers, one or two lines each):

```
PLAN TREŚCI dla [Nazwa funkcji]
  Odbiorca i zadanie:     [kto czyta (twórca, kupujący, właściciel, tester) i co chce zrobić]
  Problem:                [co go blokuje bez tej strony]
  Cele strony:            [co czytelnik umie po lekturze]
  Wartość:                [dlaczego ta strona, a nie sam interfejs]
  Typ treści:             [opis funkcji | koncepcja | procedura | referencja | rozwiązywanie problemów | szybki start]
  Scenariusze:            [2-4 najważniejsze sytuacje, które strona obsługuje]
  Poza zakresem:          [czego strona świadomie nie omawia]
```

Print it to the terminal, then say:

> "Before I outline the page, please confirm this is the right reader and the right job. Correct anything that's off, or say 'looks good' and I'll draft the outline."

**Wait for the owner's reply.** Do not produce the outline in the same message. The plan decides the content type, and the content type decides what sections the outline has - an outline shown alongside an unconfirmed plan invites the owner to anchor on the concrete sections in front of them rather than question the audience above them.

If they change the audience, the content type, or the scope, revise the plan and re-confirm before moving on. Carry the confirmed plan into the PR body in Step 6.

---

## Step 4: Present the outline and wait

Generate a concise outline - no prose - built on the **confirmed** plan from Step 3. The outline shows what you've confirmed from research and exactly what still needs owner input.

Print the outline to the terminal in this format:

```
Konspekt dokumentu: [Nazwa funkcji]

UMIEJSCOWIENIE
  Plik:     docs/<NAZWA-FUNKCJI>.md   (istniejący plik w docs/, jeśli już opisuje ten obszar)

SEKCJE
  # <Nazwa funkcji>
  Akapit otwierający: [1 zdanie o tym, co napiszesz]
  ## Najważniejsze możliwości - [2-4 możliwości jako punkty]
  ## Jak to działa - [model pojęciowy: co i dlaczego, bez kroków]
  ## <Tytuł sekcji użycia> - [np. "Wystawianie pracy", "Zwrot zamówienia"]
      Wymagania: [co musi być spełnione]
      Kroki:
        1. [Opis kroku]
        2. [Opis kroku]
        ...
  ## Powiązane - [odnośniki do innych dokumentów w docs/]
```

> The sections above are defaults. Adapt the outline to the feature: omit `## Jak to działa` if the feature needs no conceptual explanation, add multiple usage sections if the feature has distinct workflows, and collapse `## Najważniejsze możliwości` into the opening paragraph if the feature is simple enough.

```
SPRAWDZONE W KODZIE
  - [np. "Trasa: /dashboard/zamowienia potwierdzona w src/routes/dashboard.zamowienia.tsx"]

DO TWOJEGO POTWIERDZENIA
  - [np. "Krok 3: czy wypłata startuje sama, czy wymaga akcji twórcy?"]
```

After printing the outline, say:

> "I've verified what I could from the codebase. Please check the items under DO TWOJEGO POTWIERDZENIA and reply with any corrections, or say 'looks good' to proceed."

Wait for the owner's reply before continuing. Incorporate their feedback, then draft.

If their feedback contradicts the plan confirmed in Step 3 - a different reader, a different content type - revise the plan too rather than letting the two drift apart. The plan travels into the PR body, so a stale one misleads the reviewer.

---

## Step 5: Generate the Markdown draft

Generate a complete `.md` file in `docs/` based on the confirmed outline. Prefer updating an existing file in `docs/` over creating a new one whenever a file already covers the surface. Use the shape of the outline: one `#` title, an opening paragraph, then `##` sections.

### Style rules - apply exactly

- **Language**: Polish, addressed to the reader as "ty" ("możesz", "kliknij"), natural and warm, no slang. Brand voice: `docs/GLOS-MARKI.md`; the brand name is written lowercase (`bazarty`).
- **Vocabulary**: the place where a creator sells is **pracownia** (or **bazart**), never "sklep", "storefront" or "konto sprzedawcy".
- **Glyphs**: never use the separator glyphs banned in AGENTS.md (middle dot, bullet, em dash, en dash). A range or contrast uses a hyphen `-` (`1-2 dni robocze`). Lists use `-` or numbers.
- **Headings**: sentence case - capitalize only the first word and proper names.
- **Lists**: bold term + hyphen + description: `- **Termin** - opis`. Never a colon after the bold term.
- **UI elements and paths**: bold for buttons, links, menu items: `Kliknij **Zapisz**`. Bold each segment of a navigation path, leave `>` plain: `**Panel twórcy** > **Zamówienia**`.
- **Voice**: active voice, present tense for how things work, imperative for instructions. Avoid "po prostu", "łatwo", "wystarczy" - they dismiss the reader's experience.
- **No emoji.**
- **Callouts**: a plain blockquote starting with a bold word (`> **Uwaga:** ...`), no HTML, no colored boxes.

**What to leave as `[TODO: recenzent - ...]` placeholders**
- Screenshots where capture fails the quality gate, is unavailable, or the feature isn't yet shipped
- Video/GIF embeds
- Any behavior that remained unverified after the owner's confirmation

---

## Step 5.5: Capture screenshots on the running app (if available)

After generating the draft, attempt to capture screenshots for any `[TODO: recenzent - zrzut ekranu]` placeholders. This step is **optional** - only run it if a browser tool is available (Playwright, or the Chrome browser tool). If none is available, leave all placeholders as-is.

### Decide which screenshots to attempt

Only attempt screenshots where **all** of the following are true:
- The feature is already shipped (not behind a disabled switch or unreleased)
- The UI state can be reliably navigated to programmatically
- The placeholder specifies a concrete UI surface (not vague like "show the feature working")

Skip screenshots that require account-specific state, specific data, or content that would expose sensitive information.

### Pre-capture setup

Before taking any screenshot:
1. Run the app locally (`npm run dev`) and check the startup banner: it must say `srodowisko=DEV`. Never capture against the production database. Use the test accounts from `.env.example`, never real users' accounts.
2. Navigate to the relevant UI surface or trigger the relevant feature state, at a consistent viewport size (desktop and, when the feature is mobile-first, a phone viewport).
3. **Wait** for all animations to complete and the UI to be fully settled
4. Dismiss any unrelated popups, notifications, or toasts that aren't part of the feature being documented
5. Close any panels not relevant to this screenshot
6. **Verify no sensitive data is visible**: check for tokens, API keys, email addresses of real people, addresses, phone numbers, payment details or personal information. If any is visible, do not take the screenshot.

### Capture protocol: predict → capture → verify → retry once

This is a structured self-verification loop. Do not skip it — it's the primary guard against wrong-state, wrong-crop, and wrong-framing captures.

**Step 1: State the expectation before capturing**

Before taking any screenshot, write out what you expect to see:

```
CAPTURE EXPECTATION
  Subject:            [The specific UI element or surface being documented]
  Expected elements:  [2-3 specific things that MUST be visible — e.g. a panel title, a button, a specific setting]
  Expected state:     [The UI state — e.g. "Settings panel open", "Modal visible", "Feature active and showing output"]
  Must not contain:   [Anything that must NOT be visible — e.g. sensitive data, unrelated popups, loading spinners]
```

**Step 2: Capture**

Take the screenshot.

**Step 3: View and verify against the expectation**

Use the browser tool to view the captured image, then check it against the expectation:

- Is the stated **subject** visible and clearly the focal point?
- Are all **expected elements** present?
- Is the UI in the **expected state** (not a transitional or loading state)?
- Is anything from **must not contain** visible?
- Is text **legible** at the target display width?

If all pass → proceed to the quality gate.

If any fail → **attempt once more**: re-navigate to the UI state, wait longer for the UI to settle, then re-capture and re-verify.

If the second attempt also fails → **discard** the screenshot and leave the `[TODO: recenzent - zrzut ekranu]` placeholder. Do not include a screenshot you can't verify.

**Step 4: Quality gate — final check before including**

- [ ] Text in the screenshot is **legible** at the target display size
- [ ] The documented UI element is **clearly the focal point** — not buried, cropped out, or obscured
- [ ] **No sensitive data** is visible (tokens, private repos, personal info, customer data)
- [ ] UI is in a **stable, non-loading state** — no spinners, skeleton screens, or transitional states
- [ ] Screenshot **matches the capture expectation** stated before capture
- [ ] The screenshot would make sense at its target rendered width without looking blurry or oversized

If any item fails, discard the screenshot and leave the `[TODO: recenzent - zrzut ekranu]` placeholder.

> **Maximum attempts per screenshot: 2.** If both fail, move on.

### Sizing and placement

Crop unnecessary empty space. Keep sequences of screenshots in the same section at the same width. Insert each screenshot immediately after the paragraph that introduces the UI or state it shows, near configuration instructions, or near result explanations. Do **not** add a screenshot for every step in a procedure. Only add one where the visual genuinely aids comprehension.

### Markdown format

```markdown
![Opis tego, co widać na obrazku, nie samo "zrzut ekranu"](obrazy/<nazwa-funkcji>-<stan>.png)

*Podpis: pełne zdanie, do 10 słów, orientuje, nie instruuje.*
```

**File location:** Save PNGs to `docs/obrazy/` (lowercase, hyphens, descriptive names). Working screenshots that are not part of the doc go to `screenshots/` (gitignored), never to the repo root.

---

## Step 6: Open the PR

**Before opening the PR, confirm the feature is shipped**: merged to `main` and reachable by users on a public surface. If not, do not open a PR - tell the owner why and stop. This is worth checking even though the owner asked for the page, because drafting for something that has not shipped yet is the most common failure, and someone close to the work can easily be a release ahead of their users.

Then submit the draft to this repo:

1. Work on a new branch named `docs/GH<n>-dokumentacja` (or `docs/<obszar>-dokumentacja`) in a git worktree, branched from the current base branch.
2. Write the Markdown file to `docs/<NAZWA>.md` and screenshots to `docs/obrazy/`.
3. Commit and push, then **write the PR body to a temp file and open the PR with `--body-file`**. The PR is in Polish. The body must include:
   - The feature name and issue number (`#<n>`) or area
   - A link to the spec (`specs/GH<n>/` or `specs/<obszar>/`)
   - A `## Plan treści` section with the plan confirmed in Step 3
   - A list of all `[UNVERIFIED]` and `[TODO]` items in the draft for reviewer attention

   Write the body to a temp file using whatever file-writing method is available (a file-creation tool, a Python `open()` call, or a shell `cat` with a quoted heredoc), then pass it to `gh`:
   ```bash
   gh pr create --body-file <temp-file> ...
   ```

   **Never pass the PR body inline** (via `--body "..."`, `echo`, or `printf` piped directly to `gh`). Shell string interpolation expands backticks, `$vars`, and `[ ]` glob patterns before the string reaches `gh`, corrupting any markdown that contains those characters. Writing to a file first avoids all shell interpretation of the content.

   **In the "Docs outline" section of the PR body, use plain bullet points** (`-`) for agent-verified items, not `- [x]` checkboxes. Reserve `- [ ]` checkboxes only for the "Items needing review" section so reviewers know exactly which items require their action.

4. The reviewer is the owner (the repository owner). Never merge the PR yourself.

---

## No-spec fallback

If no spec exists for the feature, research the codebase first before interviewing the owner.

**Research steps:**
1. Search the local checkout for the feature name and related terms (`src/`, `supabase/functions/`, `supabase/migrations/`).
2. Read the most relevant source files to understand what the feature does.
3. Check for a spec under another directory in `specs/`.
4. Review recent merged PRs and the issue: `gh pr list --search "<feature-name>" --state merged --limit 10`, `gh issue view <n>`.

**After research,** build as complete a picture as possible, then ask the owner only about specific gaps you couldn't fill from the code - not as a broad interview. Frame the questions concretely: "I found the feature in `src/components/messages/`. Based on the code, here's what I understand: [summary]. I couldn't determine these two things: [specific questions]."

Build the plan and outline from your research and the owner's targeted answers, then work through Step 3 (plan confirmation) and Step 4 (outline confirmation) before drafting.

---

## Interactive only - there is no unattended mode

A merged spec is not a shipped feature, and no unattended run can tell the difference. Skipping outline confirmation also removes the one checkpoint where a human could redirect the draft before the prose was written.

Do not add an unattended path here. If you are running without an interactive session, stop and report that this skill requires one, rather than drafting anyway.

---

## Related skills

- `write-product-spec` - produces the product spec this skill reads
- `write-tech-spec` - produces the tech spec this skill reads
