const assert = require('assert');
const childProcess = require('child_process');
const fs = require('fs');
const http = require('http');
const os = require('os');
const path = require('path');

const appExe = process.env.FLUJOCRM_E2E_EXE
  || path.join(__dirname, '..', 'dist', 'win-unpacked', 'FlujoCRM.exe');
const userDataDir = fs.mkdtempSync(path.join(os.tmpdir(), 'flujocrm-e2e-'));
const port = Number(process.env.FLUJOCRM_E2E_PORT || 9323);

function requestJson(url) {
  return new Promise((resolve, reject) => {
    const req = http.get(url, (res) => {
      let body = '';
      res.setEncoding('utf8');
      res.on('data', (chunk) => { body += chunk; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (error) {
          reject(error);
        }
      });
    });
    req.on('error', reject);
    req.setTimeout(1000, () => {
      req.destroy(new Error(`timeout requesting ${url}`));
    });
  });
}

async function waitForDebugger() {
  const deadline = Date.now() + 30000;
  while (Date.now() < deadline) {
    try {
      const pages = await requestJson(`http://127.0.0.1:${port}/json/list`);
      const page = pages.find((item) =>
        item.webSocketDebuggerUrl
        && item.type === 'page'
        && !String(item.url || '').startsWith('devtools://')
      );
      if (page) return page.webSocketDebuggerUrl;
    } catch (error) {
      // Keep polling while Electron starts.
    }
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  throw new Error('Electron debugger endpoint did not become available');
}

function createCdpClient(webSocketUrl) {
  let nextId = 1;
  const pending = new Map();
  const ws = new WebSocket(webSocketUrl);

  ws.addEventListener('message', (event) => {
    const data = JSON.parse(event.data);
    if (!data.id) return;
    const entry = pending.get(data.id);
    if (!entry) return;
    pending.delete(data.id);
    if (data.error) {
      entry.reject(new Error(data.error.message));
    } else {
      entry.resolve(data.result);
    }
  });

  return new Promise((resolve, reject) => {
    ws.addEventListener('open', () => {
      resolve({
        send(method, params = {}) {
          const id = nextId++;
          ws.send(JSON.stringify({ id, method, params }));
          return new Promise((res, rej) => pending.set(id, { resolve: res, reject: rej }));
        },
        close() {
          ws.close();
        },
      });
    });
    ws.addEventListener('error', reject);
  });
}

function taskkill(pid) {
  childProcess.spawnSync('taskkill.exe', ['/PID', String(pid), '/T', '/F'], { stdio: 'ignore' });
}

function inspectSqlite(dbPath) {
  const code = [
    'import json, sqlite3, sys',
    'db = sqlite3.connect(sys.argv[1])',
    'cols = [row[1] for row in db.execute("PRAGMA table_info(contacts)").fetchall()]',
    'row = db.execute("SELECT COUNT(*) AS count, COALESCE(SUM(value), 0) AS total FROM contacts").fetchone()',
    'print(json.dumps({"columns": cols, "count": row[0], "total": row[1]}))',
  ].join('\n');
  const result = childProcess.spawnSync('python', ['-c', code, dbPath], {
    encoding: 'utf8',
    windowsHide: true,
  });
  if (result.status !== 0) {
    throw new Error(result.stderr || `python sqlite inspector failed with status ${result.status}`);
  }
  return JSON.parse(result.stdout);
}

async function evaluate(client, expression, options = {}) {
  const result = await client.send('Runtime.evaluate', {
    expression,
    returnByValue: true,
    ...options,
  });
  if (result.exceptionDetails) {
    throw new Error(result.exceptionDetails.text || `evaluation failed: ${expression}`);
  }
  return result.result.value;
}

async function waitForValue(client, expression, expected) {
  const deadline = Date.now() + 30000;
  while (Date.now() < deadline) {
    const value = await evaluate(client, expression);
    if (value === expected) return value;
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  throw new Error(`timed out waiting for ${expression} === ${expected}`);
}

(async () => {
  assert.strictEqual(fs.existsSync(appExe), true, `missing built app: ${appExe}`);

  const child = childProcess.spawn(appExe, [], {
    env: {
      ...process.env,
      FLUJOCRM_USER_DATA_DIR: userDataDir,
      FLUJOCRM_E2E_PORT: String(port),
    },
    stdio: 'ignore',
    windowsHide: true,
  });

  let client;
  try {
    const wsUrl = await waitForDebugger();
    client = await createCdpClient(wsUrl);
    await client.send('Runtime.enable');
    await waitForValue(client, "typeof hasNativeStorage === 'function'", true);
    assert.strictEqual(
      await evaluate(client, 'hasNativeStorage()'),
      true,
      'renderer must detect native SQLite storage',
    );
    await evaluate(client, 'loadDemo()', { awaitPromise: true });
    assert.strictEqual(
      await evaluate(client, 'contacts.length'),
      15,
      'demo contacts must be present in renderer state',
    );
  } finally {
    if (client) client.close();
    taskkill(child.pid);
  }

  const dbPath = path.join(userDataDir, 'data', 'flujocrm.db');
  assert.strictEqual(fs.existsSync(dbPath), true, 'SQLite DB must exist after renderer actions');
  const sqlite = inspectSqlite(dbPath);
  assert.strictEqual(sqlite.columns.includes('stage'), true, 'contacts table must include stage');
  assert.strictEqual(sqlite.columns.includes('value'), true, 'contacts table must include value');
  assert.strictEqual(sqlite.columns.includes('last_activity'), true, 'contacts table must include last_activity');
  assert.strictEqual(sqlite.count, 15, 'SQLite must persist demo contacts through IPC');
  assert.strictEqual(Number(sqlite.total), 958000, 'SQLite must persist contact values through IPC');

  console.log(`flujocrm e2e storage smoke passed: ${dbPath}`);
})().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
