// Commande /refus : Nabil brûle une idée en une phrase, avec sa raison.
// Règle d'origine (CLAUDE.md du dépôt Nabil) : « Une idée rejetée ne se supprime pas : elle se documente
// avec sa raison de refus, pour ne pas la voir revenir. » La ligne va dans le tableau « Brûlées »
// de phase-1-solo/scripts/02-backlog-idees.md, que toute session relit avant de proposer.
// Aucun appel au modèle : ça marche même pendant que Claude travaille, et ça ne coûte pas de tokens.
import type { Register } from 'claude-code'

const FICHIER = 'phase-1-solo/scripts/02-backlog-idees.md'
const EXEMPLE = '/refus le pote qui filme tout au concert — vu et revu'

// « idée — raison » (accepte aussi « – », « - » et « : » comme séparateur).
function couper(texte: string): { idee: string; raison: string } | undefined {
  const m = texte.match(/^(.+?)\s+[—–:-]\s+(.+)$/)
  if (m === null) return undefined
  return { idee: m[1]!.trim().replace(/\|/g, '/'), raison: m[2]!.trim().replace(/\|/g, '/') }
}

// Le jour et le mois en Belgique, comme dans le tableau existant : « (15/09) ».
function jjmm(ms: number): string {
  const p = Object.fromEntries(
    new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Brussels', day: '2-digit', month: '2-digit' }).formatToParts(new Date(ms)).map(x => [x.type, x.value]),
  )
  return `${p.day}/${p.month}`
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'refus',
      description: 'Brûler une idée, avec sa raison (liste des idées brûlées)',
      argumentHint: '[idée] — [raison]',
      immediate: true,
    })
    return next(e)
  })

  on('command.run', { command: 'refus' }, async ($, e) => {
    const lu = couper(e.args.trim())
    if (lu === undefined) return { text: `Écris l'idée puis sa raison, séparées par un tiret. Par exemple : ${EXEMPLE}` }
    if (!(await $.fs.exists(FICHIER))) return { text: `Fichier ${FICHIER} introuvable : rien n'est noté. Lance Claude Code dans le dossier du dépôt Nabil.` }

    const lignes = String(await $.fs.read(FICHIER)).split('\n')
    const debut = lignes.findIndex(l => /^##\s.*Brûlées/i.test(l))
    if (debut === -1) return { text: `Pas de section « Brûlées » dans ${FICHIER} : rien n'est noté.` }

    // Le tableau de la section : de sa première ligne « | » à sa dernière.
    let fin = debut + 1
    while (fin < lignes.length && !lignes[fin]!.startsWith('|') && !lignes[fin]!.startsWith('## ')) fin++
    if (fin >= lignes.length || !lignes[fin]!.startsWith('|')) return { text: `Pas de tableau dans la section « Brûlées » de ${FICHIER} : rien n'est noté.` }
    while (fin + 1 < lignes.length && lignes[fin + 1]!.startsWith('|')) fin++

    // Déjà brûlée ? On compare la première colonne, sans les majuscules.
    const cherche = lu.idee.toLowerCase()
    for (const l of lignes.slice(debut, fin + 1)) {
      const deja = (l.split('|')[1] ?? '').trim()
      if (deja !== '' && !/^[:\s-]+$/.test(deja) && deja !== 'Idée / thème' && (deja.toLowerCase().includes(cherche) || cherche.includes(deja.toLowerCase()))) {
        return { text: `Déjà brûlée : « ${deja} ». Rien n'est ajouté.` }
      }
    }

    const ligne = `| ${lu.idee} | ${lu.raison} (${jjmm(await $.clock.now())}) |`
    lignes.splice(fin + 1, 0, ligne)
    await $.fs.write(FICHIER, lignes.join('\n'))
    return { text: `Brûlée : « ${lu.idee} ». Notée avec sa raison dans ${FICHIER}.` }
  })
}
