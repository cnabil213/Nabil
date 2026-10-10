// Le dernier relevé noté avec /abonnes (date AAAA-MM-JJ), ou null s'il n'y en a pas encore.
export type Releve = { date: string; abonnes: number } | null

declare module 'claude-code' {
  interface PluginState {
    'objectif-100k': { dernier: Releve }
  }
}
