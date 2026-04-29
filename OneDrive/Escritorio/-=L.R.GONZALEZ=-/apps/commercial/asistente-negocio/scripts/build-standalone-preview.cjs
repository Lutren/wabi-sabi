const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const appDir = path.join(root, "app");
const outPath = process.argv[2]
  ? path.resolve(process.argv[2])
  : path.join(root, "preview", "ABRE_AQUI_PREVIEW_MEDIOEVO.html");

function readText(relativePath) {
  return fs.readFileSync(path.join(appDir, relativePath), "utf8");
}

function dataUrl(relativePath) {
  const filePath = path.join(appDir, relativePath);
  const ext = path.extname(filePath).toLowerCase();
  const mime = ext === ".png" ? "image/png" : "application/octet-stream";
  return `data:${mime};base64,${fs.readFileSync(filePath).toString("base64")}`;
}

let html = readText("index.html");
let css = readText("styles.css");
const js = readText("app.js").replace(/<\/script/gi, "<\\/script");

const assets = [
  "assets/geodia_control_chip_v1.png",
  "assets/geodia_cta_banner_v1.png",
  "assets/geodia_hub_scenario_v2.png",
  "assets/medioevo_business_hub.png"
];

for (const asset of assets) {
  const encoded = dataUrl(asset);
  const escaped = asset.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  css = css.replace(new RegExp(`url\\(["']?\\./${escaped}["']?\\)`, "g"), `url("${encoded}")`);
  html = html.replace(new RegExp(`src=["']\\./${escaped}["']`, "g"), `src="${encoded}"`);
}

html = html
  .replace(/<link rel="stylesheet" href="\.\/styles\.css">/, `<style>\n${css}\n</style>`)
  .replace(/<script src="\.\/app\.js"><\/script>/, `<script>\n${js}\n</script>`)
  .replace("</head>", "  <!-- Standalone product preview: CSS, JS and MEDIOEVO assets embedded for ZIP/direct opening. -->\n</head>");

fs.mkdirSync(path.dirname(outPath), { recursive: true });
fs.writeFileSync(outPath, html, "utf8");
console.log(outPath);
