# Legacy Publication Script Inventory - 2026-05-03

Status: `INVENTORIED / REMOVED_FROM_ACTIVE_MENTAL_ROUTE / NO_FILES_DELETED`

This inventory is a curator artifact. It records scripts and docs that look
able to publish, deploy, upload, post or package. It does not execute them and
does not authorize deletion.

## Active Central Route

Use these first for future release work:

| lane | current route | rule |
|---|---|---|
| Product manifest | `tools\release\product_manifest.py` | generate allowlist manifest before packaging |
| Secret scan | `tools\release\scan_secrets.py` | run focused scan for exact target/staging |
| Free dev packaging | `tools\release\package_free_dev.py` | dry-run first; `--execute` only after review |
| Paid app packaging | `tools\release\package_paid_apps.py` | internal QA ZIPs by default, not customer source delivery |
| Paid templates | `tools\release\package_paid_templates.py` | only selected template packs |
| GitHub open-dev publish | `tools\release\publish_free_dev_github.py` | gated; target-specific only |
| GitHub sanitized publish | `tools\release\publish_public_sanitized_github.py` | gated; target-specific only |
| Gumroad publish | `tools\release\publish_gumroad_listing.py` | gated; target-specific only |
| Publication runbook | `docs\publishing\OPEN_CORE_UI_PAID_PUBLICATION_RUNBOOK_2026-05-02.md` | strategy and gate order |
| Next gate record | `docs\publishing\NEXT_PUBLICATION_GATE_2026-05-02.md` | prevents duplicate live creates |
| Listing deliverable map | `docs\product\product-listing-deliverable-alignment-2026-05-03.md` | maps listing to real delivery lane |

## Legacy Or Blocked Families

These are not active entrypoints for future agents unless a maintainer re-gates
them explicitly.

| family | observed examples | decision |
|---|---|---|
| Old Gumroad upload/publish scripts | `-=MEDIOEVO=-\-=LIBROS\claudio\tools\gumroad_auto*.py`, `gumroad_publish*.py`, `gumroad_publicar.py`, `gumroad_subir_producto.py`, `publish_gumroad_now.py`, `publish_asistente_negocio_gumroad.py`, `update_gumroad_listings.py`, `setup_gumroad.py` | `LEGACY_HOLD`: do not run directly; route through `tools\release\publish_gumroad_listing.py` after scans/gate |
| Old social autopublish scripts | `-=MEDIOEVO=-\-=LIBROS\claudio\social_agent.py`, `social_automation.py`, `start_social_agent.bat`, `autopilot\social_workflow.py`, `marketing\auto_publisher*.py`, `publicar_redes*.py`, `tiktok_uploader.py`, `instagram_uploader.py` | `EXTERNAL_HOLD`: no auto-posting; requires channel review, copy review, host/ActionGate |
| Old Discord/push scripts | `publicar_discord*.py`, `_legacy\claudio_os_discord_publisher.py`, `brain_os\beta\DISCORD_MESSAGE.md` | `EXTERNAL_HOLD`: no direct Discord publish without current channel/gate |
| Manual website/deploy scripts | `apps\editorial_web\DEPLOY_CLOUDFLARE.bat`, `DEPLOY-MANUAL.bat`, `tools\deploy_a_cloudflare.py`, `tools\subir_cloudflare_pages.py`, `setup_cloudflare_dns.py`, `add_cloudflare_dns.py` | `DEPLOY_HOLD`: deploy only through current Cloudflare target/runbook and fresh gate |
| Old app-specific publication docs/scripts | `apps\commercial\mini-office\PUBLICAR_*.md`, `mini-office\tools\publicar_gumroad.py`, `mini-office\tools\publicar_web.py`, `products\asistente_negocio\commercial\*`, `products\asistente_negocio\scripts\package-final-release.cjs` | `PRODUCT_HOLD`: product-specific checkout remains blocked until deliverable, legal and clean-machine QA are complete |
| Editorial/book publish scripts | `publish_despertar_final.py`, `publish_gumroad_6plus1.py`, `publish_canon_10_books.py`, `publish_final_desktop_canon10.py`, `publish_illustrated_canon10.py` | `EDITORIAL_HOLD`: do not publish books/canon from legacy scripts; require editorial rights/sample boundary |
| OPPO/device deploy scripts | `deploy_oppo_new_env.py`, `deploy_sensor_oppo.bat`, `OPPO_DEPLOY_FIX.bat`, `oppo_deploy\*` | `DEVICE_HOLD`: not part of public release route; physical device/risk review required |
| Direct mouse/API publish scripts | `publicar_con_mouse.py`, `publicar_api_directa.py`, `publicar_100_auto.py`, `publicar_todo*.py`, `publicar_sin_interu.py` | `BLOCK`: high-risk automation; use only with explicit target, host/ActionGate and human override evidence |

## Route Removal Decision

Removed from active mental route:

- any script with `auto_publish`, `publicar_100`, `publicar_todo`,
  `publicar_con_mouse`, old `gumroad_auto*`, old `gumroad_publish*`, direct
  social uploaders and manual Cloudflare `.bat` flows.

Kept as historical or product-specific reference:

- existing reports under `tools\reports\*`;
- product docs that explain old Gumroad pages;
- skill docs under `.agents\skills\*`, because they are guidance, not direct
  execution by themselves.

## Next Cleanup

1. Move confirmed obsolete direct-action scripts to an archive folder only with
   a migration map.
2. Replace product docs that tell users to run old scripts with links to the
   central release tools.
3. Add tests to ensure new publication runners require target, scan and gate.
