// Garde des règles : quatre phrases du CLAUDE.md du dépôt Nabil (C'Nabil-Famous) deviennent des verrous.
// 1. « Ne jamais filtrer la sortie d'un outil avec un grep qui ne garde que la ligne de succès » (§3 bis) :
//    deux tier lists illisibles ont été livrées comme ça le 14/09.
// 2. « Ne jamais annoncer une livraison sans ffprobe sur le fichier final » (§3 bis) :
//    pas de commit d'un mp4 de livraisons/ qui n'est pas passé par ffprobe depuis sa dernière écriture.
// 3. Interdit absolu : le mot « bestie » dans un script ou un format.
// 4. « Ne jamais réécrire un script déjà marqué validé sans que Nabil le demande » : on lui demande.
import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { MontagesVerifies } from '../types'

const OUTILS_MONTAGE = /\b(ffmpeg|ffprobe|monter\.py|assembler\.py|sonoriser\.py|derusher\.py|retoucher\.py|ecoute-video\.py)\b/
// Ce qui cache une erreur : un grep, un « tail -1 », ou la sortie d'erreur jetée.
const FILTRE = /\|\s*(grep|tail\s+(-n\s*)?-?1\b)|2>\s*\/dev\/null/
const ECRITURE = /\b(ffmpeg|monter\.py|assembler\.py|sonoriser\.py|retoucher\.py|cp|mv|curl|wget|recuperer\.sh)\b/
const GIT_ENVOI = /\bgit\b[^;&|]*\b(add|commit)\b/
const TOUT_AJOUTER = /\bgit\b[^;&|]*\b(add\s+(-A|--all|\.(\s|$))|commit\s+-\w*a)/
const SCRIPTS_VALIDES = 'phase-1-solo/scripts/01-scripts-valides.md'
const INTERDITS: { motif: RegExp; raison: string }[] = [
  { motif: /\bbesties?\b/i, raison: '« bestie » est un interdit absolu (registre niang-niang, CLAUDE.md)' },
]

const verifies = atom({ plugin: 'garde-regles', key: 'verifies' } as const, [] as MontagesVerifies)

const nom = (chemin: string) => chemin.split('/').pop() ?? chemin

// Les mp4 cités dans une commande, avec ceux qui sont lus (après -i) et ceux qui sont écrits.
function mp4Cites(commande: string): { lus: string[]; autres: string[] } {
  const mots = commande.split(/\s+/).map(m => m.replace(/^["']|["';]$/g, ''))
  const lus: string[] = []
  const autres: string[] = []
  mots.forEach((mot, i) => {
    if (!/\.mp4$/i.test(mot)) return
    ;(mots[i - 1] === '-i' ? lus : autres).push(nom(mot))
  })
  return { lus, autres }
}

// Les mp4 de livraisons/ qu'un « git add » ou « git commit » va enregistrer.
async function mp4AEnregistrer($: EngineInterface, commande: string): Promise<string[]> {
  const chemins = commande.split(/\s+/).filter(m => /livraisons\/.*\.mp4$/i.test(m))
  const lancer = async (argv: string[]) => {
    try {
      const r = await $.process.run(argv)
      return r.exitCode === 0 ? r.stdout.split('\n') : []
    } catch {
      return []
    }
  }
  chemins.push(...(await lancer(['git', 'diff', '--cached', '--name-only', '--', 'livraisons'])))
  if (TOUT_AJOUTER.test(commande)) {
    const etat = await lancer(['git', 'status', '--porcelain', '-uall', '--', 'livraisons'])
    chemins.push(...etat.map(l => l.slice(3)))
  }
  return [...new Set(chemins.map(c => c.trim()).filter(c => /\.mp4$/i.test(c)).map(nom))]
}

export const register: Register = on => {
  // Verrous 1 et 2 : les commandes.
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const commande = String(e.command)

    if (OUTILS_MONTAGE.test(commande) && FILTRE.test(commande)) {
      return {
        deny:
          "Règle du dépôt (CLAUDE.md §3 bis) : ne jamais filtrer la sortie d'un outil de montage (grep, tail -1, 2>/dev/null). " +
          "Un mp4 sans atome moov sort parfois en code 0. Relance sans filtre, ou écris tout dans un fichier (> log.txt 2>&1) et lis-le en entier.",
      }
    }

    if (GIT_ENVOI.test(commande)) {
      const ok = await read($, verifies)
      const manquants = (await mp4AEnregistrer($, commande)).filter(f => !ok.includes(f))
      if (manquants.length > 0) {
        return {
          deny:
            `Pas de ffprobe sur ${manquants.map(f => 'livraisons/' + f).join(', ')} depuis sa dernière écriture (CLAUDE.md §3 bis : ` +
            'un mp4 peut avoir la bonne taille et être illisible). Lance « ffprobe -v error -show_format -show_streams » sur ce fichier, ' +
            'lis la durée, puis recommence.',
        }
      }
    }

    const fin = await next(e)

    // Après coup : un ffprobe réussi vérifie un fichier, une écriture le dé-vérifie.
    const { lus, autres } = mp4Cites(commande)
    const reussi = 'result' in fin && fin.result !== undefined && fin.isError !== true
    if (/\bffprobe\b/.test(commande) && !ECRITURE.test(commande)) {
      if (reussi) await update($, verifies, v => [...new Set([...v, ...lus, ...autres])])
    } else if (ECRITURE.test(commande) && autres.length > 0) {
      await update($, verifies, v => v.filter(f => !autres.includes(f)))
    }
    return fin
  })

  // Verrous 3 et 4 : les fichiers de scripts.
  on('tool.call', async ($, e, next) => {
    if (e.tool !== 'Edit' && e.tool !== 'Write') return next(e)
    const champs = e as { file_path?: unknown; content?: unknown; new_string?: unknown }
    const chemin = String(champs.file_path ?? '')
    const texte = String(champs.content ?? champs.new_string ?? '')

    const estUnScript = chemin.includes('phase-1-solo/scripts/') || chemin.endsWith('FORMATS.md')
    // La liste des idées brûlées a le droit de citer un interdit : c'est elle qui l'interdit.
    if (estUnScript && !chemin.endsWith('02-backlog-idees.md')) {
      const interdit = INTERDITS.find(i => i.motif.test(texte))
      if (interdit !== undefined) return { deny: `${interdit.raison}. Réécris sans.` }
    }

    if (!chemin.endsWith(SCRIPTS_VALIDES)) return next(e)
    const choix = await $.ui.ask("Claude veut modifier le fichier des scripts validés. C'est toi qui l'as demandé ?", {
      header: 'Scripts validés',
      options: ["Oui, je l'ai demandé", 'Non, bloque'],
    })
    if (choix === "Oui, je l'ai demandé") return next(e)
    return { deny: "Nabil n'a pas demandé de toucher aux scripts validés (CLAUDE.md : on ne réécrit jamais un script validé sans sa demande)." }
  }).catch(($, e, next) => (next.called ? next(e) : { deny: 'Question impossible à poser : modification des scripts validés bloquée.' }))
}
