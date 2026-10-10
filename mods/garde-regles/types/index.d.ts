// Les noms des mp4 passés par ffprobe sans erreur depuis leur dernière écriture, dans cette session.
export type MontagesVerifies = string[]

declare module 'claude-code' {
  interface PluginState {
    'garde-regles': { verifies: MontagesVerifies }
  }
}
