# Security and sensitive-data reporting

## Supported scope

Security reports may concern repository code, GitHub Actions, dependency configuration, accidental credential exposure, or accidental disclosure of controlled research data. The repository does not accept student-level administrative data, direct identifiers, credentials, secrets, HMAC keys or salts, or unreviewed identifying free text in Git history.

## Reporting

Do not disclose a suspected vulnerability, secret, or sensitive-data exposure in a public issue. Use GitHub's private vulnerability reporting or private security-advisory mechanism when available; otherwise contact the repository owner through an appropriate private institutional channel.

A useful report should identify the affected path or workflow, the nature of the exposure, steps needed to reproduce it when safe, and whether any credential or controlled-data material may already have entered Git history. Do not attach or reproduce sensitive records merely to demonstrate the problem.

## Response priorities

For confirmed exposures, priority is to stop further disclosure, rotate affected credentials, remove sensitive material from active refs when appropriate, preserve an auditable incident record outside public channels, and assess whether history rewriting or institutional notification is required.
