const { spawn } = require("child_process");
const fs = require("fs");
const http = require("http");
const net = require("net");
const os = require("os");
const path = require("path");

const root = path.resolve(__dirname, "..");
const productExe = process.env.ASISTENTE_E2E_EXE ||
  path.join(root, "release", "win-unpacked", "Asistente de Negocio MEDIOEVO.exe");
const outDir = process.env.ASISTENTE_E2E_OUTDIR ||
  path.join(root, "qa_artifacts", `asistente_negocio_e2e_render_${new Date().toISOString().slice(0, 10)}`);
const userDataDir = process.env.ASISTENTE_USER_DATA_DIR ||
  path.join(os.tmpdir(), `asistente-negocio-e2e-${process.pid}`);

function delay(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function ensureFile(file) {
  if (!fs.existsSync(file)) {
    throw new Error(`Executable not found: ${file}`);
  }
}

function getFreePort() {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.on("error", reject);
    server.listen(0, "127.0.0.1", () => {
      const { port } = server.address();
      server.close(() => resolve(port));
    });
  });
}

function requestJson(url) {
  return new Promise((resolve, reject) => {
    const req = http.get(url, (res) => {
      let body = "";
      res.setEncoding("utf8");
      res.on("data", (chunk) => {
        body += chunk;
      });
      res.on("end", () => {
        if (res.statusCode < 200 || res.statusCode >= 300) {
          reject(new Error(`HTTP ${res.statusCode}: ${body.slice(0, 200)}`));
          return;
        }
        try {
          resolve(JSON.parse(body));
        } catch (error) {
          reject(error);
        }
      });
    });
    req.on("error", reject);
    req.setTimeout(1000, () => {
      req.destroy(new Error("HTTP timeout"));
    });
  });
}

async function waitForPage(port, child) {
  const startedAt = Date.now();
  let lastError = null;
  while (Date.now() - startedAt < 30000) {
    if (child.exitCode !== null) {
      throw new Error(`Application exited before CDP was ready. exitCode=${child.exitCode}`);
    }
    try {
      const pages = await requestJson(`http://127.0.0.1:${port}/json`);
      const page = pages.find((item) =>
        item.type === "page" &&
        item.webSocketDebuggerUrl &&
        (item.url.includes("index.html") || item.title.includes("Asistente de Negocio"))
      ) || pages.find((item) => item.type === "page" && item.webSocketDebuggerUrl);
      if (page) {
        return page;
      }
    } catch (error) {
      lastError = error;
    }
    await delay(300);
  }
  throw new Error(`Timed out waiting for CDP page: ${lastError?.message || "no page"}`);
}

class CdpClient {
  constructor(url) {
    this.url = url;
    this.nextId = 1;
    this.pending = new Map();
    this.ws = null;
  }

  connect() {
    return new Promise((resolve, reject) => {
      this.ws = new WebSocket(this.url);
      this.ws.addEventListener("open", resolve, { once: true });
      this.ws.addEventListener("error", (event) => {
        reject(new Error(event.message || "WebSocket error"));
      }, { once: true });
      this.ws.addEventListener("message", (event) => {
        const message = JSON.parse(event.data);
        if (!message.id) {
          return;
        }
        const pending = this.pending.get(message.id);
        if (!pending) {
          return;
        }
        this.pending.delete(message.id);
        if (message.error) {
          pending.reject(new Error(message.error.message || JSON.stringify(message.error)));
        } else {
          pending.resolve(message.result || {});
        }
      });
      this.ws.addEventListener("close", () => {
        for (const pending of this.pending.values()) {
          pending.reject(new Error("WebSocket closed"));
        }
        this.pending.clear();
      });
    });
  }

  send(method, params = {}) {
    const id = this.nextId++;
    const payload = JSON.stringify({ id, method, params });
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(payload);
    });
  }

  close() {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.close();
    }
  }
}

async function evaluate(client, expression) {
  const result = await client.send("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.text || "Runtime exception");
  }
  return result.result.value;
}

async function waitForRendererReady(client) {
  const startedAt = Date.now();
  let lastState = null;
  while (Date.now() - startedAt < 20000) {
    lastState = await evaluate(client, `(() => ({
      title: document.title,
      readyState: document.readyState,
      hasForm: Boolean(document.querySelector("#profile-form")),
      hasDraftButton: Boolean(document.querySelector("#draft-button"))
    }))()`);
    if (
      lastState.title === "Asistente de Negocio MEDIOEVO" &&
      lastState.readyState !== "loading" &&
      lastState.hasForm &&
      lastState.hasDraftButton
    ) {
      return lastState;
    }
    await delay(250);
  }
  throw new Error(`Unexpected renderer state: ${JSON.stringify(lastState)}`);
}

