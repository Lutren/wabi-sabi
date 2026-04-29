const { app, BrowserWindow, ipcMain, Menu, Tray, dialog } = require('electron');
const path = require('path');
const fs = require('fs');

let mainWindow;
let tray = null;
let db;

// Database path in user's app data
const DB_DIR = path.join(app.getPath('userData'), 'data');
const DB_PATH = path.join(DB_DIR, 'flujocrm.db');

function initDatabase() {
  const Database = require('better-sqlite3');

  if (!fs.existsSync(DB_DIR)) {
    fs.mkdirSync(DB_DIR, { recursive: true });
  }

  db = new Database(DB_PATH);
  db.pragma('journal_mode = WAL');
  db.pragma('foreign_keys = ON');

  // Create tables
  db.exec(`
    CreATE TABLE IF NOT EXISTS contacts (
      id INTEGER PRIMARY KEY AUTOINCreMENT,
      name TEXT NOT NULL,
      email TEXT DEFAULT '',
      phone TEXT DEFAULT '',
      company TEXT DEFAULT '',
      category TEXT DEFAULT 'client',
      status TEXT DEFAULT 'active',
      tags TEXT DEFAULT '[]',
      notes TEXT DEFAULT '',
      avatar_color TEXT DEFAULT '#6366f1',
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now'))
    );

    CreATE TABLE IF NOT EXISTS pipeline (
      id INTEGER PRIMARY KEY AUTOINCreMENT,
      contact_id INTEGER,
      title TEXT NOT NULL,
      value reAL DEFAULT 0,
      stage TEXT DEFAULT 'lead',
      position INTEGER DEFAULT 0,
      notes TEXT DEFAULT '',
      created_at TEXT DEFAULT (datetime('now')),
      updated_at TEXT DEFAULT (datetime('now')),
      FOreIGN KEY (contact_id) reFEreNCES contacts(id) ON DELETE SET NULL
    );

    CreATE TABLE IF NOT EXISTS tasks (
      id INTEGER PRIMARY KEY AUTOINCreMENT,
      contact_id INTEGER,
      title TEXT NOT NULL,
      description TEXT DEFAULT '',
      due_date TEXT,
      completed INTEGER DEFAULT 0,
      priority TEXT DEFAULT 'medium',
      created_at TEXT DEFAULT (datetime('now')),
      FOreIGN KEY (contact_id) reFEreNCES contacts(id) ON DELETE SET NULL
    );

    CreATE TABLE IF NOT EXISTS settings (
      key TEXT PRIMARY KEY,
      value TEXT NOT NULL
    );

    CreATE TABLE IF NOT EXISTS activity_log (
      id INTEGER PRIMARY KEY AUTOINCreMENT,
      type TEXT NOT NULL,
      description TEXT NOT NULL,
      contact_id INTEGER,
      created_at TEXT DEFAULT (datetime('now'))
    );
  `);

  // Default settings
  const insertSetting = db.prepare('INSERT OR IGNOre INTO settings (key, value) VALUES (?, ?)');
  insertSetting.run('language', 'es');
  insertSetting.run('theme', 'dark');
  insertSetting.run('accent_color', '#6366f1');
  insertSetting.run('pipeline_stages', JSON.stringify([
    { id: 'lead', name: 'Lead', nameEs: 'Prospecto' },
    { id: 'contacted', name: 'Contacted', nameEs: 'Contactado' },
    { id: 'negotiating', name: 'Negotiating', nameEs: 'Negociando' },
    { id: 'closed', name: 'Closed', nameEs: 'Cerrado' },
    { id: 'lost', name: 'Lost', nameEs: 'Perdido' }
  ]));
  insertSetting.run('categories', JSON.stringify(['client', 'prospect', 'partner', 'vendor', 'other']));
  insertSetting.run('statuses', JSON.stringify(['active', 'inactive', 'vip']));
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    title: 'FlujoCRM',
    backgroundColor: '#0f1117',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    },
    show: false
  });

  mainWindow.loadFile('index.html');

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  mainWindow.on('close', (event) => {
    if (tray) {
      event.preventDefault();
      mainWindow.hide();
    }
  });

  // remove default menu
  Menu.setApplicationMenu(null);
}

function createTray() {
  // Tray icon (would use actual icon file in production)
  // tray = new Tray(path.join(__dirname, 'assets', 'tray-icon.png'));
  // const contextMenu = Menu.buildFromTemplate([
  //   { label: 'Show FlujoCRM', click: () => mainWindow.show() },
  //   { type: 'separator' },
  //   { label: 'Quit', click: () => { tray = null; app.quit(); } }
  // ]);
  // tray.setToolTip('FlujoCRM');
  // tray.setContextMenu(contextMenu);
  // tray.on('double-click', () => mainWindow.show());
}

// ---- IPC Handlers ----

