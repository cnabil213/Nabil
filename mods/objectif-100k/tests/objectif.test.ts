declare const h: any
import { expect, test } from 'claude-code/testing'

const SURFACES = ['terminal', 'desktop'] as const
const BANDEAU = { hasSurvey: false, isWorking: false, maxRows: 10, bodyColumns: 100 } as any
const SUIVI = 'phase-1-solo/strategie/08-suivi-abonnes.md'

// Un faux disque et une horloge fixée (heure UTC ; la Belgique est à +2 h jusqu'au 25/10, +1 h après).
function monde(on: any, utc: number | (() => number), depart: Record<string, string> = {}) {
  const fichiers: Record<string, string> = { ...depart }
  on('clock.now', () => ({ value: typeof utc === 'number' ? utc : utc() }))
  const cle = (chemin: string) => chemin.slice(chemin.indexOf('phase-1-solo/'))
  on('fs.exists', ($: any, e: any) => ({ value: cle(e.path) in fichiers }))
  on('fs.read', ($: any, e: any) => ({ value: fichiers[cle(e.path)] }))
  on('fs.write', ($: any, e: any) => { fichiers[cle(e.path)] = e.text; return { value: undefined } })
  on('command.register', () => ({ value: undefined }))
  on('session.start', () => ({ cwd: '.' }))
  return fichiers
}
const toasts = (on: any) => { const t: string[] = []; on('ui.toast', ($: any, e: any) => { t.push(e.text); return { value: undefined } }); return t }

test('/abonnes crée le fichier de suivi et répond par le palier à tenir', async ($, on) => {
  const fichiers = monde(on, Date.UTC(2026, 9, 12, 12))
  const r = await $.command.run({ command: 'abonnes', args: '13 450 après la V3' } as any)
  expect(r.text).toContain('+193/jour à tenir')
  expect(r.text).toContain('ton rythme : +375/jour')
  const contenu = fichiers[SUIVI]!
  expect(contenu).toContain('| Date | Abonnés | Gagnés depuis le 10/10 | Note |')
  expect(contenu).toMatch(/\| 2026-10-12 \| 13 450 \| \+750 \| après la V3 \|\n$/)
})

test('/abonnes comprend « 13,4k » et ajoute à la suite', async ($, on) => {
  const fichiers = monde(on, Date.UTC(2026, 9, 12, 12))
  await $.command.run({ command: 'abonnes', args: '13450' } as any)
  await $.command.run({ command: 'abonnes', args: '13,4k' } as any)
  const lignes = fichiers[SUIVI]!.split('\n').filter(l => l.startsWith('| 2026'))
  expect(lignes.length).toBe(2)
  expect(lignes[1]).toContain('| 13 400 | +700 |')
})

test('/abonnes sans nombre explique quoi écrire et ne touche à rien', async ($, on) => {
  const fichiers = monde(on, Date.UTC(2026, 9, 12, 12))
  const r = await $.command.run({ command: 'abonnes', args: 'beaucoup' } as any)
  expect(r.text).toContain('Écris le nombre')
  expect(Object.keys(fichiers).length).toBe(0)
})

test('le bandeau relit le fichier au démarrage, sur terminal et Desktop', async ($, on) => {
  monde(on, Date.UTC(2026, 9, 12, 12), {
    [SUIVI]: '# Suivi\n\n| Date | Abonnés | Gagnés depuis le 10/10 | Note |\n| :--- | ---: | ---: | :--- |\n| 2026-10-12 | 13 450 | +750 | |\n',
  })
  toasts(on)
  await $.session.start({} as any)
  for (const surface of SURFACES) {
    const ui = await $.ui.mount({ plugin: 'objectif-100k', surface, component: 'AbovePrompt', props: BANDEAU })
    expect((await ui.find({ key: 'objectif' }))?.text).toBe('100 K : 13 450 abonnés · palier 20 000 le 15/11 : +193/jour à tenir · ton rythme : +375/jour')
  }
})

test('après le 15/11 atteint, le palier suivant prend le relais', async ($, on) => {
  monde(on, Date.UTC(2026, 10, 15, 12))
  const r = await $.command.run({ command: 'abonnes', args: '21000' } as any)
  expect(r.text).toContain('palier 45 000 le 15/12 : +800/jour à tenir')
})

test('pas de bandeau tant qu aucun relevé n est noté', async ($, on) => {
  monde(on, Date.UTC(2026, 9, 12, 12))
  on('ui.render', ($: any, e: any) => { const { Box } = $.ui.resolve(e); return h(Box, { key: 'moteur' }) })
  const ui = await $.ui.mount({ plugin: 'objectif-100k', surface: 'terminal', component: 'AbovePrompt', props: BANDEAU })
  expect(await ui.find({ key: 'objectif' })).toBeUndefined()
})

test('rappel du bilan le dimanche dès 20 h heure belge, été comme hiver', async ($, on) => {
  let maintenant = Date.UTC(2026, 9, 11, 17, 30) // dim. 11/10, 19 h 30 à Bruxelles
  monde(on, () => maintenant)
  const t = toasts(on)
  await $.session.start({} as any)
  expect(t.length).toBe(0)
  maintenant = Date.UTC(2026, 9, 11, 18, 30) // 20 h 30 à Bruxelles (heure d'été)
  await $.session.start({} as any)
  expect(t.length).toBe(1)
  maintenant = Date.UTC(2026, 10, 1, 18, 30) // dim. 01/11, 19 h 30 à Bruxelles (heure d'hiver)
  await $.session.start({} as any)
  expect(t.length).toBe(1)
  maintenant = Date.UTC(2026, 10, 1, 19, 5) // 20 h 05 à Bruxelles
  await $.session.start({} as any)
  expect(t.length).toBe(2)
  expect(t[1]).toContain('bilan')
})
