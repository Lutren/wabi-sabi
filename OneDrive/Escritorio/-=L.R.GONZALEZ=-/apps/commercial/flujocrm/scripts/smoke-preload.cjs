const assert = require('assert');
const Module = require('module');

const exposed = [];
const invoked = [];
const originalLoad = Module._load;

Module._load = function patchedLoad(request, parent, isMain) {
  if (request === 'electron') {
    return {
      contextBridge: {
        exposeInMainWorld(key, value) {
          exposed.push({ key, value });
        },
      },
      ipcRenderer: {
        invoke(channel, ...args) {
          invoked.push({ channel, args });
          return { channel, args };
        },
      },
    };
  }
  return originalLoad.call(this, request, parent, isMain);
};

try {
  require('../preload.js');
} finally {
  Module._load = originalLoad;
}

assert.strictEqual(exposed.length, 1, 'preload must expose exactly one API object');
assert.strictEqual(exposed[0].key, 'api', 'preload must expose api');

const api = exposed[0].value;
assert.strictEqual(typeof api.contacts.getAll, 'function');
assert.strictEqual(typeof api.pipeline.update, 'function');
assert.strictEqual(typeof api.tasks.create, 'function');
assert.strictEqual(typeof api.settings.set, 'function');
assert.strictEqual(typeof api.reports.summary, 'function');
assert.strictEqual(typeof api.db.backup, 'function');

api.contacts.getAll({ search: 'demo' });
api.pipeline.update(7, { stage: 'closed' });
api.tasks.create({ title: 'follow up' });
api.settings.set('theme', 'dark');
api.reports.summary();
api.db.backup();

const channels = invoked.map((row) => row.channel);
assert.deepStrictEqual(channels, [
  'contacts:getAll',
  'pipeline:update',
  'tasks:create',
  'settings:set',
  'reports:summary',
  'db:backup',
]);

console.log('flujocrm preload smoke passed');