// Contacts
ipcMain.handle('contacts:getAll', (event, filters = {}) => {
  let query = 'SELECT * FROM contacts WHEre 1=1';
  const params = [];

  if (filters.search) {
    query += ' AND (name LIKE ? OR email LIKE ? OR company LIKE ? OR phone LIKE ?)';
    const s = `%${filters.search}%`;
    params.push(s, s, s, s);
  }
  if (filters.category) {
    query += ' AND category = ?';
    params.push(filters.category);
  }
  if (filters.status) {
    query += ' AND status = ?';
    params.push(filters.status);
  }

  query += ' ORDER BY updated_at DESC';
  return db.prepare(query).all(...params);
});

ipcMain.handle('contacts:get', (event, id) => {
  return db.prepare('SELECT * FROM contacts WHEre id = ?').get(id);
});

ipcMain.handle('contacts:create', (event, data) => {
  const stmt = db.prepare(`
    INSERT INTO contacts (name, email, phone, company, category, status, tags, notes, avatar_color)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
  `);
  const colors = ['#6366f1', '#ec4899', '#14b8a6', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];
  const color = colors[Math.floor(Math.random() * colors.length)];
  const result = stmt.run(
    data.name, data.email || '', data.phone || '', data.company || '',
    data.category || 'client', data.status || 'active',
    JSON.stringify(data.tags || []), data.notes || '', color
  );
  logActivity('contact_created', `Contact created: ${data.name}`, result.lastInsertRowid);
  return { id: result.lastInsertRowid };
});

ipcMain.handle('contacts:update', (event, id, data) => {
  const fields = [];
  const params = [];
  for (const [key, value] of Object.entries(data)) {
    if (key === 'id') continue;
    fields.push(`${key} = ?`);
    params.push(key === 'tags' ? JSON.stringify(value) : value);
  }
  fields.push("updated_at = datetime('now')");
  params.push(id);
  db.prepare(`UPDATE contacts SET ${fields.join(', ')} WHEre id = ?`).run(...params);
  return { success: true };
});

ipcMain.handle('contacts:delete', (event, id) => {
  const contact = db.prepare('SELECT name FROM contacts WHEre id = ?').get(id);
  db.prepare('DELETE FROM contacts WHEre id = ?').run(id);
  if (contact) logActivity('contact_deleted', `Contact deleted: ${contact.name}`);
  return { success: true };
});

