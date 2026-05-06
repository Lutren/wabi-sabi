# Mini Office

Status: `LOCAL_SMOKE_QA / FOUNDER_ACCESS_REVIEW`

Mini Office is a local browser workspace for reviewing small agent-office flows,
marketing materials, task boards, and product notes before they are packaged for
customers. It is designed as a human-approved local app: the operator decides
what to run, what to publish, and what to sell.

## What Is Verified

- Local static app served by `mini_office.py`.
- Browser entrypoint at `http://127.0.0.1:8000`.
- Five role cards used as an office metaphor: Writer, Debugger, Research, QA,
  and Archive.
- No external service is required for the local smoke path.
- Current package metadata points to `COMMERCIAL_LICENSE.md`.

## What Is Not Claimed

- No unattended production operation claim.
- No business-result guarantee.
- No public checkout is active from this folder.
- No public repository is promised from this package.
- No license grant beyond the commercial license file.

## Run Locally

```bash
python mini_office.py --status
python mini_office.py --no-browser
```

Then open:

```text
http://127.0.0.1:8000
```

Windows helper:

```bat
INSTALL_AND_RUN.bat
```

Linux or macOS helper:

```bash
chmod +x install_and_run.sh
./install_and_run.sh
```

## Tests

```bash
python -m pytest -q
```

## Product Boundary

Mini Office can become a paid local app or an open-core product later, but the
current folder is not ready for external sale until these gates are closed:

- legal review of commercial license and customer terms;
- clean-machine install test;
- final customer ZIP hash and manifest;
- final support, privacy, refund, and update policy;
- checkout page that matches the verified product.

## Evidence

- Evidence note: `docs/product/mini-office-local-smoke-evidence-2026-05-02.md`
- Product note: `docs/product/mini-office.md`
- Manifest target: `release_manifests/mini-office.json`
- Prior ZIP target: `releases/paid-apps/mini-office.zip`

## License

See `COMMERCIAL_LICENSE.md`. This package remains
`LEGAL_REVIEW_REQUIRED` before external sale or publication.
