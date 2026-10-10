import { expect, test } from 'claude-code/testing'

const BACKLOG = 'phase-1-solo/scripts/02-backlog-idees.md'
// Un extrait du vrai fichier (dépôt Nabil, 10/10/2026).
const AVANT = [
  '## 🔴 Brûlées — ne pas reproposer',
  '',
  'Ces angles sont **morts**.',
  '',
  '| Idée / thème | Raison du refus |',
  '| :--- | :--- |',
  '| Le pote toujours en retard | Vu et revu, saturé sur le feed |',
  '| Le pote qui envoie des vocaux de 4 minutes | Saturé (15/09) |',
  '',
  '## 📌 Rappel de méthode',
  '',
].join('\n')

function disque(on: any, depart: Record<string, string>) {
  const fichiers: Record<string, string> = { ...depart }
  on('clock.now', () => ({ value: Date.UTC(2026, 9, 10, 22, 30) })) // 11/10 à 0 h 30 à Bruxelles
  const cle = (chemin: string) => chemin.slice(chemin.indexOf('phase-1-solo/'))
  on('fs.exists', ($: any, e: any) => ({ value: cle(e.path) in fichiers }))
  on('fs.read', ($: any, e: any) => ({ value: fichiers[cle(e.path)] }))
  on('fs.write', ($: any, e: any) => { fichiers[cle(e.path)] = e.text; return { value: undefined } })
  return fichiers
}

test('/refus ajoute la ligne à la fin du tableau des brûlées, datée à l heure belge', async ($, on) => {
  const fichiers = disque(on, { [BACKLOG]: AVANT })
  const r = await $.command.run({ command: 'refus', args: 'Le pote qui filme tout au concert — vu et revu' } as any)
  expect(r.text).toContain('Brûlée')
  const lignes = fichiers[BACKLOG]!.split('\n')
  expect(lignes[8]).toBe('| Le pote qui filme tout au concert | vu et revu (11/10) |')
  expect(lignes[9]).toBe('')
  expect(lignes[10]).toBe('## 📌 Rappel de méthode')
})

test('/refus reconnaît une idée déjà brûlée', async ($, on) => {
  const fichiers = disque(on, { [BACKLOG]: AVANT })
  const r = await $.command.run({ command: 'refus', args: 'le pote toujours en retard : saturé' } as any)
  expect(r.text).toContain('Déjà brûlée')
  expect(fichiers[BACKLOG]).toBe(AVANT)
})

test('/refus sans raison explique quoi écrire et ne touche à rien', async ($, on) => {
  const fichiers = disque(on, { [BACKLOG]: AVANT })
  const r = await $.command.run({ command: 'refus', args: 'le pote qui filme tout' } as any)
  expect(r.text).toContain('sa raison')
  expect(fichiers[BACKLOG]).toBe(AVANT)
})

test('/refus hors du dépôt Nabil ne crée rien', async ($, on) => {
  const fichiers = disque(on, {})
  const r = await $.command.run({ command: 'refus', args: 'idée — raison' } as any)
  expect(r.text).toContain('introuvable')
  expect(Object.keys(fichiers).length).toBe(0)
})
