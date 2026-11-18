# Zmiany względem warpdotdev/common-skills (fork Enkidu-png/common-skills, gałąź bazarty)

- Odkrywanie specyfikacji: `specs/GH<n>/` i `specs/<obszar>/` (obszar sprawdzany także, gdy nie był zmieniany).
- Walidacja zachowania: podagenci przez narzędzie Agent w osobnych worktree, z Playwright na lokalnej aplikacji na bazie DEV, zamiast chmurowych agentów Oz z computer use.
- Komendy walidacji: `npm run typecheck`, `npm run check:*`, testy jednostkowe, Deno i e2e; pełna `npm run bramka` w CI.
- `ask_user_question` -> `AskUserQuestion`, komentarze PR przez `gh`, prefiks `[agent]` i stopki commita z sesji zamiast `[Warp Agent]`.
