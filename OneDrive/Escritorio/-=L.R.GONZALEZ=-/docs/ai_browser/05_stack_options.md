# AI Browser Seguro - 05 Stack Options

Status: `STACK_COMPARISON`

External research: limited to official or primary project sources on
`2026-05-06`. Licenses and security posture must be rechecked before adding a
dependency or publishing a package.

## Recommendation

Start with a dependency-light CLI extractor and SourceSnapshot schema. Add
Playwright later as the controlled rendering engine when a real browser context
is needed. Treat extensions and desktop shells as later UI surfaces, not the
security core.

## Comparison

| Stack | Strengths | Risks | Fit |
|---|---|---|---|
| CLI extractor | No browser profile, no JS, simple hashes, easy tests | Not a full browser render; misses dynamic content | Best MVP |
| Playwright | Isolated BrowserContexts, multi-browser automation, controllable contexts | Heavy dependency and browser binaries; can automate dangerous actions if ungated | Best future capture engine |
| Chromium direct | Maximum control possible | Very heavy, complex updates, sandbox and license tree complexity | Avoid for MVP |
| Tauri WebView | Small desktop shell, Rust core, CSP and capabilities model | System WebView differences; remote content still risky | Good future UI shell |
| Electron | Mature desktop stack, existing Argus lane uses it | Larger attack surface; remote content with Node is severe risk | Avoid for untrusted browser core |
| Browser extension | User-visible active tab flow, host permissions, activeTab least privilege | Extension permissions, store review, content script risks | Good later user-driven collector |
| Headless browser read mode | Can render pages without UI; controlled resource blocking possible | Still needs network/domain/JS policy; easy to drift into scraping | Good after gate policy |

## Official Source Notes

- Playwright documents isolated BrowserContexts and fresh contexts for test
  isolation: https://playwright.dev/docs/browser-contexts
- Playwright browser binaries are version-coupled and installed by CLI:
  https://playwright.dev/docs/browsers
- Chrome extension manifests and host permissions are explicit:
  https://developer.chrome.com/docs/extensions/reference/manifest
  and https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions
- Chrome `activeTab` grants temporary access after user gesture:
  https://developer.chrome.com/docs/extensions/activeTab
- Electron security docs warn against executing untrusted remote content with
  Node integration and require context isolation/sandbox:
  https://www.electronjs.org/docs/latest/tutorial/security
- Tauri CSP and capabilities are relevant for a constrained desktop shell:
  https://v2.tauri.app/security/csp/
  and https://v2.tauri.app/security/capabilities/
- Primary license pages observed:
  Playwright Apache-2.0 `https://github.com/microsoft/playwright/blob/main/LICENSE`;
  Electron MIT `https://github.com/electron/electron`;
  Tauri MIT/Apache-2.0 `https://github.com/tauri-apps/tauri`;
  Chromium root license at `https://chromium.googlesource.com/chromium/src/+/main/LICENSE`
  or revision-specific equivalent.

## INCOGNITA

- Exact redistribution implications of bundled Chromium/Electron/Tauri builds
  for a commercial package.
- Current Chrome Web Store and Edge Add-ons policy at time of publication.
- Domain-specific robots/terms/license status for any real source.
- Whether future Sabueso/Onion research modules should share the same runtime
  or remain separate gated collectors.
