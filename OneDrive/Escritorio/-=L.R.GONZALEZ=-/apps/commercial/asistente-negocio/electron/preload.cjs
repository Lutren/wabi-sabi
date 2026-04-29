const { contextBridge, clipboard } = require("electron");

contextBridge.exposeInMainWorld("medioevo", {
  readClipboardText: () => clipboard.readText()
});
