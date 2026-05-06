# FlujoCRM Local Gate Recheck - 2026-05-05

Status: `LOCAL_SOURCE_OK / UNSIGNED_WARNING_DOCUMENTED / CHECKOUT_BLOCKED`

This recheck uses the operator authorization from 2026-05-05 only as local
governance approval. It does not replace legal review, clean-machine QA, code
signing, Gumroad checkout validation or any external publication gate.

## Current Truth

- Source path: `apps/commercial/flujocrm`.
- Source ZIP path: `releases/paid-apps/flujocrm.zip`.
- Source ZIP is present and remains an internal QA/source artifact, not the
  default customer deliverable.
- `node_modules` is not present in the active source tree.
- `apps/commercial/flujocrm/dist/FlujoCRM-Setup-1.0.0.exe` is not present in
  the active source tree at this recheck.
- Historical installer/current-user QA evidence remains useful, but a customer
  checkout needs a fresh build or restored installer artifact with a final hash.

## Validation Run

```txt
cd apps/commercial/flujocrm
npm run check
flujocrm main smoke passed
flujocrm preload smoke passed
flujocrm renderer smoke passed
```

Focused secret scans:

```txt
python tools\release\scan_secrets.py --path apps\commercial\flujocrm --json --fail-on-findings
count_reported=0

python tools\release\scan_secrets.py --artifact releases\paid-apps\flujocrm.zip --json --fail-on-findings
count_reported=0
```

Unsigned installer copy check:

- `apps/commercial/flujocrm/CUSTOMER_INSTALL_NOTES.md` mentions the build is not
  code signed, warns about unknown publisher or SmartScreen, and includes the
  historical installer SHA256.
- `apps/commercial/flujocrm/installer/BUILD.md` documents the code signing
  options and the unsigned v1 warning path.

## Local Closure

Closed locally:

- unsigned-installer warning is documented for pilot/founder access;
- source smoke tests pass;
- product and source-ZIP secret scans report `0`.

Still blocked:

- clean Windows machine or VM install QA;
- final legal review of terms, privacy, refund and support;
- final customer artifact rebuild or restore plus hash verification;
- Gumroad/website checkout and any public sale ActionGate.

## Decision

FlujoCRM remains `FOUNDER_ACCESS / CHECKOUT_BLOCKED`.

Do not mark it as `BUY_NOW`, do not publish a new checkout and do not claim a
currently available customer installer until the remaining blockers above are
closed with fresh evidence.
