const assert = require('assert');
const Module = require('module');

const handlers = [];
const appEvents = [];
let whenReadyCalled = false;

const originalLoad = Module._load;

Module._load = function patchedLoad(request, parent, isMain) {
  if (request === 'electron') {
    return {
      app: {
        getPath(name) {
          assert.strictEqual(name, 'userData');
          return __dirname;
        },
        whenReady() {
          whenReadyCalled = true;
          return { then() {} };
        },
        on(eventName, callback) {
          appEvents.push({ eventName, callback });
        },
        quit() {},
      },
      BrowserWindow: {
        getAllWindows() {
          return [];
        },
      },
      ipcMain: {
        handle(channel, callback) {
          handlers.push({ channel, callback });
        },
      },
      Menu: {
        setApplicationMenu() {},
      },
      Tray: function Tray() {},
      dialog: {},
    };
  }
  return originalLoad.call(this, request, parent, isMain);
};

try {
  require('../main.js');
} finally {
  Module._load = originalLoad;
}

assert.strictEqual(whenReadyCalled, true, 'main process must call app.whenReady()');

const channels = handlers.map((row) => row.channel).sort();
assert.deepStrictEqual(channels, [
  'contacts:create',
  'contacts:delete',
  'contacts:get',
  'contacts:getAll',
  'contacts:import',
  'contacts:update',
  'db:backup',
  'db:restore',
  'pipeline:create',
  'pipeline:delete',
  'pipeline:getAll',
  'pipeline:update',
  'reports:summary',
  'settings:get',
  'settings:getAll',
  'settings:set',
  'tasks:create',
  'tasks:delete',
  'tasks:getAll',
  'tasks:update',
]);

assert.deepStrictEqual(
  appEvents.map((row) => row.eventName).sort(),
  ['activate', 'window-all-closed'],
);

const source = require('fs').readFileSync(require('path').join(__dirname, '..', 'main.js'), 'utf8');
assert.strictEqual(source.includes('.foreach('), false, 'use Array.prototype.forEach');
assert.strictEqual(source.includes('toIere'), false, 'use Date.prototype.toISOString');
assert.strictEqual(source.includes('INSERT OR rePLACE'), false, 'use valid INSERT OR REPLACE casing');
assert.strictEqual(source.includes("mainWindow.loadFile('mockup.html')"), true, 'load the complete QA UI');
assert.strictEqual(source.includes('FLUJOCRM_USER_DATA_DIR'), true, 'support isolated QA user data dir');
assert.strictEqual(source.includes('FLUJOCRM_E2E_PORT'), true, 'support isolated E2E debug port');

console.log('flujocrm main smoke passed');
