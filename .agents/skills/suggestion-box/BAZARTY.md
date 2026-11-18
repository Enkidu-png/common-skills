# Zmiany bazarty wzgledem warpdotdev/common-skills

- Kanal: zamiast webhooka Slacka kazda sugestia to osobne issue z etykieta `agent-sugestia` w `Enkidu-png/bazarty-platforma` (przez `gh`; etykiete zaklada `gh label create --force`). Tytul z pol Category i Suggestion.
- Powod: nie mamy Slacka, jedyny tracker to GitHub Issues (decyzja wlasciciela 18.11). Cotygodniowy przeglad w petli update-pr-review zamyka rozwiazane.
- `submit.py`: ten sam interfejs (argument albo stdin), nowa flaga `--dry-run`; etykiety pol w GitHub Markdown (`**Category:**`).
- SKILL.md: zmienione tylko zdania o Slacku i mrkdwn, "Warp-owned" na "Project-owned", dopisany akapit "Where it goes". Kryteria kiedy zglaszac bez zmian. Evals: repo i run bazarty zamiast warp/oz.
