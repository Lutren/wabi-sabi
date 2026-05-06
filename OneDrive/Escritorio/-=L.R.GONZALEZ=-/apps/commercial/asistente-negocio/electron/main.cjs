const { app, BrowserWindow, shell } = require("electron");
const path = require("path");

const env = process["env"];

if (env.ASISTENTE_USER_DATA_DIR) {
  app.setPath("userData", path.resolve(env.ASISTENTE_USER_DATA_DIR));
}

if (env.ASISTENTE_E2E_PORT) {
  app.commandLine.appendSwitch("remote-debugging-port", env.ASISTENTE_E2E_PORT);
  app.commandLine.appendSwitch("remote-debugging-address", "127.0.0.1");
}

function createWindow() {
  const window = new BrowserWindow({
    width: 1180,
    height: 820,
    minWidth: 920,
    minHeight: 680,
    show: false,
    title: "Asistente de Negocio MEDIOEVO",
    backgroundColor: "#0b0d12",
    webPreferences: {
      preload: path.join(__dirname, "preload.cjs"),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: false
    }
  });

  window.loadFile(path.join(__dirname, "..", "app", "index.html"));
  window.webContents.once("did-finish-load", () => {
    if (!window.isDestroyed()) {
      window.show();
    }
  });

  window.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith("https://") || url.startsWith("mailto:")) {
      shell.openExternal(url);
    }
    return { action: "deny" };
  });
}

app.whenReady().then(() => {
  createWindow();

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});
