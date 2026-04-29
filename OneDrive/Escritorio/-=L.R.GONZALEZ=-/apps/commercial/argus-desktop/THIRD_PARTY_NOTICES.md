# THIRD_PARTY_NOTICES

Argus Desktop is a proprietary commercial/internal app. It depends on npm
packages listed in `package.json` and resolved by `package-lock.json`,
including React, Vite, TypeScript, Electron, Capacitor, CodeMirror and related
tooling.

Dependency source code is not copied into this source package. Generated
`node_modules` and `dist` artifacts are denied from releases and should be
recreated with npm during verification.
