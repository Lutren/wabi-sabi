export type ServerStatus = {
  ok: boolean
  server: string
  port: number
  local_ip: string
  timestamp: number
}

export type BuddyStatus = {
  mode: 'stable' | 'degraded' | 'repair' | 'manual' | string
  observacionismo: {
    r: number
    phi_eff: number
    j_c: number
    psi_match: boolean
  }
  drift: {
    score: number
    mode: string
  }
  system: {
    node: string
    model: string
    ollama_url: string
    uptime_s: number
  }
  permissions: {
    write: boolean
    execute: boolean
    external: boolean
    memory: string
  }
}

export type SessionSummary = {
  session_id: string
  task: string
  model: string
  depto?: string | null
  status: string
  iteration: number
  created_at: number
  updated_at: number
  final_response?: string | null
  error?: string | null
}

export type CityDepartment = {
  number: number
  slug: string
  name: string
  personaje: string
  ring: string
  directory: string
  tech: string
  context_hint: string
  is_new: boolean
}

export type NamedPathItem = {
  name: string
  path?: string
  host?: string
  port?: number
}

export type CityMap = {
  departments: CityDepartment[]
  watchtowers: NamedPathItem[]
  subsuelo: NamedPathItem[]
  nodes: NamedPathItem[]
}

export type EcosystemStatus = {
  timestamp: string
  sistemas: Record<string, { available?: boolean; loaded?: boolean; running?: boolean; path?: string; hw_path?: string }>
  nodos: Record<string, Record<string, string | number | boolean>>
}

export type HumanTask = {
  task_id: string
  type: string
  question: string
  execution_id: string
  node_id: string
  created_ago_secs: number
  timeout_secs: number
}

export type HumanTasksPayload = {
  pending_count: number
  tasks: HumanTask[]
  stats: {
    total: number
    by_state: Record<string, number>
    by_type: Record<string, number>
  }
}

export type AgentState = 'working' | 'idle' | 'blocked'

export type AnthillAgent = {
  id: string
  name: string
  role: string
  state: AgentState
  last_activity: string
  task: string
}

export type AgentsStateResponse = {
  ok: boolean
  agents: AnthillAgent[]
}

export type AttachmentAsset = {
  id: string
  name: string
  kind: string
  mime: string
  size: number
  text_excerpt: string
  preview_url: string
  temp_path: string
}

export type Executeresponse = {
  ok: boolean
  session_id: string
  status: string
  final_response?: string | null
  error?: string | null
}

export type StreamPacket = {
  event_id: number
  event_type: string
  session_id: string
  payload?: Record<string, unknown>
  created_at?: number
}

export type VoiceStatus = {
  ok: boolean
  running?: boolean
  listening?: boolean
  processing?: boolean
  wake_word_active?: boolean
  last_command?: string
  last_response?: string
  commands_total?: number
  errors_total?: number
  started_at?: string | null
  model_loaded?: boolean
  current_mode?: string
  whisper_available?: boolean
  edge_tts_available?: boolean
  wake_words?: string[]
  sample_rate?: number
  silence_threshold?: number
  status?: string
}

export type CameraStatus = {
  ok: boolean
  opencv_available?: boolean
  vision_model?: string | null
  pc_camera?: boolean
  oppo_camera?: boolean
  oppo_webcam_available?: boolean | string
  last_frame_ts?: string | null
  last_description?: string
  frames_captured?: number
  analysis_enabled?: boolean
  oppo_ip?: string
  ipwebcam_url?: string
  note_install_ipwebcam?: string
  status?: string
}

export type CameraDescriberesponse = {
  ok: boolean
  source?: string
  description?: string
  ts?: string
  error?: string
}

export type ModuleId =
  | 'voice_local'
  | 'voice_duplex'
  | 'camera_pc'
  | 'camera_oppo'
  | 'screen_hub'
  | 'oppo_bridge'
  | 'oppo_root'
  | 'skill_sentinel'
  | 'sentinel_lab'

export type ModuleState = {
  enabled: boolean
  available: boolean
  status: string
  reason?: string
  last_heartbeat?: string
  dependencies?: string[]
  label?: string
}

export type ModulesStatusresponse = {
  ok: boolean
  voice_backend: VoiceBackendId
  oppo_mode: OppoMode
  modules: Partial<Record<ModuleId, ModuleState>>
}

export type VoiceBackendId = 'local' | 'personaplex_remote' | 'nemotron_remote'

export type VoiceBackendEntry = {
  id: VoiceBackendId
  configured: boolean
  available: boolean
  reason?: string
  endpoint?: string
  requires_gpu?: boolean
  early_access?: boolean
}

