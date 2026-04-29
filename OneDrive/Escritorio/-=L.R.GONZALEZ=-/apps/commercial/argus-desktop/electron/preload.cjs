const { contextBridge, ipcRenderer } = require('electron')

contextBridge.exposeInMainWorld('claudioDesktop', {
  available: true,
  getInfo: () => ipcRenderer.invoke('claudio:get-info'),
  invoke: (action, payload = {}) => ipcRenderer.invoke('claudio:invoke', action, payload)
})
