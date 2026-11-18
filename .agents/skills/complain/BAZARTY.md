# Zmiany bazarty wzgledem warpdotdev/common-skills

- Kanal: zamiast webhooka Slacka (gcloud Secret Manager, Oz managed secret) skarga idzie przez `gh` jako komentarz w jednym przypietym issue z etykieta `agent-skargi` w `Enkidu-png/bazarty-platforma`. Brak issue: skrypt je zaklada, etykietuje i przypina.
- Powod: nie mamy Slacka, jedyny tracker to GitHub Issues (decyzja wlasciciela 18.11).
- `submit.py`: ten sam interfejs (wiadomosc z argumentu albo stdin), nowa flaga `--dry-run`; sanityzacja dodatkowo tnie tokeny GitHuba i odsylacze `#123`.
- SKILL.md: zmienione tylko zdania o Slacku, mrkdwn i dopisany akapit "Where it goes" (przeglad tygodniowy w petli update-pr-review). Logika kiedy i jak sie skarzyc bez zmian. Evals: oczekiwania przepiete na komentarz w issue.
