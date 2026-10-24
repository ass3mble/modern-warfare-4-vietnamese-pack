# Security / An toàn

- Run only on files you own or may lawfully inspect.
- Do not execute the game or any game-native DLL/EXE while performing translation QA.
- Keep the original file immutable; candidates are generated with exclusive-create into separate staging paths.
- Pin the original SHA-256 before building. Record candidate SHA-256 after building and verify changes independently.
- Scan source and Git history for secrets and copyrighted assets before publishing.
- The CLI is an offline validator, **not** a game mod loader, injector or automatic installer.

To report an accidental credential disclosure, contact the repository owner privately rather than filing a public issue containing the secret.
