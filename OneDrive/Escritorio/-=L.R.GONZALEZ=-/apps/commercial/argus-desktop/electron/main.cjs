const { app, BrowserWindow, Menu, ipcMain, shell } = require('electron')
const path = require('path')
const fs = require('fs')
const fsp = require('fs/promises')
const net = require('net')
const { execFile, spawn, spawnSync } = require('child_process')

const UI_ROOT = path.join(__dirname, '..')
const DIST_INDEX = path.join(UI_ROOT, 'dist', 'index.html')
const CLAUDIO_ROOT = path.resolve(UI_ROOT, '..', '..')
const HUB_ROOT = path.join(CLAUDIO_ROOT, 'screen_hub')
const EVIDENCE_PATH = path.join(UI_ROOT, 'electron', 'system_actions.log')
const BACKEND_LOG = path.join(UI_ROOT, 'electron', 'backend.log')
const USER_HOME = process.env.USERPROFILE || process.env.HOME || ''
const POWERSHELL_7 = 'C:\\Program Files\\PowerShell\\7\\pwsh.exe'
const NEMO_PS1 = path.join(USER_HOME, '.nemo-code', 'nemo-code.ps1')
const LIBRARY_ROOT = 'E:\\-=Medioevo=-\\-=Libros'
const LIBRARY_SHORTCUT = 'C:\\Users\\L-Tyr\\OneDrive\\Escritorio\\-=L.R.GONZALEZ=-\\CLAUDIO - researchs\\-=Libros - Shortcut.lnk'
const API_PORT = 47047
const HUB_PORT = 7474
let mainWindow = null
let backendProc = null
let hubProc = null
let backendRestartCount = 0
const BACKEND_RESTART_LIMIT = 3

function portInUse(port) {
  return new Promise((resolve) => {
    const tester = net.createServer()
      .once('error', (err) => {
        if (err && err.code === 'EADDRINUSE') resolve(true)
        else resolve(false)
      })
      .once('listening', () => tester.close(() => resolve(false)))
      .listen(port, '127.0.0.1')
  })
}

function waitForPort(port, timeoutMs = 30000) {
  const start = Date.now()
  return new Promise((resolve) => {
    const attempt = () => {
      const sock = net.connect({ port, host: '127.0.0.1' })
      sock.once('connect', () => { sock.destroy(); resolve(true) })
      sock.once('error', () => {
        sock.destroy()
        if (Date.now() - start >= timeoutMs) return resolve(false)
        setTimeout(attempt, 500)
      })
    }
    attempt()
  })
}

function spawnBackend(name, cwd, args, port) {
  const logStream = fs.createWriteStream(BACKEND_LOG, { flags: 'a' })
  logStream.write(`\n[${new Date().toISOString()}] [${name}] spawn python ${args.join(' ')} (cwd=${cwd})\n`)
  const child = spawn('python', args, {
    cwd,
    windowsHide: true,
    detached: false,
    stdio: ['ignore', 'pipe', 'pipe']
  })
  child.stdout.on('data', (d) => logStream.write(d))
  child.stderr.on('data', (d) => logStream.write(d))
  child.on('exit', (code, signal) => {
    logStream.write(`[${new Date().toISOString()}] [${name}] exit code=${code} signal=${signal}\n`)
    if (name === 'API' && backendProc === child) {
      backendProc = null
      if (backendRestartCount < BACKEND_RESTART_LIMIT && !app.isQuitting) {
        backendRestartCount += 1
        logStream.write(`[${new Date().toISOString()}] [API] auto-restart ${backendRestartCount}/${BACKEND_RESTART_LIMIT}\n`)
        setTimeout(() => startBackendIfNeeded().catch(() => {}), 2000)
      }
    }
    if (name === 'HUB' && hubProc === child) {
      hubProc = null
    }
  })
  return child
}