export type VoiceBackendsresponse = {
  ok: boolean
  selected_backend: VoiceBackendId
  effective_backend: VoiceBackendId
  fallback_reason?: string
  backends: Partial<Record<VoiceBackendId, VoiceBackendEntry>>
}

export type VoiceDuplexStatus = {
  ok: boolean
  selected_backend: VoiceBackendId
  effective_backend: VoiceBackendId
  fallback_reason?: string
  available: boolean
  configured: boolean
  requires_gpu: boolean
}

export type OppoMode = 'sync' | 'rooted'

export type OppoStatus = {
  ok: boolean
  mode: OppoMode
  adb_online: boolean
  device?: string
  sensor_server_state?: string
  sensor_server_url?: string
  screen_hub_online?: boolean
  root_script_available?: boolean
  root_ready?: boolean
  last_sensor_ts?: string | number | null
}

export type SensoryFeed = {
  ok: boolean
  audio: {
    active_source: string
    backend: VoiceBackendId
    running: boolean
    listening: boolean
    last_transcription: string
    last_response: string
    status: string
  }
  vision: {
    active_source: string
    pc_camera: boolean
    oppo_camera: boolean
    screen_hub: string
    last_frame_ts?: string | null
    last_description: string
    frames_captured: number
  }
  oppo: {
    mode: OppoMode
    adb_online: boolean
    sensor_server: string
    screen_hub_linked: boolean
    device?: string
    last_sensor_ts?: string | number | null
  }
  active_sources: {
    audio: string
    vision: string
  }
  events: Array<{
    type: string
    value: string
    ts: string
  }>
  modules: Partial<Record<ModuleId, ModuleState>>
  ts: string
}

export type RadiocinemaStatus = {
  ok: boolean
  studio?: Record<string, unknown>
  active_job?: Record<string, unknown>
  recent_jobs?: Array<Record<string, unknown>>
  status?: string
  error?: string
}

export type RadiocinemaGenerateresponse = {
  ok: boolean
  job?: Record<string, unknown>
  error?: string
}

export type RadiocinemaLogresponse = {
  ok: boolean
  log?: Array<Record<string, unknown>>
  error?: string
}

const API_BASE = (import.meta.env.VITE_CLAUDIO_API_URL || 'http://127.0.0.1:47047').replace(/\/$/, '')

type ApiFetchOptions = RequestInit & {
  timeoutMs?: number
}

async function apiFetch<T>(path: string, init?: ApiFetchOptions): Promise<T> {
  const { timeoutMs = 8000, ...requestInit } = init || {}
  const controller = new AbortController()
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs)

  try {
    const response = await fetch(`${API_BASE}${path}`, {
      ...requestInit,
      signal: controller.signal
    })

    if (!response.ok) {
      const text = await response.text()
      throw new Error(text || `HTTP ${response.status}`)
    }

    return response.json() as Promise<T>
  } catch (error) {
    if (error instanceof DOMException && error.name === 'AbortError') {
      throw new Error(`Tiempo de espera agotado para ${path}`)
    }
    throw error
  } finally {
    window.clearTimeout(timeoutId)
  }
}

function jsonHeaders(): Record<string, string> {
  return {
    'Content-Type': 'application/json'
  }
}

export function getAchicase(): string {
  return API_BASE
}

export async function getServerStatus(): Promise<ServerStatus> {
  return apiFetch<ServerStatus>('/api/status', {
    timeoutMs: 2000
  })
}

export async function getAgentsState(): Promise<AnthillAgent[]> {
  const data = await apiFetch<AgentsStateResponse>('/api/agents/state', {
    timeoutMs: 3000
  })
  return data.agents || []
}

export async function getBuddyStatus(): Promise<BuddyStatus> {
  const data = await apiFetch<{ ok: boolean; buddy: BuddyStatus }>('/api/buddy/status')
  return data.buddy
}

export async function getEcosystemStatus(): Promise<EcosystemStatus> {
  const data = await apiFetch<EcosystemStatus & { ok: boolean }>('/api/ecosistema/status', {
    timeoutMs: 3000
  })
  return data
}

export async function getCityMap(): Promise<CityMap> {
  const data = await apiFetch<{ ok: boolean } & CityMap>('/api/ciudad/map')
  return {
    departments: data.departments,
    watchtowers: data.watchtowers,
    subsuelo: data.subsuelo,
    nodes: data.nodes
  }
}

export async function getAgentSessions(): Promise<SessionSummary[]> {
  const data = await apiFetch<{ ok: boolean; sessions: SessionSummary[] }>('/api/agent/sessions')
  return data.sessions
}

export async function getHumanTasks(): Promise<HumanTasksPayload> {
  const data = await apiFetch<{ ok: boolean; data: HumanTasksPayload }>('/api/tasks/human')
  return data.data
}

