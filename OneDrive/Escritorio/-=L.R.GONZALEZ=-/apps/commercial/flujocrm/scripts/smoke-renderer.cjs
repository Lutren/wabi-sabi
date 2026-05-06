const assert = require('assert');
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, '..', 'mockup.html'), 'utf8');

assert.strictEqual(html.includes('cdn.jsdelivr.net'), false, 'renderer must not depend on CDN Chart.js');
assert.strictEqual(html.includes('This is the Electron version'), false, 'renderer must not expose placeholder copy');
assert.strictEqual(html.includes('POWEreD'), false, 'renderer must not contain corrupted POWERED copy');
assert.strictEqual(html.includes('Ingreeres'), false, 'renderer must not contain corrupted ingresos copy');
assert.strictEqual(html.includes('hasNativeStorage()'), true, 'renderer must detect Electron native storage');
assert.strictEqual(html.includes('window.api.contacts.create'), true, 'renderer must create contacts through SQLite IPC when available');
assert.strictEqual(html.includes('window.api.contacts.update'), true, 'renderer must update contacts through SQLite IPC when available');
assert.strictEqual(html.includes('window.api.contacts.delete'), true, 'renderer must delete contacts through SQLite IPC when available');
assert.strictEqual(html.includes('./node_modules/chart.js/dist/chart.umd.js'), true, 'renderer must use bundled Chart.js');

console.log('flujocrm renderer smoke passed');
