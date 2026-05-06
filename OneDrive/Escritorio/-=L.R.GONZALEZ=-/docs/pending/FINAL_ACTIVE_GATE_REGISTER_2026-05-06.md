# Final Active Gate Register - 2026-05-06

## Decision

After local verification passes, the remaining `PENDIENTES_MASTER.md` open
checkboxes are not autonomous local tasks. They are gates that require one or
more of:

- authenticated external account access;
- target-specific ActionGate;
- legal/tax/labor review;
- clean-machine QA;
- renderer/admin dependency;
- private-boundary release review.

They were converted from open checkboxes to explicit gate markers. This does not
mean the underlying work is complete.

## Gates

| gate | source item | status |
|---|---|---|
| LinkedIn canonical URL | confirm canonical URL visually before profile edits | `external-auth-gate` |
| LinkedIn profile edit | paste public-safe profile packet into authenticated LinkedIn | `external-auth-gate` |
| FlujoCRM final sale | clean VM, legal/support, final installer/hash | `release-legal-gate` |
| Wave FC sale/publication | EULA, install docs, landing copy, ActionGate | `release-legal-gate` |
| Legal/tax/payment | jurisdiction, taxes, payment platform, final policy | `legal-manual` |
| Release manifests to ZIP | no customer ZIP until scans, legal and checklist pass | `private-release-gate` |
| Public packaging copy | landing/copy only after license, captures, install and ActionGate | `publication-gate` |
| Public captures/video | generate/decide public artifacts only after publication gate | `publication-gate` |
| Physical checker connector | read-only with consent, logs, manual fallback and legal/labor approval | `legal-manual` |
| Social sessions | validate real sessions/credentials before automated publication | `external-auth-gate` |
| Gumroad dashboard sync | synchronize dashboard only with authenticated target and exact product diff | `external-auth-gate` |

## Current Local Truth

- Pending tracker after conversion should report `0` active local open items.
- Remaining gates have now been packeted into:
  `docs/pending/REMAINING_GATED_WORKPACK_2026-05-06.md`.
- Model gates were checked separately:
  `-=MEDIOEVO=-\-=LIBROS\claudio\docs\LOCAL_MODEL_GATE_RECHECK_2026-05-06.md`.
- DOCX/WSL dependency gates were checked separately:
  `-=MEDIOEVO=-\-=LIBROS\claudio\docs\DOCX_WSL_DEPENDENCY_GATE_RECHECK_2026-05-06.md`.
- No live LinkedIn, Gumroad, social, website, push, payment, tax or legal action
  was executed by this conversion.

## Reopen Rule

To reopen any gate as executable work, create a target-specific workpack with:

- exact URL/account/product/repo;
- exact copy or operation;
- current host gate;
- secret scan scope;
- rollback or no-op proof;
- post-action verification command;
- explicit owner/legal approval where required.
