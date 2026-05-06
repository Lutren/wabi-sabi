# Publicacion Perfiles Observatorio Handoff 2026-05-05

Recipient: `publicacion-perfiles-observatorio`

Sender: `codex`

Status: `READY_FOR_LOCAL_USE / EXTERNAL_ACTIONS_BLOCKED`

## Summary

This handoff creates a specialized local agent for public networks, Gumroad,
website, GitHub, GitHub Sponsors, LinkedIn and social-channel strategy. It is a
strategy and copy agent, not an external publisher.

## Primary Evidence

- Strategy: `docs/publishing/PUBLIC_PROFILE_NETWORK_OBSERVATORY_2026-05-05.md`
- Agent spec: `docs/publishing/PUBLICACION_PERFILES_OBSERVATORIO_AGENT_2026-05-05.md`
- Agent state: `COMMS/agents_state/publicacion-perfiles-observatorio.json`
- Required workspace gates: `AGENTS.md`, `VISIBILITY_MATRIX.md`,
  `SECRET_SCAN_REPORT.md`, `RISK_REGISTER.md`

## Live Read-Only Snapshot

- `https://medioevo.space/` returned HTTP 200.
- `https://medioevo.space/software.html` returned HTTP 200.
- `https://medioevo.space/apps.html` returned HTTP 200.
- `https://lrgonzalez.gumroad.com/` returned HTTP 200.
- `https://lrgonzalez.gumroad.com/l/medioevo-agent-ops-pack` returned HTTP 200.
- `https://lrgonzalez.gumroad.com/l/duat-templates` returned HTTP 200.
- `https://github.com/Lutren` returned HTTP 200.
- `https://github.com/sponsors/Lutren` returned HTTP 200.
- GitHub API read-only check: `Lutren`, name `Tyr`, 23 public repos, 9
  followers, bio points to Sponsors.
- Current host gate no-write check at 2026-05-05T20:57:30Z returned `BLOCK`
  because CPU, memory, dominant CPU process and residue were high.

## Operating Rules

- Keep publication, Gumroad, GitHub push, LinkedIn edit, website deploy and
  social posting in `BLOCK` until exact target gate passes.
- Use Observacionismo to ask what is visible, evidenced and falsifiable.
- Use inverse Observacionismo to ask what leaks advantage, data, formulas,
  private IP or account risk.
- Publish method, evidence discipline and public-safe tools.
- Keep exact parameters, private runtime, private data, prompts, unpublished
  books, RPG/TCG and premium wrappers private.

## First Tasks

1. Confirm canonical LinkedIn URL manually with authenticated visual evidence.
2. Prepare a local GitHub profile README patch; do not push it.
3. Prepare Gumroad product media/copy improvements for the two live products;
   do not save in Gumroad.
4. Prepare website copy/structured-data patch; do not deploy.
5. Create a monthly public content calendar after the target channel is chosen.

## Blocks

- Global workspace secret scan is still not clean for broad publication.
- Current host gate is `BLOCK`; do not attempt external publication from this
  session state.
- LinkedIn canonical URL remains `REVIEW`.
- Any new target must pass focused secret scan, claims scan, private-boundary
  check and ActionGate.
