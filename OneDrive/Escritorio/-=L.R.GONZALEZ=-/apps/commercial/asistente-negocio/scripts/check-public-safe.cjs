const fs = require("fs");
const path = require("path");

const root = path.resolve(__dirname, "..");
const manifest = JSON.parse(fs.readFileSync(path.join(root, "manifest.json"), "utf8"));

const runtimeDirs = ["app", "electron"];
const textExtensions = new Set([".html", ".css", ".js", ".cjs", ".mjs", ".json", ".md", ".txt"]);
const forbidden = [
  "playwright",
  "puppeteer",
  "whatsapp web",
  "document.cookie",
  "process.env.GUMROAD",
  "process.env.STRIPE",
  "shell.openPath",
  "child_process",
  ".env"
];

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

const failures = [];

if (manifest.profile !== "public_safe") {
  failures.push("manifest.profile must be public_safe");
}

if (manifest.autonomy !== "human_approved_external_send") {
  failures.push("manifest.autonomy must be human_approved_external_send");
}

if (!manifest.blocked_from_public.includes("whatsapp_web_playwright")) {
  failures.push("manifest must explicitly block whatsapp_web_playwright");
}

for (const dirName of runtimeDirs) {
  const dir = path.join(root, dirName);
  for (const file of walk(dir)) {
    if (!textExtensions.has(path.extname(file).toLowerCase())) {
      continue;
    }
    const text = fs.readFileSync(file, "utf8").toLowerCase();
    for (const token of forbidden) {
      if (text.includes(token)) {
        failures.push(`${path.relative(root, file)} contains forbidden marker "${token}"`);
      }
    }
  }
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log("public_safe check passed");
