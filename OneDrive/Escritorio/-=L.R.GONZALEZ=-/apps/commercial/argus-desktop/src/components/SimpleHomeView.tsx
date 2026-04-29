import { useState } from 'react'
import type { KeyboardEvent } from 'react'
import { getCameraSnapshotImageUrl } from '../lib/api'
import { HormigueroPanel } from './HormigueroPanel'
import type {
  CameraStatus,
  ModuleId,
  ModulesStatusresponse,
  OppoMode,
  OppoStatus,
  SensoryFeed,
  VoiceBackendId,
  VoiceBackendsresponse,
  VoiceStatus
} from '../lib/api'

type SimpleMessage = {
  id: string
  role: 'system' | 'user' | 'assistant'
  content: string
  meta?: string
}

type Props = {
  connectionState: 'connecting' | 'connected' | 'slow' | 'offline'
  connectionMessage: string
  messages: SimpleMessage[]
  input: string
  isSending: boolean
  voiceStatus: VoiceStatus | null
  cameraStatus: CameraStatus | null
  modulesStatus: ModulesStatusresponse | null
  voiceBackends: VoiceBackendsresponse | null
  oppoStatus: OppoStatus | null
  sensoryFeed: SensoryFeed | null
  onInputChange: (value: string) => void
  onSend: () => void
  onComposerKeyDown: (event: KeyboardEvent<HTMLTextAreaElement>) => void
  onActionTalk: () => void
  onActionSee: () => void
  onActionWrite: () => void
  onActionHelp: () => void
  onToggleModule: (moduleId: ModuleId) => void
  onSetVoiceBackend: (backend: VoiceBackendId) => void
  onSetOppoMode: (mode: OppoMode) => void
  onOpenTechnicalMode: () => void
  onWakeup?: () => void
}

const ACTIONS = [
  {
    id: 'talk',
    title: 'Voz',
    detail: 'Conversacion local con Argus',
  },
  {
    id: 'see',
    title: 'Vision',
    detail: 'Camara y lectura de escena',
  },
  {
    id: 'write',
    title: 'Writer',
    detail: 'Mesa de escritura MEDIOEVO',
  },
  {
    id: 'help',
    title: 'Soporte',
    detail: 'Ruta simple para resolver bloqueos',
  },
] as const

function humanConnection(state: Props['connectionState']) {
  switch (state) {
    case 'connected':
      return 'listo'
    case 'slow':
      return 'degradado'
    case 'offline':
      return 'sin conexión'
    default:
      return 'conectando'
  }
}

function humanModuleState(modulesStatus: ModulesStatusresponse | null, moduleId: ModuleId) {
  const moduleState = modulesStatus?.modules?.[moduleId]
  if (!moduleState) return 'apagado'
  if (!moduleState.enabled) return 'apagado'
  if (!moduleState.available) return moduleState.reason === 'usb_brom_required' ? 'requiere permiso' : 'no disponible'
  if (moduleState.status === 'fallback') return 'degradado'
  if (moduleState.status === 'requiere_permiso') return 'requiere permiso'
  if (moduleState.status === 'offline') return 'sin conexión'
  return 'listo'
}

function moduleEnabled(modulesStatus: ModulesStatusresponse | null, moduleId: ModuleId) {
  return Boolean(modulesStatus?.modules?.[moduleId]?.enabled)
}

function StatusPill({ label, tone }: { label: string; tone: 'ok' | 'warn' | 'danger' | 'muted' }) {
  return <span className={`simple-pill simple-pill-${tone}`}>{label}</span>
}

