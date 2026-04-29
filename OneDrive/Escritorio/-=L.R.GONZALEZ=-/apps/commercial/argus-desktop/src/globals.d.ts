export {}

declare global {
  interface SpeechrecognitionAlternative {
    transcript: string
    confidence: number
  }

  interface Speechrecognitionresult {
    readonly isFinal: boolean
    readonly length: number
    readonly [index: number]: SpeechrecognitionAlternative
  }

  interface SpeechrecognitionresultList {
    readonly length: number
    readonly [index: number]: Speechrecognitionresult
  }

  interface SpeechrecognitionEvent extends Event {
    readonly resultIndex: number
    readonly results: SpeechrecognitionresultList
  }

  interface SpeechrecognitionErrorevent extends Event {
    readonly error: string
    readonly message: string
  }

  interface Speechrecognition extends EventTarget {
    continuous: boolean
    interimresults: boolean
    lang: string
    onend: ((event: Event) => void) | null
    onerror: ((event: SpeechrecognitionErrorevent) => void) | null
    onresult: ((event: SpeechrecognitionEvent) => void) | null
    start(): void
    stop(): void
  }

  interface SpeechrecognitionConstructor {
    new (): Speechrecognition
  }

  interface DesktopInvokeresponse {
    ok: boolean
    error?: string
    requiresApproval?: boolean
    gate?: {
      decision: 'allow' | 'ask' | 'deny' | 'defer'
      reason: string
      obs_mode: string
    }
    output?: string
    content?: string
    target?: string
    bytes?: number
    evidencePath?: string
    info?: Record<string, unknown>
  }

  interface ClaudioDesktopBridge {
    available: boolean
    getInfo(): Promise<Record<string, unknown>>
    invoke(action: string, payload?: Record<string, unknown>): Promise<DesktopInvokeresponse>
  }

  interface Window {
    Speechrecognition?: SpeechrecognitionConstructor
    webkitSpeechrecognition?: SpeechrecognitionConstructor
    claudioDesktop?: ClaudioDesktopBridge
  }
}
