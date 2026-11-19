# Zmiany w forku bazarty (Enkidu-png/common-skills, gałąź bazarty)

- `run_agents` (Oz) zastąpione narzędziem `Agent`: jeden worker = jedno wywołanie, równoległość przez kilka wywołań w jednej wiadomości, dopytanie przez `SendMessage`, `worker_run_id` = id agenta. Powód: w Claude Code nie ma Oz.
- `ask_user_question` -> `AskUserQuestion` (domyślna opcja pierwsza z dopiskiem „(Recommended)").
- Zdalni workerzy z computer use usunięci: walidacja w przeglądarce lokalnie przez Playwright. Worktree w `.warp-wt/` albo `isolation: "worktree"`.
- Przy roli `boss:orkiestrator` ścieżka sagi trafia też do stanu pluginu, a przed kompakcją idzie `boss:handoff`. Kontrakt zadania, fazy i szablony bez zmian.