export default function SimpleHomeView({
  connectionState,
  connectionMessage,
  messages,
  input,
  isSending,
  voiceStatus,
  cameraStatus,
  modulesStatus,
  voiceBackends,
  oppoStatus,
  sensoryFeed,
  onInputChange,
  onSend,
  onComposerKeyDown,
  onActionTalk,
  onActionSee,
  onActionWrite,
  onActionHelp,
  onToggleModule,
  onSetVoiceBackend,
  onSetOppoMode,
  onOpenTechnicalMode,
  onWakeup,
}: Props) {
  const [snapshotTs, setSnapshotTs] = useState<number | null>(null)
  const [snapshotError, setSnapshotError] = useState<string | null>(null)

  const connectionLabel = humanConnection(connectionState)
  const latestMessages = messages.slice(-8)
  const voiceOn = moduleEnabled(modulesStatus, 'voice_local')
  const cameraOn = moduleEnabled(modulesStatus, 'camera_pc')
  const oppoOn = moduleEnabled(modulesStatus, 'oppo_bridge')
  const voiceBackend = voiceBackends?.selected_backend || 'local'

  function handleTakeSnapshot() {
    if (!cameraOn) {
      setSnapshotError('Activa la cámara primero.')
      return
    }
    setSnapshotError(null)
    setSnapshotTs(Date.now())
  }

  return (
    <div className="simple-shell">
      {connectionState === 'offline' && (
        <section className="simple-offline-banner glass-panel">
          <div className="simple-offline-message">
            <strong>Claudio está dormido.</strong> Los servicios no responden.
          </div>
          <button className="simple-wakeup-button" onClick={onWakeup} type="button">
            Despertar
          </button>
        </section>
      )}
      <section className="simple-hero glass-panel">
        <div className="simple-hero-copy">
          <div className="eyebrow">Argus Control</div>
          <h1 className="simple-title">Consola operativa MEDIOEVO</h1>
          <p className="simple-subtitle">
            Voz, vision, escritura y agentes Conway en una superficie clara.
          </p>
          <div className="simple-status-row">
            <StatusPill label={`Sistema ${connectionLabel}`} tone={connectionState === 'connected' ? 'ok' : connectionState === 'slow' ? 'warn' : connectionState === 'offline' ? 'danger' : 'muted'} />
            <StatusPill label={`Voz ${humanModuleState(modulesStatus, 'voice_local')}`} tone={voiceOn ? 'ok' : 'muted'} />
            <StatusPill label={`Cámara ${humanModuleState(modulesStatus, 'camera_pc')}`} tone={cameraOn ? 'ok' : 'muted'} />
            <StatusPill label={`OPPO ${humanModuleState(modulesStatus, 'oppo_bridge')}`} tone={oppoOn ? 'ok' : 'muted'} />
          </div>
          <div className="simple-connection-note">{connectionMessage}</div>
        </div>
        <div className="simple-hero-media" aria-hidden="true">
          <img src="/medioevo-geodia-plaza.png" alt="" />
          <div className="simple-hero-media-status">
            <span>GEODIA</span>
            <strong>Hormiguero vivo</strong>
          </div>
        </div>
        <button className="simple-tech-button" onClick={onOpenTechnicalMode} type="button">
          Modo técnico
        </button>
      </section>

      <section className="simple-actions">
        {ACTIONS.map((action) => (
          <button
            className="simple-action-card"
            key={action.id}
            onClick={() => {
              if (action.id === 'talk') onActionTalk()
              if (action.id === 'see') onActionSee()
              if (action.id === 'write') onActionWrite()
              if (action.id === 'help') onActionHelp()
            }}
            type="button"
          >
            <div className="simple-action-title">{action.title}</div>
            <div className="simple-action-detail">{action.detail}</div>
          </button>
        ))}
      </section>

      <section className="simple-hormiguero-panel glass-panel">
        <div className="simple-panel-header">
          <div>
            <div className="eyebrow">Hormiguero</div>
            <h2 className="simple-section-title">Agentes Conway trabajando</h2>
          </div>
        </div>
        <HormigueroPanel />
      </section>

      <section className="simple-main-grid">
        <div className="simple-panel glass-panel">
          <div className="simple-panel-header">
            <div>
              <div className="eyebrow">Controles</div>
              <h2 className="simple-section-title">Módulos encendidos</h2>
            </div>
          </div>
          <div className="simple-toggle-list">
            <ModuleToggle
              active={voiceOn}
              detail={voiceStatus?.running ? 'Escuchando y lista para responder' : 'Puede activarse cuando quieras'}
              label="Voz local"
              stateLabel={humanModuleState(modulesStatus, 'voice_local')}
              onClick={() => onToggleModule('voice_local')}
            />
            <ModuleToggle
              active={cameraOn}
              detail={cameraStatus?.last_description || 'Usa la cámara de la PC para describir la escena'}
              label="Cámara"
              stateLabel={humanModuleState(modulesStatus, 'camera_pc')}
              onClick={() => onToggleModule('camera_pc')}
            />
            <ModuleToggle
              active={oppoOn}
              detail={oppoStatus?.adb_online ? `Conectado: ${oppoStatus.device || 'OPPO'}` : 'Sincroniza teléfono y sensores cuando esté conectado'}
              label="OPPO companion"
              stateLabel={humanModuleState(modulesStatus, 'oppo_bridge')}
              onClick={() => onToggleModule('oppo_bridge')}
            />
          </div>

          <div className="simple-inline-group">
            <div className="eyebrow">Backend de voz</div>
            <div className="simple-chip-row">
              {(['local', 'personaplex_remote', 'nemotron_remote'] as VoiceBackendId[]).map((backend) => {
                const item = voiceBackends?.backends?.[backend]
                return (
                  <button
                    className={`simple-chip-button ${voiceBackend === backend ? 'is-active' : ''}`}
                    key={backend}
                    onClick={() => onSetVoiceBackend(backend)}
                    type="button"
                  >
                    <span>{backend === 'local' ? 'Local' : backend === 'personaplex_remote' ? 'PersonaPlex' : 'Nemotron'}</span>
                    <small>{item?.available ? 'listo' : item?.configured ? 'sin conexión' : 'requiere GPU'}</small>
                  </button>
                )
              })}
            </div>
          </div>

          <div className="simple-inline-group">
            <div className="eyebrow">Modo OPPO</div>
            <div className="simple-chip-row">
              {(['sync', 'rooted'] as OppoMode[]).map((mode) => (
                <button
                  className={`simple-chip-button ${oppoStatus?.mode === mode ? 'is-active' : ''}`}
                  key={mode}
                  onClick={() => onSetOppoMode(mode)}
                  type="button"
                >
                  <span>{mode === 'sync' ? 'Sync' : 'Rooted'}</span>
                  <small>{mode === 'sync' ? 'Tiempo real' : 'requiere USB/BROM'}</small>
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="simple-panel glass-panel">
          <div className="simple-panel-header">
            <div>
              <div className="eyebrow">Feed sensorial</div>
              <h2 className="simple-section-title">Lo que Argus está recibiendo</h2>
            </div>
            <button
              className="simple-chip-button"
              onClick={handleTakeSnapshot}
              type="button"
              title={cameraOn ? 'Tomar foto ahora' : 'Activa la cámara primero'}
            >
              Tomar foto
            </button>
          </div>
          {snapshotTs && (
            <div className="simple-snapshot-preview">
              <img
                alt="Snapshot de cámara"
                src={getCameraSnapshotImageUrl('pc') + `&t=${snapshotTs}`}
                onError={() => setSnapshotError('Cámara no disponible o sin permiso.')}
                style={{ width: '100%', borderRadius: 14, marginBottom: 8 }}
              />
            </div>
          )}
          {snapshotError && (
            <p style={{ color: 'var(--warn, #f3be5d)', fontSize: '0.88rem', margin: '0 0 12px' }}>
              {snapshotError}
            </p>
          )}
          <div className="simple-sensory-grid">
            <FeedCard
              title="Audio"
              value={sensoryFeed?.audio.active_source || 'apagado'}
              detail={sensoryFeed?.audio.last_transcription || voiceStatus?.last_command || 'Sin transcripción reciente'}
            />
            <FeedCard
              title="Visión"
              value={sensoryFeed?.vision.active_source || 'apagado'}
              detail={sensoryFeed?.vision.last_description || cameraStatus?.last_description || 'Sin descripción reciente'}
            />
            <FeedCard
              title="OPPO"
              value={sensoryFeed?.oppo.sensor_server || oppoStatus?.sensor_server_state || 'offline'}
              detail={oppoStatus?.adb_online ? `ADB en línea${oppoStatus.device ? `: ${oppoStatus.device}` : ''}` : 'Aún no hay puente activo'}
            />
          </div>
          <div className="simple-event-list">
            {(sensoryFeed?.events || []).slice(-3).map((event) => (
              <div className="simple-event-card" key={`${event.type}-${event.ts}`}>
                <div className="simple-event-type">{event.type}</div>
                <div className="simple-event-value">{event.value}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="simple-chat-grid">
        <div className="simple-panel glass-panel">
          <div className="simple-panel-header">
            <div>
              <div className="eyebrow">Conversación</div>
              <h2 className="simple-section-title">Habla o escribe con Argus</h2>
            </div>
          </div>
          <div className="simple-message-list">
            {latestMessages.map((message) => (
              <div className={`simple-message simple-message-${message.role}`} key={message.id}>
                <div className="simple-message-role">
                  {message.role === 'assistant' ? 'Argus' : message.role === 'user' ? 'Tú' : 'Sistema'}
                </div>
                <div className="simple-message-content">{message.content}</div>
                {message.meta ? <div className="simple-message-meta">{message.meta}</div> : null}
              </div>
            ))}
          </div>
          <div className="simple-composer">
            <textarea
              aria-label="Mensaje para Argus"
              className="simple-composer-input"
              onChange={(event) => onInputChange(event.target.value)}
              onKeyDown={onComposerKeyDown}
              placeholder="Escribe aquí o usa Hablar para activar la voz."
              value={input}
            />
            <button className="simple-send-button" disabled={isSending} onClick={onSend} type="button">
              {isSending ? 'Enviando...' : 'Enviar'}
            </button>
          </div>
        </div>
      </section>
    </div>
  )
}

function ModuleToggle({
  label,
  detail,
  active,
  stateLabel,
  onClick,
}: {
  label: string
  detail: string
  active: boolean
  stateLabel: string
  onClick: () => void
}) {
  return (
    <button className="simple-toggle-card" onClick={onClick} type="button">
      <div>
        <div className="simple-toggle-title">{label}</div>
        <div className="simple-toggle-detail">{detail}</div>
      </div>
      <div className={`simple-switch ${active ? 'is-on' : ''}`}>
        <span>{stateLabel}</span>
      </div>
    </button>
  )
}

function FeedCard({ title, value, detail }: { title: string; value: string; detail: string }) {
  return (
    <div className="simple-feed-card">
      <div className="simple-feed-title">{title}</div>
      <div className="simple-feed-value">{value}</div>
      <div className="simple-feed-detail">{detail}</div>
    </div>
  )
}
