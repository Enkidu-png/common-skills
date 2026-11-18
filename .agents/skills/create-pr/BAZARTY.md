# Zmiany wzgledem warpdotdev/common-skills

- Galaz bazowa `main` (praca nad przejsciem: `warp/przejscie`) zamiast `master`; zakaz pushu i merge'a do `main`.
- Linear zamieniony na GitHub Issues (`Fixes #N`), dopisany trailer `Scope-Files` dla `check:zakres`, opis PR po polsku.
- Walidacja z Rusta (clippy, ./script/format, presubmit) zamieniona na `npm run typecheck`, `check:*`, prettier i bramke w CI `warp-ci.yml`.
- Test ukladu widoku w Ruscie zamieniony na dowod wizualny; skille testowe to nasze `testy-e2e` i `testy-jednostkowe`; `add-feature-flag` usuniety (nie bierzemy go).
