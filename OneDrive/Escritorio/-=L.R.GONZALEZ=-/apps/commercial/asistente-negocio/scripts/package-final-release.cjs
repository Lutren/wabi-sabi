const crypto = require("crypto");
const fs = require("fs");
const os = require("os");
const path = require("path");

const root = path.resolve(__dirname, "..");
const pkg = JSON.parse(fs.readFileSync(path.join(root, "package.json"), "utf8"));
const version = pkg.version;
const desktopRoot = process.env.MEDIOEVO_FINAL_RELEASE_DIR ||
  path.join(os.homedir(), "OneDrive", "Escritorio", "PRODUCTO_FINAL_MEDIOEVO");
const outDir = path.join(desktopRoot, `Asistente_Negocio_MEDIOEVO_v${version}`);

function ensureInside(parent, child) {
  const rel = path.relative(parent, child);
  if (rel.startsWith("..") || path.isAbsolute(rel)) {
    throw new Error(`Unsafe output path: ${child}`);
  }
}

function copyFile(src, dest) {
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.copyFileSync(src, dest);
}

function writeFile(dest, text) {
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, text, "utf8");
}

function hashFile(file) {
  return crypto.createHash("sha256").update(fs.readFileSync(file)).digest("hex").toUpperCase();
}

function walk(dir) {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walk(full));
    } else {
      files.push(full);
    }
  }
  return files;
}

fs.mkdirSync(desktopRoot, { recursive: true });
ensureInside(desktopRoot, outDir);
fs.rmSync(outDir, { recursive: true, force: true });
fs.mkdirSync(outDir, { recursive: true });

const releaseDir = path.join(root, "release");
if (fs.existsSync(releaseDir)) {
  for (const entry of fs.readdirSync(releaseDir)) {
    if (entry.includes(version) && /\.(exe|zip|blockmap)$/i.test(entry)) {
      copyFile(path.join(releaseDir, entry), path.join(outDir, "Windows", entry));
    }
  }
}

copyFile(
  path.join(root, "preview", "ABRE_AQUI_PREVIEW_MEDIOEVO.html"),
  path.join(outDir, "ABRE_AQUI_DEMO_MEDIOEVO.html")
);
copyFile(
  path.join(root, "preview", "ABRE_AQUI_PREVIEW_MEDIOEVO.html"),
  path.join(outDir, "Preview_HTML_multiplataforma", "app", "index.html")
);
copyFile(path.join(root, "build", "icon.ico"), path.join(outDir, "Windows", "icon.ico"));
copyFile(path.join(root, "build", "icon.icns"), path.join(outDir, "Mac", "icon.icns"));
copyFile(path.join(root, "README.md"), path.join(outDir, "Documentos", "README_PRODUCTO.md"));
copyFile(path.join(root, "public_safe_policy.md"), path.join(outDir, "Documentos", "POLITICA_PUBLIC_SAFE.md"));
copyFile(path.join(root, "LICENSE_EULA.md"), path.join(outDir, "Documentos", "LICENCIA_EULA.md"));

writeFile(path.join(outDir, "README_PRIMERO.md"), `# Asistente de Negocio MEDIOEVO v${version}

## Para empezar en Windows

1. Abre la carpeta Windows.
2. Da doble click en el instalador .exe.
3. Sigue el instalador normal.
4. Abre Asistente de Negocio MEDIOEVO.
5. Escribe los datos de tu negocio una sola vez.
6. Pega o dicta el mensaje del cliente.
7. Revisa la respuesta.
8. Abre correo o WhatsApp y pulsa Enviar en tu app.

## Para probar sin instalar

Abre ABRE_AQUI_DEMO_MEDIOEVO.html. Es una demo local con el estilo MEDIOEVO y los assets embebidos.

## Importante

- La app guarda datos en esta computadora.
- El envio final ocurre en tu correo o WhatsApp.
- La app no envia mensajes sola.
- Puedes descargar respaldo o borrar datos desde Datos y privacidad.
`);

writeFile(path.join(outDir, "Mac", "COMO_COMPILAR_MAC.md"), `# macOS

El icono y la configuracion de macOS ya estan preparados en el proyecto.

Para generar .dmg y .app.zip se necesita ejecutar en una Mac:

\`\`\`bash
npm install
npm run build:mac
\`\`\`

Para venta fuera de una tienda hace falta cuenta Apple Developer y notarizacion.
`);

writeFile(path.join(outDir, "VERSION.txt"), [
  `product=Asistente de Negocio MEDIOEVO`,
  `version=${version}`,
  `profile=public_safe`,
  `autonomy=human_approved_external_send`,
  `release_state=final_local_package`,
  `built_at=${new Date().toISOString()}`
].join("\n") + "\n");

const files = walk(outDir)
  .filter((file) => path.basename(file) !== "CHECKSUMS_SHA256.txt")
  .sort((a, b) => a.localeCompare(b));
const checksums = files
  .map((file) => `${hashFile(file)}  ${path.relative(outDir, file).replace(/\\/g, "/")}`)
  .join("\n") + "\n";
writeFile(path.join(outDir, "CHECKSUMS_SHA256.txt"), checksums);

console.log(outDir);
