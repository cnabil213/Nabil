// Barrière « feu vert » propre à C'Nabil-Famous : publier, toucher au Drive, dépenser des crédits.
// Elle COMPLÈTE le mod feu-vert de C'Nabil Rich (e-mails, agenda partagé avec Sady, partage d'un fichier),
// qui s'installe pour tous les projets : ici, on ne repose pas les questions qu'il pose déjà.
// Règles d'origine (CLAUDE.md du dépôt Nabil, 10/10/2026) : « Avant d'agir (classer, renommer, couper,
// publier, conseiller), on confirme » ; et « Tourner, publier, répondre aux commentaires : toi ».
import type { Register } from 'claude-code'

// Chaque famille d'action : le motif du nom de l'outil, et ce qu'on dit à Nabil.
// Pour en ajouter une, ajoute une ligne.
const FAMILLES: { motif: RegExp; quoi: string }[] = [
  // Programmer, modifier ou envoyer en validation une publication sur ses réseaux.
  { motif: /^mcp__.*metricool.*__(create|update|send)/i, quoi: 'publier ou programmer sur tes réseaux' },
  // Renommer, déplacer, copier, créer ou jeter un fichier du Drive (le partage est déjà gardé par feu-vert).
  { motif: /^mcp__.*drive.*__(update|trash|copy|create)_file/i, quoi: 'modifier ton Google Drive' },
  // Lancer un robot Apify : il consomme des crédits payants.
  { motif: /^mcp__.*apify.*__call-actor/i, quoi: 'dépenser des crédits Apify' },
  // Générer ou retoucher un son, une image ou une vidéo : chaque génération est facturée.
  { motif: /^mcp__.*elevenlabs.*__creative_(generate|edit|design)/i, quoi: 'dépenser des crédits ElevenLabs' },
]

const OUI = 'Oui, vas-y'
const NON = 'Non, bloque'

// Résume l'action en une ligne : l'outil et ses principaux champs.
function resume(e: Record<string, unknown>): string {
  const champs = Object.entries(e)
    .filter(([cle]) => cle !== 'tool' && cle !== 'tool_use_id')
    .map(([cle, valeur]) => `${cle} : ${typeof valeur === 'string' ? valeur : JSON.stringify(valeur)}`)
    .join(' · ')
  const court = champs.length > 300 ? champs.slice(0, 300) + '…' : champs
  return `${String(e.tool).replace(/^mcp__/, '')} (${court})`
}

export const register: Register = on => {
  on('tool.call', async ($, e, next) => {
    const famille = FAMILLES.find(f => f.motif.test(String(e.tool)))
    if (famille === undefined) return next(e)

    const choix = await $.ui.ask(`Claude veut ${famille.quoi} : ${resume(e)}. Tu donnes ton feu vert ?`, {
      header: 'Feu vert',
      options: [OUI, NON],
    })
    if (choix === OUI) {
      $.ui.log(`feu vert donné : ${String(e.tool)}`)
      return next(e)
    }
    $.ui.log(`feu vert refusé : ${String(e.tool)}`)
    return { deny: `Nabil n'a pas donné son feu vert pour ${famille.quoi} (réponse : « ${choix} »). Ne réessaie pas sans son accord écrit.` }
  }).catch(($, e, next) =>
    // Si la question n'a pas pu être posée (fenêtre fermée, mode sans écran), on bloque.
    next.called ? next(e) : { deny: 'Feu vert impossible à demander : action bloquée par sécurité.' },
  )
}
