# Security

## Scope

`obs-safe-integration-kit` is a local-first wrapper/kernel. It evaluates proposed actions and records evidence; it does not execute shell commands, drive browsers, upload files, call production APIs or publish externally.

## Reporting

For now, report issues through the repository issue tracker after the public repo exists. Until then, keep reports local and do not paste real secrets into examples, tests or issues.

## Secret Handling

- Do not add real tokens, credentials, cookies, `.env` files or account exports.
- Tests must use synthetic fixtures only, preferably assembled at runtime when they resemble a known secret format.
- Any external action, publication, push, browser automation, deployment or account operation must pass the workspace ActionGate and host gate.

## Supported Posture

- Local tests and dry-run demos are supported.
- Production safety certification is not claimed.
- Downstream projects must run their own threat model, dependency review, secret scan and human review process.
