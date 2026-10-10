// Ce que le HUD a lu dans Metricool la dernière fois.
export type Hud = {
  // Abonnés au dernier jour connu, gagnés sur 7 jours, vues sur 7 jours, likes du compte.
  tiktok: { abonnes: number; jour: string; gagnes7j: number; vues7j: number; likes: number } | null
  // La dernière vidéo publiée.
  video: { date: string; titre: string; vues: number; likes: number; vueEntiere: number } | null
  // La prochaine publication programmée dans Metricool.
  prochaine: { date: string; texte: string } | null
  // Quand Metricool a été lu (ms), 0 si jamais.
  majA: number
  // Pourquoi la lecture a échoué, s'il y a lieu.
  erreur: string
}

declare module 'claude-code' {
  interface PluginState {
    'cnabil-hud': { hud: Hud }
  }
}
