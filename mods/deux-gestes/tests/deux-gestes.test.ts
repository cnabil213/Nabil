declare const h: any
import { expect, test } from 'claude-code/testing'

const BANDEAU = { hasSurvey: false, isWorking: false, maxRows: 10, bodyColumns: 80 } as any

// Ce que git répond : les fichiers du prochain push, et l'état du dossier.
function git(on: any, aPousser: string[], pasCommites: string[] = []) {
  on('process.run', ($: any, e: any) => {
    const argv: string[] = e.argv
    const sortie = (lignes: string[]) => ({ value: { exitCode: 0, stdout: lignes.join('\n'), stderr: '' } })
    if (argv.includes('diff')) return sortie(aPousser)
    if (argv.includes('status')) return sortie(pasCommites.map(f => ' M ' + f))
    if (argv.includes('rev-list')) return sortie(['2'])
    return { value: { exitCode: 1, stdout: '', stderr: '' } }
  })
}
const ecrire = (file_path: string) => ({ tool: 'Edit', file_path, old_string: 'a', new_string: 'b' } as any)
// Ce que Claude Code dessine quand le mod passe la main.
const moteur = (on: any) => on('ui.render', ($: any, e: any) => { const { Box } = $.ui.resolve(e); return h(Box, { key: 'moteur' }) })

test('le bandeau apparaît après du travail, et disparaît quand ETAT et JOURNAL sont faits', async ($, on) => {
  moteur(on)
  on('tool.call', () => ({ result: 'ok' }))
  await $.tool.call(ecrire('/repo/phase-1-solo/tournage/01-coach-tournage.md'))
  let ui: any = await $.ui.mount({ plugin: 'deux-gestes', surface: 'terminal', component: 'AbovePrompt', props: BANDEAU })
  expect((await ui.find({ key: 'deux-gestes' }))?.text).toBe('Avant de finir : ETAT.md ✗ · JOURNAL.md ✗ (1 fichier modifié)')

  await $.tool.call(ecrire('/repo/ETAT.md'))
  ui = await $.ui.mount({ plugin: 'deux-gestes', surface: 'desktop', component: 'AbovePrompt', props: BANDEAU })
  expect((await ui.find({ key: 'deux-gestes' }))?.text).toBe('Avant de finir : ETAT.md ✓ · JOURNAL.md ✗ (1 fichier modifié)')

  await $.tool.call(ecrire('/repo/JOURNAL.md'))
  ui = await $.ui.mount({ plugin: 'deux-gestes', surface: 'terminal', component: 'AbovePrompt', props: BANDEAU })
  expect(await ui.find({ key: 'deux-gestes' })).toBeUndefined()
})

test('pas de bandeau tant que rien n a été modifié', async ($, on) => {
  moteur(on)
  const ui = await $.ui.mount({ plugin: 'deux-gestes', surface: 'terminal', component: 'AbovePrompt', props: BANDEAU })
  expect(await ui.find({ key: 'deux-gestes' })).toBeUndefined()
  expect(await ui.find({ key: 'moteur' })).toBeDefined()
})

test('un push avec ETAT.md sans JOURNAL.md est refusé', async ($, on) => {
  git(on, ['ETAT.md', 'phase-1-solo/strategie/06-plan-croissance-100k.md'])
  on('tool.call', () => ({ result: { stdout: '', stderr: '' } }))
  const r: any = await $.tool.call({ tool: 'Bash', command: 'git push -u origin main' } as any)
  expect(r.deny).toContain('ETAT.md sans JOURNAL.md')
})

test('un push avec les deux passe sans rappel', async ($, on) => {
  git(on, ['ETAT.md', 'JOURNAL.md', 'FORMATS.md'])
  on('tool.call', () => ({ result: { stdout: '', stderr: '' } }))
  const r: any = await $.tool.call({ tool: 'Bash', command: 'git push' } as any)
  expect(r.deny).toBeUndefined()
  expect(r.context ?? []).toEqual([])
})

test('un push sans aucun des deux passe, avec un rappel pour Claude', async ($, on) => {
  git(on, ['FORMATS.md'])
  on('tool.call', () => ({ result: { stdout: '', stderr: '' } }))
  const r: any = await $.tool.call({ tool: 'Bash', command: 'git push origin main' } as any)
  expect(r.deny).toBeUndefined()
  expect(r.context.join(' ')).toContain('réécris ETAT.md')
})

test('/fin fait le bilan', async ($, on) => {
  git(on, [], ['ETAT.md'])
  on('tool.call', () => ({ result: 'ok' }))
  await $.tool.call(ecrire('/repo/FORMATS.md'))
  await $.tool.call(ecrire('/repo/ETAT.md'))
  const r = await $.command.run({ command: 'fin', args: '' } as any)
  expect(r.text).toBe([
    'ETAT.md réécrit : ✓',
    'JOURNAL.md, nouvelle entrée : ✗',
    'Fichiers modifiés par Claude dans cette session : 1',
    'Fichiers pas commités : 1 (seul ce qui est commité reste)',
    'Commits pas poussés : 2',
  ].join('\n'))
})
