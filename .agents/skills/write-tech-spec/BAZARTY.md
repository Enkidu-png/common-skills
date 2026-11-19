# Zmiany względem warpdotdev/common-skills (fork Enkidu-png/common-skills, gałąź bazarty)

- Ścieżki specyfikacji: `specs/GH<n>/tech.md` albo `specs/<obszar>/TECH.md` (decyzje w sekcji Decisions tech.md; osobny DECISIONS.md jest opcjonalny jak w Warpie, tylko przy dużej funkcji) zamiast `specs/<id>/TECH.md` z Linearem, zgodnie z `specs/README.md` repo bazarty.
- Przykłady odwołań do kodu i sekcja Testing: nasz stos (TanStack Start, Supabase, funkcje edge Deno, Playwright, `npm run check:*`, `npm run bramka`) zamiast Rusta.
- Proposed changes jest miejscem decyzji architektonicznych, bo rejestr ADR jest zamrożony.
- Parallelization: narzędzie Agent + worktree + plugin boss zamiast `run_agents`/Oz (u nas niedostępne).
