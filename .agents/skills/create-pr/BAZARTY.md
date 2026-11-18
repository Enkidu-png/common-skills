# Zmiany wzgledem warpdotdev/common-skills

- Galaz bazowa `dev` (galaz domyslna, ADR 320; praca nad przejsciem: `warp/przejscie`) zamiast `master`; `main` tylko wydaniem albo pilna poprawka wg `.ai/docs/RUNBOOK-WYDANIE.md`, po zgodzie wlasciciela. `gh pr create --base dev` w przykladach. `Refs #N` dla limitu szybkiej sciezki; `Fixes #N` zamyka issue tylko przy scaleniu do `dev`.
- Linear zamieniony na GitHub Issues (`Fixes #N`), dopisany trailer `Scope-Files` dla `check:zakres`, opis PR po polsku.
- Walidacja z Rusta (clippy, ./script/format, presubmit) zamieniona na `npm run typecheck`, `check:*`, prettier i bramke w CI `warp-ci.yml`.
- Test ukladu widoku w Ruscie zamieniony na dowod wizualny; skille testowe to nasze `testy-e2e` i `testy-jednostkowe`; `add-feature-flag` usuniety (nie bierzemy go).
