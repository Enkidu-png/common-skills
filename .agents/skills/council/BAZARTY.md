# Zmiany w forku bazarty (Enkidu-png/common-skills, gałąź bazarty)

- `run_agents` (Oz, wybór modelu na cały bieg) zastąpione narzędziem `Agent` z parametrem `model` na członka i `SendMessage` do dopytania. Powód: w Claude Code nie ma Oz.
- Dopisane, że poza Anthropic model z innej rodziny jest tylko przez zainstalowany most (np. plugin `codex`), inaczej różne modele Anthropic plus różne kąty.
- Członkowie zmieniający kod: `isolation: "worktree"` albo worktree w `.warp-wt/<slug>`.
- Reszta (rola rady, format raportu, synteza) bez zmian, słowo w słowo.
