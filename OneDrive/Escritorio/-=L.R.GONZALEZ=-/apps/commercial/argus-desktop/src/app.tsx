import CodeMirror from '@uiw/react-codemirror'
import { javascript } from '@codemirror/lang-javascript'
import { python } from '@codemirror/lang-python'
import {
  startTransition,
  type KeyboardEvent,
  useEffect,
  useEffectEvent,
  useRef,
  useState
} from 'react'
import Markdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import SimpleHomeView from './components/SimpleHomeView'
import {
  approveToolCall,
  describeCamera,
  executeAgent,
  generateRadiocinema,
  getAgentsState,
  getAgentSessions,
  getAchicase,
  getBuddyStatus,
  getCameraSnapshotImageUrl,
  getCameraStatus,
  getCityMap,
  getEcosystemStatus,
  getHubDevices,
  getHubStreamUrl,
  getHumanTasks,
  getModulesStatus,
  getOppoStatus,
  getRadiocinemaLog,
  getRadiocinemaStatus,
  getRadiocinemaTools,
  getSensoryFeed,
  getServerStatus,
  getVoiceBackends,
  getVoiceStatus,
  hubDeviceIdForSource,
  launchRadiocinemaTool,
  respondHumanTask,
  setModuleState,
  setOppoMode,
  setVoiceBackend,
  speakText,
  startCameraStream,
  startVoiceDaemon,
  stopCameraStream,
  stopVoiceDaemon,
  streamAgentSession,
  uploadAttachments,
  type AnthillAgent,
  type AttachmentAsset,
  type BuddyStatus,
  type CameraStatus,
  type CityDepartment,
  type CityMap,
  type EcosystemStatus,
  type HubDevicesresponse,
  type HumanTask,
  type ModuleId,
  type ModulesStatusresponse,
  type OppoMode,
  type OppoStatus,
  type RadiocinemaStatus,
  type RadiocinemaTool,
  type SensoryFeed,
  type ServerStatus,
  type SessionSummary,
  type StreamPacket,
  type VoiceBackendId,
  type VoiceBackendsresponse,
  type VoiceStatus
} from './lib/api'

type Message = {
  id: string
  role: 'system' | 'user' | 'assistant'
  content: string
  meta?: string
}

type AgentFeedEntry = {
  id: string
  tone: 'neutral' | 'success' | 'danger' | 'accent'
  label: string
  detail: string
}

type PendingApproval = {
  toolCallId: string
  tool: string
  args: string
}

type ArtifactDraft = {
  language: string
  title: string
  code: string
}

type UserProfileId = 'average' | 'nonTechnical' | 'creative' | 'glitch'
type NavSectionId = 'history' | 'radiocinema' | 'tools' | 'settings'
type RightViewId = 'hud' | 'city' | 'vision' | 'studio' | 'canvas' | 'terchical' | 'evidence' | 'anthill'
type ConnectionState = 'connecting' | 'connected' | 'slow' | 'offline'
type TerchicalShellId = 'pwsh' | 'powershell' | 'cmd'

type PromptCard = {
  id: string
  label: string
  prompt: string
  detail: string
  sections?: NavSectionId[]
}

type DesktopLogEntry = {
  id: string
  tone: 'neutral' | 'success' | 'danger' | 'accent'
  label: string
  detail: string
}

type DesktopApproval = {
  action: string
  payload: Record<string, unknown>
  gate: NonNullable<DesktopInvokeresponse['gate']>
}

type LiveVisionState = {
  enabled: boolean
  source: 'auto' | 'pc' | 'oppo_adb' | 'oppo_webcam'
  intervalMs: number
  autoDescribe: boolean
  lastDescription: string
  lastUpdated: string
}

type SidebarShortcut =
  | {
      id: string
      label: string
      detail: string
      kind: 'nav'
      section: NavSectionId
      view?: RightViewId
    }
  | {
      id: string
      label: string
      detail: string
      kind: 'prompt'
      prompt: string
    }
  | {
      id: string
      label: string
      detail: string
      kind: 'command'
      command: string
    }
  | {
      id: string
      label: string
      detail: string
      kind: 'open'
      path: string
      commandId?: string
    }

const MODEL_OPTIONS = [
  { value: 'gemma4:e4b', label: 'Gemma 4 e4b' },
  { value: 'qwen2.5-coder:3b', label: 'Qwen 2.5 Coder 3b' },
  { value: 'codex-bridge', label: 'Codex bridge' }
]

const PROFILE_CONFIG: Record<UserProfileId, {
  label: string
  short: string
  description: string
  chatPlaceholder: string
  helper: string
}> = {
  average: {
    label: 'Promedio',
    short: 'Diario',
    description: 'Chat calido, botones claros y acceso a juegos, prompts y ciudad.',
    chatPlaceholder: 'Pide una idea, una imagen, una historia o un juego con Argus.',
    helper: 'Perfil simple para chatear, jugar y crear sin ruido.'
  },
  nonTechnical: {
    label: 'No técnico',
    short: 'Calma',
    description: 'Tipografía grande, ayuda hablada, menos opciones y chat siempre visible.',
    chatPlaceholder: 'Habla o escribe lo que necesitas. Argus te guía paso a paso.',
    helper: 'Diseñado para niños, personas mayores y usuarios con baja tolerancia a la complejidad.'
  },
  creative: {
    label: 'Creativo',
    short: 'Diseño',
    description: 'Radiocinema, canvas, proyectos y revisión observacionista.',
    chatPlaceholder: 'Describe tu proyecto. Argus puede ayudarte a producir, revisar y exportar.',
    helper: 'Studio abierto para prompts, artefactos y producción multimedia.'
  },
  glitch: {
    label: 'Glitch',
    short: 'Glitch',
    description: 'Modo avanzado con terminal, archivos, API y evidencias.',
    chatPlaceholder: 'Pide código, diagnósticos, automatización o una operación del sistema.',
    helper: 'Usa /ps7, /nemo, /cw o /libros. Las acciones peligrosas pasan por gate PSI y aprobación humana.'
  }
}

const NAV_ITEMS: Array<{
  id: NavSectionId
  label: string
  detail: string
}> = [
  { id: 'history', label: 'Historial', detail: 'Conversaciones y sesiones' },
  { id: 'radiocinema', label: 'Radiocinema', detail: 'Studio, clips y minijuegos' },
  { id: 'tools', label: 'Herramientas', detail: 'Ciudad, generadores y utilidades' },
  { id: 'settings', label: 'Configuración', detail: 'Conexión, voz y accesibilidad' }
]

const PROMPTS: Record<UserProfileId, PromptCard[]> = {
  average: [
    {
      id: 'avg-1',
      label: 'Charla libre',
      prompt: 'Argus, quiero platicar contigo de forma tranquila y humana.',
      detail: 'Conversación simple y cálida',
      sections: ['history']
    },
    {
      id: 'avg-2',
      label: 'Imagen con prompt',
      prompt: 'Ayúdame a escribir un prompt corto para generar una imagen cinematográfica.',
      detail: 'Generación guiada por texto',
      sections: ['tools', 'radiocinema']
    },
    {
      id: 'avg-3',
      label: 'Minijuego',
      prompt: 'Juguemos una trivia corta de MEDIOEVO con tres rondas.',
      detail: 'Juego conversacional',
      sections: ['radiocinema', 'tools']
    }
  ],
  nonTechnical: [
    {
      id: 'nt-1',
      label: 'Ayúdame',
      prompt: 'Explícame lo que está pasando con palabras fáciles y dame solo un paso a la vez.',
      detail: 'Asistencia clara',
      sections: ['history', 'settings']
    },
    {
      id: 'nt-2',
      label: 'Cuéntame algo',
      prompt: 'Cuéntame una historia breve, amable y fácil de seguir.',
      detail: 'relato sencillo',
      sections: ['history']
    },
    {
      id: 'nt-3',
      label: 'Jugar con Argus',
      prompt: 'Argus, juguemos memoria 47 con instrucciones fáciles.',
      detail: 'Juego guiado',
      sections: ['tools', 'radiocinema']
    }
  ],
  creative: [
    {
      id: 'cr-1',
      label: 'Pitch visual',
      prompt: 'Crea un brief visual para un proyecto medioevo sci-fi con referencias de color, encuadre y atmósfera.',
      detail: 'Dirección de arte',
      sections: ['radiocinema', 'tools']
    },
    {
      id: 'cr-2',
      label: 'Storyboard',
      prompt: 'Construye un storyboard breve para una escena nocturna en la ciudad de MEDIOEVO.',
      detail: 'Preproducción',
      sections: ['radiocinema']
    },
    {
      id: 'cr-3',
      label: 'Proyecto',
      prompt: 'Ayúdame a definir un proyecto creativo con entregables, riesgos y paeres de producción.',
      detail: 'Planeación',
      sections: ['history', 'tools']
    }
  ],
  glitch: [
    {
      id: 'gl-1',
      label: 'Analiza carpeta',
      prompt: 'Analiza esta base de código y dime los riesgos, el flujo principal y los siguientes cambios.',
      detail: 'Auditoría técnica',
      sections: ['history', 'tools']
    },
    {
      id: 'gl-2',
      label: 'Script nuevo',
      prompt: 'Crea un script nuevo con enfoque seguro y explica cómo verificarlo.',
      detail: 'Programación guiada',
      sections: ['history']
    },
    {
      id: 'gl-3',
      label: 'API y redes',
      prompt: 'Dame un plan técnico para conectar esta app con servicios locales y APIs externas sin perder control PSI.',
      detail: 'Infraestructura',
      sections: ['tools', 'settings']
    }
  ]
}

const MINI_GAMES: Array<{
  label: string
  prompt: string
  detail: string
}> = [
  {
    label: 'Memoria 47',
    prompt: 'Argus, dirige un juego de memoria 47 con dificultad media y una ronda final sorpresa.',
    detail: 'Memoria rápida y patrón'
  },
  {
    label: 'Trivia Argus',
    prompt: 'Argus, hagamos una trivia corta de ciencia ficción y observacionismo con puntaje.',
    detail: 'Preguntas y respuestas'
  },
  {
    label: 'Historia guiada',
    prompt: 'Argus, construye una aventura guiada dentro de la ciudad de MEDIOEVO estilo RPG conversacional.',
    detail: 'Narrativa interactiva'
  }
]

const LIBRARY_LABEL = 'Biblioteca Medioevo'
const LIBRARY_TARGET = 'E:\\-=Medioevo=-\\-=Libros'
const LIBRARY_SHORTCUT = 'C:\\Users\\L-Tyr\\OneDrive\\Escritorio\\-=L.R.GONZALEZ=-\\CLAUDIO - researchs\\-=Libros - Shortcut.lnk'

const WELCOME_MESSAGE = `Bienvenido a Argus.

- Inicio simple: Hablar, Ver, Escribir y Ayuda.
- Modo técnico: ciudad, terminal, evidencias y paneles avanzados.
- El companion oculta el stack técnico para que la experiencia siga simple.

Puedes decir "modo técnico" o "modo glitch" cuando quieras entrar al panel avanzado.`

