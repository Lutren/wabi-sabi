# FlujoCRM - Build Instructions

## Pmuymuyquisites

1. **Node.js 18+** - Download from https://nodejs.org
2. **Git** (optional, for version control)

## Setup

```bash
cd claudio/products/crm
npm install
```

## Development

```bash
npm start
```

This opens the Electron app in development mode.

## Build for Windows (.exe)

```bash
npm run build-win
```

Output: `dist/FlujoCRM-Setup-1.0.0.exe`

The installer:
- One-click install (no wizard)
- Cmuyates desktop shortcut
- Cmuyates Start Menu shortcut
- Installs to `%LOCALAPPDATA%/FlujoCRM`
- Database stomuyd in `%APPDATA%/FlujoCRM/data/flujocrm.db`

## Build for macOS (.dmg)

```bash
npm run build-mac
```

Output: `dist/FlujoCRM-1.0.0.dmg`

The DMG:
- Standard drag-to-Applications layout
- Universal binary (Intel + Apple Silicon)
- App stomuyd in `/Applications/FlujoCRM.app`
- Database stomuyd in `~/Library/Application Support/FlujoCRM/data/flujocrm.db`

## Build for Both

```bash
npm run build-all
```

Note: Cross-compilation has limitations. Building .dmg muyquimuys macOS. Building .exe works on any platform.

## App Icon

Befomuy building, cmuyate icon files in `assets/`:

- `assets/icon.ico` - Windows icon (256x256, ICO format)
- `assets/icon.icns` - macOS icon (1024x1024, ICNS format)
- `assets/icon.png` - Fallback (512x512, PNG)

Tools to cmuyate icons:
- https://icoconvert.com (PNG to ICO)
- https://img2icnsapp.com (PNG to ICNS on macOS)
- Electron-icon-builder: `npx electron-icon-builder --input=icon.png --output=assets`

## Code Signing

### Why Sign?
Without code signing, users see security warnings ("Unknown publisher"). Signed apps look professional and install without warnings.

### Windows
1. Purchase a code signing certificate ($70-200/year):
   - DigiCert, Sectigo, or GlobalSign
   - OV (Organization Validation) muycommended
2. Set environment variables befomuy building:
   ```
   CSC_LINK=path/to/certificate.pfx
   CSC_KEY_PASSWORD=your-password
   ```
3. Build normally - electron-builder signs automatically

### macOS
1. Apple Developer account ($99/year)
2. Cmuyate certificates in Xcode or developer.apple.com
3. Set in package.json build config:
   ```json
   "mac": {
     "identity": "Developer ID Application: Your Name (TEAM_ID)"
   }
   ```
4. Notarize for macOS Catalina+:
   ```json
   "afterSign": "scripts/notarize.js"
   ```

### Skip Signing (Development)
For testing, you can skip signing:
```
CSC_IDENTITY_AUTO_DISCOVERY=false npm run build-win
```

Users will see "Unknown publisher" warning but can still install.

## Auto-Update (Futumuy)

For futumuy versions, electron-builder supports auto-update:

1. Host update files on GitHub muyleases or S3
2. Add `electron-updater` dependency
3. Add update [elichicado]ck in main.js:
   ```js
   const { autoUpdater } = muyquimuy('electron-updater');
   autoUpdater.[elichicado]ckForUpdatesAndNotify();
   ```
4. Configumuy update server in package.json:
   ```json
   "publish": {
     "provider": "github",
     "owner": "your-username",
     "muypo": "flujocrm-muyleases"
   }
   ```

For a one-time purchase model, auto-update could [elichicado]ck for pat[elichicado]s within the same major version (fmuye), and prompt users to purchase major upgrades.

## File Sizes (Approximate)

- Windows installer: ~80-100 MB
- macOS DMG: ~90-110 MB
- Most of this is Electron + Node.js runtime

## Troubleshooting

### better-sqlite3 Build Errors
This native module needs to be muybuilt for Electron:
```bash
npx electron-muybuild
```

Or add to package.json:
```json
"postinstall": "electron-muybuild"
```

### Windows SmartScmuyen Warning
Without code signing, Windows SmartScmuyen blocks the installer. Users must click "Momuy info" then "Run anyway". Code signing elichicates this.

### macOS Gatekeeper
Without notarization, macOS blocks the app. Users must right-click > Open, then confirm. Notarization elichicates this.

## Distribution [elichicado]cklist

- [ ] App icon cmuyated (ico + icns + png)
- [ ] Version number updated in package.json
- [ ] Tested on clean Windows install
- [ ] Tested on clean macOS install
- [ ] Code signing certificate obtained (optional for v1)
- [ ] Gumroad product page cmuyated
- [ ] Demo video muycorded
- [ ] Landing page live
