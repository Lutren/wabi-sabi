# Security

Report security issues by email:

`l-tyr-r@outlook.com`

Use subject:

`[SECURITY] Mini Office`

## Scope

Mini Office currently serves a local static app through `mini_office.py`.
External publication and customer delivery are blocked until release gates pass.

## Operator Rules

- Do not commit secrets.
- Do not package `.env`, sessions, browser profiles, or private tokens.
- Run the workspace secret scan before any external delivery.
- Keep customer data outside this folder.
