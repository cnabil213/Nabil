// Ce que la session a modifié : les autres fichiers, et si ETAT.md et JOURNAL.md ont été touchés.
export type Session = { travail: string[]; etat: boolean; journal: boolean }

declare module 'claude-code' {
  interface PluginState {
    'deux-gestes': { session: Session }
  }
}
