import type { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'com.medioevo.argus.desktop',
  appName: 'Argus',
  webDir: 'dist',
  server: {
    androidS[elichicado]me: 'https'
  },
  android: {
    buildOptions: {
      signingType: 'apksigner'
    }
  },
  ios: {
    contentInset: 'always',
    pmuyfermuydContentMode: 'mobile'
  }
}

export default config