export async function respondHumanTask(taskId: string, answer: string): Promise<void> {
  await apiFetch('/api/tasks/human/respond', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({
      task_id: taskId,
      answer
    })
  })
}

export async function getVoiceStatus(): Promise<VoiceStatus> {
  return apiFetch<VoiceStatus>('/api/voice/status', {
    timeoutMs: 2500
  })
}

export async function getVoiceBackends(): Promise<VoiceBackendsresponse> {
  return apiFetch<VoiceBackendsresponse>('/api/voice/backends', {
    timeoutMs: 2500
  })
}

export async function setVoiceBackend(backend: VoiceBackendId): Promise<VoiceBackendsresponse> {
  return apiFetch<VoiceBackendsresponse>('/api/voice/backend', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({ backend }),
    timeoutMs: 4000
  })
}

export async function getVoiceDuplexStatus(): Promise<VoiceDuplexStatus> {
  return apiFetch<VoiceDuplexStatus>('/api/voice/duplex/status', {
    timeoutMs: 2500
  })
}

export async function startVoiceDaemon(input?: { model?: string; always_on?: boolean }): Promise<VoiceStatus> {
  return apiFetch<VoiceStatus>('/api/voice/start', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({
      model: input?.model || 'small',
      always_on: Boolean(input?.always_on)
    })
  })
}

export async function stopVoiceDaemon(): Promise<VoiceStatus> {
  return apiFetch<VoiceStatus>('/api/voice/stop', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({})
  })
}

export async function speakText(text: string, voice = 'es-MX-JorgeNeural'): Promise<VoiceStatus> {
  return apiFetch<VoiceStatus>('/api/voice/speak', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({
      text,
      voice
    }),
    timeoutMs: 5000
  })
}

export async function getCameraStatus(): Promise<CameraStatus> {
  return apiFetch<CameraStatus>('/api/camera/status', {
    timeoutMs: 3000
  })
}

export async function getModulesStatus(): Promise<ModulesStatusresponse> {
  return apiFetch<ModulesStatusresponse>('/api/modules/status', {
    timeoutMs: 3000
  })
}

export async function setModuleState(moduleId: ModuleId, enabled: boolean): Promise<ModulesStatusresponse> {
  return apiFetch<ModulesStatusresponse>('/api/modules/set', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({
      module_id: moduleId,
      enabled
    }),
    timeoutMs: 5000
  })
}

export async function getSensoryFeed(): Promise<SensoryFeed> {
  return apiFetch<SensoryFeed>('/api/sensory/feed', {
    timeoutMs: 3000
  })
}

export async function getOppoStatus(): Promise<OppoStatus> {
  return apiFetch<OppoStatus>('/api/oppo/status', {
    timeoutMs: 2500
  })
}

export async function setOppoMode(mode: OppoMode): Promise<OppoStatus> {
  return apiFetch<OppoStatus>('/api/oppo/mode', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({ mode }),
    timeoutMs: 4000
  })
}

export function getCameraSnapshotImageUrl(source = 'auto'): string {
  return `${API_BASE}/api/camera/snapshot/image?source=${encodeURIComponent(source)}`
}

export const HUB_BASE = 'http://127.0.0.1:7474'

export type HubDevice = {
  id: string
  name: string
  type: string
  platform: string
  online?: boolean
  ip?: string
  note?: string
}

export type HubDevicesresponse = Record<string, HubDevice>

// Mapea nuestra fuente logica de Vision al device_id del Screen Hub.
export function hubDeviceIdForSource(source: string): string {
  switch (source) {
    case 'pc':
    case 'auto':
      return 'laptop'
    case 'oppo_adb':
    case 'oppo_webcam':
      return 'oppo'
    case 'pc2':
      return 'pc2'
    case 'tv':
      return 'tv'
    default:
      return 'laptop'
  }
}

export function getHubStreamUrl(source: string): string {
  return `${HUB_BASE}/stream/${hubDeviceIdForSource(source)}`
}

export function getHubSnapshotUrl(source: string): string {
  return `${HUB_BASE}/snapshot/${hubDeviceIdForSource(source)}`
}

export async function getHubDevices(): Promise<HubDevicesresponse | null> {
  try {
    const controller = new AbortController()
    const timer = setTimeout(() => controller.abort(), 2500)
    const response = await fetch(`${HUB_BASE}/devices`, { signal: controller.signal })
    clearTimeout(timer)
    if (!response.ok) return null
    return (await response.json()) as HubDevicesresponse
  } catch {
    return null
  }
}

export async function startCameraStream(input?: { source?: string; interval?: number; analyze?: boolean }): Promise<{ ok: boolean; msg?: string; error?: string }> {
  return apiFetch('/api/camera/stream/start', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({
      source: input?.source || 'auto',
      interval: input?.interval ?? 3,
      analyze: Boolean(input?.analyze)
    }),
    timeoutMs: 5000
  })
}

