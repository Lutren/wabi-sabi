import { useEffect, useState } from 'react'

const API_BASE = 'http://127.0.0.1:47047'

type ConwayAgent = {
  id: string
  name: string
  role: string
  department: string
  last_state: string
  last_task: string
  last_work: string
  performance: number
  tasks_completed: number
}

type ConwayStateResponse = {
  ok: boolean
  agents: ConwayAgent[]
  total: number
}

const ROLE_COLORS: Record<string, string> = {
  writer: '#f0c27b',
  debugger: '#37d3d0',
  researcher: '#59cf91',
  tester: '#ff6a66',
  archivist: '#e2a760',
  observer: '#8a2be2',
  cleaner: '#40e0d0',
  guard: '#ff4500',
  market_researcher: '#59cf91',
  monitor: '#37d3d0',
  defender: '#ff6a66',
  organizer: '#e2a760',
  compressor: '#f0c27b',
}

const ROLE_NAMES: Record<string, string> = {
  writer: 'Escritor',
  debugger: 'Debugger',
  researcher: 'Investigador',
  tester: 'Tester',
  archivist: 'Archivista',
  observer: 'Observador',
  cleaner: 'Limpiador',
  guard: 'Guardia',
  market_researcher: 'Investigador de mercado',
  monitor: 'Monitor',
  defender: 'Defensor',
  organizer: 'Organizador',
  compressor: 'Compresor',
}

function normalizeRole(role?: string) {
  const rawRole = (role || 'unknown').trim().toLowerCase()
  const decodedRole = rawRole.replace(/\[elichicado\]/g, 'che').replace(/muy/g, 're')
  return decodedRole || 'unknown'
}

function getRoleName(role: string) {
  if (ROLE_NAMES[role]) return ROLE_NAMES[role]
  return role
    .split('_')
    .filter(Boolean)
    .map((part) => `${part.charAt(0).toUpperCase()}${part.slice(1)}`)
    .join(' ')
}

export function HormigueroPanel() {
  const [agents, setAgents] = useState<ConwayAgent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let interval: number

    const fetchAgents = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/agents/conway/state`, { cache: 'no-store' })
        const data: ConwayStateResponse = await res.json()
        if (data.ok) {
          setAgents(data.agents || [])
          setError(null)
        } else {
          setError('Error en respuesta de API')
        }
      } catch (e) {
        setError('No se pudieron cargar los agentes')
      } finally {
        setLoading(false)
      }
    }

    fetchAgents()
    interval = window.setInterval(fetchAgents, 5000)

    return () => clearInterval(interval)
  }, [])

  if (loading) {
    return (
      <div style={{ padding: '1rem', color: '#7d969f' }}>
        Cargando hormiguero...
      </div>
    )
  }

  if (error) {
    return (
      <div style={{ padding: '1rem', color: '#ff6a66' }}>
        {error}
      </div>
    )
  }

  const agentsByRole = agents.reduce((acc, agent) => {
    const role = normalizeRole(agent.role)
    if (!acc[role]) acc[role] = []
    acc[role].push(agent)
    return acc
  }, {} as Record<string, ConwayAgent[]>)

  return (
    <div
      style={{
        padding: '1rem',
        background: 'linear-gradient(180deg, #0d1a24, #081118)',
        borderRadius: '8px',
        border: '1px solid rgba(55,211,208,0.16)',
      }}
    >
      <h3
        style={{
          margin: '0 0 1rem 0',
          fontSize: '0.9rem',
          letterSpacing: '2px',
          color: '#c88a3d',
          textTransform: 'uppercase',
        }}
      >
        Hormiguero Conway ({agents.length} agentes)
      </h3>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: '0.75rem',
        }}
      >
        {Object.entries(agentsByRole).map(([role, roleAgents]) => (
          <div
            key={role}
            style={{
              padding: '0.75rem',
              background: 'rgba(18,38,50,0.6)',
              borderRadius: '6px',
              borderLeft: `3px solid ${ROLE_COLORS[role] || '#7d969f'}`,
            }}
          >
            <div
              style={{
                fontSize: '0.75rem',
                color: ROLE_COLORS[role] || '#7d969f',
                marginBottom: '0.5rem',
                textTransform: 'uppercase',
                letterSpacing: '1px',
              }}
            >
              {getRoleName(role)}
            </div>

            {roleAgents.map((agent) => (
              <div
                key={agent.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  padding: '0.4rem 0',
                  borderBottom: '1px solid rgba(125,150,159,0.1)',
                }}
              >
                <div
                  style={{
                    width: 8,
                    height: 8,
                    borderRadius: '50%',
                    background:
                      agent.last_state === 'active' || agent.last_state === 'working'
                        ? '#59cf91'
                        : agent.last_state === 'idle'
                        ? '#7d969f'
                        : '#ff6a66',
                    boxShadow: `0 0 6px ${
                      agent.last_state === 'active' || agent.last_state === 'working'
                        ? '#59cf91'
                        : agent.last_state === 'idle'
                        ? '#7d969f'
                        : '#ff6a66'
                    }`,
                  }}
                />
                <span style={{ fontSize: '0.85rem', color: '#dfd3bf' }}>
                  {agent.name}
                </span>
                <span
                  style={{
                    fontSize: '0.75rem',
                    color: '#7d969f',
                    marginLeft: 'auto',
                  }}
                >
                  {agent.last_state}
                </span>
              </div>
            ))}
          </div>
        ))}
      </div>

      <div
        style={{
          marginTop: '1rem',
          paddingTop: '0.75rem',
          borderTop: '1px solid rgba(125,150,159,0.2)',
          fontSize: '0.75rem',
          color: '#7d969f',
          textAlign: 'center',
        }}
      >
        Actualización automatica cada 5 segundos
      </div>
    </div>
  )
}