async function startBackendIfNeeded() {
  const apiBusy = await portInUse(API_PORT)
  if (!apiBusy) {
    const apiPath = path.join(CLAUDIO_ROOT, 'claudio_api_server.py')
    if (fs.existsSync(apiPath)) {
      backendProc = spawnBackend('API', CLAUDIO_ROOT, [apiPath], API_PORT)
      await waitForPort(API_PORT, 30000)
    }
  }
  const hubBusy = await portInUse(HUB_PORT)
  if (!hubBusy) {
    const hubPath = path.join(HUB_ROOT, 'claudio_screen_hub.py')
    if (fs.existsSync(hubPath)) {
      hubProc = spawnBackend('HUB', HUB_ROOT, [hubPath, '--port', String(HUB_PORT)], HUB_PORT)
      await waitForPort(HUB_PORT, 15000)
    }
  }
}

function killBackend() {
  app.isQuitting = true
  for (const [name, proc] of [['API', backendProc], ['HUB', hubProc]]) {
    if (proc && !proc.killed) {
      try {
        if (process.platform === 'win32') {
          spawnSync('taskkill', ['/PID', String(proc.pid), '/T', '/F'], { windowsHide: true })
        } else {
          proc.kill('SIGTERM')
        }
      } catch (err) {
        try { fs.appendFileSync(BACKEND_LOG, `[${name}] kill error: ${err}\n`) } catch {}
      }
    }
  }
  backendProc = null
  hubProc = null
}

function ensureEvidenceFile() {
  fs.mkdirSync(path.dirname(EVIDENCE_PATH), { recursive: true })
  if (!fs.existsSync(EVIDENCE_PATH)) {
    fs.writeFileSync(EVIDENCE_PATH, '', 'utf8')
  }
}

function appendEvidence(entry) {
  ensureEvidenceFile()
  fs.appendFileSync(
    EVIDENCE_PATH,
    `${JSON.stringify({ ...entry, timestamp: new Date().toISOString() })}\n`,
    'utf8'
  )
}

function resolveShellExecutable(shellName = 'pwsh') {
  const normalized = String(shellName || 'pwsh').toLowerCase()
  if (normalized === 'cmd') {
    return process.env.ComSpec || 'cmd.exe'
  }
  if (normalized === 'powershell') {
    return 'powershell.exe'
  }
  if (fs.existsSync(POWERSHELL_7)) {
    return POWERSHELL_7
  }
  return normalized === 'pwsh' ? 'pwsh.exe' : 'powershell.exe'
}

