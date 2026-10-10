import { expect, test } from 'claude-code/testing'

const SURFACES = ['terminal', 'desktop'] as const
const BANDEAU = { hasSurvey: false, isWorking: false, maxRows: 10, bodyColumns: 160 } as any
const PANE = { title: "C'NABIL HUD", isFocused: false, bodyColumns: 90, placement: 'dock' } as any

// Les réponses de Metricool, au format relevé pour de vrai sur le compte de Nabil le 10/10/2026.
const REPONSES: Record<string, unknown> = {
  getBrandSettings: { data: [{ id: 7346603, timezone: 'Europe/Brussels' }] },
  evolution: { rows: [['12733.0', null, null, '378316.0', '20261009'], [null, '0.0', '0.0', null, '20261010']] },
  posts: { rows: [['2026-10-12 19:00:00', "T'inquiète #humour", '15234', '1820', '38.5'], ['2026-10-11 12:00:00', 'Ancienne', '900', '40', '20']] },
  getScheduledPosts: { data: [{ publicationDate: { dateTime: '2026-10-13T19:00:00', timezone: 'Europe/Brussels' }, text: 'Tier list foot' }] },
}

// Simule Metricool. `refuse` = noms de connecteur qui n'existent pas ; `panne` = tout échoue.
function metricool(on: any, options: { refuse?: string[]; panne?: boolean } = {}) {
  const appels: string[] = []
  on('mcp.call', ($: any, e: any) => {
    appels.push(`${e.server}/${e.tool}`)
    if (options.panne || options.refuse?.includes(e.server)) throw new Error(`serveur inconnu : ${e.server}`)
    const cle = e.tool === 'getAnalyticsDataByMetrics' ? (e.args.metrics[0].startsWith('TKEV') ? 'evolution' : 'posts') : e.tool
    return { value: { content: [{ type: 'text', text: JSON.stringify(REPONSES[cle]) }], isError: false } }
  })
  return appels
}
function session(on: any, maintenant: () => number = () => Date.UTC(2026, 9, 10, 15)) {
  on('clock.now', () => ({ value: maintenant() }))
  on('command.register', () => ({ value: undefined }))
  on('session.start', () => ({ cwd: '.' }))
  on('session.usage', () => ({
    value: { startedAt: 0, context: { window: 1_000_000, tokens: 310_000, percent: 31 }, rateLimits: [{ kind: 'five_hour', percentUsed: 23 }, { kind: 'seven_day', percentUsed: 41 }], cost: { usd: 4.2 } },
  }))
}

test('la ligne du HUD montre TikTok, le palier, le contexte et le forfait', async ($, on) => {
  metricool(on)
  session(on)
  await $.session.start({ cwd: '.' } as any)
  for (const surface of SURFACES) {
    const ui: any = await $.ui.mount({ plugin: 'cnabil-hud', surface, component: 'AbovePrompt', props: BANDEAU })
    expect((await ui.find({ key: 'tiktok' }))?.text).toBe('TikTok 12 733 ▲33 · palier 20 K le 15/11 : +197/j')
    expect((await ui.find({ key: 'contexte' }))?.text).toBe('Contexte ▰▰▰▱▱▱▱▱▱▱ 31 %')
    expect((await ui.find({ key: 'forfait' }))?.text).toBe('Forfait 5 h 23 % · 7 j 41 %')
  }
})

test('/hud ouvre le panneau : abonnés, dernière vidéo, prochaine publication, objectif, Claude', async ($, on) => {
  metricool(on)
  session(on)
  on('ui.open', () => ({ value: { isPlaced: true } }))
  await $.command.run({ command: 'hud', args: '' } as any)
  for (const surface of SURFACES) {
    const ui: any = await $.ui.mount({ plugin: 'cnabil-hud', surface, component: 'Pane', props: PANE, requestId: 'hud' })
    expect((await ui.find({ key: 't-abonnes' }))?.text).toBe('Abonnés 12 733 le 09/10 · +0 en 7 j · vues 7 j 0 · likes 378 K')
    expect((await ui.find({ key: 't-video' }))?.text).toBe("Dernière vidéo (12/10) « T'inquiète #humour » : 15 234 vues · 1 820 likes · 38,5 % vue en entier")
    expect((await ui.find({ key: 't-prochaine' }))?.text).toBe('Prochaine : 2026-10-13 19:00 · Tier list foot')
    expect((await ui.find({ key: 'o-palier' }))?.text).toBe('Palier 20 000 le 15/11 : +197 abonnés par jour à tenir')
    expect((await ui.find({ key: 'c-forfait' }))?.text).toBe('Forfait : 5 h 23 % · 7 jours 41 % · ce fil 4,20 $')
    expect(await ui.find({ key: 'actualiser' })).toBeDefined()
  }
})

test('si Metricool ne répond pas, le HUD le dit et garde le contexte', async ($, on) => {
  metricool(on, { panne: true })
  session(on)
  await $.session.start({ cwd: '.' } as any)
  const ui: any = await $.ui.mount({ plugin: 'cnabil-hud', surface: 'terminal', component: 'AbovePrompt', props: BANDEAU })
  expect((await ui.find({ key: 'tiktok' }))?.text).toBe('TikTok : Metricool pas joignable (/hud)')
  expect((await ui.find({ key: 'contexte' }))?.text).toBe('Contexte ▰▰▰▱▱▱▱▱▱▱ 31 %')
})

test('le HUD trouve le connecteur Metricool sous son autre nom', async ($, on) => {
  const appels = metricool(on, { refuse: ['claude.ai Metricool Social Media Management'] })
  session(on)
  await $.session.start({ cwd: '.' } as any)
  const ui: any = await $.ui.mount({ plugin: 'cnabil-hud', surface: 'terminal', component: 'AbovePrompt', props: BANDEAU })
  expect((await ui.find({ key: 'tiktok' }))?.text).toContain('12 733')
  expect(appels.filter(a => a.endsWith('/getScheduledPosts'))).toEqual(['Metricool Social Media Management/getScheduledPosts'])
})

test('Metricool n est relu qu après 15 minutes, pas à chaque réponse de Claude', async ($, on) => {
  const appels = metricool(on)
  let maintenant = Date.UTC(2026, 9, 10, 15)
  session(on, () => maintenant)
  on('turn.complete', ($: any, e: any) => ({ text: e.answer }))
  const tour = { answer: 'ok', durationMs: 1, isAborted: false, turnId: 't', reason: 'answer', usage: null } as any
  await $.session.start({ cwd: '.' } as any)
  const apresDemarrage = appels.length
  maintenant += 5 * 60_000
  await $.turn.complete(tour)
  expect(appels.length).toBe(apresDemarrage)
  maintenant += 11 * 60_000
  await $.turn.complete(tour)
  expect(appels.length).toBe(apresDemarrage * 2)
})
