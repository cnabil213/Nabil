// C'Nabil HUD : le tableau de bord de C'Nabil-Famous, toujours sous les yeux, sans demander à Claude.
// - Au-dessus de la saisie, une ligne : abonnés TikTok, palier 100 K, fenêtre de contexte, forfait.
// - /hud ouvre le panneau complet : TikTok, dernière vidéo, objectif 100 K, prochaine publication, Claude.
// Les chiffres TikTok viennent de Metricool, appelé directement par le mod : aucun appel au modèle,
// donc aucun token. Le contexte et le forfait viennent de Claude Code lui-même ($.session.usage).
import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Hud } from '../types'

// Le connecteur Metricool, sous les noms qu'il peut porter dans /mcp.
const SERVEURS = ['claude.ai Metricool Social Media Management', 'Metricool Social Media Management', 'claude.ai Metricool', 'Metricool']
const RAFRAICHIR_MS = 15 * 60_000 // Metricool relu au plus toutes les 15 minutes
const DEPART = { date: '2026-10-10', abonnes: 12_700 } // @hitmakingz, plan du 10/10
const PALIERS = [
  { date: '2026-11-15', objectif: 20_000 },
  { date: '2026-12-15', objectif: 45_000 },
  { date: '2027-01-31', objectif: 100_000 },
]
const PANNEAU = 'hud'
const VIDE: Hud = { tiktok: null, video: null, prochaine: null, majA: 0, erreur: '' }

const hud = atom({ plugin: 'cnabil-hud', key: 'hud' } as const, VIDE)

// ---------- petits outils d'affichage ----------
const nombre = (n: number) => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
const kilo = (n: number) => (n >= 1000 ? (n / 1000).toFixed(n >= 100_000 ? 0 : 1).replace('.', ',').replace(',0', '') + ' K' : String(n))
const barre = (pourcent: number, cases = 10) => {
  const pleines = Math.max(0, Math.min(cases, Math.round((pourcent / 100) * cases)))
  return '▰'.repeat(pleines) + '▱'.repeat(cases - pleines)
}
const couleurJauge = (p: number) => (p >= 85 ? 'error' : p >= 60 ? 'warning' : 'success')
const jjmm = (date: string) => `${date.slice(8, 10)}/${date.slice(5, 7)}`
const JOUR = 86_400_000
const jours = (de: string, a: string) => Math.round((Date.parse(a) - Date.parse(de)) / JOUR)

function aujourdhui(ms: number): string {
  const p = Object.fromEntries(
    new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Brussels', year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(new Date(ms)).map(x => [x.type, x.value]),
  )
  return `${p.year}-${p.month}-${p.day}`
}
const moinsJours = (date: string, n: number) => new Date(Date.parse(date) - n * JOUR).toISOString().slice(0, 10)
const nb = (v: unknown) => (v === null || v === undefined || v === '' ? undefined : Number(v))

// Le prochain palier du plan, et ce qu'il faut gagner par jour pour l'atteindre.
function palier(abonnes: number, jour: string) {
  const p = PALIERS.find(x => x.date >= jour && x.objectif > abonnes) ?? PALIERS[PALIERS.length - 1]!
  const restants = Math.max(1, jours(jour, p.date))
  return { ...p, parJour: Math.max(0, Math.ceil((p.objectif - abonnes) / restants)) }
}

// ---------- Metricool ----------
let serveurTrouve: string | undefined

// Appelle un outil Metricool et rend son JSON ; essaie chaque nom du connecteur la première fois.
async function metricool($: EngineInterface, outil: string, args: Record<string, unknown>): Promise<any> {
  const noms = serveurTrouve !== undefined ? [serveurTrouve] : SERVEURS
  let derniere = ''
  for (const serveur of noms) {
    try {
      const r = await $.mcp.call(serveur, outil, args)
      const texte = r.content.map(b => ('text' in b ? String(b.text) : '')).join('')
      if (r.isError) throw new Error(texte)
      serveurTrouve = serveur
      return JSON.parse(texte)
    } catch (err) {
      derniere = err instanceof Error ? err.message : String(err)
    }
  }
  throw new Error(derniere)
}