function buildShellCommand(shellName, command) {
  const normalized = String(shellName || 'pwsh').toLowerCase()
  if (normalized === 'cmd') {
    return {
      file: resolveShellExecutable('cmd'),
      args: ['/d', '/s', '/c', command]
    }
  }

  const file = resolveShellExecutable(normalized === 'powershell' ? 'powershell' : 'pwsh')
  return {
    file,
    args: ['-NoLogo', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', command]
  }
}

function sanitizeProcessOutput(output) {
  return String(output || '')
    .split(/\r?\n/)
    .filter((line) => !line.includes('RequestsDependencyWarning'))
    .filter((line) => !line.trim().startsWith('warnings.warn('))
    .join('\n')
    .trim()
}

function runExecFile(file, args, options = {}) {
  const timeout = Math.min(Math.max(Number(options.timeout) || 120000, 1000), 900000)
  return new Promise((resolve) => {
    execFile(
      file,
      args,
      {
        cwd: options.cwd || CLAUDIO_ROOT,
        windowsHide: true,
        maxBuffer: 1024 * 1024 * 16,
        timeout,
        env: {
          ...process.env,
          ...(options.env || {})
        }
      },
      (error, stdout, stderr) => {
        const output = sanitizeProcessOutput([stdout, stderr].filter(Boolean).join('\n'))
        resolve({
          ok: !error,
          output: output || (error ? String(error) : 'Proceso completado sin salida.')
        })
      }
    )
  })
}

function evaluateGate(actionType, actionTarget = '', riskLevel = 'low') {
  const bridge = `
import json
import sys

action = sys.argv[1]
target = sys.argv[2]
risk = sys.argv[3]
root = sys.argv[4]
if root not in sys.path:
    sys.path.insert(0, root)

from hook_gateway import pre_tool_use

decision = pre_tool_use(action, target, risk)
print(json.dumps({
    "decision": decision.decision,
    "reason": decision.reason,
    "obs_mode": decision.obs_mode,
}))
`

  const result = spawnSync('python', [ '-c', bridge, actionType, actionTarget, riskLevel, CLAUDIO_ROOT ], {
    cwd: CLAUDIO_ROOT,
    encoding: 'utf8',
    windowsHide: true
  })

  if (result.status !== 0) {
    return {
      decision: 'ask',
      reason: (result.stderr || result.stdout || 'HookGateway no disponible').trim(),
      obs_mode: 'manual'
    }
  }

  try {
    return JSON.parse(result.stdout.trim())
  } catch {
    return {
      decision: 'ask',
      reason: 'No se pudo interpretar la decision del gate',
      obs_mode: 'manual'
    }
  }
}

function createWindow() {
  const windowRef = new BrowserWindow({
    width: 1560,
    height: 980,
    minWidth: 1080,
    minHeight: 720,
    backgroundColor: '#07090f',
    icon: path.join(__dirname, 'argus-icon.png'),
    title: 'Argus',
    show: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.cjs')
    }
  })

  windowRef.loadFile(DIST_INDEX)

  windowRef.webContents.once('did-finish-load', () => {
    windowRef.show()
  })

  windowRef.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url)
    return { action: 'deny' }
  })

  windowRef.on('closed', () => {
    if (mainWindow === windowRef) {
      mainWindow = null
    }
  })

  mainWindow = windowRef
  return windowRef
}

