# Zmiany wzgledem warpdotdev/common-skills

- Komendy Rusta (cargo fmt, clippy, nextest, WASM, clang-format) zastapione stosem bazarty: `npm run bramka`, `npm run typecheck`, `npm run build`, `npm run check:*`, testy jednostkowe, Deno i Playwright.
- Sekcje typow bledow przepisane z Rusta na TypeScript; sekcja WASM zamieniona na bledy funkcji edge na Deno.
- Struktura i zasady bez zmian: najwezsza komenda, pelna bramka tylko na zadanie, formatter raz na koncu.
- Powod: zastepuje lokalny skill `naprawa-bramki`; upstream zaklada repo w Ruscie.
