// Les deux gestes de fin de session (CLAUDE.md du dépôt Nabil) : « Réécrire ETAT.md, ajouter une entrée
// en haut de JOURNAL.md. Jamais l'un sans l'autre. » Et : « seul ce qui est commité reste ».
// - un bandeau au-dessus de la saisie tant que du travail a été fait sans ces deux gestes ;
// - un push qui contient l'un sans l'autre est refusé ; un push qui n'en contient aucun reçoit un rappel ;
// - /fin dit en une fois ce qui manque (ETAT, JOURNAL, fichiers pas commités, commits pas poussés).
import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { Session } from '../types'

const VIDE: Session = { travail: [], etat: false, journal: false }
const session = atom({ plugin: 'deux-gestes', key: 'session' } as const, VIDE)

const coche = (fait: boolean) => (fait ? '✓' : '✗')

// Lance git et rend ses lignes, ou rien s'il échoue (pas de dépôt, pas de branche distante).
async function git($: EngineInterface, argv: string[]): Promise<string[] | undefined> {
  try {
    const r = await $.process.run(['git', ...argv])
    return r.exitCode === 0 ? r.stdout.split('\n').map(l => l.trim()).filter(l => l !== '') : undefined
  } catch {
    return undefined
  }
}

// Les fichiers que le push va envoyer : depuis la branche distante, ou depuis main pour une branche neuve.
async function fichiersAPousser($: EngineInterface): Promise<string[]> {
  return (await git($, ['diff', '--name-only', '@{u}..HEAD'])) ?? (await git($, ['diff', '--name-only', 'origin/main...HEAD'])) ?? []
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'fin', description: 'Ce qui manque avant de finir la session (ETAT, JOURNAL, commit, push)', immediate: true })
    return next(e)
  })

  // On note chaque fichier modifié par Claude.
  on('tool.call', async ($, e, next) => {
    if (e.tool !== 'Edit' && e.tool !== 'Write') return next(e)
    const fin = await next(e)
    if (!('result' in fin) || fin.isError === true) return fin
    const chemin = String((e as { file_path?: unknown }).file_path ?? '')
    await update($, session, s =>
      chemin.endsWith('ETAT.md') ? { ...s, etat: true }
      : chemin.endsWith('JOURNAL.md') ? { ...s, journal: true }
      : { ...s, travail: [...new Set([...s.travail, chemin])] },
    )
    return fin
  }).catch(($, e, next) => next(e)) // ce suivi ne bloque jamais une modification

  // Le push : jamais l'un sans l'autre.
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    if (!/\bgit\b[^;&|]*\bpush\b/.test(String(e.command))) return next(e)
    const fichiers = await fichiersAPousser($)
    const etat = fichiers.includes('ETAT.md')
    const journal = fichiers.includes('JOURNAL.md')
    if (etat !== journal) {
      return {
        deny: `Ce push contient ${etat ? 'ETAT.md sans JOURNAL.md' : 'JOURNAL.md sans ETAT.md'}. Règle du dépôt (CLAUDE.md) : ` +
          `les deux gestes de fin de session vont ensemble, jamais l'un sans l'autre. Ajoute ${etat ? "l'entrée en haut de JOURNAL.md" : 'la réécriture d’ETAT.md'}, commite, puis pousse.`,
      }
    }
    const fin = await next(e)
    if (etat || fichiers.length === 0 || fin.deny !== undefined) return fin
    const rappel = "Rappel du dépôt (CLAUDE.md) : ce push ne contient ni ETAT.md ni JOURNAL.md. Avant de finir la session, réécris ETAT.md et ajoute une entrée en haut de JOURNAL.md."
    return { ...fin, context: [...(fin.context ?? []), rappel] }
  }).catch(($, e, next) => next(e))

  // /clear : nouvelle session, on repart de zéro.
  on('session.end', async ($, e, next) => {
    if (e.reason === 'clear') await update($, session, () => VIDE)
    return next(e)
  })

  on('command.run', { command: 'fin' }, async $ => {
    const s = await read($, session)
    const pasCommites = (await git($, ['status', '--porcelain'])) ?? []
    const pasPousses = (await git($, ['rev-list', '--count', '@{u}..HEAD']))?.[0] ?? '?'
    const lignes = [
      `ETAT.md réécrit : ${coche(s.etat)}`,
      `JOURNAL.md, nouvelle entrée : ${coche(s.journal)}`,
      `Fichiers modifiés par Claude dans cette session : ${s.travail.length}`,
      `Fichiers pas commités : ${pasCommites.length}${pasCommites.length > 0 ? ' (seul ce qui est commité reste)' : ''}`,
      `Commits pas poussés : ${pasPousses}`,
    ]
    return { text: lignes.join('\n') }
  })

  // Le bandeau : visible seulement quand du travail a été fait sans les deux gestes.
  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const s = await read($, session)
    if (e.props.hasSurvey || s.travail.length === 0 || (s.etat && s.journal)) return next(e)
    const { Box, Text } = $.ui.resolve(e)
    return (
      <Box key="deux-gestes">
        <Text color="warning">
          Avant de finir : ETAT.md {coche(s.etat)} · JOURNAL.md {coche(s.journal)} ({s.travail.length} fichier{s.travail.length > 1 ? 's' : ''} modifié{s.travail.length > 1 ? 's' : ''})
        </Text>
      </Box>
    )
  })
}