async function invokeAction(action, payload = {}) {
  const approve = Boolean(payload.approve)

  if (action === 'health') {
    return {
      ok: true,
      info: {
        apiBase: 'http://127.0.0.1:47047',
        claudioRoot: CLAUDIO_ROOT,
        evidencePath: EVIDENCE_PATH,
        distReady: fs.existsSync(DIST_INDEX),
        platform: process.platform,
        pwsh7: fs.existsSync(POWERSHELL_7) ? POWERSHELL_7 : null,
        nemoPs1: fs.existsSync(NEMO_PS1) ? NEMO_PS1 : null,
        libraryRoot: fs.existsSync(LIBRARY_ROOT) ? LIBRARY_ROOT : null,
        libraryShortcut: fs.existsSync(LIBRARY_SHORTCUT) ? LIBRARY_SHORTCUT : null
      }
    }
  }

  if (action === 'exec') {
    const command = String(payload.command || '').trim()
    const shellName = String(payload.shell || 'pwsh').trim() || 'pwsh'
    const requestedCwd = String(payload.cwd || '').trim()
    const cwd = requestedCwd ? path.resolve(requestedCwd) : CLAUDIO_ROOT
    const timeout = Number(payload.timeoutMs) || 120000
    if (!command) {
      return { ok: false, error: 'Falta comando para la terminal.' }
    }

    const gate = evaluateGate('shell_exec', `${shellName}: ${command}`, 'high')
    appendEvidence({ action, target: `${shellName}: ${command}`, gate, approved: approve, state: gate.decision })

    if (gate.decision === 'deny') {
      return { ok: false, gate, error: gate.reason, evidencePath: EVIDENCE_PATH }
    }

    if (gate.decision === 'ask' && !approve) {
      return { ok: false, gate, requiresApproval: true, evidencePath: EVIDENCE_PATH }
    }

    const execution = buildShellCommand(shellName, command)
    const result = await runExecFile(execution.file, execution.args, { cwd, timeout })
    appendEvidence({
      action,
      target: `${shellName}: ${command}`,
      gate,
      approved: approve,
      state: result.ok ? 'completed' : 'failed'
    })
    return {
      ok: result.ok,
      gate,
      output: result.output,
      evidencePath: EVIDENCE_PATH,
      info: {
        shell: shellName,
        cwd
      }
    }
  }

  if (action === 'launchKnown') {
    const commandId = String(payload.commandId || payload.id || '').trim()
    const prompt = String(payload.prompt || '').trim()
    if (!commandId) {
      return { ok: false, error: 'Falta identificador del launcher.' }
    }

    const launchTarget = commandId === 'clawdworks_print'
      ? `clawdworks: ${prompt}`
      : commandId === 'nemo_task'
        ? `nemo_task: ${prompt}`
        : commandId
    const riskLevel = ['clawdworks_print', 'nemo_task', 'clawdworks_open'].includes(commandId) ? 'high' : 'medium'
    const gate = evaluateGate('shell_exec', launchTarget, riskLevel)
    appendEvidence({ action, target: launchTarget, gate, approved: approve, state: gate.decision })

    if (gate.decision === 'deny') {
      return { ok: false, gate, error: gate.reason, evidencePath: EVIDENCE_PATH }
    }

    if (gate.decision === 'ask' && !approve) {
      return { ok: false, gate, requiresApproval: true, evidencePath: EVIDENCE_PATH }
    }

    if (commandId === 'open_library') {
      const target = fs.existsSync(LIBRARY_SHORTCUT) ? LIBRARY_SHORTCUT : LIBRARY_ROOT
      const result = await shell.openPath(target)
      appendEvidence({ action, target, gate, approved: approve, state: result ? 'failed' : 'completed' })
      return {
        ok: !result,
        gate,
        target,
        error: result || undefined,
        evidencePath: EVIDENCE_PATH
      }
    }

    if (commandId === 'clawdworks_open') {
      if (!fs.existsSync(NEMO_PS1)) {
        return { ok: false, gate, error: 'No se encontró nemo-code.ps1.', evidencePath: EVIDENCE_PATH }
      }
      const shellPath = resolveShellExecutable('pwsh')
      const child = spawn(shellPath, ['-NoExit', '-NoLogo', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', NEMO_PS1], {
        cwd: CLAUDIO_ROOT,
        detached: true,
        windowsHide: false,
        stdio: 'ignore'
      })
      child.unref()
      appendEvidence({ action, target: commandId, gate, approved: approve, state: 'completed' })
      return {
        ok: true,
        gate,
        output: 'ClawdWorks se abrió en una ventana independiente.',
        evidencePath: EVIDENCE_PATH,
        info: { pid: child.pid }
      }
    }

    if (commandId === 'clawdworks_print') {
      if (!prompt) {
        return { ok: false, gate, error: 'Falta prompt para ClawdWorks.', evidencePath: EVIDENCE_PATH }
      }
      if (!fs.existsSync(NEMO_PS1)) {
        return { ok: false, gate, error: 'No se encontró nemo-code.ps1.', evidencePath: EVIDENCE_PATH }
      }

      const shellPath = resolveShellExecutable('pwsh')
      const result = await runExecFile(shellPath, [
        '-NoLogo',
        '-NoProfile',
        '-ExecutionPolicy',
        'Bypass',
        '-File',
        NEMO_PS1,
        '--print',
        prompt
      ], {
        cwd: CLAUDIO_ROOT,
        timeout: Number(payload.timeoutMs) || 480000
      })
      appendEvidence({ action, target: launchTarget, gate, approved: approve, state: result.ok ? 'completed' : 'failed' })
      return {
        ok: result.ok,
        gate,
        output: result.output,
        evidencePath: EVIDENCE_PATH,
        info: { launcher: commandId, shell: 'pwsh' }
      }
    }

    if (commandId === 'nemo_task') {
      if (!prompt) {
        return { ok: false, gate, error: 'Falta prompt para Nemo.', evidencePath: EVIDENCE_PATH }
      }

      const nemoScript = path.join(CLAUDIO_ROOT, 'nemo_research_loop.py')
      if (!fs.existsSync(nemoScript)) {
        return { ok: false, gate, error: 'No se encontró nemo_research_loop.py.', evidencePath: EVIDENCE_PATH }
      }

      const result = await runExecFile('python', [nemoScript, '--task', prompt], {
        cwd: CLAUDIO_ROOT,
        timeout: Number(payload.timeoutMs) || 480000
      })
      appendEvidence({ action, target: launchTarget, gate, approved: approve, state: result.ok ? 'completed' : 'failed' })
      return {
        ok: result.ok,
        gate,
        output: result.output,
        evidencePath: EVIDENCE_PATH,
        info: { launcher: commandId }
      }
    }

    if (commandId === 'launch_thesis') {
      const batPath = path.join(CLAUDIO_ROOT, 'LAUNCH_THESIS.bat')
      if (!fs.existsSync(batPath)) {
        return { ok: false, gate, error: 'LAUNCH_THESIS.bat no encontrado.', evidencePath: EVIDENCE_PATH }
      }
      const child = spawn('cmd.exe', ['/c', batPath], {
        cwd: CLAUDIO_ROOT,
        detached: true,
        windowsHide: false,
        stdio: 'ignore'
      })
      child.unref()
      appendEvidence({ action, target: batPath, gate, approved: approve, state: 'completed' })
      return { ok: true, gate, output: 'MEDIOEVO despertando...', evidencePath: EVIDENCE_PATH, info: { pid: child.pid } }
    }

    return { ok: false, gate, error: `Launcher no soportado: ${commandId}`, evidencePath: EVIDENCE_PATH }
  }

  if (action === 'readFile') {
    const rawPath = String(payload.path || '').trim()
    if (!rawPath) {
      return { ok: false, error: 'Falta ruta para leer.' }
    }
    const target = path.resolve(rawPath)

    const gate = evaluateGate('read_file', target, 'low')
    appendEvidence({ action, target, gate, approved: approve, state: gate.decision })

    if (gate.decision === 'deny') {
      return { ok: false, gate, error: gate.reason, evidencePath: EVIDENCE_PATH }
    }

    if (gate.decision === 'ask' && !approve) {
      return { ok: false, gate, requiresApproval: true, evidencePath: EVIDENCE_PATH }
    }

    try {
      const content = await fsp.readFile(target, 'utf8')
      appendEvidence({ action, target, gate, approved: approve, state: 'completed' })
      return { ok: true, gate, content, target, evidencePath: EVIDENCE_PATH }
    } catch (error) {
      appendEvidence({ action, target, gate, approved: approve, state: 'failed' })
      return { ok: false, gate, error: error instanceof Error ? error.message : 'No se pudo leer el archivo.', evidencePath: EVIDENCE_PATH }
    }
  }

  if (action === 'writeFile') {
    const rawPath = String(payload.path || '').trim()
    const content = String(payload.content || '')
    if (!rawPath) {
      return { ok: false, error: 'Falta ruta para escribir.' }
    }
    const target = path.resolve(rawPath)

    const gate = evaluateGate('write_file', target, 'medium')
    appendEvidence({ action, target, gate, approved: approve, state: gate.decision })

    if (gate.decision === 'deny') {
      return { ok: false, gate, error: gate.reason, evidencePath: EVIDENCE_PATH }
    }

    if (gate.decision === 'ask' && !approve) {
      return { ok: false, gate, requiresApproval: true, evidencePath: EVIDENCE_PATH }
    }

    try {
      await fsp.mkdir(path.dirname(target), { recursive: true })
      await fsp.writeFile(target, content, 'utf8')
      appendEvidence({ action, target, gate, approved: approve, state: 'completed' })
      return { ok: true, gate, target, bytes: Buffer.byteLength(content, 'utf8'), evidencePath: EVIDENCE_PATH }
    } catch (error) {
      appendEvidence({ action, target, gate, approved: approve, state: 'failed' })
      return { ok: false, gate, error: error instanceof Error ? error.message : 'No se pudo escribir el archivo.', evidencePath: EVIDENCE_PATH }
    }
  }

  if (action === 'openPath') {
    const rawPath = String(payload.path || '').trim()
    if (!rawPath) {
      return { ok: false, error: 'Falta ruta para abrir.' }
    }
    const target = path.resolve(rawPath)
    const pathExists = fs.existsSync(target)
    const stats = pathExists ? fs.statSync(target) : null
    const extension = path.extname(target).toLowerCase()
    const executableExts = new Set(['.exe', '.cmd', '.bat', '.ps1', '.psm1', '.vbs', '.js', '.lnk'])
    const riskLevel = stats?.isDirectory() ? 'low' : executableExts.has(extension) ? 'medium' : 'low'
    const gate = evaluateGate('open_path', target, riskLevel)
    appendEvidence({ action, target, gate, approved: approve, state: gate.decision })

    if (gate.decision === 'deny') {
      return { ok: false, gate, error: gate.reason, evidencePath: EVIDENCE_PATH }
    }

    if (gate.decision === 'ask' && !approve) {
      return { ok: false, gate, requiresApproval: true, evidencePath: EVIDENCE_PATH }
    }

    const result = await shell.openPath(target)
    appendEvidence({ action, target, gate, approved: approve, state: result ? 'failed' : 'completed' })
    return {
      ok: !result,
      gate,
      target,
      error: result || undefined,
      evidencePath: EVIDENCE_PATH
    }
  }

  return { ok: false, error: `Accion no soportada: ${action}` }
}

