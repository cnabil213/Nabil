// Objectif 100 K : le plan de croissance (phase-1-solo/strategie/06-plan-croissance-100k.md) devient visible.
// - /abonnes 13450 : ajoute le relevé du jour au fichier de suivi (sans faire travailler Claude) ;
// - un bandeau au-dessus de la saisie : le prochain palier, ce qu'il faut gagner par jour, et ton rythme ;
// - le dimanche à partir de 20 h (heure belge) : rappel du bilan de la semaine.
// Les paliers sont des hypothèses du plan (09/10/2026) : s'ils changent, on change les lignes PALIERS.
import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Releve } from '../types'

const FICHIER = 'phase-1-solo/strategie/08-suivi-abonnes.md'
const DEPART = { date: '2026-10-10', abonnes: 12_700 } // @hitmakingz, plan du 10/10
const PALIERS = [
  { date: '2026-11-15', objectif: 20_000 },
  { date: '2026-12-15', objectif: 45_000 },
  { date: '2027-01-31', objectif: 100_000 },
]
const ENTETE =
  '# Suivi des abonnés TikTok\n\n' +
  'Noté avec la commande /abonnes. Départ : 12 700 abonnés le 10/10/2026 (@hitmakingz). ' +
  'Paliers du plan ([06-plan-croissance-100k.md](06-plan-croissance-100k.md)) : 20 000 le 15/11, 45 000 le 15/12, 100 000 le 31/01/2027.\n\n' +
  '| Date | Abonnés | Gagnés depuis le 10/10 | Note |\n| :--- | ---: | ---: | :--- |\n'

const dernier = atom({ plugin: 'objectif-100k', key: 'dernier' } as const, null as Releve)

const JOUR = 86_400_000
const jours = (de: string, a: string) => Math.round((Date.parse(a) - Date.parse(de)) / JOUR)
const nombre = (n: number) => String(Math.round(n)).replace(/\B(?=(\d{3})+(?!\d))/g, ' ')
const jjmm = (date: string) => `${date.slice(8, 10)}/${date.slice(5, 7)}`

// L'heure belge, quelle que soit l'heure d'été.
function enBelgique(ms: number): { date: string; jour: number; heure: number } {
  const parts = Object.fromEntries(
    new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Brussels', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', hourCycle: 'h23', weekday: 'short' })
      .formatToParts(new Date(ms))
      .map(p => [p.type, p.value]),
  )
  const jour = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(String(parts.weekday))
  return { date: `${parts.year}-${parts.month}-${parts.day}`, jour, heure: Number(parts.hour) }
}

// Le dernier relevé du fichier, s'il y en a un.
function dernierReleve(texte: string): Releve {
  const lignes = texte.split('\n').filter(l => /^\|\s*\d{4}-\d{2}-\d{2}\s*\|/.test(l))
  const derniere = lignes.at(-1)
  if (derniere === undefined) return null
  const [, date, abonnes] = derniere.split('|').map(c => c.trim())
  return { date: String(date), abonnes: Number(String(abonnes).replace(/\D/g, '')) }
}

// « 13 450 », « 13450 », « 13,4k » → 13450 / 13400. Le reste du texte est la note.
function lire(args: string): { abonnes: number; note: string } | undefined {
  const m = args.trim().match(/^(\d[\d\s.]*(?:[.,]\d+)?)\s*([kK])?\s*(.*)$/)
  if (m === null) return undefined
  const [, chiffre = '', k, note = ''] = m
  const abonnes = k ? Math.round(Number(chiffre.replace(/\s/g, '').replace(',', '.')) * 1000) : Number(chiffre.replace(/\D/g, ''))
  return Number.isFinite(abonnes) && abonnes > 0 ? { abonnes, note: note.trim() } : undefined
}

// Le prochain palier, ce qu'il faut gagner par jour pour l'atteindre, et le rythme depuis le départ.
function bilan(r: NonNullable<Releve>) {
  const palier = PALIERS.find(p => p.date >= r.date && p.objectif > r.abonnes) ?? PALIERS[PALIERS.length - 1]!
  const restants = Math.max(1, jours(r.date, palier.date))
  const aTenir = Math.max(0, Math.ceil((palier.objectif - r.abonnes) / restants))
  const rythme = (r.abonnes - DEPART.abonnes) / Math.max(1, jours(DEPART.date, r.date))
  return { palier, aTenir, rythme }
}

function phrase(r: NonNullable<Releve>): string {
  const { palier, aTenir, rythme } = bilan(r)
  const signe = rythme >= 0 ? '+' : '−'
  return `${nombre(r.abonnes)} abonnés · palier ${nombre(palier.objectif)} le ${jjmm(palier.date)} : +${nombre(aTenir)}/jour à tenir · ton rythme : ${signe}${nombre(Math.abs(rythme))}/jour`
}

async function relire($: EngineInterface): Promise<string> {
  const texte = (await $.fs.exists(FICHIER)) ? String(await $.fs.read(FICHIER)) : ''
  await update($, dernier, () => dernierReleve(texte))
  return texte
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'abonnes', description: 'Noter tes abonnés TikTok du jour', argumentHint: '[nombre] [note]', immediate: true })
    await relire($)
    const maintenant = enBelgique(await $.clock.now())
    const r = await read($, dernier)
    if (maintenant.jour === 0 && maintenant.heure >= 20 && r?.date !== maintenant.date) {
      $.ui.toast("Dimanche 20 h : c'est le bilan. Envoie tes captures TikTok Studio, et note tes abonnés avec /abonnes.", { timeoutMs: 15_000 })
    }
    return next(e)
  })

  on('command.run', { command: 'abonnes' }, async ($, e) => noter($, e.args))

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const r = await read($, dernier)
    if (e.props.hasSurvey || r === null) return next(e)
    const { Box, Text } = $.ui.resolve(e)
    const { aTenir, rythme } = bilan(r)
    return (
      <Box key="objectif">
        <Text color={rythme >= aTenir ? 'success' : 'warning'}>100 K : {phrase(r)}</Text>
      </Box>
    )
  })
}

// /abonnes : ajoute une ligne datée au fichier de suivi et répond par le bilan.
async function noter($: EngineInterface, args: string): Promise<{ text: string }> {
  const lu = lire(args)
  if (lu === undefined) return { text: 'Écris le nombre après la commande, par exemple : /abonnes 13450 (ou /abonnes 13,4k après la V3)' }
  const date = enBelgique(await $.clock.now()).date
  const avant = (await $.fs.exists(FICHIER)) ? String(await $.fs.read(FICHIER)) : ENTETE
  const gagnes = lu.abonnes - DEPART.abonnes
  const ligne = `| ${date} | ${nombre(lu.abonnes)} | ${gagnes >= 0 ? '+' : '−'}${nombre(Math.abs(gagnes))} | ${lu.note.replace(/\|/g, '/')} |\n`
  await $.fs.write(FICHIER, `${avant}${avant.endsWith('\n') ? '' : '\n'}${ligne}`)
  const r = { date, abonnes: lu.abonnes }
  await update($, dernier, () => r)
  return { text: `Noté dans ${FICHIER}.\n${phrase(r)}` }
}
