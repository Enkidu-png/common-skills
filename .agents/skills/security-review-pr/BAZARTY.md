# Zmiany względem warpdotdev/oz-for-oss (fork Enkidu-png/common-skills, gałąź bazarty)

- Źródło: `warpdotdev/oz-for-oss`, ścieżka `.agents/skills/security-review-pr/SKILL.md`. Skill przeniesiony do tego forka tylko po to, żeby mógł wczytać nakładkę; upstream oz-for-oss nie przewiduje jej.
- Jedna zmiana: sekcja „Repository-specific companion” (jeden akapit). Skill czyta `.agents/skills/security-review-pr-local/SKILL.md`, jeśli istnieje, i stosuje stamtąd ścieżki wyzwalające, kontrole, czerwone flagi i progi wagi. Nakładka nie może zmienić kontraktu wyniku (`review.json`, tag `[SECURITY]`, etykiety wagi, reguły linii diffa).
- Reszta treści słowo w słowo jak w upstreamie. Powód: lista kontroli, format wyniku i granice upstreamu są dobre; brakowało tylko haka na zasady repo (pieniądze, paczki, webhooki, dane osobowe), wzór jak w `review-pr`, `triage-issue`, `dedupe-issue`.
