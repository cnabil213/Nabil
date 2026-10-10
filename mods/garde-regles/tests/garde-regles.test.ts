import { expect, test } from 'claude-code/testing'

// Le dépôt simulé : ce que git répond sur les fichiers prêts à être enregistrés.
function git(on: any, prets: string[] = [], nonSuivis: string[] = []) {
  on('process.run', ($: any, e: any) => {
    const argv: string[] = e.argv
    if (argv.includes('diff')) return { value: { exitCode: 0, stdout: prets.join('\n'), stderr: '' } }
    if (argv.includes('status')) return { value: { exitCode: 0, stdout: nonSuivis.map(f => '?? ' + f).join('\n'), stderr: '' } }
    return { value: { exitCode: 1, stdout: '', stderr: '' } }
  })
}
const bash = (command: string) => ({ tool: 'Bash', command } as any)

test('un grep sur la sortie de monter.py est refusé', async ($, on) => {
  on('tool.call', () => ({ result: { stdout: 'OK', stderr: '' } }))
  const r: any = await $.tool.call(bash('python3 outils/monter.py rush.mov 0:1-9 -o livraisons/v.mp4 | grep OK'))
  expect(r.deny).toContain('ne jamais filtrer')
  const r2: any = await $.tool.call(bash('ffmpeg -i a.mov b.mp4 2>/dev/null'))
  expect(r2.deny).toBeDefined()
})

test('la sortie complète dans un fichier passe', async ($, on) => {
  git(on)
  on('tool.call', () => ({ result: { stdout: '', stderr: '' } }))
  const r: any = await $.tool.call(bash('python3 outils/monter.py rush.mov 0:1-9 -o /tmp/v.mp4 > log.txt 2>&1; tail -n 40 log.txt'))
  expect(r.deny).toBeUndefined()
})

test('un commit d un montage jamais passé par ffprobe est refusé', async ($, on) => {
  git(on, ['livraisons/11oct-pote-volant-HQ.mp4'])
  on('tool.call', () => ({ result: { stdout: '', stderr: '' } }))
  const r: any = await $.tool.call(bash('git commit -m "Livre le pote au volant"'))
  expect(r.deny).toContain('livraisons/11oct-pote-volant-HQ.mp4')
})

test('après un ffprobe réussi, le commit passe', async ($, on) => {
  git(on, ['livraisons/11oct-pote-volant-HQ.mp4'])
  on('tool.call', () => ({ result: { stdout: '"duration": "41.7"', stderr: '' } }))
  await $.tool.call(bash('ffprobe -v error -show_format -show_streams livraisons/11oct-pote-volant-HQ.mp4'))
  const r: any = await $.tool.call(bash('git add livraisons/11oct-pote-volant-HQ.mp4 && git commit -m "Livre"'))
  expect(r.deny).toBeUndefined()
})

test('un ffprobe en erreur ne vérifie rien, et un réencodage efface la vérification', async ($, on) => {
  git(on, ['livraisons/v.mp4'])
  let erreur = true
  on('tool.call', () => (erreur ? { result: { stdout: '', stderr: 'moov atom not found' }, isError: true } : { result: { stdout: '', stderr: '' } }))
  await $.tool.call(bash('ffprobe -v error -show_format livraisons/v.mp4'))
  expect(((await $.tool.call(bash('git commit -m x'))) as any).deny).toBeDefined()

  erreur = false
  await $.tool.call(bash('ffprobe -v error -show_format livraisons/v.mp4'))
  expect(((await $.tool.call(bash('git commit -m x'))) as any).deny).toBeUndefined()
  await $.tool.call(bash('ffmpeg -y -i rush.mov -c:v libx264 livraisons/v.mp4 > log.txt 2>&1'))
  expect(((await $.tool.call(bash('git commit -m x'))) as any).deny).toBeDefined()
})

test('git add -A voit aussi un mp4 pas encore suivi', async ($, on) => {
  git(on, [], ['livraisons/nouveau.mp4'])
  on('tool.call', () => ({ result: { stdout: '', stderr: '' } }))
  const r: any = await $.tool.call(bash('git add -A && git commit -m "Tout"'))
  expect(r.deny).toContain('nouveau.mp4')
})

test('un commit sans vidéo passe sans rien demander', async ($, on) => {
  git(on, [])
  on('tool.call', () => ({ result: { stdout: '', stderr: '' } }))
  const r: any = await $.tool.call(bash('git add ETAT.md JOURNAL.md && git commit -m "Fin de session"'))
  expect(r.deny).toBeUndefined()
})

test('« bestie » est refusé dans un script, pas dans la liste des brûlées', async ($, on) => {
  on('tool.call', () => ({ result: 'écrit' }))
  const script: any = await $.tool.call({ tool: 'Write', file_path: '/repo/phase-1-solo/scripts/10-nouveaux.md', content: 'Hook : ma bestie a fait…' } as any)
  expect(script.deny).toContain('interdit absolu')
  const backlog: any = await $.tool.call({ tool: 'Edit', file_path: '/repo/phase-1-solo/scripts/02-backlog-idees.md', old_string: 'a', new_string: '| Tout script contenant « bestie » |' } as any)
  expect(backlog.result).toBe('écrit')
})

test('toucher aux scripts validés demande à Nabil', async ($, on) => {
  const questions: string[] = []
  on('tool.call', { tool: 'AskUserQuestion' }, ($: any, e: any) => {
    questions.push(e.questions[0].question)
    return { result: { questions: e.questions, answers: { [e.questions[0].question]: 'Non, bloque' } } }
  })
  on('tool.call', () => ({ result: 'écrit' }))
  const r: any = await $.tool.call({ tool: 'Edit', file_path: '/repo/phase-1-solo/scripts/01-scripts-valides.md', old_string: 'a', new_string: 'b' } as any)
  expect(r.deny).toContain('scripts validés')
  expect(questions.length).toBe(1)
  const autre: any = await $.tool.call({ tool: 'Edit', file_path: '/repo/phase-1-solo/scripts/07-scripts-narrateur-17-09.md', old_string: 'a', new_string: 'b' } as any)
  expect(autre.result).toBe('écrit')
  expect(questions.length).toBe(1)
})
