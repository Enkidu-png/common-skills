# Zmiany w forku bazarty (Enkidu-png/common-skills, gałąź bazarty)

- `run_agents` (Oz, lokalny child) zastąpione narzędziem `Agent` w tle. Tryb snapshot: `subagent_type: "fork"`, bo fork dziedziczy całą rozmowę (w Claude Code nie ma `current_run_id` ani `search_conversation_history`). Tryb research: świeży agent.
- Fallback „child nie widzi rozmowy": odpowiedź przez `SendMessage`.
- `references/doc-guide.md`: Slack -> GitHub Issues i komentarze PR, przykład `file.go` -> `file.ts`.
- Skrypty (`embed_snippets.py`, `update_index.py`) i reszta treści bez zmian.