// Relit tout ce que le HUD montre de TikTok. Une erreur ne casse rien : elle s'affiche.
async function relireMetricool($: EngineInterface): Promise<void> {
  const maintenant = await $.clock.now()
  const jour = aujourdhui(maintenant)
  try {
    const marques = await metricool($, 'getBrandSettings', {})
    const marque = marques?.data?.[0]
    if (marque === undefined) throw new Error('aucune marque dans Metricool')
    const brandId = String(marque.id)
    const fuseau = String(marque.timezone ?? 'Europe/Brussels')

    // Évolution du compte sur 7 jours : abonnés, nouveaux abonnés, vues, likes.
    const evo = await metricool($, 'getAnalyticsDataByMetrics', {
      brandId, from: `${moinsJours(jour, 7)}T00:00:00+00:00`, to: `${jour}T23:59:59+00:00`, metrics: ['TKEV07', 'TKEV08', 'TKEV12', 'TKEV13'],
    })
    const lignes: unknown[][] = evo?.rows ?? []
    let tiktok: Hud['tiktok'] = null
    const avecAbonnes = lignes.filter(l => nb(l[0]) !== undefined)
    const derniere = avecAbonnes.at(-1)
    if (derniere !== undefined) {
      const brut = String(derniere.at(-1))
      tiktok = {
        abonnes: nb(derniere[0])!,
        jour: `${brut.slice(0, 4)}-${brut.slice(4, 6)}-${brut.slice(6, 8)}`,
        gagnes7j: lignes.reduce((s, l) => s + (nb(l[1]) ?? 0), 0),
        vues7j: lignes.reduce((s, l) => s + (nb(l[2]) ?? 0), 0),
        likes: nb(lignes.filter(l => nb(l[3]) !== undefined).at(-1)?.[3]) ?? 0,
      }
    }

    // La dernière vidéo publiée (60 derniers jours).
    const posts = await metricool($, 'getAnalyticsDataByMetrics', {
      brandId, from: `${moinsJours(jour, 60)}T00:00:00+00:00`, to: `${jour}T23:59:59+00:00`, metrics: ['TKPO02', 'TKPO05', 'TKPO07', 'TKPO08', 'TKPO13'],
    })
    const recente = [...((posts?.rows ?? []) as unknown[][])].sort((a, b) => String(b[0]).localeCompare(String(a[0])))[0]
    const video: Hud['video'] = recente === undefined ? null : {
      date: String(recente[0]).slice(0, 10),
      titre: String(recente[1] ?? '').slice(0, 60),
      vues: nb(recente[2]) ?? 0,
      likes: nb(recente[3]) ?? 0,
      vueEntiere: nb(recente[4]) ?? 0,
    }

    // La prochaine publication programmée (14 jours).
    const prog = await metricool($, 'getScheduledPosts', {
      brandId, fromDate: `${jour}T00:00:00+00:00`, toDate: `${moinsJours(jour, -14)}T23:59:59+00:00`, timezone: fuseau,
    })
    const quand = (p: any) => String(p?.publicationDate?.dateTime ?? p?.publicationDate ?? p?.date ?? '')
    const suivante = [...((prog?.data ?? []) as any[])].sort((a, b) => quand(a).localeCompare(quand(b)))[0]
    const prochaine: Hud['prochaine'] = suivante === undefined ? null : { date: quand(suivante).slice(0, 16).replace('T', ' '), texte: String(suivante.text ?? '').slice(0, 50) }

    await update($, hud, () => ({ tiktok, video, prochaine, majA: maintenant, erreur: '' }))
  } catch (err) {
    const raison = err instanceof Error ? err.message : String(err)
    await update($, hud, h => ({ ...h, majA: maintenant, erreur: raison.slice(0, 120) }))
  }
}

