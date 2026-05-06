# Deploy Gate

Mini Office is not cleared for external deployment.

## Blockers

- Legal review of `COMMERCIAL_LICENSE.md`.
- Clean-machine install test.
- Final customer ZIP and SHA256.
- Support, privacy, refund, and update policy.
- Checkout copy that matches the verified package.
- Secret scan with `count_reported=0`.

## Local Verification

```bash
python -m pytest -q
python mini_office.py --status
```

## Publication Rule

Do not create a public repository, public checkout, or website buy button from
this folder until all blockers are closed and recorded in the product note.
