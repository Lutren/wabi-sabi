# ActionGate Checklist

Use before push, deploy, Gumroad, social posting, browser automation, model
downloads, file moves or any irreversible action.

## Required

- Destination is exact.
- Package or staging path is exact.
- Secret scan reports zero findings.
- Path scrub reports zero private/local paths.
- Claims scan reports zero prohibited claims.
- Private game/book/customer/account material is excluded.
- Human approval is recorded.
- Host gate is APPROVE, or owner override is recorded with evidence and host is
  not BLOCK/JAMMING.

## Block Immediately

- Unknown destination.
- Broad glob packaging.
- Secrets, tokens, account sessions or `.env` files.
- Private RPG, TCG, book or canon material.
- Legal/license block.
- Strong claims without evidence.
- Host BLOCK/JAMMING.
