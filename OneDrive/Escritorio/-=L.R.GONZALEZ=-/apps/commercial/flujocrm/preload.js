const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  // Contacts
  contacts: {
    getAll: (filters) => ipcRenderer.invoke('contacts:getAll', filters),
    get: (id) => ipcRenderer.invoke('contacts:get', id),
    create: (data) => ipcRenderer.invoke('contacts:create', data),
    update: (id, data) => ipcRenderer.invoke('contacts:update', id, data),
    delete: (id) => ipcRenderer.invoke('contacts:delete', id),
    import: () => ipcRenderer.invoke('contacts:import')
  },

  // Pipeline
  pipeline: {
    getAll: () => ipcRenderer.invoke('pipeline:getAll'),
    create: (data) => ipcRenderer.invoke('pipeline:create', data),
    update: (id, data) => ipcRenderer.invoke('pipeline:update', id, data),
    delete: (id) => ipcRenderer.invoke('pipeline:delete', id)
  },

  // Tasks
  tasks: {
    getAll: (filters) => ipcRenderer.invoke('tasks:getAll', filters),
    create: (data) => ipcRenderer.invoke('tasks:create', data),
    update: (id, data) => ipcRenderer.invoke('tasks:update', id, data),
    delete: (id) => ipcRenderer.invoke('tasks:delete', id)
  },

  // Settings
  settings: {
    get: (key) => ipcRenderer.invoke('settings:get', key),
    getAll: () => ipcRenderer.invoke('settings:getAll'),
    set: (key, value) => ipcRenderer.invoke('settings:set', key, value)
  },

  // reports
  reports: {
    summary: () => ipcRenderer.invoke('reports:summary')
  },

  // Database
  db: {
    backup: () => ipcRenderer.invoke('db:backup'),
    restore: () => ipcRenderer.invoke('db:restore')
  }
});
