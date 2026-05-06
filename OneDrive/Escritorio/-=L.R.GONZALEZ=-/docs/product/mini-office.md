# Mini Office

Classification: `COMMERCIAL / FOUNDER_ACCESS_REVIEW`

Current path: `apps\commercial\mini-office`

Current evidence:

- `docs\product\mini-office-lane-unification-2026-05-06.md`
- `docs\product\mini-office-local-smoke-evidence-2026-05-02.md`

Cleanup evidence: `qa_artifacts\release_validation\mini-office-cleanup-2026-05-03.json`.

Resolved locally:

- `npm test`: `22 passed`.
- `python -m pytest -q`: `22 passed`.
- `npm run smoke`: runtime status OK.
- HTTP server smoke: `200`, `index.html` served.
- Product and ZIP secret scans: `count_reported=0`.
- Cleaned source ZIP rebuilt: `releases\paid-apps\mini-office.zip`, SHA256
  `4315003693566D93F6F48DEF1C5EACE14BBE6531CEDFB878BE121699502D3710`.
- Updated manifest: `release_manifests\mini-office.json`, `file_count=53`,
  `blocked_count=0`, `excluded_count=17`, `total_bytes=91294`.

2026-05-02 cleanup:

- public README, local landing, Gumroad draft, quickstart and installer scripts
  now use low-claim local-app language;
- top-level `LICENSE` no longer conflicts with `COMMERCIAL_LICENSE.md`;
- generators in `agents/` and `tools/` no longer create public copy that says
  free, MIT, public GitHub, unattended operation or guaranteed outcomes.
- rebuilt ZIP and manifest after cleanup; artifact secret scan reports
  `count_reported=0`.

Before release:

- legal review of commercial license and customer terms;
- clean-machine install test;
- final customer ZIP hash and manifest;
- support, privacy, refund and update policy;
- checkout page that matches the verified package.
