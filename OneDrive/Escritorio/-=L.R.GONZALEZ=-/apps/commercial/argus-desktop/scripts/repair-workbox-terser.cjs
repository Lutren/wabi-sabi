const fs = require('fs')
const path = require('path')

const packageJsonPath = path.join(
  __dirname,
  '..',
  'node_modules',
  'workbox-build',
  'package.json'
)

if (!fs.existsSync(packageJsonPath)) {
  process.exit(0)
}

const raw = fs.readFileSync(packageJsonPath, 'utf8')
const data = JSON.parse(raw)

if (!data.dependencies || !data.dependencies['@rollup/plugin-terser']) {
  process.exit(0)
}

if (data.dependencies['@rollup/plugin-terser'] === '^1.0.0') {
  process.exit(0)
}

// Workbox 7.4.0 runs correctly with @rollup/plugin-terser 1.0.0, which in turn
// pulls the fixed serialize-javascript line required to clear npm audit.
data.dependencies['@rollup/plugin-terser'] = '^1.0.0'
fs.writeFileSync(packageJsonPath, `${JSON.stringify(data, null, 2)}\n`, 'utf8')
