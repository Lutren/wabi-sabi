# FlujoCRM Current Gate Recheck - 2026-05-06

Status: `LOCAL_QA_PASS / CUSTOMER_INSTALLER_PENDING / SALE_BLOCKED`

This recheck continues the pending item that says FlujoCRM must not be declared
ready for final sale until clean-machine QA, legal/support review and final
customer artifact hash are closed.

## Commands

```powershell
npm run check
npm run smoke:e2e-storage
python tools\release\scan_secrets.py --path apps\commercial\flujocrm --json --fail-on-findings
python tools\release\product_manifest.py --product flujocrm --hash --write
python tools\release\scan_secrets.py --path release_manifests\flujocrm.json --json --fail-on-findings
```

## Results

| check | result |
|---|---|
| source smoke | `flujocrm main smoke passed`; `preload smoke passed`; `renderer smoke passed` |
| SQLite storage smoke | `flujocrm e2e storage smoke passed` with temp profile DB |
| source secret scan | `count_reported=0` |
| manifest refresh | `release_manifests\flujocrm.json` rewritten |
| manifest summary | `file_count=20`, `blocked_count=0`, `excluded_count=244`, `total_bytes=311852` |
| manifest secret scan | `count_reported=0` |
| unpacked QA exe | `apps\commercial\flujocrm\dist\win-unpacked\FlujoCRM.exe` exists |
| unpacked QA exe SHA256 | `7F26D6AF4808C7C2FEA90E0A3625F99582875C3C7BF32E181868FAB3D255A320` |
| NSIS setup installer | `apps\commercial\flujocrm\dist\FlujoCRM-Setup-1.0.0.exe` missing |

## Decision

FlujoCRM remains usable for local/founder QA but is still blocked from public
sale.

Closed in this recheck:

- current source smoke;
- SQLite storage smoke;
- source secret scan;
- refreshed release manifest;
- manifest secret scan;
- unpacked QA executable hash recorded.

Still blocked:

- final NSIS/customer installer rebuild or restore;
- clean Windows machine/VM install QA;
- legal/support/refund/privacy final review;
- code signing decision or explicit unsigned pilot acceptance;
- Gumroad/website checkout update and live verification.

Do not mark FlujoCRM as `BUY_NOW` or final customer-ready from this evidence.