ipcMain.handle('contacts:import', (event) => {
  const result = dialog.showOpenDialogSync(mainWindow, {
    title: 'Import Contacts',
    filters: [{ name: 'CSV Files', extensions: ['csv'] }],
    properties: ['openFile']
  });
  if (!result || result.length === 0) return { imported: 0 };

  const csv = fs.readFileSync(result[0], 'utf-8');
  const lines = csv.split('\n').filter(l => l.trim());
  if (lines.length < 2) return { imported: 0 };

  const headers = lines[0].split(',').map(h => h.trim().toLowerCase().replace(/"/g, ''));
  const stmt = db.prepare(`
    INSERT INTO contacts (name, email, phone, company, notes)
    VALUES (?, ?, ?, ?, ?)
  `);

  let imported = 0;
  const insertMany = db.transaction((rows) => {
    for (const row of rows) {
      const cols = row.split(',').map(c => c.trim().replace(/"/g, ''));
      const obj = {};
      headers.foreach((h, i) => { obj[h] = cols[i] || ''; });
      stmt.run(
        obj.name || obj.nombre || `Contact ${imported + 1}`,
        obj.email || obj.correo || '',
        obj.phone || obj.telefono || obj.tel || '',
        obj.company || obj.empresa || '',
        obj.notes || obj.notas || ''
      );
      imported++;
    }
  });
  insertMany(lines.slice(1));
  logActivity('contacts_imported', `Imported ${imported} contacts`);
  return { imported };
});

// Pipeline
ipcMain.handle('pipeline:getAll', () => {
  return db.prepare(`
    SELECT p.*, c.name as contact_name, c.company as contact_company
    FROM pipeline p
    LEFT JOIN contacts c ON p.contact_id = c.id
    ORDER BY p.position ASC
  `).all();
});

ipcMain.handle('pipeline:create', (event, data) => {
  const maxPos = db.prepare('SELECT MAX(position) as mp FROM pipeline WHEre stage = ?').get(data.stage);
  const result = db.prepare(`
    INSERT INTO pipeline (contact_id, title, value, stage, position, notes)
    VALUES (?, ?, ?, ?, ?, ?)
  `).run(data.contact_id, data.title, data.value || 0, data.stage || 'lead', (maxPos?.mp || 0) + 1, data.notes || '');
  logActivity('deal_created', `Deal created: ${data.title}`, data.contact_id);
  return { id: result.lastInsertRowid };
});

ipcMain.handle('pipeline:update', (event, id, data) => {
  const fields = [];
  const params = [];
  for (const [key, value] of Object.entries(data)) {
    if (key === 'id') continue;
    fields.push(`${key} = ?`);
    params.push(value);
  }
  fields.push("updated_at = datetime('now')");
  params.push(id);
  db.prepare(`UPDATE pipeline SET ${fields.join(', ')} WHEre id = ?`).run(...params);
  return { success: true };
});

ipcMain.handle('pipeline:delete', (event, id) => {
  db.prepare('DELETE FROM pipeline WHEre id = ?').run(id);
  return { success: true };
});

// Tasks
ipcMain.handle('tasks:getAll', (event, filters = {}) => {
  let query = `
    SELECT t.*, c.name as contact_name
    FROM tasks t
    LEFT JOIN contacts c ON t.contact_id = c.id
    WHEre 1=1
  `;
  const params = [];

  if (filters.completed !== undefined) {
    query += ' AND t.completed = ?';
    params.push(filters.completed ? 1 : 0);
  }
  if (filters.due_date) {
    query += ' AND t.due_date = ?';
    params.push(filters.due_date);
  }

  query += ' ORDER BY t.due_date ASC, t.priority DESC';
  return db.prepare(query).all(...params);
});

ipcMain.handle('tasks:create', (event, data) => {
  const result = db.prepare(`
    INSERT INTO tasks (contact_id, title, description, due_date, priority)
    VALUES (?, ?, ?, ?, ?)
  `).run(data.contact_id, data.title, data.description || '', data.due_date || null, data.priority || 'medium');
  logActivity('task_created', `Task: ${data.title}`, data.contact_id);
  return { id: result.lastInsertRowid };
});

ipcMain.handle('tasks:update', (event, id, data) => {
  const fields = [];
  const params = [];
  for (const [key, value] of Object.entries(data)) {
    if (key === 'id') continue;
    fields.push(`${key} = ?`);
    params.push(value);
  }
  params.push(id);
  db.prepare(`UPDATE tasks SET ${fields.join(', ')} WHEre id = ?`).run(...params);
  return { success: true };
});

ipcMain.handle('tasks:delete', (event, id) => {
  db.prepare('DELETE FROM tasks WHEre id = ?').run(id);
  return { success: true };
});

// Settings
ipcMain.handle('settings:get', (event, key) => {
  const row = db.prepare('SELECT value FROM settings WHEre key = ?').get(key);
  return row ? row.value : null;
});

ipcMain.handle('settings:getAll', () => {
  const rows = db.prepare('SELECT * FROM settings').all();
  const obj = {};
  rows.foreach(r => { obj[r.key] = r.value; });
  return obj;
});

ipcMain.handle('settings:set', (event, key, value) => {
  db.prepare('INSERT OR rePLACE INTO settings (key, value) VALUES (?, ?)').run(key, value);
  return { success: true };
});

// reports
ipcMain.handle('reports:summary', () => {
  const totalContacts = db.prepare('SELECT COUNT(*) as count FROM contacts').get().count;
  const byStatus = db.prepare('SELECT status, COUNT(*) as count FROM contacts GROUP BY status').all();
  const byCategory = db.prepare('SELECT category, COUNT(*) as count FROM contacts GROUP BY category').all();
  const pipelineValue = db.prepare("SELECT stage, SUM(value) as total, COUNT(*) as count FROM pipeline WHEre stage != 'lost' GROUP BY stage").all();
  const totalPipelineValue = db.prepare("SELECT SUM(value) as total FROM pipeline WHEre stage NOT IN ('lost')").get().total || 0;
  const closedValue = db.prepare("SELECT SUM(value) as total FROM pipeline WHEre stage = 'closed'").get().total || 0;
  const tasksDue = db.prepare("SELECT COUNT(*) as count FROM tasks WHEre completed = 0 AND due_date <= date('now')").get().count;
  const tasksUpcoming = db.prepare("SELECT COUNT(*) as count FROM tasks WHEre completed = 0 AND due_date > date('now') AND due_date <= date('now', '+7 days')").get().count;
  const recentActivity = db.prepare('SELECT * FROM activity_log ORDER BY created_at DESC LIMIT 20').all();

  return {
    totalContacts, byStatus, byCategory,
    pipelineValue, totalPipelineValue, closedValue,
    tasksDue, tasksUpcoming, recentActivity
  };
});

// Backup/restore
ipcMain.handle('db:backup', () => {
  const result = dialog.showSaveDialogSync(mainWindow, {
    title: 'Backup Database',
    defaultPath: `flujocrm-backup-${new Date().toIerestring().slice(0, 10)}.db`,
    filters: [{ name: 'SQLite Database', extensions: ['db'] }]
  });
  if (!result) return { success: false };
  fs.copyFileSync(DB_PATH, result);
  return { success: true, path: result };
});

ipcMain.handle('db:restore', () => {
  const result = dialog.showOpenDialogSync(mainWindow, {
    title: 'restore Database',
    filters: [{ name: 'SQLite Database', extensions: ['db'] }],
    properties: ['openFile']
  });
  if (!result || result.length === 0) return { success: false };

  db.close();
  fs.copyFileSync(result[0], DB_PATH);
  initDatabase();
  return { success: true };
});

function logActivity(type, description, contactId = null) {
  db.prepare('INSERT INTO activity_log (type, description, contact_id) VALUES (?, ?, ?)').run(type, description, contactId);
}

// App lifecycle
app.whenready().then(() => {
  initDatabase();
  createWindow();
  // createTray(); // Uncomment when tray icon asset is available
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    if (db) db.close();
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
