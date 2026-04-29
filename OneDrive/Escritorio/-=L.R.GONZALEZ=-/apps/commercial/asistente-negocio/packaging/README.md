# Packaging Windows y macOS

Este producto es una app publica reducida. No empaqueta Claudio local ni agentes privados. La beta abre correo real con `mailto:` y WhatsApp real con `wa.me` despues de aprobacion humana.

## Windows

```powershell
.\packaging\build-windows.ps1
```

Salida esperada cuando dependencias y certificado esten listos:

- `release/Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.exe`
- `release/Asistente-Negocio-MEDIOEVO-1.0.0-win-x64.zip`

Estado actual: Windows v1.0.0 ya se puede entregar como beta/fundador, pero el instalador no esta firmado. Al venderlo se debe advertir que Windows SmartScreen puede mostrar aviso.

## macOS

```bash
chmod +x packaging/build-macos.sh
./packaging/build-macos.sh
```

Salida esperada en runner macOS:

- `release/Asistente-Negocio-MEDIOEVO-1.0.0-mac-x64.dmg`
- `release/Asistente-Negocio-MEDIOEVO-1.0.0-mac-arm64.dmg`
- `release/Asistente-Negocio-MEDIOEVO-1.0.0-mac-*.zip`

La notarizacion requiere Apple Developer ID. No se debe vender macOS como entregable final hasta generar y probar `.dmg` o `.app.zip` en una Mac real.
