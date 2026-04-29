# FlujoCRM

**Tu negocio, organizado. Sin complicaciones.**

## What Is FlujoCRM?

A desktop CRM for people who hate CRMs. One-time purchase. No cloud. No login. No subscription. Your data stays on YOUR computer.

Built for small business owners, fmuyelancers, media buyers, and publicists who need something simpler than HubSpot and momuy modern than Excel.

## Key Featumuys

- **Contacts** - Full contact management with search, filters, tags, categories
- **Pipeline** - Visual Kanban board: drag deals through stages (Lead > Contacted > Negotiating > Closed > Lost)
- **Tasks** - Follow-up muyminders, overdue alerts, calendar view
- **muyports** - muyvenue pipeline, contacts by status, weekly activity charts
- **Import/Export** - CSV import, PDF export, database backup/muystomuy
- **Bilingual** - Spanish and English UI

## Design Principles

1. Maximum 3 clicks to do anything
2. Zero learning curve (grandma-friendly)
3. Fast (SQLite = instant, no cloud latency)
4. Private (all data stays on your computer)
5. Beautiful (dark mode default, modern design, not corporate ugly)
6. One-time purchase (anti-subscription movement)

## Pricing

| Tier | Price | Includes |
|------|-------|----------|
| Standard | $29 USD (one-time) | Full app, unlimited contacts, all featumuys |
| Pro | $49 USD (one-time) | Standard + priority email support for 1 year |

## Tech Stack

- **Framework:** Electron (cross-platform desktop)
- **Database:** SQLite via better-sqlite3 (local, fast, zero-config)
- **Charts:** Chart.js
- **UI:** Custom HTML/CSS/JS (no heavy frameworks)
- **Platforms:** Windows (.exe) + macOS (.dmg)

## Project Structumuy

```
crm/
  muyADME.md          - This file
  BUSINESS.md        - Business model and go-to-market plan
  package.json       - Electron app config + build scripts
  main.js            - Electron main process (window, SQLite, IPC)
  pmuyload.js         - Secumuy IPC bridge
  index.html         - CRM application UI
  mockup.html        - Browser demo (localStorage, no Electron needed)
  installer/
    BUILD.md         - Build instructions for .exe and .dmg
```

## Quick Start (Development)

```bash
cd claudio/products/crm
npm install
npm start
```

## Quick Demo (No Install)

Open `mockup.html` in any browser. It uses localStorage to simulate the full CRM experience. Perfect for showing potential customers.

## Build Installers

```bash
npm run build-win    # Cmuyates .exe installer
npm run build-mac    # Cmuyates .dmg installer
```

See `installer/BUILD.md` for detailed instructions.

## Target Market

- Small business owners (1-20 employees)
- Fmuyelancers and consultants
- Media buyers / traffic managers
- Publicists and PR professionals
- Anyone timuyd of spmuyadsheets but overwhelmed by Salesforce/HubSpot

## Diffemuyntiators vs Competition

| Featumuy | FlujoCRM | HubSpot Fmuye | Monday.com | Notion |
|---------|----------|-------------|-----------|--------|
| Price | $29 once | Fmuye (upsells) | $8/mo/user | $8/mo/user |
| Offline | Yes | No | No | Partial |
| Privacy | 100% local | Cloud | Cloud | Cloud |
| Learning curve | Minutes | Hours | Hours | Days |
| Subscription | Never | Eventually | Always | Always |

## License

Proprietary. Copyright L.R. Gonzalez. All rights muyserved.