// ---------- ce que Claude Code sait de la session ----------
async function claude($: EngineInterface) {
  try {
    const u = await $.session.usage()
    const limite = (genre: string) => u.rateLimits.find(r => r.kind === genre)?.percentUsed
    return { contexte: u.context.percent, cinqH: limite('five_hour'), septJ: limite('seven_day'), cout: u.cost?.usd }
  } catch {
    return { contexte: undefined, cinqH: undefined, septJ: undefined, cout: undefined }
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'hud', description: "Ouvrir le HUD de C'Nabil-Famous (TikTok, objectif 100 K, contexte)", immediate: true })
    await relireMetricool($)
    return next(e)
  })

  // Metricool relu en passant, au plus toutes les 15 minutes.
  on('turn.complete', async ($, e, next) => {
    const fin = await next(e)
    const etat = await read($, hud)
    if ((await $.clock.now()) - etat.majA >= RAFRAICHIR_MS) await relireMetricool($)
    return fin
  })

  on('command.run', { command: 'hud' }, async $ => {
    await relireMetricool($)
    await $.ui.open({ id: PANNEAU, title: "C'NABIL HUD" })
    return {}
  })

  // La ligne au-dessus de la saisie.
  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey) return next(e)
    const etat = await read($, hud)
    const c = await claude($)
    const { Box, Text } = $.ui.resolve(e)
    const t = etat.tiktok
    const p = t === null ? undefined : palier(t.abonnes, t.jour)
    return (
      <Box key="hud" flexDirection="row" gap={1}>
        <Box key="titre"><Text color="claude" bold>◆ C'NABIL</Text></Box>
        <Box key="tiktok">
          {t === null || p === undefined
            ? <Text dimColor>TikTok : {etat.erreur === '' ? 'lecture…' : 'Metricool pas joignable (/hud)'}</Text>
            : <Text>TikTok <Text bold>{nombre(t.abonnes)}</Text> {t.abonnes >= DEPART.abonnes ? '▲' : '▼'}{nombre(Math.abs(t.abonnes - DEPART.abonnes))} · palier {kilo(p.objectif)} le {jjmm(p.date)} : +{nombre(p.parJour)}/j</Text>}
        </Box>
        <Box key="sep1"><Text dimColor>│</Text></Box>
        <Box key="contexte"><Text color={couleurJauge(c.contexte ?? 0)}>Contexte {barre(c.contexte ?? 0)} {c.contexte ?? '?'} %</Text></Box>
        {c.cinqH === undefined ? null : <Box key="sep2"><Text dimColor>│</Text></Box>}
        {c.cinqH === undefined ? null : <Box key="forfait"><Text color={couleurJauge(Math.max(c.cinqH, c.septJ ?? 0))}>Forfait 5 h {c.cinqH} % · 7 j {c.septJ ?? '?'} %</Text></Box>}
      </Box>
    )
  })

  // Le panneau complet.
  on('ui.render', { component: 'Pane', requestId: PANNEAU }, async ($, e) => {
    const etat = await read($, hud)
    const c = await claude($)
    const { Box, Button, Text } = $.ui.resolve(e)
    const t = etat.tiktok
    const v = etat.video
    const p = t === null ? undefined : palier(t.abonnes, t.jour)
    const vers100k = t === null ? 0 : Math.round(((t.abonnes - DEPART.abonnes) / (100_000 - DEPART.abonnes)) * 1000) / 10
    return (
      <Box flexDirection="column" borderStyle="round" borderColor="claude" paddingX={1} gap={1}>
        <Box key="tiktok" flexDirection="column">
          <Box key="t-titre"><Text color="claude" bold>▌TIKTOK</Text></Box>
          {t === null
            ? <Box key="t-vide"><Text dimColor>{etat.erreur === '' ? 'Pas encore lu.' : `Metricool pas joignable : ${etat.erreur}`}</Text></Box>
            : <Box key="t-abonnes"><Text>Abonnés <Text bold>{nombre(t.abonnes)}</Text> le {jjmm(t.jour)} · +{nombre(t.gagnes7j)} en 7 j · vues 7 j {nombre(t.vues7j)} · likes {kilo(t.likes)}</Text></Box>}
          {v === null
            ? <Box key="t-video"><Text dimColor>Aucune vidéo publiée ces 60 derniers jours.</Text></Box>
            : <Box key="t-video"><Text>Dernière vidéo ({jjmm(v.date)}) « {v.titre} » : {nombre(v.vues)} vues · {nombre(v.likes)} likes · {String(v.vueEntiere).replace('.', ',')} % vue en entier</Text></Box>}
          <Box key="t-prochaine"><Text>{etat.prochaine === null ? 'Rien de programmé dans Metricool ces 14 jours.' : `Prochaine : ${etat.prochaine.date} · ${etat.prochaine.texte}`}</Text></Box>
        </Box>
        <Box key="objectif" flexDirection="column">
          <Box key="o-titre"><Text color="claude" bold>▌OBJECTIF 100 K · 31/01/2027</Text></Box>
          {t === null || p === undefined
            ? <Box key="o-vide"><Text dimColor>En attente des abonnés.</Text></Box>
            : <Box key="o-barre"><Text color="success">{barre(Math.max(0, vers100k), 20)} {String(vers100k).replace('.', ',')} % du chemin depuis le 10/10</Text></Box>}
          {p === undefined ? null : <Box key="o-palier"><Text>Palier {nombre(p.objectif)} le {jjmm(p.date)} : +{nombre(p.parJour)} abonnés par jour à tenir</Text></Box>}
        </Box>
        <Box key="claude" flexDirection="column">
          <Box key="c-titre"><Text color="claude" bold>▌CLAUDE</Text></Box>
          <Box key="c-contexte"><Text color={couleurJauge(c.contexte ?? 0)}>Fenêtre de contexte {barre(c.contexte ?? 0, 20)} {c.contexte ?? '?'} %</Text></Box>
          <Box key="c-forfait"><Text>Forfait : 5 h {c.cinqH ?? '?'} % · 7 jours {c.septJ ?? '?'} %{c.cout === undefined ? '' : ` · ce fil ${c.cout.toFixed(2).replace('.', ',')} $`}</Text></Box>
        </Box>
        <Button key="actualiser" label="Actualiser" onPress={() => relireMetricool($)} />
      </Box>
    )
  })
}