export async function stopCameraStream(): Promise<{ ok: boolean; msg?: string; error?: string }> {
  return apiFetch('/api/camera/stream/stop', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({})
  })
}

export async function describeCamera(input?: { source?: string; prompt?: string }): Promise<CameraDescriberesponse> {
  return apiFetch<CameraDescriberesponse>('/api/camera/describe', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({
      source: input?.source || 'auto',
      prompt: input?.prompt || 'Describe la escena y detecta riesgos, personas y objetos importantes.'
    }),
    timeoutMs: 30000
  })
}

export async function getRadiocinemaStatus(): Promise<RadiocinemaStatus> {
  return apiFetch<RadiocinemaStatus>('/api/radiocinema/status', {
    timeoutMs: 4000
  })
}

export async function generateRadiocinema(input: { book: string; chapter?: string; style?: string }): Promise<RadiocinemaGenerateresponse> {
  return apiFetch<RadiocinemaGenerateresponse>('/api/radiocinema/generate', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({
      book: input.book,
      chapter: input.chapter || '',
      style: input.style || 'binaural'
    }),
    timeoutMs: 8000
  })
}

export async function getRadiocinemaLog(limit = 12): Promise<RadiocinemaLogresponse> {
  return apiFetch<RadiocinemaLogresponse>(`/api/radiocinema/log?n=${limit}`, {
    timeoutMs: 4000
  })
}

export type RadiocinemaTool = {
  id: string
  label: string
  category: string
  description: string
  available: boolean
  path: string | null
  status?: string
  launch_mode?: string | null
  repo_path?: string | null
  repo_exists?: boolean
  node_modules_ready?: boolean
  submodules_ready?: boolean
  dist_ready?: boolean
  preview_entry?: string | null
  default_url?: string | null
}

export type RadiocinemaToolsresponse = {
  ok: boolean
  total?: number
  available?: number
  tools?: RadiocinemaTool[]
  error?: string
  timestamp?: number
}

export type RadiocinemaLaunchresponse = {
  ok: boolean
  tool_id?: string
  label?: string
  path?: string
  pid?: number
  args?: string[]
  launch_mode?: string
  npm_script?: string
  cwd?: string
  url?: string | null
  error?: string
}

export async function getRadiocinemaTools(): Promise<RadiocinemaToolsresponse> {
  return apiFetch<RadiocinemaToolsresponse>('/api/radiocinema/tools', {
    timeoutMs: 5000
  })
}

export async function launchRadiocinemaTool(toolId: string, args: string[] = []): Promise<RadiocinemaLaunchresponse> {
  return apiFetch<RadiocinemaLaunchresponse>('/api/radiocinema/launch', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({ tool_id: toolId, args }),
    timeoutMs: 6000
  })
}

export async function uploadAttachments(files: File[]): Promise<AttachmentAsset[]> {
  const formData = new FormData()
  files.forEach((file) => {
    formData.append('files', file)
  })

  const response = await fetch(`${API_BASE}/api/ui/attachments`, {
    method: 'POST',
    body: formData
  })

  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || `HTTP ${response.status}`)
  }

  const payload = (await response.json()) as { ok: boolean; assets: AttachmentAsset[] }
  return payload.assets.map((asset) => ({
    ...asset,
    preview_url: new URL(asset.preview_url, API_BASE).toString()
  }))
}

export async function executeAgent(input: {
  task: string
  model: string
  depto?: string
  attachment_ids?: string[]
}): Promise<Executeresponse> {
  return apiFetch<Executeresponse>('/api/agent/execute', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({
      task: input.task,
      model: input.model,
      depto: input.depto,
      attachment_ids: input.attachment_ids || [],
      auto_approve: false,
      max_iters: 15
    }),
    timeoutMs: 15000
  })
}

export async function approveToolCall(sessionId: string, toolCallId: string, approved: boolean): Promise<void> {
  await apiFetch('/api/agent/approve', {
    method: 'POST',
    headers: jsonHeaders(),
    body: JSON.stringify({
      session_id: sessionId,
      tool_call_id: toolCallId,
      approved
    })
  })
}

export function streamAgentSession(
  sessionId: string,
  onPacket: (packet: StreamPacket) => void,
  aftereventId = 0
): () => void {
  const source = new EventSource(`${API_BASE}/api/agent/stream/${sessionId}?after=${aftereventId}`)
  source.onmessage = (event) => {
    const payload = JSON.parse(event.data) as StreamPacket
    onPacket(payload)
    if (payload.event_type === 'done') {
      source.close()
    }
  }
  source.onerror = () => {
    source.close()
  }

  return () => {
    source.close()
  }
}