export default function App() {
  const [serverStatus, setServerStatus] = useState<ServerStatus | null>(null)
  const [buddy, setBuddy] = useState<BuddyStatus | null>(null)
  const [ecosystem, setEcosystem] = useState<EcosystemStatus | null>(null)
  const [cityMap, setCityMap] = useState<CityMap | null>(null)
  const [sessions, setSessions] = useState<SessionSummary[]>([])
  const [humanTasks, setHumanTasks] = useState<HumanTask[]>([])
  const [anthillAgents, setAnthillAgents] = useState<AnthillAgent[]>([])
  const [voiceStatus, setVoiceStatus] = useState<VoiceStatus | null>(null)
  const [cameraStatus, setCameraStatus] = useState<CameraStatus | null>(null)
  const [modulesStatus, setModulesStatus] = useState<ModulesStatusresponse | null>(null)
  const [voiceBackends, setVoiceBackends] = useState<VoiceBackendsresponse | null>(null)
  const [oppoStatus, setOppoStatus] = useState<OppoStatus | null>(null)
  const [sensoryFeed, setSensoryFeed] = useState<SensoryFeed | null>(null)
  const [radiocinemaStatus, setRadiocinemaStatus] = useState<RadiocinemaStatus | null>(null)
  const [hubDevices, setHubDevices] = useState<HubDevicesresponse | null>(null)
  const [radiocinemaTools, setRadiocinemaTools] = useState<RadiocinemaTool[]>([])
  const [launchingTool, setLaunchingTool] = useState<string | null>(null)
  const [radiocinemaLog, setRadiocinemaLog] = useState<Array<Record<string, unknown>>>([])

  const [messages, setMessages] = useState<Message[]>([
    { id: crypto.randomUUID(), role: 'system', content: WELCOME_MESSAGE }
  ])
  const [agentFeed, setAgentFeed] = useState<AgentFeedEntry[]>([
    {
      id: crypto.randomUUID(),
      tone: 'accent',
      label: 'FCU activo',
      detail: 'Argus integra perfiles humanos, ciudad, visión y runtime local sobre 127.0.0.1:47047.'
    }
  ])
  const [desktopFeed, setDesktopFeed] = useState<DesktopLogEntry[]>([])

  const [profile, setProfile] = useState<UserProfileId>('nonTechnical')
  const [activeNav, setActiveNav] = useState<NavSectionId>('history')
  const [rightMode, setRightMode] = useState<RightViewId>('hud')
  const [connectionState, setConnectionState] = useState<ConnectionState>('connecting')
  const [connectionMessage, setConnectionMessage] = useState('Conectando con Argus')

  const [input, setInput] = useState('')
  const [selectedModel, setSelectedModel] = useState('gemma4:e4b')
  const [selectedDepto, setSelectedDepto] = useState('')
  const [attachments, setAttachments] = useState<AttachmentAsset[]>([])
  const [artifact, setArtifact] = useState<ArtifactDraft | null>(null)

  const [leftCollapsed, setLeftCollapsed] = useState(false)
  const [rightCollapsed, setRightCollapsed] = useState(false)
  const [leftDrawerOpen, setLeftDrawerOpen] = useState(false)
  const [rightDrawerOpen, setRightDrawerOpen] = useState(false)

  const [isSending, setIsSending] = useState(false)
  const [streamState, setStreamState] = useState('Listo')
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null)
  const [pendingApproval, setPendingApproval] = useState<PendingApproval | null>(null)
  const [taskAnswers, setTaskAnswers] = useState<Record<string, string>>({})
  const [desktopApproval, setDesktopApproval] = useState<DesktopApproval | null>(null)

  const [manualVoiceDaemon, setManualVoiceDaemon] = useState(false)
  const [voiceCommandsEnabled, setVoiceCommandsEnabled] = useState(false)
  const [voiceTranscript, setVoiceTranscript] = useState('')
  const [voiceCommandsState, setVoiceCommandsState] = useState({
    supported: false,
    listening: false,
    error: ''
  })

  const [liveVision, setLiveVision] = useState<LiveVisionState>({
    enabled: false,
    source: 'auto',
    intervalMs: 3200,
    autoDescribe: true,
    lastDescription: '',
    lastUpdated: ''
  })
  const [visionBusy, setVisionBusy] = useState(false)
  const [visionImageNonce, setVisionImageNonce] = useState(Date.now())

  const [studioPrompt, setStudioPrompt] = useState('')
  const [studioDetail, setStudioDetail] = useState('')
  const [studioStyle, setStudioStyle] = useState('binaural')
  const [isGeneratingStudio, setIsGeneratingStudio] = useState(false)

  const [terchicalShell, setTerchicalShell] = useState<TerchicalShellId>('pwsh')
  const [terchicalCommand, setTerchicalCommand] = useState('Get-ChildItem')
  const [terchicalOutput, setTerchicalOutput] = useState('La terminal Glitch aparecerá aquí. Las acciones con riesgo pedirán confirmación.')
  const [glitchFilePath, setGlitchFilePath] = useState('')
  const [glitchFileDraft, setGlitchFileDraft] = useState('')
  const [glitchFileStatus, setGlitchFileStatus] = useState('Sin archivo cargado')

  const [showJumpToBottom, setShowJumpToBottom] = useState(false)

  const streamCleanupref = useRef<(() => void) | null>(null)
  const typingTimerref = useRef<number | null>(null)
  const lastEventIdref = useRef(0)
  const activeAssistantMessageref = useRef<string | null>(null)
  const fileInputref = useRef<HTMLInputElement | null>(null)
  const messageViewportref = useRef<HTMLDivElement | null>(null)
  const recognitionref = useRef<Speechrecognition | null>(null)
  const shouldrestartVoiceref = useRef(false)
  const autoPinnedref = useRef(true)
  const lastAnnouncementref = useRef<{ text: string; at: number }>({ text: '', at: 0 })
  const voiceDaemonBusyref = useRef(false)
  const cameraStopLockref = useRef(false)

  const desktopAvailable = Boolean(window.claudioDesktop?.available)
  const selectedDepartment =
    cityMap?.departments.find((department) => department.slug === selectedDepto) ||
    cityMap?.departments[0] ||
    null
  const observacionismoState = getObservacionismoState(buddy)
  const desktopGridTemplate = `${leftCollapsed ? '96px' : '328px'} minmax(0, 1fr) ${rightCollapsed ? '96px' : '416px'}`
  const promptDeck = PROMPTS[profile].filter((card) => !card.sections || card.sections.includes(activeNav))
  const sidebarShortcuts = getSidebarShortcuts(profile)
  const composerPlaceholder = PROFILE_CONFIG[profile].chatPlaceholder
  const profileCopy = PROFILE_CONFIG[profile]
  const quickPsiLabel = getPsiSummary(profile, buddy)
  const rightTabs = getRightTabs(profile)
  const selectedRightMode = rightTabs.find((tab) => tab.id === rightMode)?.id || rightTabs[0].id
  const visionImageUrl = getCameraSnapshotImageUrl(liveVision.source)
  const voiceModuleEnabled = modulesStatus?.modules?.voice_local?.enabled ?? true
  const cameraModuleEnabled = modulesStatus?.modules?.camera_pc?.enabled ?? true

  const closeStream = useEffectEvent(() => {
    if (streamCleanupref.current) {
      streamCleanupref.current()
      streamCleanupref.current = null
    }
  })

  const stopTyping = useEffectEvent(() => {
    if (typingTimerref.current !== null) {
      window.clearInterval(typingTimerref.current)
      typingTimerref.current = null
    }
  })

  const pushAgentFeed = useEffectEvent((entry: AgentFeedEntry) => {
    startTransition(() => {
      setAgentFeed((current) => [entry, ...current].slice(0, 24))
    })
  })

  const pushDesktopFeed = useEffectEvent((entry: DesktopLogEntry) => {
    startTransition(() => {
      setDesktopFeed((current) => [entry, ...current].slice(0, 20))
    })
  })

  const scrollToBottom = useEffectEvent((behavior: ScrollBehavior = 'smooth') => {
    const viewport = messageViewportref.current
    if (!viewport) {
      return
    }
    viewport.scrollTo({
      top: viewport.scrollHeight,
      behavior
    })
    autoPinnedref.current = true
    setShowJumpToBottom(false)
  })

  const syncScrollState = useEffectEvent(() => {
    const viewport = messageViewportref.current
    if (!viewport) {
      return
    }
    const pinned = viewport.scrollHeight - viewport.scrollTop - viewport.clientHeight < 96
    autoPinnedref.current = pinned
    setShowJumpToBottom(!pinned)
  })

  const announce = useEffectEvent(async (text: string) => {
    const normalized = text.trim()
    if (!normalized) {
      return
    }
    const now = Date.now()
    if (lastAnnouncementref.current.text === normalized && now - lastAnnouncementref.current.at < 4000) {
      return
    }
    lastAnnouncementref.current = { text: normalized, at: now }
    try {
      await speakText(normalized)
    } catch {
      if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel()
        window.speechSynthesis.speak(new SpeechSynthesisUtterance(normalized))
      }
    }
  })

  const handleComposerKeyDown = useEffectEvent((event: KeyboardEvent<HTMLTextAreaElement>) => {
    if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
      event.preventDefault()
      void handleSubmit()
    }
  })

  const handleToggleModule = useEffectEvent(async (moduleId: ModuleId) => {
    const enabled = Boolean(modulesStatus?.modules?.[moduleId]?.enabled)
    try {
      const next = await setModuleState(moduleId, !enabled)
      setModulesStatus(next)

      if (moduleId === 'camera_pc' && enabled) {
        setLiveVision((current) => ({ ...current, enabled: false }))
      }
      if (moduleId === 'camera_pc' && !enabled) {
        setLiveVision((current) => ({ ...current, enabled: true, source: 'pc' }))
      }
      if (moduleId === 'oppo_bridge' && !enabled) {
        setLiveVision((current) => ({ ...current, source: 'oppo_adb' }))
      }

      void refreshTelemetry()
    } catch (error) {
      pushAgentFeed({
        id: crypto.randomUUID(),
        tone: 'danger',
        label: 'Módulos',
        detail: error instanceof Error ? error.message : 'No se pudo cambiar el módulo.'
      })
    }
  })

  const handleSetVoiceBackend = useEffectEvent(async (backend: VoiceBackendId) => {
    try {
      const next = await setVoiceBackend(backend)
      setVoiceBackends(next)
      void refreshTelemetry()
    } catch (error) {
      pushAgentFeed({
        id: crypto.randomUUID(),
        tone: 'danger',
        label: 'Voz remota',
        detail: error instanceof Error ? error.message : 'No se pudo cambiar el backend de voz.'
      })
    }
  })

  const handleSetOppoMode = useEffectEvent(async (mode: OppoMode) => {
    try {
      const next = await setOppoMode(mode)
      setOppoStatus(next)
      void refreshTelemetry()
    } catch (error) {
      pushAgentFeed({
        id: crypto.randomUUID(),
        tone: 'danger',
        label: 'OPPO',
        detail: error instanceof Error ? error.message : 'No se pudo cambiar el modo OPPO.'
      })
    }
  })

  const openWriterWorkbench = useEffectEvent(() => {
    window.open(`${getAchicase()}/writer`, '_blank', 'noopener')
  })

  const openSimpleTalk = useEffectEvent(() => {
    if (!voiceModuleEnabled) {
      void handleToggleModule('voice_local')
      return
    }
    void announce('Te escucho.')
  })

  const openSimpleVision = useEffectEvent(() => {
    if (!cameraModuleEnabled) {
      void handleToggleModule('camera_pc')
      return
    }
    setLiveVision((current) => ({ ...current, enabled: true, source: 'pc' }))
  })

  const openSimpleHelp = useEffectEvent(() => {
    void handleSubmit('Explícame con palabras fáciles qué puedo hacer aquí y dame solo un paso a la vez.')
  })

  const openTechnicalMode = useEffectEvent(() => {
    setProfile('glitch')
    setActiveNav('tools')
    setRightMode('terchical')
  })

  const refreshTelemetry = useEffectEvent(async () => {
    const startedAt = performance.now()
    const [
      serverresult,
      buddyresult,
      ecosystemresult,
      cityresult,
      sessionsresult,
      humanTasksresult,
      agentsStateresult,
      voiceresult,
      cameraresult,
      modulesresult,
      voiceBackendsresult,
      opporesult,
      sensoryFeedresult,
      radiocinemaresult,
      radiocinemaLogresult,
      hubDevicesresult,
      radiocinemaToolsresult
    ] = await Promise.allSettled([
      getServerStatus(),
      getBuddyStatus(),
      getEcosystemStatus(),
      getCityMap(),
      getAgentSessions(),
      getHumanTasks(),
      getAgentsState(),
      getVoiceStatus(),
      getCameraStatus(),
      getModulesStatus(),
      getVoiceBackends(),
      getOppoStatus(),
      getSensoryFeed(),
      getRadiocinemaStatus(),
      getRadiocinemaLog(),
      getHubDevices(),
      getRadiocinemaTools()
    ])

    const duration = performance.now() - startedAt

    startTransition(() => {
      if (serverresult.status === 'fulfilled') {
        setServerStatus(serverresult.value)
      }
      if (buddyresult.status === 'fulfilled') {
        setBuddy(buddyresult.value)
      }
      if (ecosystemresult.status === 'fulfilled') {
        setEcosystem(ecosystemresult.value)
      }
      if (cityresult.status === 'fulfilled') {
        setCityMap(cityresult.value)
        if (!selectedDepto && cityresult.value.departments[0]) {
          setSelectedDepto(cityresult.value.departments[0].slug)
        }
      }
      if (sessionsresult.status === 'fulfilled') {
        setSessions(sessionsresult.value)
      }
      if (humanTasksresult.status === 'fulfilled') {
        setHumanTasks(humanTasksresult.value.tasks)
      }
      if (agentsStateresult.status === 'fulfilled') {
        setAnthillAgents(agentsStateresult.value)
      }
      if (voiceresult.status === 'fulfilled') {
        setVoiceStatus(voiceresult.value)
      }
      if (cameraresult.status === 'fulfilled') {
        setCameraStatus(cameraresult.value)
      }
      if (modulesresult.status === 'fulfilled') {
        setModulesStatus(modulesresult.value)
      }
      if (voiceBackendsresult.status === 'fulfilled') {
        setVoiceBackends(voiceBackendsresult.value)
      }
      if (opporesult.status === 'fulfilled') {
        setOppoStatus(opporesult.value)
      }
      if (sensoryFeedresult.status === 'fulfilled') {
        setSensoryFeed(sensoryFeedresult.value)
      }
      if (radiocinemaresult.status === 'fulfilled') {
        setRadiocinemaStatus(radiocinemaresult.value)
      }
      if (radiocinemaLogresult.status === 'fulfilled') {
        setRadiocinemaLog(radiocinemaLogresult.value.log || [])
      }
      if (hubDevicesresult.status === 'fulfilled') {
        setHubDevices(hubDevicesresult.value)
      }
      if (radiocinemaToolsresult.status === 'fulfilled' && radiocinemaToolsresult.value.tools) {
        setRadiocinemaTools(radiocinemaToolsresult.value.tools)
      }
    })

    if (serverresult.status === 'rejected') {
      setConnectionState('offline')
      setConnectionMessage('Servidor sin respuesta en localhost:47047')
      throw new Error('No se pudo contactar la API local.')
    }

    if (
      duration > 3500 ||
      buddyresult.status === 'rejected' ||
      cityresult.status === 'rejected' ||
      sessionsresult.status === 'rejected'
    ) {
      setConnectionState('slow')
      setConnectionMessage('Conexión lenta o parcial. Claudio sigue intentando.')
      return
    }

    setConnectionState('connected')
    setConnectionMessage(`Conectado a ${serverresult.value.local_ip}:${serverresult.value.port}`)
  })

  const hydrateArtifact = useEffectEvent((markdown: string) => {
    const nextArtifact = extractArtifact(markdown)
    if (nextArtifact) {
      setArtifact(nextArtifact)
      setRightMode('canvas')
    }
  })

  const updateAssistantMessage = useEffectEvent((messageId: string, content: string, meta?: string) => {
    setMessages((current) =>
      current.map((message) =>
        message.id === messageId
          ? {
              ...message,
              content,
              meta
            }
          : message
      )
    )
  })

  const animateAssistantreply = useEffectEvent((messageId: string, finalText: string) => {
    stopTyping()
    let cursor = 0
    const safeText = finalText || 'Sin respuesta final del runtime.'
    updateAssistantMessage(messageId, '', 'Transmitiendo salida final…')

    typingTimerref.current = window.setInterval(() => {
      cursor = Math.min(cursor + Math.max(4, Math.ceil(safeText.length / 90)), safeText.length)
      const nextText = safeText.slice(0, cursor)
      updateAssistantMessage(
        messageId,
        nextText,
        cursor === safeText.length ? undefined : 'Transmitiendo salida final…'
      )
      if (cursor === safeText.length) {
        stopTyping()
        hydrateArtifact(safeText)
      }
    }, 20)
  })

  const openSessionStream = useEffectEvent((sessionId: string, aftereventId = 0) => {
    closeStream()
    streamCleanupref.current = streamAgentSession(sessionId, (packet) => {
      lastEventIdref.current = packet.event_id || lastEventIdref.current

      if (packet.event_type === 'llm_output') {
        const thought = String(packet.payload?.thought || 'Sin thought expuesto')
        const iteration = String(packet.payload?.iteration || '-')
        setStreamState(`Iteración ${iteration}`)
        pushAgentFeed({
          id: `${packet.event_id}`,
          tone: 'accent',
          label: `Loop ${iteration}`,
          detail: thought
        })
      }

      if (packet.event_type === 'tool_result') {
        pushAgentFeed({
          id: `${packet.event_id}`,
          tone: 'success',
          label: String(packet.payload?.tool || 'Tool'),
          detail: previewJson(packet.payload?.result)
        })
      }

      if (packet.event_type === 'approval_requested') {
        const toolCallId = String(packet.payload?.tool_call_id || '')
        const tool = String(packet.payload?.tool || 'tool')
        const args = previewJson(packet.payload?.args)
        setPendingApproval({
          toolCallId,
          tool,
          args
        })
        setStreamState('Aprobación requerida')
        setRightMode('canvas')
        pushAgentFeed({
          id: `${packet.event_id}`,
          tone: 'danger',
          label: 'HookGateway',
          detail: `Aprobación humana solicitada para ${tool}.`
        })
      }

      if (packet.event_type === 'completed') {
        setStreamState('Completado')
        const assistantId = activeAssistantMessageref.current
        if (assistantId) {
          animateAssistantreply(assistantId, String(packet.payload?.final_response || ''))
        }
        pushAgentFeed({
          id: `${packet.event_id}`,
          tone: 'success',
          label: 'respuesta final',
          detail: 'La sesión terminó y el panel derecho revisó el artefacto.'
        })
        setPendingApproval(null)
        void refreshTelemetry()
      }

      if (packet.event_type === 'failed') {
        setStreamState('Falló')
        const assistantId = activeAssistantMessageref.current
        if (assistantId) {
          updateAssistantMessage(
            assistantId,
            `No se pudo completar la sesión.\n\n${String(packet.payload?.error || 'Error sin detalle.')}`
          )
        }
        pushAgentFeed({
          id: `${packet.event_id}`,
          tone: 'danger',
          label: 'Sesión fallida',
          detail: String(packet.payload?.error || 'Error sin detalle')
        })
      }

      if (packet.event_type === 'done') {
        setIsSending(false)
      }
    }, aftereventId)
  })

  const handleUpload = useEffectEvent(async (files: File[]) => {
    if (!files.length) {
      return
    }

    try {
      const uploadedAssets = await uploadAttachments(files)
      setAttachments((current) => [...current, ...uploadedAssets])
      pushAgentFeed({
        id: crypto.randomUUID(),
        tone: 'accent',
        label: 'Adjuntos',
        detail: `${uploadedAssets.length} archivo(s) listos para chat, imagen o video.`
      })
    } catch (error) {
      pushAgentFeed({
        id: crypto.randomUUID(),
        tone: 'danger',
        label: 'Adjuntos',
        detail: error instanceof Error ? error.message : 'No se pudieron subir los adjuntos.'
      })
    }
  })

  const handleSubmit = useEffectEvent(async (draft?: string) => {
    const trimmed = (draft ?? input).trim()
    if (!trimmed || isSending) {
      return
    }

    if (profile === 'glitch' && trimmed.startsWith('/')) {
      const userMessage: Message = {
        id: crypto.randomUUID(),
        role: 'user',
        content: trimmed
      }
      const assistantMessage: Message = {
        id: crypto.randomUUID(),
        role: 'assistant',
        content: '',
        meta: 'Ejecutando Glitch local…'
      }

      setMessages((current) => [...current, userMessage, assistantMessage])
      setInput('')
      setIsSending(true)
      setStreamState('Glitch local')
      scrollToBottom('smooth')

      try {
        const result = await handleGlitchChatCommand(trimmed)
        updateAssistantMessage(assistantMessage.id, result.content, result.meta)
      } catch (error) {
        updateAssistantMessage(
          assistantMessage.id,
          error instanceof Error ? error.message : 'No se pudo ejecutar el comando local.',
          'Glitch'
        )
      } finally {
        setIsSending(false)
        setStreamState('Listo')
      }
      return
    }

    const resolvedModel = selectedModel === 'codex-bridge' ? 'qwen2.5-coder:3b' : selectedModel
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: trimmed
    }
    const assistantMessage: Message = {
      id: crypto.randomUUID(),
      role: 'assistant',
      content: '',
      meta: 'Abriendo sesión con el runtime de Claudio…'
    }

    activeAssistantMessageref.current = assistantMessage.id
    setMessages((current) => [...current, userMessage, assistantMessage])
    setInput('')
    setIsSending(true)
    setStreamState('Abriendo sesión')
    setPendingApproval(null)
    lastEventIdref.current = 0
    scrollToBottom('smooth')

    try {
      const response = await executeAgent({
        task: trimmed,
        model: resolvedModel,
        depto: selectedDepto || undefined,
        attachment_ids: attachments.map((item) => item.id)
      })

      setActiveSessionId(response.session_id)
      openSessionStream(response.session_id)

      if (!response.ok && activeAssistantMessageref.current) {
        updateAssistantMessage(
          activeAssistantMessageref.current,
          `La sesión devolvió un error inicial.\n\n${response.error || 'Error sin detalle.'}`
        )
        setIsSending(false)
      }

      pushAgentFeed({
        id: crypto.randomUUID(),
        tone: 'neutral',
        label: 'Agent runtime',
        detail:
          selectedModel === 'codex-bridge'
            ? 'Codex bridge encaminó la tarea a Qwen Coder local para mantener compatibilidad.'
            : `Sesión abierta con ${resolvedModel}.`
      })
    } catch (error) {
      setIsSending(false)
      setStreamState('Error')
      if (activeAssistantMessageref.current) {
        updateAssistantMessage(
          activeAssistantMessageref.current,
          `No se pudo abrir la sesión.\n\n${error instanceof Error ? error.message : 'Error sin detalle.'}`
        )
      }
      pushAgentFeed({
        id: crypto.randomUUID(),
        tone: 'danger',
        label: 'Agent runtime',
        detail: error instanceof Error ? error.message : 'No se pudo abrir la sesión.'
      })
    }
  })

  const handleApprove = useEffectEvent(async (approved: boolean) => {
    if (!activeSessionId || !pendingApproval) {
      return
    }

    try {
      await approveToolCall(activeSessionId, pendingApproval.toolCallId, approved)
      pushAgentFeed({
        id: crypto.randomUUID(),
        tone: approved ? 'success' : 'danger',
        label: approved ? 'Aprobado' : 'rechazado',
        detail: `${pendingApproval.tool} fue ${approved ? 'aprobado' : 'rechazado'} desde Argus.`
      })
      openSessionStream(activeSessionId, lastEventIdref.current)
      setPendingApproval(null)
    } catch (error) {
      pushAgentFeed({
        id: crypto.randomUUID(),
        tone: 'danger',
        label: 'HookGateway',
        detail: error instanceof Error ? error.message : 'No se pudo responder la aprobación.'
      })
    }
  })

  const handleTaskresponse = useEffectEvent(async (taskId: string) => {
    const answer = (taskAnswers[taskId] || '').trim()
    if (!answer) {
      return
    }

    try {
      await respondHumanTask(taskId, answer)
      setTaskAnswers((current) => {
        const nextState = { ...current }
        delete nextState[taskId]
        return nextState
      })
      pushAgentFeed({
        id: crypto.randomUUID(),
        tone: 'success',
        label: 'Buddy query',
        detail: `respuesta enviada para la tarea ${taskId}.`
      })
      void refreshTelemetry()
    } catch (error) {
      pushAgentFeed({
        id: crypto.randomUUID(),
        tone: 'danger',
        label: 'Buddy query',
        detail: error instanceof Error ? error.message : 'No se pudo responder la tarea humana.'
      })
    }
  })

  const runDesktopAction = useEffectEvent(async (action: string, payload: Record<string, unknown>, approve = false) => {
    if (!desktopAvailable || !window.claudioDesktop) {
      pushDesktopFeed({
        id: crypto.randomUUID(),
        tone: 'danger',
        label: 'Desktop',
        detail: 'Las acciones Glitch completas requieren la app de escritorio.'
      })
      return null
    }

    const result = await window.claudioDesktop.invoke(action, {
      ...payload,
      approve
    })

    if (result.requiresApproval && result.gate) {
      setDesktopApproval({
        action,
        payload,
        gate: result.gate
      })
      setRightMode('evidence')
      pushDesktopFeed({
        id: crypto.randomUUID(),
        tone: 'danger',
        label: 'Aprobación requerida',
        detail: `${result.gate.reason} - modo ${result.gate.obs_mode}.`
      })
      return result
    }

    if (!result.ok) {
      const detail = result.error || result.gate?.reason || 'No se pudo completar la acción.'
      setTerchicalOutput((current) => `${current}\n\n[ERROR]\n${detail}`)
      pushDesktopFeed({
        id: crypto.randomUUID(),
        tone: 'danger',
        label: action,
        detail
      })
      return result
    }

    if (action === 'exec' && result.output) {
      setTerchicalOutput(result.output)
    }

    if (action === 'readFile' && result.content) {
      setGlitchFileDraft(result.content)
      setGlitchFileStatus(result.target || 'Archivo cargado')
    }

    if (action === 'writeFile') {
      setGlitchFileStatus(`Guardado en ${result.target || 'ruta desconocida'} - ${result.bytes || 0} bytes`)
    }

    pushDesktopFeed({
      id: crypto.randomUUID(),
      tone: 'success',
      label: action,
      detail: result.target || result.output || 'Acción completada'
    })

    return result
  })

  const handleGlitchChatCommand = useEffectEvent(async (trimmed: string) => {
    const [rawCommand = ''] = trimmed.split(/\s+/, 1)
    const commandName = rawCommand.toLowerCase()
    const rest = trimmed.slice(rawCommand.length).trim()

    const getOutput = (result: DesktopInvokeresponse | null, fallback: string) => {
      if (!result) {
        return fallback
      }
      if (result.requiresApproval && result.gate) {
        return `La acción quedó lista para aprobación humana.\n\n${result.gate.reason}\nModo PSI: ${result.gate.obs_mode}`
      }
      if (!result.ok) {
        return result.error || result.gate?.reason || fallback
      }
      return result.output || result.target || fallback
    }

    if (commandName === '/help' || commandName === '/glitch') {
      return {
        content: [
          'Comandos de Glitch disponibles:',
          '- `/ps7 <comando>` ejecuta PowerShell 7 local',
          '- `/nemo <tarea>` corre el research loop de Nemo',
          '- `/cw <prompt>` llama a ClawdWorks en modo print',
          '- `/cw-open` abre ClawdWorks interactivo',
          `- \`/libros\` abre ${LIBRARY_LABEL}`
        ].join('\n')
      }
    }

    if (['/ps', '/ps7', '/pwsh'].includes(commandName)) {
      const result = await runDesktopAction('exec', {
        command: rest || 'Get-ChildItem',
        shell: 'pwsh',
        timeoutMs: 480000
      })
      return {
        content: getOutput(result, 'No se pudo ejecutar PowerShell 7.'),
        meta: 'Glitch ejecutó PowerShell 7 local.'
      }
    }

    if (commandName === '/powershell') {
      const result = await runDesktopAction('exec', {
        command: rest || 'Get-ChildItem',
        shell: 'powershell',
        timeoutMs: 480000
      })
      return {
        content: getOutput(result, 'No se pudo ejecutar Windows PowerShell.'),
        meta: 'Glitch ejecutó Windows PowerShell.'
      }
    }

    if (commandName === '/cmd') {
      const result = await runDesktopAction('exec', {
        command: rest || 'dir',
        shell: 'cmd',
        timeoutMs: 240000
      })
      return {
        content: getOutput(result, 'No se pudo ejecutar CMD.'),
        meta: 'Glitch ejecutó CMD local.'
      }
    }

    if (commandName === '/nemo') {
      if (!rest) {
        return {
          content: 'Uso: `/nemo <tarea>`\n\nEjemplo: `/nemo resume esta carpeta y detecta riesgos`',
          meta: 'Glitch'
        }
      }
      const result = await runDesktopAction('launchKnown', {
        commandId: 'nemo_task',
        prompt: rest,
        timeoutMs: 480000
      })
      return {
        content: getOutput(result, 'No se pudo lanzar Nemo.'),
        meta: 'Nemo research loop ejecutado desde Glitch.'
      }
    }

    if (['/cw', '/clawdwork', '/claudework'].includes(commandName)) {
      if (!rest) {
        return {
          content: 'Uso: `/cw <prompt>`\n\nEjemplo: `/cw revisa este error y dame un parche mínimo`',
          meta: 'Glitch'
        }
      }
      const result = await runDesktopAction('launchKnown', {
        commandId: 'clawdworks_print',
        prompt: rest,
        timeoutMs: 480000
      })
      return {
        content: getOutput(result, 'No se pudo llamar a ClawdWorks.'),
        meta: 'ClawdWorks respondió por el bridge local.'
      }
    }

    if (commandName === '/cw-open') {
      const result = await runDesktopAction('launchKnown', {
        commandId: 'clawdworks_open'
      })
      return {
        content: getOutput(result, 'No se pudo abrir ClawdWorks.'),
        meta: 'Se abrió una sesión interactiva de ClawdWorks.'
      }
    }

    if (commandName === '/libros') {
      const result = await runDesktopAction('launchKnown', {
        commandId: 'open_library'
      })
      return {
        content: getOutput(result, `Se abrió ${LIBRARY_LABEL}.`),
        meta: `Acceso directo a ${LIBRARY_LABEL}.`
      }
    }

    if (commandName === '/leer') {
      if (!rest) {
        return {
          content: 'Uso: `/leer <ruta absoluta>`',
          meta: 'Glitch'
        }
      }
      const result = await runDesktopAction('readFile', {
        path: rest
      })
      return {
        content: getOutput(result, 'No se pudo leer el archivo pedido.'),
        meta: 'Lectura local desde Glitch.'
      }
    }

    if (commandName === '/abrir') {
      if (!rest) {
        return {
          content: 'Uso: `/abrir <ruta absoluta>`',
          meta: 'Glitch'
        }
      }
      const result = await runDesktopAction('openPath', {
        path: rest
      })
      return {
        content: getOutput(result, 'No se pudo abrir la ruta pedida.'),
        meta: 'Ruta abierta desde Glitch.'
      }
    }

    return {
      content: `Comando no reconocido: ${commandName}\n\nUsa \`/help\` para ver comandos de Glitch.`,
      meta: 'Glitch'
    }
  })

  const handleDesktopApproval = useEffectEvent(async (approved: boolean) => {
    if (!desktopApproval) {
      return
    }

    if (!approved) {
      pushDesktopFeed({
        id: crypto.randomUUID(),
        tone: 'danger',
        label: 'Glitch',
        detail: 'Acción cancelada por la persona usuaria.'
      })
      setDesktopApproval(null)
      return
    }

    const approval = desktopApproval
    setDesktopApproval(null)
    await runDesktopAction(approval.action, approval.payload, true)
  })

  const handleVoiceTranscript = useEffectEvent((rawTranscript: string) => {
    const transcript = rawTranscript.trim()
    if (!transcript) {
      return
    }

    setVoiceTranscript(transcript)
    const lower = transcript
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')

    const matchSection = (section: NavSectionId, view?: RightViewId) => {
      setActiveNav(section)
      if (view) {
        setRightMode(view)
      }
    }

    if (lower.includes('modo diario') || lower.includes('modo promedio') || lower.includes('modo usuario')) {
      setProfile('average')
      void announce('Modo diario activado.')
      return
    }

    if (lower.includes('modo no tecnico') || lower.includes('modo sencillo') || lower.includes('modo ayuda')) {
      setProfile('nonTechnical')
      void announce('Modo no técnico activado.')
      return
    }

    if (lower.includes('modo diseno') || lower.includes('modo creativo') || lower.includes('modo constante')) {
      setProfile('creative')
      matchSection('radiocinema', 'studio')
      void announce('Modo diseño activado.')
      return
    }

    if (lower.includes('modo glitch')) {
      setProfile('glitch')
      matchSection('tools', 'terchical')
      void announce('Modo glitch activado.')
      return
    }

    if (lower.includes('abrir historial')) {
      matchSection('history', 'hud')
      return
    }

    if (lower.includes('abrir radiocinema') || lower === 'radiocinema') {
      matchSection('radiocinema', 'studio')
      return
    }

    if (lower.includes('abrir herramientas') || lower === 'herramientas') {
      matchSection('tools', profile === 'glitch' ? 'terchical' : 'city')
      return
    }

    if (lower.includes('abrir configuracion') || lower === 'configuracion') {
      matchSection('settings', 'hud')
      return
    }

    if (lower.includes('activar vision') || lower.includes('enciende vision') || lower.includes('enciende camara')) {
      setRightMode('vision')
      setLiveVision((current) => ({ ...current, enabled: true }))
      return
    }

    if (lower.includes('apaga vision') || lower.includes('deten vision') || lower.includes('deten camara')) {
      setLiveVision((current) => ({ ...current, enabled: false }))
      return
    }

    if (lower.includes('lee esto')) {
      void announce(input || transcript)
      return
    }

    if (lower.startsWith('claudio ')) {
      const prompt = transcript.replace(/^claudio\s+/i, '').trim()
      if (!prompt) {
        return
      }
      if (profile === 'nonTechnical') {
        void handleSubmit(prompt)
      } else {
        setInput(prompt)
      }
    }
  })

  useEffect(() => {
    document.body.dataset.profile = profile
    return () => {
      delete document.body.dataset.profile
    }
  }, [profile])

  useEffect(() => {
    const nextMode = deriveRightMode(profile, activeNav)
    setRightMode((current) => (getRightTabs(profile).some((tab) => tab.id === current) ? current : nextMode))
  }, [activeNav, profile])

  useEffect(() => {
    void refreshTelemetry().catch((error) => {
      pushAgentFeed({
        id: crypto.randomUUID(),
        tone: 'danger',
        label: 'Conexión',
        detail: error instanceof Error ? error.message : 'No se pudo cargar el estado inicial.'
      })
    })

    const intervalId = window.setInterval(() => {
      void refreshTelemetry().catch((error) => {
        pushAgentFeed({
          id: crypto.randomUUID(),
          tone: 'danger',
          label: 'Telemetry',
          detail: error instanceof Error ? error.message : 'No se pudo refrescar el estado.'
        })
      })
    }, 5000)

    return () => {
      window.clearInterval(intervalId)
      closeStream()
      stopTyping()
    }
  }, [closeStream, pushAgentFeed, refreshTelemetry, stopTyping])

  useEffect(() => {
    if (autoPinnedref.current) {
      scrollToBottom(messages.length > 2 ? 'smooth' : 'auto')
    }
  }, [attachments, messages, scrollToBottom, streamState])

  useEffect(() => {
    const wantsVoiceDaemon = (profile === 'nonTechnical' && voiceModuleEnabled) || manualVoiceDaemon
    if (!voiceStatus || voiceStatus.status === 'unavailable') {
      return
    }

    if (voiceDaemonBusyref.current) {
      return
    }

    if (wantsVoiceDaemon && !voiceStatus.running) {
      voiceDaemonBusyref.current = true
      void startVoiceDaemon({
        model: 'small',
        always_on: true
      })
        .then(() => refreshTelemetry())
        .catch((error) => {
          pushAgentFeed({
            id: crypto.randomUUID(),
            tone: 'danger',
            label: 'Voice daemon',
            detail: error instanceof Error ? error.message : 'No se pudo iniciar la voz.'
          })
        })
        .finally(() => {
          voiceDaemonBusyref.current = false
        })
      return
    }

    if (!wantsVoiceDaemon && voiceStatus.running) {
      voiceDaemonBusyref.current = true
      void stopVoiceDaemon()
        .then(() => refreshTelemetry())
        .catch(() => {
          pushAgentFeed({
            id: crypto.randomUUID(),
            tone: 'danger',
            label: 'Voice daemon',
            detail: 'No se pudo detener la voz en segundo plano.'
          })
        })
        .finally(() => {
          voiceDaemonBusyref.current = false
        })
    }
  }, [manualVoiceDaemon, profile, pushAgentFeed, refreshTelemetry, voiceModuleEnabled, voiceStatus])

  useEffect(() => {
    const SpeechrecognitionCtor = window.Speechrecognition || window.webkitSpeechrecognition
    const shouldListen = voiceCommandsEnabled || (profile === 'nonTechnical' && voiceModuleEnabled)

    if (!SpeechrecognitionCtor) {
      setVoiceCommandsState({
        supported: false,
        listening: false,
        error: 'Speechrecognition no disponible en este runtime.'
      })
      return
    }

    if (!shouldListen) {
      shouldrestartVoiceref.current = false
      recognitionref.current?.stop()
      setVoiceCommandsState({
        supported: true,
        listening: false,
        error: ''
      })
      return
    }

    const recognition = recognitionref.current || new SpeechrecognitionCtor()
    recognition.continuous = true
    recognition.interimresults = false
    recognition.lang = 'es-MX'

    recognition.onresult = (event) => {
      const transcript = Array.from({ length: event.results.length })
        .map((_, index) => event.results[index][0]?.transcript || '')
        .join(' ')
        .trim()
      if (transcript) {
        handleVoiceTranscript(transcript)
      }
    }

    recognition.onerror = (event) => {
      if (['not-allowed', 'service-not-allowed', 'audio-capture'].includes(event.error)) {
        shouldrestartVoiceref.current = false
      }
      setVoiceCommandsState({
        supported: true,
        listening: false,
        error: event.error || 'Error de reconocimiento'
      })
    }

    recognition.onend = () => {
      setVoiceCommandsState((current) => ({
        ...current,
        listening: false
      }))
      if (shouldrestartVoiceref.current) {
        window.setTimeout(() => {
          try {
            recognition.start()
            setVoiceCommandsState({
              supported: true,
              listening: true,
              error: ''
            })
          } catch {
            // El runtime puede estar arrancando o reiniciando.
          }
        }, 650)
      }
    }

    recognitionref.current = recognition
    shouldrestartVoiceref.current = true

    try {
      recognition.start()
      setVoiceCommandsState({
        supported: true,
        listening: true,
        error: ''
      })
    } catch {
      setVoiceCommandsState({
        supported: true,
        listening: false,
        error: ''
      })
    }

    return () => {
      shouldrestartVoiceref.current = false
      try {
        recognition.stop()
      } catch {
        // Ignorar errores al desmontar.
      }
    }
  }, [handleVoiceTranscript, profile, voiceCommandsEnabled, voiceModuleEnabled])

  useEffect(() => {
    const { enabled, source, intervalMs, autoDescribe } = liveVision

    if (!enabled || !cameraModuleEnabled) {
      if (!cameraStopLockref.current) {
        cameraStopLockref.current = true
        void stopCameraStream().catch(() => {})
      }
      return
    }

    cameraStopLockref.current = false
    let cancelled = false

    const loop = async () => {
      try {
        await startCameraStream({
          source,
          interval: Math.max(1, intervalMs / 1000),
          analyze: autoDescribe
        })
      } catch {
        // El stream ya pudo estar activo. Seguimos con el polling.
      }

      while (!cancelled) {
        setVisionBusy(true)
        setVisionImageNonce(Date.now())
        try {
          const [status, description] = await Promise.all([
            getCameraStatus(),
            autoDescribe
              ? describeCamera({
                  source,
                  prompt: 'Describe la escena, detecta personas, objetos importantes y señales de riesgo.'
                })
              : Promise.resolve({ ok: true, description: '', ts: '' })
          ])

          if (cancelled) {
            return
          }

          setCameraStatus(status)
          setLiveVision((current) => ({
            ...current,
            lastDescription: description.description || status.last_description || current.lastDescription,
            lastUpdated: description.ts || new Date().toISOString()
          }))
        } catch (error) {
          if (!cancelled) {
            pushAgentFeed({
              id: crypto.randomUUID(),
              tone: 'danger',
              label: 'Visión',
              detail: error instanceof Error ? error.message : 'No se pudo refrescar la visión.'
            })
          }
        } finally {
          if (!cancelled) {
            setVisionBusy(false)
          }
        }

        await new Promise((resolve) => window.setTimeout(resolve, intervalMs))
      }
    }

    void loop()

    return () => {
      cancelled = true
      if (!cameraStopLockref.current) {
        cameraStopLockref.current = true
        void stopCameraStream().catch(() => {})
      }
    }
  }, [cameraModuleEnabled, liveVision.autoDescribe, liveVision.enabled, liveVision.intervalMs, liveVision.source, pushAgentFeed])

  useEffect(() => {
    if (profile === 'nonTechnical') {
      void announce('Modo no técnico listo. Puedes hablar con Claudio en voz alta.')
    }
  }, [announce, profile])

  function handleWakeup() {
    void (window as any).claudioDesktop?.invoke('launchKnown', { commandId: 'launch_thesis' })
  }

  if (profile === 'nonTechnical') {
    return (
      <div className="relative flex h-dvh w-full max-w-full min-w-0 flex-col overflow-x-hidden overflow-y-auto px-2 py-2 sm:px-3 sm:py-3 md:px-5 md:py-5">
        <SimpleHomeView
          cameraStatus={cameraStatus}
          connectionMessage={connectionMessage}
          connectionState={connectionState}
          input={input}
          isSending={isSending}
          messages={messages}
          modulesStatus={modulesStatus}
          onActionHelp={openSimpleHelp}
          onActionSee={openSimpleVision}
          onActionTalk={openSimpleTalk}
          onActionWrite={openWriterWorkbench}
          onComposerKeyDown={handleComposerKeyDown}
          onInputChange={setInput}
          onOpenTechnicalMode={openTechnicalMode}
          onSend={() => {
            void handleSubmit()
          }}
          onSetOppoMode={handleSetOppoMode}
          onSetVoiceBackend={handleSetVoiceBackend}
          onToggleModule={handleToggleModule}
          onWakeup={handleWakeup}
          oppoStatus={oppoStatus}
          sensoryFeed={sensoryFeed}
          voiceBackends={voiceBackends}
          voiceStatus={voiceStatus}
        />
      </div>
    )
  }

  return (
    <div className="relative flex h-dvh flex-col overflow-hidden px-3 py-3 md:px-5 md:py-5">
      <div className="glass-panel mb-3 flex flex-wrap items-center justify-between gap-3 px-4 py-3 md:px-5">
        <div className="flex items-center gap-3">
          <button
            className="action-chip touch-target lg:hidden"
            onClick={() => setLeftDrawerOpen(true)}
            type="button"
          >
            Menú
          </button>
          <div>
            <div className="eyebrow">Claudio UI FCU</div>
            <div className="text-sm text-slate-200">{connectionMessage}</div>
            <div className="text-xs text-slate-500">
              {profileCopy.label} - {profileCopy.helper}
            </div>
          </div>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <ConnectionBadge state={connectionState} />
          <StatusBadge label="R" value={buddy?.observacionismo.r ?? 0} tone={observacionismoState.tone} />
          <StatusBadge label="Phi" value={buddy?.observacionismo.phi_eff ?? 0} tone="cool" />
          <StatusBadge label="Jc" value={buddy?.observacionismo.j_c ?? 0} tone="warm" />
          <button
            className="action-chip touch-target lg:hidden"
            onClick={() => setRightDrawerOpen(true)}
            type="button"
          >
            Hub
          </button>
        </div>
      </div>

      <div className="relative min-h-0 flex-1 flex-col gap-3 lg:grid lg:min-h-0 lg:h-full" style={{ gridTemplateColumns: desktopGridTemplate }}>
        <aside
          className={`${leftDrawerOpen ? 'translate-x-0 opacity-100' : '-translate-x-full opacity-0'} fixed inset-y-3 left-3 z-40 w-[min(23rem,calc(100vw-2rem))] transition duration-200 ease-observatory lg:static lg:z-auto lg:h-full lg:w-auto lg:translate-x-0 lg:opacity-100`}
        >
          <div className={`glass-panel flex h-full flex-col ${leftCollapsed ? 'px-3 py-4' : 'px-4 py-4'}`}>
            <div className="mb-4 flex items-start justify-between gap-3">
              <div className={`flex items-center gap-3 ${leftCollapsed ? 'justify-center' : ''}`}>
                <ArgusMark compact={leftCollapsed} />
                {!leftCollapsed && (
                  <div>
                    <div className="eyebrow text-cyan-100/80">Argus visible</div>
                    <div className="text-lg font-semibold text-slate-50">Claudio - Argus</div>
                    <div className="text-xs text-slate-400">Medioevo sci-fi, ciudad viva y frecuencia 47</div>
                  </div>
                )}
              </div>
              <div className="flex gap-2">
                <button className="action-chip hidden lg:inline-flex" onClick={() => setLeftCollapsed((value) => !value)} type="button">
                  {leftCollapsed ? 'Abrir' : 'Cerrar'}
                </button>
                <button className="action-chip lg:hidden" onClick={() => setLeftDrawerOpen(false)} type="button">
                  Cerrar
                </button>
              </div>
            </div>

            {!leftCollapsed && (
              <>
                <div className="glass-panel-warm mb-4 px-4 py-4">
                  <div className="mb-3 flex items-center justify-between gap-3">
                    <div>
                      <div className="eyebrow mb-1">Perfil</div>
                      <div className="text-base font-semibold text-slate-50">{profileCopy.label}</div>
                    </div>
                    <div className={`status-glow rounded-full border px-3 py-1 text-xs font-semibold ${observacionismoState.className}`} data-tone={observacionismoState.statusGlow}>
                      {quickPsiLabel}
                    </div>
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    {(Object.keys(PROFILE_CONFIG) as UserProfileId[]).map((profileId) => (
                      <ProfileButton
                        active={profileId === profile}
                        key={profileId}
                        label={PROFILE_CONFIG[profileId].label}
                        onClick={() => setProfile(profileId)}
                        short={PROFILE_CONFIG[profileId].short}
                      />
                    ))}
                  </div>
                </div>

                <div className="pixel-city-frame scanlines mb-4">
                  <div className="pixel-grid absolute inset-0 opacity-40" />
                  <img
                    alt="Ciudad Claudio pixel art"
                    className="h-40 w-full object-cover opacity-90"
                    height="720"
                    loading="eager"
                    src="/city-pixel-scene.svg"
                    width="1600"
                  />
                  <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-[#07090f] via-[#07090f]/82 to-transparent px-4 py-4">
                    <div className="eyebrow mb-1">Ciudad Claudio</div>
                    <div className="text-lg font-semibold text-slate-50">Mapa RPG - punto de partida del metroidvania</div>
                    <div className="mt-1 text-xs text-slate-400">
                      {cityMap?.departments.length || 0} zonas, {cityMap?.watchtowers.length || 0} torres y {cityMap?.nodes.length || 0} puertas de red
                    </div>
                  </div>
                </div>
              </>
            )}

            <div className="mb-3 flex items-center justify-between">
              {!leftCollapsed && <div className="eyebrow">Navegación</div>}
              {!leftCollapsed && <div className="text-xs text-slate-500">{PROFILE_CONFIG[profile].short}</div>}
            </div>

            <div className="space-y-2 overflow-y-auto pr-1">
              {NAV_ITEMS.map((item) => (
                <NavButton
                  active={!leftCollapsed && activeNav === item.id}
                  compact={leftCollapsed}
                  detail={item.detail}
                  key={item.id}
                  label={item.label}
                  onClick={() => setActiveNav(item.id)}
                />
              ))}
            </div>

            {!leftCollapsed && (
              <div className="mt-4 rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
                <div className="mb-3 flex items-center justify-between gap-3">
                  <div className="eyebrow">Acceeres rápidos</div>
                  <div className="text-[11px] uppercase tracking-[0.22em] text-slate-500">{PROFILE_CONFIG[profile].short}</div>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  {sidebarShortcuts.map((shortcut) => (
                    <button
                      className="shortcut-card touch-target text-left"
                      key={shortcut.id}
                      onClick={() => {
                        if (shortcut.kind === 'nav') {
                          setActiveNav(shortcut.section)
                          if (shortcut.view) {
                            setRightMode(shortcut.view)
                          }
                          return
                        }
                        if (shortcut.kind === 'prompt') {
                          void handleSubmit(shortcut.prompt)
                          return
                        }
                        if (shortcut.kind === 'command') {
                          setProfile('glitch')
                          setActiveNav('tools')
                          setRightMode('terchical')
                          setInput(shortcut.command)
                          return
                        }
                        if (shortcut.kind === 'open') {
                          if (shortcut.commandId) {
                            void runDesktopAction('launchKnown', { commandId: shortcut.commandId })
                          } else {
                            void runDesktopAction('openPath', { path: shortcut.path })
                          }
                        }
                      }}
                      type="button"
                    >
                      <span className="shortcut-card__label">{shortcut.label}</span>
                      <span className="shortcut-card__detail">{shortcut.detail}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {!leftCollapsed && (
              <div className="mt-5 grid grid-cols-3 gap-2">
                <MetricTile label="R" value={formatMetric(buddy?.observacionismo.r)} tone={observacionismoState.tone} />
                <MetricTile label="Phi" value={formatMetric(buddy?.observacionismo.phi_eff)} tone="cool" />
                <MetricTile label="Jc" value={formatMetric(buddy?.observacionismo.j_c)} tone="warm" />
              </div>
            )}

            {!leftCollapsed && (
              <div className="mt-4 rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
                <div className="eyebrow mb-2">Estado humano</div>
                <div className="text-sm text-slate-100">{quickPsiLabel}</div>
                <div className="mt-2 text-xs leading-6 text-slate-400">
                  Voz: {voiceStatus?.running ? 'activa' : 'inactiva'} - Visión: {cameraStatus?.vision_model || 'sin modelo'}
                </div>
              </div>
            )}
          </div>
        </aside>

        <section className="glass-panel relative flex min-h-[68dvh] flex-1 flex-col overflow-hidden lg:min-h-0 lg:h-full">
          <div className="flex flex-none flex-wrap items-center justify-between gap-3 border-b border-white/6 px-4 py-4 md:px-5">
            <div>
              <div className="eyebrow">Diálogo central</div>
              <div className="text-2xl font-semibold tracking-tight text-slate-50">Claudio Runtime</div>
              <div className="text-sm text-slate-400">
                {streamState} {activeSessionId ? `- ${activeSessionId.slice(0, 12)}` : ''}
              </div>
            </div>
            <div className={`inline-flex items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold ${observacionismoState.className}`}>
              <span className="inline-block h-2.5 w-2.5 rounded-full bg-current" />
              Observacionismo {observacionismoState.label}
            </div>
          </div>

          <div className="flex flex-none flex-col gap-3 border-b border-white/6 px-4 py-3 md:px-5">
            <div className="flex flex-wrap gap-2">
              {promptDeck.map((card) => (
                <button
                  className="touch-target rounded-full border border-white/10 bg-white/[0.04] px-4 py-2 text-left text-sm text-slate-100 transition duration-200 ease-observatory hover:-translate-y-0.5 hover:border-cyan-300/30 hover:bg-cyan-300/10"
                  key={card.id}
                  onClick={() => void handleSubmit(card.prompt)}
                  type="button"
                >
                  <div className="font-semibold">{card.label}</div>
                  <div className="text-xs text-slate-400">{card.detail}</div>
                </button>
              ))}
            </div>

            {activeNav === 'radiocinema' && (
              <div className="flex flex-wrap gap-2">
                {MINI_GAMES.map((game) => (
                  <button
                    className="touch-target rounded-2xl border border-amber-300/20 bg-amber-300/8 px-4 py-3 text-left transition duration-200 ease-observatory hover:-translate-y-0.5 hover:border-amber-300/40"
                    key={game.label}
                    onClick={() => void handleSubmit(game.prompt)}
                    type="button"
                  >
                    <div className="text-sm font-semibold text-amber-50">{game.label}</div>
                    <div className="text-xs text-amber-100/70">{game.detail}</div>
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="relative min-h-0 flex-1">
            <div
              className="h-full overflow-y-auto px-4 py-4 md:px-5"
              onScroll={syncScrollState}
              ref={messageViewportref}
            >
              <div className="space-y-4 pb-6">
                {messages.map((message) => (
                  <article
                    className={`fade-in max-w-[94%] rounded-[26px] border px-4 py-4 md:px-5 ${
                      message.role === 'user'
                        ? 'ml-auto border-cyan-300/30 bg-cyan-400/10'
                        : message.role === 'assistant'
                          ? 'border-amber-300/20 bg-white/[0.04]'
                          : 'mx-auto border-white/6 bg-white/[0.02]'
                    }`}
                    key={message.id}
                  >
                    <div className="mb-2 flex items-center justify-between gap-2">
                      <div className="text-xs uppercase tracking-[0.28em] text-slate-500">
                        {message.role === 'user' ? 'Tú' : message.role === 'assistant' ? 'Claudio' : 'Sistema'}
                      </div>
                      {message.meta && <div className="text-[11px] text-slate-500">{message.meta}</div>}
                    </div>
                    <div className="markdown-body">
                      <Markdown remarkPlugins={[remarkGfm]}>{message.content || '…'}</Markdown>
                    </div>
                  </article>
                ))}
              </div>
            </div>

            {showJumpToBottom && (
              <button
                className="focus-ring absolute bottom-4 right-4 rounded-full border border-cyan-300/25 bg-[#08101a]/92 px-4 py-2 text-sm font-semibold text-cyan-50 shadow-aura transition duration-200 ease-observatory hover:-translate-y-0.5"
                onClick={() => scrollToBottom('smooth')}
                type="button"
              >
                Volver al final
              </button>
            )}
          </div>

          {!!attachments.length && (
            <div className="flex flex-none flex-col gap-2 border-t border-white/6 px-4 py-3 md:px-5">
              <div className="eyebrow">Adjuntos actitú</div>
              <div className="grid gap-2 md:grid-cols-2 xl:grid-cols-3">
                {attachments.map((asset) => (
                  <div key={asset.id} className="rounded-2xl border border-white/8 bg-white/[0.03] px-3 py-3">
                    <div className="flex items-start justify-between gap-3">
                      <div className="min-w-0">
                        <div className="truncate text-sm font-semibold text-slate-100">{asset.name}</div>
                        <div className="mt-1 text-[11px] uppercase tracking-[0.22em] text-slate-500">
                          {asset.kind} - {asset.mime}
                        </div>
                      </div>
                      <button
                        className="action-chip"
                        onClick={() => setAttachments((current) => current.filter((item) => item.id !== asset.id))}
                        type="button"
                      >
                        Quitar
                      </button>
                    </div>
                    {asset.kind === 'image' && (
                      <img
                        alt={asset.name}
                        className="mt-3 h-28 w-full rounded-2xl border border-white/8 object-cover"
                        src={asset.preview_url}
                      />
                    )}
                    {asset.kind === 'video' && (
                      <video className="mt-3 h-28 w-full rounded-2xl border border-white/8 object-cover" controls src={asset.preview_url} />
                    )}
                    {!!asset.text_excerpt && (
                      <p className="mt-3 text-xs leading-6 text-slate-400">{asset.text_excerpt}</p>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          <div className="flex flex-none flex-col gap-3 border-t border-white/6 px-4 py-4 md:px-5">
            <div className="flex flex-wrap items-center gap-2">
              <select
                aria-label="Seleccionar modelo"
                className="focus-ring touch-target rounded-full border border-white/10 bg-black/20 px-3 py-2 text-sm text-slate-100 outline-none transition duration-200 ease-observatory focus:border-cyan-300/40"
                name="selected_model"
                onChange={(event) => setSelectedModel(event.target.value)}
                value={selectedModel}
              >
                {MODEL_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              <select
                aria-label="Seleccionar departamento"
                className="focus-ring touch-target rounded-full border border-white/10 bg-black/20 px-3 py-2 text-sm text-slate-100 outline-none transition duration-200 ease-observatory focus:border-cyan-300/40"
                name="selected_department"
                onChange={(event) => setSelectedDepto(event.target.value)}
                value={selectedDepto}
              >
                {(cityMap?.departments || []).map((department) => (
                  <option key={department.slug} value={department.slug}>
                    {department.name}
                  </option>
                ))}
              </select>
              <button className="action-chip touch-target" onClick={() => fileInputref.current?.click()} type="button">
                Adjuntar
              </button>
              <button
                className={`action-chip touch-target ${voiceCommandsState.listening ? 'border-emerald-300/30 bg-emerald-300/10 text-emerald-100' : ''}`}
                onClick={() => setVoiceCommandsEnabled((value) => !value)}
                type="button"
              >
                Voz UI {voiceCommandsState.listening ? 'on' : 'off'}
              </button>
              <button
                className={`action-chip touch-target ${manualVoiceDaemon ? 'border-amber-300/30 bg-amber-300/10 text-amber-50' : ''}`}
                onClick={() => setManualVoiceDaemon((value) => !value)}
                type="button"
              >
                Voz Claudio {voiceStatus?.running ? 'on' : 'off'}
              </button>
            </div>

            <div className="flex flex-col gap-3 xl:flex-row">
              <div className="flex-1">
                <textarea
                  aria-label="Mensaje para Claudio"
                  autoComplete="off"
                  className="focus-ring min-h-[108px] w-full rounded-[24px] border border-white/8 bg-black/25 px-4 py-4 text-sm text-slate-100 outline-none transition duration-200 ease-observatory focus:border-cyan-300/40 md:min-h-[120px]"
                  name="chat_prompt"
                  onChange={(event) => setInput(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === 'Enter' && (event.ctrlKey || event.metaKey)) {
                      event.preventDefault()
                      void handleSubmit()
                    }
                  }}
                  placeholder={composerPlaceholder}
                  value={input}
                />
                <div className="mt-2 flex flex-wrap items-center gap-2 text-xs text-slate-500">
                  <span>Entrada siempre visible</span>
                  <span>-</span>
                  <span>Ctrl + Enter para enviar</span>
                  <span>-</span>
                  <span>
                    {profile === 'glitch'
                      ? 'Glitch: /ps7, /nemo, /cw, /libros'
                      : voiceCommandsState.error || (voiceTranscript ? `Última voz: ${voiceTranscript}` : 'Comandos de voz listos')}
                  </span>
                </div>
              </div>

              <div className="flex min-w-[220px] flex-col gap-3">
                <button
                  className="touch-target rounded-[22px] border border-cyan-300/30 bg-cyan-300/15 px-4 py-4 text-sm font-semibold text-cyan-50 transition duration-200 ease-observatory hover:-translate-y-0.5 hover:border-cyan-200/50 hover:bg-cyan-300/20 disabled:translate-y-0 disabled:cursor-not-allowed disabled:opacity-50"
                  disabled={isSending || !input.trim()}
                  onClick={() => void handleSubmit()}
                  type="button"
                >
                  {isSending ? 'Procesando…' : 'Enviar'}
                </button>
                <div className="rounded-[22px] border border-white/8 bg-white/[0.03] px-4 py-4 text-sm leading-7 text-slate-400">
                  {profileCopy.helper}
                </div>
              </div>
            </div>
          </div>

          <input
            aria-label="Adjuntar archivo"
            className="hidden"
            multiple
            name="attachments"
            onChange={(event) => {
              const files = Array.from(event.target.files || [])
              void handleUpload(files)
              event.currentTarget.value = ''
            }}
            ref={fileInputref}
            type="file"
          />
        </section>

        <aside
          className={`${rightDrawerOpen ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'} fixed inset-y-3 right-3 z-40 w-[min(26rem,calc(100vw-2rem))] transition duration-200 ease-observatory lg:static lg:z-auto lg:h-full lg:w-auto lg:translate-x-0 lg:opacity-100`}
        >
          <div className={`glass-panel flex h-full flex-col ${rightCollapsed ? 'px-3 py-4' : 'px-4 py-4'}`}>
            <div className="mb-4 flex items-center justify-between gap-3">
              {!rightCollapsed && (
                <div>
                  <div className="eyebrow">Hub derecho</div>
                  <div className="text-lg font-semibold text-slate-50">
                    {profile === 'glitch' ? 'Terminal - Evidencia - Ciudad' : profile === 'creative' ? 'Studio - Canvas - Ciudad' : 'HUD - Ciudad - Visión'}
                  </div>
                </div>
              )}
              <div className="flex gap-2">
                <button className="action-chip hidden lg:inline-flex" onClick={() => setRightCollapsed((value) => !value)} type="button">
                  {rightCollapsed ? 'Abrir' : 'Cerrar'}
                </button>
                <button className="action-chip lg:hidden" onClick={() => setRightDrawerOpen(false)} type="button">
                  Cerrar
                </button>
              </div>
            </div>

            {!rightCollapsed && (
              <div className="mb-4 flex flex-wrap gap-2">
                {rightTabs.map((tab) => (
                  <ModeButton active={selectedRightMode === tab.id} key={tab.id} label={tab.label} onClick={() => setRightMode(tab.id)} />
                ))}
              </div>
            )}

            <div className="flex-1 overflow-y-auto pr-1">
              {rightCollapsed ? (
                <div className="flex h-full flex-col items-center justify-start gap-3 pt-3">
                  <MiniIndicator label="R" value={formatMetric(buddy?.observacionismo.r)} tone={observacionismoState.tone} />
                  <MiniIndicator label="Phi" value={formatMetric(buddy?.observacionismo.phi_eff)} tone="cool" />
                  <MiniIndicator label="Jc" value={formatMetric(buddy?.observacionismo.j_c)} tone="warm" />
                </div>
              ) : selectedRightMode === 'canvas' ? (
                <CanvasView
                  artifact={artifact}
                  onApprove={handleApprove}
                  onArtifactChange={(code) => setArtifact((current) => (current ? { ...current, code } : current))}
                  pendingApproval={pendingApproval}
                />
              ) : selectedRightMode === 'studio' ? (
                <StudioView
                  isGenerating={isGeneratingStudio}
                  log={radiocinemaLog}
                  onGenerate={async () => {
                    if (!studioPrompt.trim()) {
                      pushAgentFeed({
                        id: crypto.randomUUID(),
                        tone: 'danger',
                        label: 'Radiocinema',
                        detail: 'Falta prompt o nombre de proyecto.'
                      })
                      return
                    }

                    setIsGeneratingStudio(true)
                    try {
                      const result = await generateRadiocinema({
                        book: studioPrompt.trim(),
                        chapter: studioDetail.trim(),
                        style: studioStyle
                      })
                      pushAgentFeed({
                        id: crypto.randomUUID(),
                        tone: result.ok ? 'success' : 'danger',
                        label: 'Radiocinema',
                        detail: result.ok
                          ? `Job lanzado para ${studioPrompt.trim()}.`
                          : result.error || 'No se pudo iniciar la generación.'
                      })
                      if (result.ok) {
                        setStudioPrompt('')
                        setStudioDetail('')
                        void refreshTelemetry()
                      }
                    } catch (error) {
                      pushAgentFeed({
                        id: crypto.randomUUID(),
                        tone: 'danger',
                        label: 'Radiocinema',
                        detail: error instanceof Error ? error.message : 'No se pudo iniciar el studio.'
                      })
                    } finally {
                      setIsGeneratingStudio(false)
                    }
                  }}
                  onPromptChange={setStudioPrompt}
                  onStyleChange={setStudioStyle}
                  onDetailChange={setStudioDetail}
                  prompt={studioPrompt}
                  radiocinemaStatus={radiocinemaStatus}
                  style={studioStyle}
                  detail={studioDetail}
                  tools={radiocinemaTools}
                  launchingTool={launchingTool}
                  onLaunchTool={async (toolId) => {
                    setLaunchingTool(toolId)
                    try {
                      const result = await launchRadiocinemaTool(toolId)
                      pushAgentFeed({
                        id: crypto.randomUUID(),
                        tone: result.ok ? 'success' : 'danger',
                        label: 'Radiocinema',
                        detail: result.ok
                          ? [
                              `${result.label || toolId} abierto${result.pid ? ` (pid ${result.pid})` : ''}.`,
                              result.npm_script ? `Script ${result.npm_script}.` : null,
                              result.url ? `URL ${result.url}.` : null
                            ].filter(Boolean).join(' ')
                          : result.error || 'No se pudo abrir la herramienta.'
                      })
                    } catch (error) {
                      pushAgentFeed({
                        id: crypto.randomUUID(),
                        tone: 'danger',
                        label: 'Radiocinema',
                        detail: error instanceof Error ? error.message : 'No se pudo abrir la herramienta.'
                      })
                    } finally {
                      setLaunchingTool(null)
                    }
                  }}
                />
              ) : selectedRightMode === 'vision' ? (
                <VisionView
                  cameraStatus={cameraStatus}
                  hubAvailable={Boolean(hubDevices && hubDevices[hubDeviceIdForSource(liveVision.source)]?.online !== false)}
                  hubStreamUrl={getHubStreamUrl(liveVision.source)}
                  imageUrl={`${visionImageUrl}&t=${visionImageNonce}`}
                  isBusy={visionBusy}
                  liveVision={liveVision}
                  onChangeSource={(source) => setLiveVision((current) => ({ ...current, source }))}
                  onToggle={() => setLiveVision((current) => ({ ...current, enabled: !current.enabled }))}
                  onToggleDescribe={() => setLiveVision((current) => ({ ...current, autoDescribe: !current.autoDescribe }))}
                  onUseSpeed={(intervalMs) => setLiveVision((current) => ({ ...current, intervalMs }))}
                />
              ) : selectedRightMode === 'terchical' ? (
                <TerchicalView
                  desktopApproval={desktopApproval}
                  desktopAvailable={desktopAvailable}
                  fileDraft={glitchFileDraft}
                  filePath={glitchFilePath}
                  fileStatus={glitchFileStatus}
                  onApproveDesktop={handleDesktopApproval}
                  onChangeDraft={setGlitchFileDraft}
                  onChangeFilePath={setGlitchFilePath}
                  onChangeCommand={setTerchicalCommand}
                  onChangeShell={setTerchicalShell}
                  onQuickCommand={(value) => {
                    setActiveNav('tools')
                    setRightMode('terchical')
                    setInput(value)
                  }}
                  onOpenPath={() => void runDesktopAction('openPath', { path: glitchFilePath })}
                  onreadFile={() => void runDesktopAction('readFile', { path: glitchFilePath })}
                  onRunCommand={() => void runDesktopAction('exec', { command: terchicalCommand, shell: terchicalShell, timeoutMs: 480000 })}
                  onWriteFile={() => void runDesktopAction('writeFile', { path: glitchFilePath, content: glitchFileDraft })}
                  output={terchicalOutput}
                  terchicalCommand={terchicalCommand}
                  terchicalShell={terchicalShell}
                />
              ) : selectedRightMode === 'anthill' ? (
                <AnthillView agents={anthillAgents} />
              ) : selectedRightMode === 'evidence' ? (
                <EvidenceView agentFeed={agentFeed} desktopApproval={desktopApproval} desktopFeed={desktopFeed} onApproveDesktop={handleDesktopApproval} />
              ) : selectedRightMode === 'city' ? (
                <CityView cityMap={cityMap} selectedDepartment={selectedDepartment} />
              ) : (
                <HudView
                  buddy={buddy}
                  ecosystem={ecosystem}
                  humanTasks={humanTasks}
                  observacionismoState={observacionismoState}
                  onTaskAnswerChange={(taskId, value) =>
                    setTaskAnswers((current) => ({
                      ...current,
                      [taskId]: value
                    }))
                  }
                  onTaskSubmit={handleTaskresponse}
                  taskAnswers={taskAnswers}
                  voiceCommandsState={voiceCommandsState}
                  voiceStatus={voiceStatus}
                />
              )}
            </div>
          </div>
        </aside>
      </div>
    </div>
  )
}

function ArgusMark({ compact = false }: { compact?: boolean }) {
  return (
    <div className={`voice-orb relative overflow-hidden rounded-[32px] border border-cyan-300/20 bg-black/25 ${compact ? 'h-16 w-16' : 'h-20 w-20'}`}>
      <svg className="h-full w-full" viewBox="0 0 256 256" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="256" height="256" rx="56" fill="#07090F" />
        <path d="M58 80L128 42L198 80L128 116L58 80Z" fill="#101924" stroke="#00E5FF" strokeWidth="10" />
        <path d="M58 80V144L128 182V116L58 80Z" fill="#0B121A" stroke="#00E5FF" strokeWidth="10" />
        <path d="M198 80V144L128 182V116L198 80Z" fill="#10212D" stroke="#00E5FF" strokeWidth="10" />
        <path d="M74 136C90 116 110 106 128 106C146 106 166 116 182 136C166 156 146 166 128 166C110 166 90 156 74 136Z" fill="#121B27" stroke="#FFD368" strokeWidth="8" />
        <circle cx="128" cy="136" r="18" fill="#00E5FF" />
        <path d="M106 58H118V74H106V58Z" fill="#FFB300" />
        <path d="M138 58H150V74H138V58Z" fill="#FFB300" />
        <path d="M92 196L128 182L164 196" stroke="#FFB300" strokeWidth="8" strokeLinecap="round" />
      </svg>
    </div>
  )
}

function ProfileButton({
  active,
  label,
  onClick,
  short
}: {
  active: boolean
  label: string
  onClick: () => void
  short: string
}) {
  return (
    <button
      className={`touch-target rounded-[22px] border px-3 py-3 text-left transition duration-200 ease-observatory ${
        active
          ? 'border-cyan-300/35 bg-cyan-300/10 text-slate-50 shadow-aura'
          : 'border-white/8 bg-white/[0.03] text-slate-300 hover:border-white/14 hover:bg-white/[0.05]'
      }`}
      onClick={onClick}
      type="button"
    >
      <div className="text-sm font-semibold">{label}</div>
      <div className="text-xs text-slate-500">{short}</div>
    </button>
  )
}

function NavButton({
  active,
  compact,
  label,
  detail,
  onClick
}: {
  active: boolean
  compact: boolean
  label: string
  detail: string
  onClick: () => void
}) {
  return (
    <button
      className={`touch-target w-full rounded-[22px] border px-3 py-3 text-left transition duration-200 ease-observatory ${
        active
          ? 'border-cyan-300/35 bg-cyan-300/10 text-slate-50'
          : 'border-white/8 bg-white/[0.03] text-slate-300 hover:border-white/14 hover:bg-white/[0.05]'
      }`}
      onClick={onClick}
      type="button"
    >
      {compact ? (
        <div className="text-center text-xs font-semibold uppercase tracking-[0.18em]">{label.slice(0, 4)}</div>
      ) : (
        <>
          <div className="text-sm font-semibold">{label}</div>
          <div className="text-xs text-slate-500">{detail}</div>
        </>
      )}
    </button>
  )
}

function ConnectionBadge({ state }: { state: ConnectionState }) {
  const styleMap: Record<ConnectionState, string> = {
    connecting: 'border-white/10 bg-white/[0.04] text-slate-200',
    connected: 'border-emerald-300/30 bg-emerald-300/10 text-emerald-100',
    slow: 'border-amber-300/30 bg-amber-300/10 text-amber-50',
    offline: 'border-rose-300/30 bg-rose-300/10 text-rose-100'
  }

  const labels: Record<ConnectionState, string> = {
    connecting: 'Conectando',
    connected: 'En línea',
    slow: 'Lento',
    offline: 'Sin conexión'
  }

  return <div className={`rounded-full border px-3 py-2 text-xs font-semibold uppercase tracking-[0.22em] ${styleMap[state]}`}>{labels[state]}</div>
}

function StatusBadge({ label, value, tone }: { label: string; value: number; tone: 'cool' | 'warm' | 'danger' | 'mint' }) {
  const styleMap = {
    cool: 'border-cyan-300/30 bg-cyan-300/10 text-cyan-50',
    warm: 'border-amber-300/30 bg-amber-300/10 text-amber-50',
    danger: 'border-rose-300/30 bg-rose-300/10 text-rose-100',
    mint: 'border-emerald-300/30 bg-emerald-300/10 text-emerald-100'
  }
  return (
    <div className={`rounded-full border px-3 py-2 text-xs font-semibold uppercase tracking-[0.22em] ${styleMap[tone]}`}>
      {label} {formatMetric(value)}
    </div>
  )
}

function MetricTile({ label, value, tone }: { label: string; value: string; tone: 'cool' | 'warm' | 'danger' | 'mint' }) {
  const styleMap = {
    cool: 'border-cyan-300/25 bg-cyan-300/10 text-cyan-50',
    warm: 'border-amber-300/25 bg-amber-300/10 text-amber-50',
    danger: 'border-rose-300/25 bg-rose-300/10 text-rose-100',
    mint: 'border-emerald-300/25 bg-emerald-300/10 text-emerald-100'
  }
  return (
    <div className={`rounded-[20px] border px-3 py-3 text-center ${styleMap[tone]}`}>
      <div className="text-[10px] uppercase tracking-[0.24em] text-slate-300">{label}</div>
      <div className="mt-2 text-lg font-semibold">{value}</div>
    </div>
  )
}

function HudMetric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-[20px] border border-white/8 bg-black/15 px-3 py-3">
      <div className="text-[10px] uppercase tracking-[0.22em] text-slate-500">{label}</div>
      <div className="mt-2 text-sm font-semibold text-slate-100">{value}</div>
    </div>
  )
}

function MiniIndicator({ label, value, tone }: { label: string; value: string; tone: 'cool' | 'warm' | 'danger' | 'mint' }) {
  const styleMap = {
    cool: 'border-cyan-300/25 bg-cyan-300/10 text-cyan-50',
    warm: 'border-amber-300/25 bg-amber-300/10 text-amber-50',
    danger: 'border-rose-300/25 bg-rose-300/10 text-rose-100',
    mint: 'border-emerald-300/25 bg-emerald-300/10 text-emerald-100'
  }
  return (
    <div className={`flex h-14 w-14 flex-col items-center justify-center rounded-[20px] border text-center ${styleMap[tone]}`}>
      <div className="text-[9px] uppercase tracking-[0.22em]">{label}</div>
      <div className="mt-1 text-xs font-semibold">{value}</div>
    </div>
  )
}

function ModeButton({ active, label, onClick }: { active: boolean; label: string; onClick: () => void }) {
  return (
    <button
      className={`touch-target rounded-full border px-4 py-2 text-xs font-semibold uppercase tracking-[0.24em] transition duration-200 ease-observatory ${
        active
          ? 'border-cyan-300/35 bg-cyan-300/15 text-cyan-50'
          : 'border-white/10 bg-white/[0.03] text-slate-400 hover:border-white/20 hover:text-slate-100'
      }`}
      onClick={onClick}
      type="button"
    >
      {label}
    </button>
  )
}

function HudView({
  buddy,
  ecosystem,
  humanTasks,
  observacionismoState,
  onTaskAnswerChange,
  onTaskSubmit,
  taskAnswers,
  voiceCommandsState,
  voiceStatus
}: {
  buddy: BuddyStatus | null
  ecosystem: EcosystemStatus | null
  humanTasks: HumanTask[]
  observacionismoState: ReturnType<typeof getObservacionismoState>
  onTaskAnswerChange: (taskId: string, value: string) => void
  onTaskSubmit: (taskId: string) => void
  taskAnswers: Record<string, string>
  voiceCommandsState: {
    supported: boolean
    listening: boolean
    error: string
  }
  voiceStatus: VoiceStatus | null
}) {
  return (
    <div className="space-y-4">
      <div className="glass-panel-warm px-4 py-4">
        <div className="eyebrow mb-2">Argus HUD</div>
        <div className="grid grid-cols-2 gap-3">
          <HudMetric label="Modo" value={buddy?.mode || 'offline'} />
          <HudMetric label="Drift" value={buddy ? `${formatMetric(buddy.drift.score)} - ${buddy.drift.mode}` : '-'} />
          <HudMetric label="Nodo" value={buddy?.system.node || 'PC1'} />
          <HudMetric label="Modelo" value={buddy?.system.model || 'gemma4:e4b'} />
        </div>
        <div className="mt-4 grid grid-cols-3 gap-2">
          <MetricTile label="R" value={formatMetric(buddy?.observacionismo.r)} tone={observacionismoState.tone} />
          <MetricTile label="Phi" value={formatMetric(buddy?.observacionismo.phi_eff)} tone="cool" />
          <MetricTile label="Jc" value={formatMetric(buddy?.observacionismo.j_c)} tone="warm" />
        </div>
      </div>

      <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
        <div className="eyebrow mb-3">Voz y ayuda</div>
        <div className="grid grid-cols-2 gap-3">
          <HudMetric label="UI voz" value={voiceCommandsState.listening ? 'escuchando' : voiceCommandsState.supported ? 'lista' : 'sin soporte'} />
          <HudMetric label="Daemon voz" value={voiceStatus?.running ? 'activo' : 'apagado'} />
          <HudMetric label="Wake word" value={(voiceStatus?.wake_words || ['claudio']).join(', ')} />
          <HudMetric label="Ayuda" value={voiceCommandsState.error || 'lista'} />
        </div>
      </div>

      <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
        <div className="eyebrow mb-3">Buddy queries</div>
        {humanTasks.length ? (
          <div className="space-y-3">
            {humanTasks.map((task) => (
              <div key={task.task_id} className="rounded-[20px] border border-white/6 bg-black/15 px-3 py-3">
                <div className="text-sm text-slate-100">{task.question}</div>
                <div className="mt-1 text-[11px] uppercase tracking-[0.2em] text-slate-500">
                  {task.node_id} - {task.created_ago_secs}s
                </div>
                <div className="mt-3 flex gap-2">
                  <input
                    className="focus-ring flex-1 rounded-full border border-white/10 bg-black/20 px-3 py-2 text-sm text-slate-100 outline-none"
                    onChange={(event) => onTaskAnswerChange(task.task_id, event.target.value)}
                    placeholder="respuesta humana"
                    value={taskAnswers[task.task_id] || ''}
                  />
                  <button
                    className="action-chip border-cyan-300/30 bg-cyan-300/15 text-cyan-50"
                    onClick={() => onTaskSubmit(task.task_id)}
                    type="button"
                  >
                    Enviar
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-sm text-slate-400">No hay aprobaciones humanas pendientes.</div>
        )}
      </div>

      <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
        <div className="eyebrow mb-3">red activa</div>
        <div className="space-y-2">
          {Object.entries(ecosystem?.nodos || {}).map(([name, node]) => (
            <div key={name} className="flex items-center justify-between gap-3 rounded-2xl border border-white/6 bg-black/15 px-3 py-3 text-sm">
              <div className="font-medium text-slate-100">{name}</div>
              <div className="text-right text-xs text-slate-500">{Object.entries(node).map(([key, value]) => `${key}:${String(value)}`).join(' | ')}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function CityView({
  cityMap,
  selectedDepartment
}: {
  cityMap: CityMap | null
  selectedDepartment: CityDepartment | null
}) {
  return (
    <div className="space-y-4">
      <div className="pixel-city-frame scanlines">
        <div className="pixel-grid absolute inset-0 opacity-50" />
        <img alt="Ciudad Claudio pixel art" className="h-52 w-full object-cover opacity-95" src="/city-pixel-scene.svg" />
        <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-[#06080f] via-[#06080f]/90 to-transparent px-4 py-4">
          <div className="eyebrow mb-1">Ciudad Claudio RPG</div>
          <div className="text-xl font-semibold text-slate-50">Mapa vivo para el metroidvania observacionista</div>
          <div className="mt-1 text-sm text-slate-400">
            Selecciona una zona, revisa sus torres y usa el chat como interfaz del mundo.
          </div>
        </div>
      </div>

      {selectedDepartment && (
        <div className="pixel-card px-4 py-4">
          <div className="eyebrow mb-2">Zona activa</div>
          <div className="text-lg font-semibold text-slate-50">{selectedDepartment.name}</div>
          <div className="mt-1 text-sm text-slate-400">{selectedDepartment.personaje} - {selectedDepartment.ring} - {selectedDepartment.tech}</div>
          <p className="mt-3 text-sm leading-7 text-slate-300">{selectedDepartment.context_hint}</p>
        </div>
      )}

      <div className="grid gap-3 md:grid-cols-2">
        {(cityMap?.departments || []).slice(0, 8).map((department) => (
          <div key={department.slug} className="pixel-card px-4 py-4">
            <div className="text-[10px] uppercase tracking-[0.24em] text-cyan-200/70">{String(department.number).padStart(2, '0')}</div>
            <div className="mt-2 text-lg font-semibold text-slate-50">{department.name}</div>
            <div className="mt-1 text-sm text-slate-400">{department.personaje}</div>
            <div className="mt-3 text-xs leading-6 text-slate-400">{department.context_hint}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

function VisionView({
  cameraStatus,
  hubAvailable,
  hubStreamUrl,
  imageUrl,
  isBusy,
  liveVision,
  onChangeSource,
  onToggle,
  onToggleDescribe,
  onUseSpeed
}: {
  cameraStatus: CameraStatus | null
  hubAvailable: boolean
  hubStreamUrl: string
  imageUrl: string
  isBusy: boolean
  liveVision: LiveVisionState
  onChangeSource: (source: LiveVisionState['source']) => void
  onToggle: () => void
  onToggleDescribe: () => void
  onUseSpeed: (intervalMs: number) => void
}) {
  const streamLive = liveVision.enabled && hubAvailable
  const displayUrl = streamLive ? hubStreamUrl : imageUrl
  const modeLabel = streamLive ? 'MJPEG Hub' : liveVision.enabled ? 'snapshot' : 'pausa'
  return (
    <div className="space-y-4">
      <div className="glass-panel-warm px-4 py-4">
        <div className="mb-3 flex items-center justify-between gap-3">
          <div>
            <div className="eyebrow mb-1">Visión en tiempo real</div>
            <div className="text-lg font-semibold text-slate-50">Imagen y video para Claudio</div>
          </div>
          <button
            className={`touch-target rounded-full border px-4 py-2 text-sm font-semibold transition duration-200 ease-observatory ${
              liveVision.enabled
                ? 'border-emerald-300/30 bg-emerald-300/10 text-emerald-100'
                : 'border-white/10 bg-white/[0.04] text-slate-200'
            }`}
            onClick={onToggle}
            type="button"
          >
            {liveVision.enabled ? 'Detener' : 'Activar'}
          </button>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <HudMetric label="Modelo" value={cameraStatus?.vision_model || 'Sin modelo'} />
          <HudMetric label="Frames" value={String(cameraStatus?.frames_captured || 0)} />
          <HudMetric label="Fuente" value={`${liveVision.source} • ${modeLabel}`} />
          <HudMetric label="Estado" value={isBusy ? 'analizando' : liveVision.enabled ? 'activo' : 'en pausa'} />
        </div>
      </div>

      <div className="pixel-panel px-4 py-4">
        <div className="mb-3 flex flex-wrap gap-2">
          {(['auto', 'pc', 'oppo_adb', 'oppo_webcam'] as const).map((source) => (
            <button
              className={`touch-target rounded-full border px-3 py-2 text-xs font-semibold uppercase tracking-[0.18em] ${
                liveVision.source === source
                  ? 'border-cyan-300/35 bg-cyan-300/10 text-cyan-50'
                  : 'border-white/10 bg-white/[0.03] text-slate-400'
              }`}
              key={source}
              onClick={() => onChangeSource(source)}
              type="button"
            >
              {source}
            </button>
          ))}
        </div>
        <img
          alt={streamLive ? 'Transmisión en vivo desde el Hub' : 'Snapshot de cámara'}
          className="aspect-video w-full rounded-[24px] border border-white/10 object-cover"
          height="720"
          loading="eager"
          src={displayUrl}
          width="1280"
        />
        <div className="mt-2 text-[11px] uppercase tracking-[0.22em] text-slate-500">
          {streamLive
            ? 'Stream MJPEG en vivo (Screen Hub 7474)'
            : liveVision.enabled
              ? 'Hub no disponible: usando snapshot del API'
              : 'Activa la visión para ver la escena en vivo'}
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          <button
            className={`action-chip ${liveVision.autoDescribe ? 'border-amber-300/30 bg-amber-300/10 text-amber-50' : ''}`}
            onClick={onToggleDescribe}
            type="button"
          >
            Describir {liveVision.autoDescribe ? 'on' : 'off'}
          </button>
          {[1800, 3200, 5200].map((speed) => (
            <button
              className={`action-chip ${liveVision.intervalMs === speed ? 'border-cyan-300/30 bg-cyan-300/10 text-cyan-50' : ''}`}
              key={speed}
              onClick={() => onUseSpeed(speed)}
              type="button"
            >
              {speed / 1000}s
            </button>
          ))}
        </div>
      </div>

      <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
        <div className="eyebrow mb-3">Descripción</div>
        <div className="text-sm leading-7 text-slate-300">
          {liveVision.lastDescription || cameraStatus?.last_description || 'Activa la visión para empezar a describir la escena.'}
        </div>
        <div className="mt-2 text-xs text-slate-500">
          {liveVision.lastUpdated ? `Última actualización: ${new Date(liveVision.lastUpdated).toLocaleTimeString('es-MX')}` : 'Sin actualización todavía'}
        </div>
      </div>
    </div>
  )
}

function describeRadiocinemaTool(tool: RadiocinemaTool): string {
  if (tool.id === 'open_generative_ai') {
    if (tool.status === 'repo_ready') {
      return 'Repo integrado en Claudio; levanta studio por npm y deja preview local listo.'
    }
    if (tool.status === 'repo_cloned') {
      return 'El repo ya esta dentro de Claudio, pero todavia le faltan dependencias o build.'
    }
    if (tool.status === 'desktop_installed') {
      return 'Studio instalado como app local y listo para abrir directo.'
    }
  }
  return tool.description || 'Abrir tool'
}

function getRadiocinemaToolMeta(tool: RadiocinemaTool): string[] {
  const meta: string[] = []
  if (tool.status === 'repo_ready') {
    meta.push('repo listo')
  } else if (tool.status === 'repo_cloned') {
    meta.push('repo clonado')
  } else if (tool.status === 'desktop_installed') {
    meta.push('app instalada')
  }
  if (tool.launch_mode === 'npm_script') {
    meta.push('npm')
  } else if (tool.launch_mode === 'binary') {
    meta.push('app')
  }
  if (tool.default_url) {
    meta.push(tool.default_url.replace(/^https?:\/\//, ''))
  }
  if (tool.dist_ready) {
    meta.push('dist')
  }
  return meta.slice(0, 4)
}

function StudioView({
  detail,
  isGenerating,
  launchingTool,
  log,
  onDetailChange,
  onGenerate,
  onLaunchTool,
  onPromptChange,
  onStyleChange,
  prompt,
  radiocinemaStatus,
  style,
  tools
}: {
  detail: string
  isGenerating: boolean
  launchingTool: string | null
  log: Array<Record<string, unknown>>
  onDetailChange: (value: string) => void
  onGenerate: () => Promise<void>
  onLaunchTool: (toolId: string) => Promise<void>
  onPromptChange: (value: string) => void
  onStyleChange: (value: string) => void
  prompt: string
  radiocinemaStatus: RadiocinemaStatus | null
  style: string
  tools: RadiocinemaTool[]
}) {
  const availableTools = tools.filter((tool) => tool.available)
  const missingTools = tools.filter((tool) => !tool.available)
  const openGenerativeTool = tools.find((tool) => tool.id === 'open_generative_ai') || null
  return (
    <div className="space-y-4">
      <div className="glass-panel-warm px-4 py-4">
        <div className="eyebrow mb-2">Radiocinema studio</div>
        <div className="text-lg font-semibold text-slate-50">Prompts primero, producción abierta y herramientas libres</div>
        <div className="mt-2 text-sm text-slate-400">
          Blender, Inkscape, Ardour y el resto entran aquí como extensión del canvas creativo.
        </div>
      </div>

      <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
        <div className="grid gap-3">
          <input
            aria-label="Prompt principal de Radiocinema"
            autoComplete="off"
            className="focus-ring rounded-[18px] border border-white/10 bg-black/20 px-4 py-3 text-sm text-slate-100 outline-none"
            name="studio_prompt"
            onChange={(event) => onPromptChange(event.target.value)}
            placeholder="Proyecto o prompt principal"
            value={prompt}
          />
          <textarea
            aria-label="Detalle creativo del proyecto"
            autoComplete="off"
            className="focus-ring min-h-[110px] rounded-[18px] border border-white/10 bg-black/20 px-4 py-3 text-sm text-slate-100 outline-none"
            name="studio_detail"
            onChange={(event) => onDetailChange(event.target.value)}
            placeholder="Capítulo, escena, emoción, BPM o notas de producción"
            value={detail}
          />
          <div className="flex flex-wrap items-center gap-2">
            {['binaural', 'music', 'ambience', 'narrative'].map((option) => (
              <button
                className={`touch-target rounded-full border px-3 py-2 text-xs font-semibold uppercase tracking-[0.18em] ${
                  style === option
                    ? 'border-cyan-300/35 bg-cyan-300/10 text-cyan-50'
                    : 'border-white/10 bg-white/[0.03] text-slate-400'
                }`}
                key={option}
                onClick={() => onStyleChange(option)}
                type="button"
              >
                {option}
              </button>
            ))}
          </div>
          <button
            className="touch-target rounded-[22px] border border-cyan-300/30 bg-cyan-300/15 px-4 py-4 text-sm font-semibold text-cyan-50 transition duration-200 ease-observatory hover:-translate-y-0.5 disabled:cursor-not-allowed disabled:opacity-50"
            disabled={isGenerating}
            onClick={() => void onGenerate()}
            type="button"
          >
            {isGenerating ? 'Generando…' : 'Lanzar studio'}
          </button>
        </div>
      </div>

      <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
        <div className="mb-3 flex items-center justify-between">
          <div className="eyebrow">Taller creativo ({availableTools.length}/{tools.length})</div>
          <div className="text-[11px] uppercase tracking-[0.22em] text-slate-500">abrir tool local</div>
        </div>
        {openGenerativeTool ? (
          <div className="mb-3 rounded-[18px] border border-cyan-300/20 bg-cyan-300/5 px-3 py-3">
            <div className="text-sm font-semibold text-cyan-50">Open Generative AI</div>
            <div className="mt-1 text-[11px] leading-snug text-cyan-100/80">
              {describeRadiocinemaTool(openGenerativeTool)}
            </div>
            {getRadiocinemaToolMeta(openGenerativeTool).length ? (
              <div className="mt-2 flex flex-wrap gap-1.5">
                {getRadiocinemaToolMeta(openGenerativeTool).map((meta) => (
                  <span
                    className="rounded-full border border-cyan-300/15 bg-black/20 px-2 py-0.5 text-[9px] uppercase tracking-[0.16em] text-cyan-100/75"
                    key={`open-generative-${meta}`}
                  >
                    {meta}
                  </span>
                ))}
              </div>
            ) : null}
          </div>
        ) : null}
        {availableTools.length === 0 && tools.length === 0 ? (
          <div className="text-sm text-slate-400">Detectando herramientas…</div>
        ) : availableTools.length === 0 ? (
          <div className="text-sm text-slate-400">Ninguna herramienta creativa detectada todavía.</div>
        ) : (
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-3">
            {availableTools.map((tool) => (
              <button
                className="action-chip flex flex-col items-start gap-1 rounded-[18px] border border-emerald-300/20 bg-emerald-300/5 px-3 py-3 text-left text-xs text-emerald-50 transition disabled:cursor-not-allowed disabled:opacity-50"
                disabled={launchingTool === tool.id}
                key={tool.id}
                onClick={() => void onLaunchTool(tool.id)}
                title={tool.repo_path || tool.path || tool.description}
                type="button"
              >
                <span className="text-sm font-semibold text-emerald-50">{tool.label}</span>
                <span className="text-[10px] uppercase tracking-[0.2em] text-emerald-200/70">{tool.category}</span>
                {getRadiocinemaToolMeta(tool).length ? (
                  <div className="mt-1 flex flex-wrap gap-1">
                    {getRadiocinemaToolMeta(tool).map((meta) => (
                      <span
                        className="rounded-full border border-emerald-300/15 bg-black/20 px-2 py-0.5 text-[9px] uppercase tracking-[0.16em] text-emerald-100/70"
                        key={`${tool.id}-${meta}`}
                      >
                        {meta}
                      </span>
                    ))}
                  </div>
                ) : null}
                <span className="mt-1 text-[11px] leading-snug text-emerald-100/80">
                  {launchingTool === tool.id ? 'Abriendo…' : describeRadiocinemaTool(tool)}
                </span>
              </button>
            ))}
          </div>
        )}
        {missingTools.length > 0 ? (
          <div className="mt-3 rounded-[16px] border border-white/5 bg-black/20 px-3 py-2 text-[11px] text-slate-500">
            No detectadas: {missingTools.map((tool) => tool.label).join(' • ')}
          </div>
        ) : null}
      </div>

      <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
        <div className="eyebrow mb-3">Estado del studio</div>
        <pre className="overflow-x-auto rounded-2xl border border-white/6 bg-black/20 p-3 text-xs text-slate-300">
          {previewJson(radiocinemaStatus?.studio || radiocinemaStatus?.active_job || { status: 'sin datos' })}
        </pre>
      </div>

      <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
        <div className="eyebrow mb-3">Bitácora reciente</div>
        <div className="space-y-2">
          {log.length ? log.map((entry, index) => (
            <div key={index} className="rounded-[20px] border border-white/6 bg-black/15 px-3 py-3 text-sm text-slate-300">
              {previewJson(entry)}
            </div>
          )) : <div className="text-sm text-slate-400">Sin eventos recientes.</div>}
        </div>
      </div>
    </div>
  )
}

function CanvasView({
  artifact,
  onApprove,
  onArtifactChange,
  pendingApproval
}: {
  artifact: ArtifactDraft | null
  onApprove: (approved: boolean) => void
  onArtifactChange: (code: string) => void
  pendingApproval: PendingApproval | null
}) {
  return (
    <div className="space-y-4">
      <div className="glass-panel-warm px-4 py-4">
        <div className="eyebrow mb-2">Artefacto activo</div>
        <div className="text-sm text-slate-400">
          {artifact ? `${artifact.title} - ${artifact.language}` : 'Aún no hay artefacto elevado desde la sesión.'}
        </div>
      </div>

      <div className="overflow-hidden rounded-[26px] border border-white/8 bg-[#05070b]">
        <CodeMirror
          basicSetup={{
            lineNumbers: true,
            foldGutter: true,
            highlightActiveLine: true
          }}
          extensions={artifact?.language === 'python' ? [python()] : [javascript({ jsx: true, typescript: true })]}
          height="420px"
          onChange={onArtifactChange}
          theme="dark"
          value={artifact?.code || '// El canvas mostrará aquí el código detectado en la respuesta del runtime.'}
        />
      </div>

      {pendingApproval ? (
        <div className="rounded-[24px] border border-amber-300/30 bg-amber-300/10 px-4 py-4">
          <div className="eyebrow mb-2 text-amber-100/80">ObservacionismoGate</div>
          <div className="text-sm font-semibold text-slate-50">{pendingApproval.tool}</div>
          <pre className="mt-3 overflow-x-auto rounded-2xl border border-black/20 bg-black/25 p-3 text-xs text-slate-300">
            {pendingApproval.args}
          </pre>
          <div className="mt-4 flex gap-2">
            <button className="action-chip border-cyan-300/30 bg-cyan-300/15 text-cyan-50" onClick={() => onApprove(true)} type="button">
              Aplicar
            </button>
            <button className="action-chip border-rose-300/30 bg-rose-300/10 text-rose-100" onClick={() => onApprove(false)} type="button">
              rechazar
            </button>
          </div>
        </div>
      ) : (
        <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4 text-sm text-slate-400">
          Sin tool call pendiente. El botón Aplicar aparecerá cuando HookGateway pida aprobación humana.
        </div>
      )}
    </div>
  )
}

function TerchicalView({
  desktopApproval,
  desktopAvailable,
  fileDraft,
  filePath,
  fileStatus,
  onApproveDesktop,
  onChangeDraft,
  onChangeFilePath,
  onChangeCommand,
  onChangeShell,
  onQuickCommand,
  onOpenPath,
  onreadFile,
  onRunCommand,
  onWriteFile,
  output,
  terchicalCommand,
  terchicalShell
}: {
  desktopApproval: DesktopApproval | null
  desktopAvailable: boolean
  fileDraft: string
  filePath: string
  fileStatus: string
  onApproveDesktop: (approved: boolean) => void
  onChangeDraft: (value: string) => void
  onChangeFilePath: (value: string) => void
  onChangeCommand: (value: string) => void
  onChangeShell: (value: TerchicalShellId) => void
  onQuickCommand: (value: string) => void
  onOpenPath: () => void
  onreadFile: () => void
  onRunCommand: () => void
  onWriteFile: () => void
  output: string
  terchicalCommand: string
  terchicalShell: TerchicalShellId
}) {
  return (
    <div className="space-y-4">
      <div className="glass-panel-warm px-4 py-4">
        <div className="eyebrow mb-2">Claudio Glitch</div>
        <div className="text-lg font-semibold text-slate-50">Terminal, archivos y administración segura</div>
        <div className="mt-2 text-sm text-slate-400">
          {desktopAvailable ? 'Bridge de escritorio disponible.' : 'En web y PWA solo se muestra la vista. La ejecución real requiere Desktop.'}
        </div>
      </div>

      {desktopApproval && (
        <div className="rounded-[24px] border border-amber-300/30 bg-amber-300/10 px-4 py-4">
          <div className="eyebrow mb-2 text-amber-100/80">Aprobación humana</div>
          <div className="text-sm text-slate-100">{desktopApproval.gate.reason}</div>
          <div className="mt-1 text-xs text-slate-500">Modo PSI: {desktopApproval.gate.obs_mode}</div>
          <div className="mt-4 flex gap-2">
            <button className="action-chip border-cyan-300/30 bg-cyan-300/15 text-cyan-50" onClick={() => onApproveDesktop(true)} type="button">
              Autorizar
            </button>
            <button className="action-chip border-rose-300/30 bg-rose-300/10 text-rose-100" onClick={() => onApproveDesktop(false)} type="button">
              Cancelar
            </button>
          </div>
        </div>
      )}

      <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
        <div className="eyebrow mb-3">Terminal</div>
        <div className="mb-3 flex flex-wrap gap-2">
          {[
            { label: 'PS7', value: '/ps7 ' },
            { label: 'Nemo', value: '/nemo ' },
            { label: 'ClawdWorks', value: '/cw ' },
            { label: LIBRARY_LABEL, value: '/libros' }
          ].map((item) => (
            <button
              className="action-chip"
              key={item.label}
              onClick={() => onQuickCommand(item.value)}
              type="button"
            >
              {item.label}
            </button>
          ))}
        </div>
        <div className="flex flex-col gap-2 xl:flex-row">
          <select
            aria-label="Shell local"
            className="focus-ring touch-target rounded-full border border-white/10 bg-black/20 px-3 py-2 text-sm text-slate-100 outline-none xl:w-[180px]"
            name="terchical_shell"
            onChange={(event) => onChangeShell(event.target.value as TerchicalShellId)}
            value={terchicalShell}
          >
            <option value="pwsh">PowerShell 7</option>
            <option value="powershell">Windows PowerShell</option>
            <option value="cmd">CMD</option>
          </select>
          <input
            aria-label="Comando PowerShell"
            autoComplete="off"
            className="focus-ring flex-1 rounded-full border border-white/10 bg-black/20 px-3 py-2 text-sm text-slate-100 outline-none"
            name="terchical_command"
            onChange={(event) => onChangeCommand(event.target.value)}
            placeholder="Comando PowerShell"
            value={terchicalCommand}
          />
          <button className="action-chip border-cyan-300/30 bg-cyan-300/15 text-cyan-50" onClick={onRunCommand} type="button">
            Ejecutar
          </button>
        </div>
        <div className="mt-3 rounded-[18px] border border-white/6 bg-black/20 px-3 py-3 text-xs leading-6 text-slate-400">
          También puedes usar el chat con <code>/ps7</code>, <code>/nemo</code>, <code>/cw</code>, <code>/leer</code> y <code>/libros</code>.
        </div>
        <pre className="mt-3 overflow-x-auto rounded-2xl border border-white/6 bg-black/35 p-3 text-xs text-slate-300">
          {output}
        </pre>
      </div>

      <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
        <div className="eyebrow mb-3">Archivos</div>
        <input
          aria-label="Ruta absoluta del archivo"
          autoComplete="off"
          className="focus-ring w-full rounded-[18px] border border-white/10 bg-black/20 px-3 py-3 text-sm text-slate-100 outline-none"
          name="file_path"
          onChange={(event) => onChangeFilePath(event.target.value)}
          placeholder="Ruta absoluta del archivo"
          value={filePath}
        />
        <div className="mt-3 flex flex-wrap gap-2">
          <button className="action-chip" onClick={onreadFile} type="button">Leer</button>
          <button className="action-chip" onClick={onWriteFile} type="button">Guardar</button>
          <button className="action-chip" onClick={onOpenPath} type="button">Abrir ruta</button>
        </div>
        <div className="mt-2 text-xs text-slate-500">{fileStatus}</div>
        <textarea
          aria-label="Contenido del archivo"
          autoComplete="off"
          className="focus-ring mt-3 min-h-[220px] w-full rounded-[18px] border border-white/10 bg-black/20 px-3 py-3 font-mono text-xs text-slate-100 outline-none"
          name="file_draft"
          onChange={(event) => onChangeDraft(event.target.value)}
          value={fileDraft}
        />
      </div>
    </div>
  )
}

function AnthillView({ agents }: { agents: AnthillAgent[] }) {
  const palette = {
    working: 'border-cyan-300/35 bg-cyan-300/10 text-cyan-100',
    idle: 'border-emerald-300/30 bg-emerald-300/10 text-emerald-100',
    blocked: 'border-rose-300/30 bg-rose-300/10 text-rose-100'
  } as const
  const roleLabels: Record<string, string> = {
    writer: 'Escritor',
    debugger: 'Debugger',
    researcher: 'Investigador',
    tester: 'Tester',
    archivist: 'Archivista',
    observer: 'Observador',
    market_researcher: 'Investigador de mercado',
    monitor: 'Monitor',
    defender: 'Defensor',
    organizer: 'Organizador',
    compressor: 'Compresor'
  }

  const formatRole = (role: string) => {
    const normalized = role.trim().toLowerCase().replace(/\[elichicado\]/g, 'che').replace(/muy/g, 're')
    if (roleLabels[normalized]) return roleLabels[normalized]
    return normalized
      .split('_')
      .filter(Boolean)
      .map((part) => `${part.charAt(0).toUpperCase()}${part.slice(1)}`)
      .join(' ')
  }

  return (
    <div className="space-y-4">
      <div className="glass-panel-warm px-4 py-4">
        <div className="eyebrow mb-2">Hormiguero Argus</div>
        <h3 className="text-lg font-semibold text-slate-50">Agentes visibles, runtime intacto</h3>
        <p className="mt-2 text-sm text-slate-300">
          Vista sandbox para observar roles, estado y tarea actual sin exponer razonamiento interno.
        </p>
      </div>

      <div className="grid gap-3 md:grid-cols-2">
        {agents.length ? (
          agents.map((agent, index) => (
            <article
              key={agent.id}
              className={`rounded-[24px] border px-4 py-4 ${palette[agent.state]}`}
              style={{ animationDelay: `${index * 120}ms` }}
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="text-sm uppercase tracking-[0.22em] text-white/70">{formatRole(agent.role)}</div>
                  <div className="mt-1 text-xl font-semibold">{agent.name}</div>
                </div>
                <div className="relative h-12 w-12 rounded-full border border-white/15 bg-black/20">
                  <div className="absolute inset-3 rounded-full bg-current opacity-75 animate-pulse" />
                  <div className="absolute left-2 top-4 h-1.5 w-8 rounded-full bg-white/75" />
                  <div className="absolute left-4 top-1 h-4 w-1 rounded-full bg-white/55" />
                  <div className="absolute left-7 top-1 h-4 w-1 rounded-full bg-white/55" />
                </div>
              </div>
              <div className="mt-3 text-sm text-white/80">{agent.task}</div>
              <div className="mt-3 flex items-center justify-between text-xs uppercase tracking-[0.16em] text-white/55">
                <span>{agent.state}</span>
                <span>{agent.last_activity}</span>
              </div>
            </article>
          ))
        ) : (
          <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-6 text-sm text-slate-300">
            Sin agentes visibles todavía. El endpoint `/api/agents/state` responderá aquí en cuanto el backend cargue.
          </div>
        )}
      </div>
    </div>
  )
}

function EvidenceView({
  agentFeed,
  desktopApproval,
  desktopFeed,
  onApproveDesktop
}: {
  agentFeed: AgentFeedEntry[]
  desktopApproval: DesktopApproval | null
  desktopFeed: DesktopLogEntry[]
  onApproveDesktop: (approved: boolean) => void
}) {
  return (
    <div className="space-y-4">
      {desktopApproval && (
        <div className="rounded-[24px] border border-amber-300/30 bg-amber-300/10 px-4 py-4">
          <div className="eyebrow mb-2 text-amber-100/80">Gate PSI</div>
          <div className="text-sm text-slate-100">{desktopApproval.gate.reason}</div>
          <div className="mt-4 flex gap-2">
            <button className="action-chip border-cyan-300/30 bg-cyan-300/15 text-cyan-50" onClick={() => onApproveDesktop(true)} type="button">
              Aprobar
            </button>
            <button className="action-chip border-rose-300/30 bg-rose-300/10 text-rose-100" onClick={() => onApproveDesktop(false)} type="button">
              Denegar
            </button>
          </div>
        </div>
      )}

      <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
        <div className="eyebrow mb-3">Evidencia Glitch</div>
        <div className="space-y-2">
          {desktopFeed.length ? desktopFeed.map((entry) => (
            <div key={entry.id} className={`rounded-[20px] border px-3 py-3 ${feedTone(entry.tone)}`}>
              <div className="text-xs uppercase tracking-[0.22em]">{entry.label}</div>
              <div className="mt-2 text-sm leading-6 text-slate-100">{entry.detail}</div>
            </div>
          )) : <div className="text-sm text-slate-400">Sin eventos de escritorio todavía.</div>}
        </div>
      </div>

      <div className="rounded-[24px] border border-white/8 bg-white/[0.03] px-4 py-4">
        <div className="eyebrow mb-3">Feed operativo</div>
        <div className="space-y-2">
          {agentFeed.map((entry) => (
            <div key={entry.id} className={`rounded-[20px] border px-3 py-3 ${feedTone(entry.tone)}`}>
              <div className="text-xs uppercase tracking-[0.22em]">{entry.label}</div>
              <div className="mt-2 text-sm leading-6 text-slate-100">{entry.detail}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

function getSidebarShortcuts(profile: UserProfileId): SidebarShortcut[] {
  if (profile === 'glitch') {
    return [
      { id: 'gl-shortcut-ps7', label: 'PowerShell 7', detail: 'Shell local seguro', kind: 'command', command: '/ps7 ' },
      { id: 'gl-shortcut-nemo', label: 'Nemo', detail: 'research loop', kind: 'command', command: '/nemo ' },
      { id: 'gl-shortcut-cw', label: 'ClawdWorks', detail: 'Bridge print', kind: 'command', command: '/cw ' },
      { id: 'gl-shortcut-libros', label: LIBRARY_LABEL, detail: 'Abrir biblioteca', kind: 'open', path: LIBRARY_TARGET, commandId: 'open_library' }
    ]
  }

  if (profile === 'creative') {
    return [
      { id: 'cr-shortcut-studio', label: 'Studio', detail: 'Radiocinema abierto', kind: 'nav', section: 'radiocinema', view: 'studio' },
      { id: 'cr-shortcut-canvas', label: 'Canvas', detail: 'revisión de artefactos', kind: 'nav', section: 'history', view: 'canvas' },
      { id: 'cr-shortcut-libros', label: LIBRARY_LABEL, detail: 'referencias y libros', kind: 'open', path: LIBRARY_TARGET, commandId: 'open_library' },
      { id: 'cr-shortcut-project', label: 'Proyecto', detail: 'Arrancar brief creativo', kind: 'prompt', prompt: PROMPTS.creative[2].prompt }
    ]
  }

  if (profile === 'nonTechnical') {
    return [
      { id: 'nt-shortcut-help', label: 'Ayuda', detail: 'Explicación simple', kind: 'prompt', prompt: PROMPTS.nonTechnical[0].prompt },
      { id: 'nt-shortcut-story', label: 'Historia', detail: 'Algo amable y breve', kind: 'prompt', prompt: PROMPTS.nonTechnical[1].prompt },
      { id: 'nt-shortcut-play', label: 'Jugar', detail: 'Argus guía el juego', kind: 'prompt', prompt: PROMPTS.nonTechnical[2].prompt },
      { id: 'nt-shortcut-vision', label: 'Visión', detail: 'Panel derecho amable', kind: 'nav', section: 'radiocinema', view: 'vision' }
    ]
  }

  return [
    { id: 'avg-shortcut-chat', label: 'Charla', detail: 'Conversación libre', kind: 'prompt', prompt: PROMPTS.average[0].prompt },
    { id: 'avg-shortcut-image', label: 'Imagen', detail: 'Generar con prompt', kind: 'prompt', prompt: PROMPTS.average[1].prompt },
    { id: 'avg-shortcut-games', label: 'Jugar', detail: 'Trivia o memoria', kind: 'prompt', prompt: MINI_GAMES[0].prompt },
    { id: 'avg-shortcut-city', label: 'Ciudad', detail: 'Mapa RPG activo', kind: 'nav', section: 'tools', view: 'city' }
  ]
}

function deriveRightMode(profile: UserProfileId, activeNav: NavSectionId): RightViewId {
  if (profile === 'glitch') {
    if (activeNav === 'settings') {
      return 'evidence'
    }
    return activeNav === 'tools' ? 'terchical' : 'city'
  }

  if (profile === 'creative') {
    if (activeNav === 'radiocinema') {
      return 'studio'
    }
    if (activeNav === 'history') {
      return 'canvas'
    }
    return 'city'
  }

  if (activeNav === 'settings') {
    return 'hud'
  }
  if (activeNav === 'radiocinema') {
    return 'vision'
  }
  return activeNav === 'tools' ? 'city' : 'hud'
}

function getRightTabs(profile: UserProfileId): Array<{ id: RightViewId; label: string }> {
  if (profile === 'glitch') {
    return [
      { id: 'terchical', label: 'Terminal' },
      { id: 'evidence', label: 'Evidencia' },
      { id: 'anthill', label: 'Hormiguero' },
      { id: 'city', label: 'Ciudad' },
      { id: 'hud', label: 'HUD' }
    ]
  }

  if (profile === 'creative') {
    return [
      { id: 'studio', label: 'Studio' },
      { id: 'canvas', label: 'Canvas' },
      { id: 'anthill', label: 'Hormiguero' },
      { id: 'city', label: 'Ciudad' },
      { id: 'vision', label: 'Visión' }
    ]
  }

  return [
    { id: 'hud', label: 'HUD' },
    { id: 'anthill', label: 'Hormiguero' },
    { id: 'city', label: 'Ciudad' },
    { id: 'vision', label: 'Visión' }
  ]
}

function formatMetric(value?: number | null) {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return '-'
  }
  return value.toFixed(2)
}

function previewJson(value: unknown) {
  if (!value) {
    return 'Sin detalle disponible.'
  }
  try {
    return JSON.stringify(value, null, 2).slice(0, 480)
  } catch {
    return String(value)
  }
}

function getObservacionismoState(buddy: BuddyStatus | null) {
  const r = buddy?.observacionismo.r ?? 0
  if (r > 0.4) {
    return {
      label: 'Jamming',
      tone: 'danger' as const,
      className: 'border-rose-300/30 bg-rose-300/10 text-rose-100',
      statusGlow: 'danger'
    }
  }
  if (r > 0.24) {
    return {
      label: 'Cautela',
      tone: 'warm' as const,
      className: 'border-amber-300/30 bg-amber-300/10 text-amber-50',
      statusGlow: 'warn'
    }
  }
  return {
    label: 'Seguro',
    tone: 'mint' as const,
    className: 'border-emerald-300/30 bg-emerald-300/10 text-emerald-100',
    statusGlow: 'safe'
  }
}

function getPsiSummary(profile: UserProfileId, buddy: BuddyStatus | null) {
  const r = buddy?.observacionismo.r ?? 0
  if (profile === 'average' || profile === 'nonTechnical') {
    if (r > 0.4) {
      return 'Precaución'
    }
    return 'Todo bien'
  }
  if (r > 0.4) {
    return 'Jamming'
  }
  if (r > 0.24) {
    return 'Cautela'
  }
  return 'Seguro'
}

function feedTone(tone: AgentFeedEntry['tone']) {
  if (tone === 'success') {
    return 'border-emerald-300/20 bg-emerald-300/10 text-emerald-100'
  }
  if (tone === 'danger') {
    return 'border-rose-300/20 bg-rose-300/10 text-rose-100'
  }
  if (tone === 'accent') {
    return 'border-cyan-300/20 bg-cyan-300/10 text-cyan-100'
  }
  return 'border-white/8 bg-white/[0.03] text-slate-300'
}

function extractArtifact(markdown: string): ArtifactDraft | null {
  const blocks = [...markdown.matchAll(/```([\w-]+)?\n([\s\S]*?)```/g)]
    .map((match) => ({
      language: (match[1] || 'text').toLowerCase(),
      code: match[2].trim()
    }))
    .filter((block) => block.code.split('\n').length >= 5)
    .sort((a, b) => b.code.length - a.code.length)

  const winner = blocks[0]
  if (!winner) {
    return null
  }

  const language = winner.language.includes('python')
    ? 'python'
    : winner.language.includes('ts') || winner.language.includes('jsx') || winner.language.includes('js')
      ? 'typescript'
      : winner.language

  return {
    language,
    title: 'Artefacto detectado',
    code: winner.code
  }
}