async function main() {
  ensureFile(productExe);
  fs.mkdirSync(outDir, { recursive: true });
  fs.mkdirSync(userDataDir, { recursive: true });

  const port = Number(process.env.ASISTENTE_E2E_PORT || await getFreePort());
  const child = spawn(productExe, [], {
    cwd: path.dirname(productExe),
    env: {
      ...process.env,
      ASISTENTE_E2E_PORT: String(port),
      ASISTENTE_USER_DATA_DIR: userDataDir
    },
    stdio: "ignore",
    windowsHide: true
  });

  const evidence = {
    product: "Asistente de Negocio MEDIOEVO",
    exe: productExe,
    outDir,
    userDataDir,
    port,
    pid: child.pid,
    startedAt: new Date().toISOString()
  };

  let client;
  try {
    const page = await waitForPage(port, child);
    evidence.page = { title: page.title, url: page.url };
    client = new CdpClient(page.webSocketDebuggerUrl);
    await client.connect();
    await client.send("Runtime.enable");
    await client.send("Page.enable");
    await client.send("Page.bringToFront");

    const ready = await waitForRendererReady(client);

    const interaction = await evaluate(client, `(() => {
      const setValue = (selector, value) => {
        const element = document.querySelector(selector);
        if (!element) throw new Error("Missing selector " + selector);
        element.value = value;
        element.dispatchEvent(new Event("input", { bubbles: true }));
        element.dispatchEvent(new Event("change", { bubbles: true }));
      };
      const setChecked = (selector, value) => {
        const element = document.querySelector(selector);
        if (!element) throw new Error("Missing selector " + selector);
        element.checked = value;
        element.dispatchEvent(new Event("change", { bubbles: true }));
      };

      document.querySelector("#tutorial-close-button")?.click();
      setValue("#business-name", "MEDIOEVO Taller Demo");
      setValue("#contact-email", "ventas@example.com");
      setValue("#customer-email", "cliente@example.com");
      setValue("#customer-whatsapp", "+52 5512345678");
      setValue("#tone", "claro");
      setValue("#price-list", "Diagnostico $500. Instalacion desde $1200.");
      setValue("#business-hours", "Lunes a sabado de 9 a 6. Citas por WhatsApp.");
      setValue("#business-notes", "Aceptamos efectivo, transferencia y tarjeta.");
      setChecked("#privacy-ok", true);
      setChecked("#approval-ok", true);
      document.querySelector("#profile-form").dispatchEvent(new Event("submit", {
        bubbles: true,
        cancelable: true
      }));

      setValue("#incoming-message", "Hola, quiero saber precios, horarios y si puedo agendar una cita.");
      document.querySelector("#draft-button").click();
      setChecked("#reviewed-ok", true);
      document.querySelector("#approve-button").click();

      return {
        title: document.title,
        assistantState: document.querySelector("#assistant-state")?.textContent || "",
        savedBusinessName: document.querySelector("#saved-business-name")?.textContent || "",
        messageState: document.querySelector("#message-state")?.textContent || "",
        draftState: document.querySelector("#draft-state")?.textContent || "",
        draft: document.querySelector("#draft-output")?.value || "",
        emailEnabled: !document.querySelector("#email-send-link")?.classList.contains("disabled"),
        whatsappEnabled: !document.querySelector("#whatsapp-send-link")?.classList.contains("disabled"),
        logText: document.querySelector("#approval-log")?.textContent || "",
        tutorialHidden: document.querySelector("#tutorial-panel")?.hidden === true
      };
    })()`);

    const draft = interaction.draft || "";
    const requiredDraftMarkers = [
      "MEDIOEVO Taller Demo",
      "Precios:",
      "Horarios:",
      "agendar una cita"
    ];
    const missing = requiredDraftMarkers.filter((marker) => !draft.includes(marker));
    if (missing.length) {
      throw new Error(`Draft missing markers: ${missing.join(", ")}`);
    }
    if (!interaction.emailEnabled || !interaction.whatsappEnabled) {
      throw new Error(`External handoff links are not enabled after approval: ${JSON.stringify(interaction)}`);
    }

    const screenshot = await client.send("Page.captureScreenshot", {
      format: "png",
      captureBeyondViewport: false
    });
    const screenshotPath = path.join(outDir, "asistente-e2e-render.png");
    fs.writeFileSync(screenshotPath, Buffer.from(screenshot.data, "base64"));

    evidence.ready = ready;
    evidence.interaction = {
      ...interaction,
      draft: `${draft.slice(0, 220)}${draft.length > 220 ? "..." : ""}`
    };
    evidence.screenshot = screenshotPath;
    evidence.status = "passed";
  } catch (error) {
    evidence.status = "failed";
    evidence.error = error.stack || error.message;
    throw error;
  } finally {
    evidence.finishedAt = new Date().toISOString();
    fs.writeFileSync(path.join(outDir, "e2e-render-smoke.json"), JSON.stringify(evidence, null, 2));
    if (client) {
      try {
        await client.send("Browser.close");
      } catch {
        client.close();
      }
    }
    await delay(1000);
    if (child.exitCode === null) {
      child.kill();
    }
  }

  console.log(`E2E render smoke passed: ${path.join(outDir, "e2e-render-smoke.json")}`);
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
