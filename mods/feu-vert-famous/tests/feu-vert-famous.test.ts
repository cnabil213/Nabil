import { expect, test } from 'claude-code/testing'

// Simule la fenêtre de question : répond `reponse` à la première question posée, et garde la question.
function repondre(on: any, reponse: string, questions: string[] = []) {
  on('tool.call', { tool: 'AskUserQuestion' }, ($: any, e: any) => {
    questions.push(e.questions[0].question)
    return { result: { questions: e.questions, answers: { [e.questions[0].question]: reponse } } }
  })
  return questions
}

test('une publication Metricool part quand Nabil dit oui', async ($, on) => {
  const questions = repondre(on, 'Oui, vas-y')
  on('tool.call', () => ({ result: 'programmé' }))
  const r: any = await $.tool.call({ tool: 'mcp__Metricool_Social_Media_Management__createScheduledPost', text: 'V1 · T inquiète' } as any)
  expect(r.result).toBe('programmé')
  expect(questions[0]).toContain('publier ou programmer sur tes réseaux')
})

test('une publication est bloquée quand Nabil dit non', async ($, on) => {
  repondre(on, 'Non, bloque')
  on('tool.call', () => ({ result: 'programmé' }))
  const r: any = await $.tool.call({ tool: 'mcp__Metricool_Social_Media_Management__updateScheduledPost', id: 7 } as any)
  expect(r.deny).toContain('publier')
})

test('renommer ou jeter un fichier du Drive demande le feu vert', async ($, on) => {
  const questions = repondre(on, 'Non, bloque')
  on('tool.call', () => ({ result: 'fait' }))
  const renommer: any = await $.tool.call({ tool: 'mcp__Google_Drive__update_file', fileId: 'abc', name: 'rush-1.mov' } as any)
  const jeter: any = await $.tool.call({ tool: 'mcp__Google_Drive__trash_file', fileId: 'abc' } as any)
  expect(renommer.deny).toBeDefined()
  expect(jeter.deny).toBeDefined()
  expect(questions.every(q => q.includes('modifier ton Google Drive'))).toBe(true)
})

test('lancer un robot Apify ou une génération ElevenLabs demande le feu vert', async ($, on) => {
  const questions = repondre(on, 'Non, bloque')
  on('tool.call', () => ({ result: 'lancé' }))
  await $.tool.call({ tool: 'mcp__Apify__call-actor', actor: 'clockworks/tiktok-scraper' } as any)
  await $.tool.call({ tool: 'mcp__ElevenLabs__creative_generate_speech', text: 'JORDAN' } as any)
  expect(questions[0]).toContain('crédits Apify')
  expect(questions[1]).toContain('crédits ElevenLabs')
})

test('si la question ne peut pas être posée, on bloque', async ($, on) => {
  on('tool.call', { tool: 'AskUserQuestion' }, () => { throw new Error('fenêtre fermée') })
  on('tool.call', () => ({ result: 'programmé' }))
  const r: any = await $.tool.call({ tool: 'mcp__Metricool_Social_Media_Management__createScheduledPost' } as any)
  expect(r.deny).toBeDefined()
})

test('les lectures passent sans question, et le partage reste au mod feu-vert', async ($, on) => {
  const questions = repondre(on, 'Non, bloque')
  on('tool.call', () => ({ result: 'ok' }))
  for (const tool of [
    'mcp__Metricool_Social_Media_Management__getAnalyticsDataByMetrics',
    'mcp__Metricool_Social_Media_Management__getBestTimeToPostByNetwork',
    'mcp__Google_Drive__download_file_content',
    'mcp__Google_Drive__share_file',
    'mcp__Apify__get-dataset-items',
    'mcp__ElevenLabs__creative_list_voices',
    'Read',
  ]) {
    const r: any = await $.tool.call({ tool } as any)
    expect(r.result).toBe('ok')
  }
  expect(questions.length).toBe(0)
})