const menuTemplate = [
  ...(process.platform === 'darwin'
    ? [{
        label: app.name,
        submenu: [
          { role: 'about' },
          { type: 'separator' },
          { role: 'hide' },
          { role: 'hideOthers' },
          { role: 'unhide' },
          { type: 'separator' },
          { role: 'quit' }
        ]
      }]
    : []),
  {
    label: 'Editar',
    submenu: [
      { role: 'undo' },
      { role: 'redo' },
      { type: 'separator' },
      { role: 'cut' },
      { role: 'copy' },
      { role: 'paste' },
      { role: 'selectAll' }
    ]
  },
  {
    label: 'Ver',
    submenu: [
      { role: 'reload' },
      { role: 'forceReload' },
      { role: 'toggleDevTools' },
      { type: 'separator' },
      { role: 'togglefullscreen' }
    ]
  }
]

ipcMain.handle('claudio:get-info', async () => ({
  available: true,
  apiBase: 'http://127.0.0.1:47047',
  claudioRoot: CLAUDIO_ROOT,
  evidencePath: EVIDENCE_PATH,
  distReady: fs.existsSync(DIST_INDEX),
  platform: process.platform
}))

ipcMain.handle('claudio:invoke', async (_event, action, payload) => invokeAction(action, payload))

const hasSingleInstanceLock = app.requestSingleInstanceLock()

if (!hasSingleInstanceLock) {
  app.quit()
} else {
  app.on('second-instance', () => {
    if (!mainWindow) {
      return
    }
    if (mainWindow.isMinimized()) {
      mainWindow.restore()
    }
    mainWindow.focus()
  })

  app.whenReady().then(async () => {
    ensureEvidenceFile()
    Menu.setApplicationMenu(Menu.buildFromTemplate(menuTemplate))
    try {
      await startBackendIfNeeded()
    } catch (err) {
      try { fs.appendFileSync(BACKEND_LOG, `[boot] startBackendIfNeeded error: ${err}\n`) } catch {}
    }
    createWindow()

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        createWindow()
      }
    })
  })
}

app.on('before-quit', () => {
  killBackend()
})

app.on('window-all-closed', () => {
  killBackend()
  app.quit()
})
