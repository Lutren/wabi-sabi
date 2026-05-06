# FlujoCRM - Business Model

Status: `FOUNDER_ACCESS_SQLITE_QA / DO_NOT_PUBLISH_CHECKOUT`

FlujoCRM is a Windows-first local CRM for freelancers, small agencies and local
businesses that want contacts, follow-up tasks and a simple pipeline without a
monthly SaaS bill.

## Positioning

Tagline:

- Spanish: `Tu negocio, organizado. Sin complicaciones.`
- English: `Your business, organized. No complications.`

Promise:

- One-time purchase, no subscription.
- Local-first SQLite data storage.
- Simple contact and pipeline workflow.
- Human-controlled business operations; no external sending automation.

Avoid:

- Claims that it replaces full enterprise CRMs.
- Guarantees about revenue, compliance or security.
- Promising macOS in the first release.
- Saying the installer is signed until it is actually signed.

## Offer Ladder

| tier | price draft | includes | status |
|---|---:|---|---|
| Pilot Standard | 29 USD | Windows app, basic install notes, self-service support docs | draft |
| Pilot Support | 49 USD | Windows app, install notes and priority email support during pilot | founder access |
| Setup Service | TBD | installation help and light CRM setup | future service |

Final prices depend on Gumroad/platform fees, support capacity and clean install
QA.

## Target Customers

1. Freelancers managing 20-100 active contacts.
2. Small agencies that want a local pipeline without per-seat subscriptions.
3. Local businesses that need follow-up reminders and simple client notes.
4. Consultants or coaches that value privacy and simple local workflows.

## Distribution Channels

- Website contact flow first: `Acceso fundador`.
- Gumroad checkout only after installer, legal/support and install QA gates pass.
- Organic launch channels: blog posts, video demo, founder access list and direct
  outreach to small businesses.

## Launch Gates

- Clean Windows install test passes.
- Current-user install QA has passed; repeat on a clean Windows machine before
  public checkout.
- Installer SHA256 and signature state are documented.
- UI/data-storage contract is documented: installed Electron builds use SQLite
  through IPC; standalone HTML preview uses browser storage.
- Pilot install/support/refund/privacy copy exists in `CUSTOMER_INSTALL_NOTES.md`
  and still requires legal review before checkout.
- Support/refund/privacy/terms are final for the pilot.
- The public listing states local data behavior and any unsigned installer
  warning.
- Customer deliverable is the installer and notes, not the source ZIP.

## Risks

| risk | mitigation |
|---|---|
| Windows warning reduces trust | Sign the installer or disclose the unsigned warning clearly |
| Support burden grows | Keep pilot small and sell founder access before public checkout |
| Users expect SaaS/team sync | State local-first single-machine scope in the listing |
| Product overpromises | Keep claims to contact, pipeline, tasks and local storage only |

## Next Step

Run the clean-machine evidence package next. If it passes and legal/support copy
is closed, FlujoCRM can move from `FOUNDER_ACCESS` to a limited paid pilot.
Until then, keep checkout blocked and offer only contact-based founder access.
