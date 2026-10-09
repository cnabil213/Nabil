# Porter ce dépôt vers Codex (OpenAI)

> Préparé le 16/09/2026, à la demande de Nabil : « si c'est trop compliqué avec toi, autant faire
> ça avec ChatGPT, et toi tu m'aides à construire le skill pour ChatGPT. »
>
> **Tout ce qui est portable est déjà porté et commité.** Ce qui reste, c'est deux réglages dans
> l'interface Codex, et une limite qu'aucun réglage ne résout — elle est en bas, lis-la avant de
> décider.

---

## Ce qui est déjà fait dans le dépôt

| | |
| :--- | :--- |
| `AGENTS.md` | Lien symbolique vers [`CLAUDE.md`](../CLAUDE.md). Codex lit `AGENTS.md` pour les règles permanentes du dépôt — c'est son équivalent de `CLAUDE.md`. Un seul fichier, donc **aucune dérive possible** entre les deux. |
| `.agents/skills/montage/` | Lien symbolique vers [`.claude/skills/montage/`](../.claude/skills/montage/SKILL.md). `.agents/skills` est l'emplacement que Codex balaie — **pas** `.codex/skills`, qui traîne dans de vieux tutos. |
| [`setup-codex.sh`](setup-codex.sh) | Le script d'installation à coller dans Codex (voir ci-dessous). |

Le format du skill est le même des deux côtés : un `SKILL.md` avec un frontmatter `name` +
`description`. OpenAI le dit : *« Skills build on the open agent skills standard »*, et ils sont
*« exported and imported into other tools that support the Agent Skills format »*. **Aucun
enfermement**, dans un sens comme dans l'autre.

Les outils (`derusher.py`, `monter.py`, `assembler.py`, `sonoriser.py`, `icloud.py`) sont du Python
et du ffmpeg : ils tournent partout. **Rien à réécrire.**

---

## Les deux réglages à faire dans Codex

### 1. Coller le script de setup

Codex → **Settings → Environments →** (l'environnement du dépôt) **→ Setup script**.
Y coller le contenu de [`setup-codex.sh`](setup-codex.sh).

Il installe ffmpeg, les dépendances de montage et d'écoute, et **pré-télécharge le modèle Whisper
(1,6 Go)**. Ce pré-téléchargement n'est pas du confort : chez Codex, *« Setup scripts run with
internet access »* mais *« Agent internet access is off by default »*. Ce qui n'est pas descendu
pendant le setup risque de ne jamais descendre.

Le conteneur est mis en cache **jusqu'à 12 h**, et Codex *« automatically invalidates the cache if
you change the setup script »* — donc une modif du script = une réinstallation complète.

### 2. ⚠️ Activer l'accès Internet de l'agent

**C'est le réglage qui décide si le dépôt marche ou pas.** Il est sur OFF par défaut.

Sans lui : `recuperer.sh` et `icloud.py` ne peuvent rien télécharger, donc **aucun rush ne peut
entrer**, donc il n'y a pas de montage du tout. Ce n'est pas une dégradation, c'est un arrêt net.

---

## 🛑 La limite qu'aucun réglage ne résout

**Chez Codex, aucun fichier n'entre par le chat.**

La doc est explicite : *« Cloud tasks know the repository state they checked out plus the prompt and
configured environment. They do not automatically receive additional inputs beyond what is
explicitly provided in the repository. »* Et même pour les images, qui sont le seul type accepté en
pièce jointe, l'agent *« cannot access them as file bytes »*.

**Conséquence concrète pour Nabil :** le raccourci iOS « Audio pour Claude » ne sert plus à rien.
Aujourd'hui il glisse 872 Ko d'audio dans le chat et le montage démarre. Chez Codex, **même ce
fichier d'un mégaoctet devra passer par un lien iCloud**. Pour chaque clip, à chaque fois.

Autrement dit : le portage résout zéro problème d'envoi de fichier — **il en rajoute un.**

---

## La comparaison, mesurée

| | Ici (Claude Code) | Codex Cloud | ChatGPT (chat) |
| :--- | :--- | :--- | :--- |
| Fichier déposé dans le chat | **30 Mio** | **impossible** | 512 Mo, mais vidéo/audio non supportés |
| ffmpeg | installé (mesuré) | **oui, via le setup** | pas garanti dans le sandbox |
| Internet pendant le travail | oui — **15 Mo/s mesuré** | **OFF par défaut**, activable | **aucun** |
| Persistance entre sessions | git | git | session éphémère |
| Format de skill | `SKILL.md` | `SKILL.md` (même standard) | `SKILL.md` (même standard) |
| Le rush entre comment ? | chat **ou** lien | **lien uniquement** | upload aléatoire |

**Verdict honnête : Codex est à égalité sur l'exécution, et en retrait sur l'entrée des fichiers.**
ChatGPT en chat est hors course pour exécuter un montage — pas de réseau dans son sandbox, ffmpeg
incertain, session éphémère.

---

## Ce qui ne se porte pas, et qui est le vrai actif

Ni le modèle ni l'outil ne valent grand-chose ici. Ce qui vaut, c'est ce qui a été **payé par un
montage raté** :

- la prémisse du Business Bro coupée le 13/09 (« y'a plus de sens du tout à la vanne ») ;
- le blanc de 3,94 s de la tier list foot, comprimé à 0,22 s, qui fabriquait un effet qui n'a jamais
  eu lieu ;
- deux mp4 livrés sans atome `moov`, illisibles, avec ffmpeg qui sortait en code 0 ;
- la plage de couleur écrasée — noirs à 3 dans la source, 19 dans la livraison ;
- le décalage audio de 0,283 s qui posait les coupes en pleine queue de mot.

Tout ça est du markdown et du Python dans git. **Ça suit Nabil partout, quel que soit le modèle
qu'il met devant.** Le choix d'outil ne met rien de ça en danger — et n'en apporte rien non plus.

---

## Non vérifié

**Ce portage n'a jamais tourné sur un vrai Codex.** Les emplacements (`AGENTS.md`,
`.agents/skills/`) et les comportements (réseau au setup, agent hors ligne par défaut, cache 12 h)
viennent de la documentation d'OpenAI, pas d'un essai. Les liens symboliques se résolvent
correctement ici, c'est tout ce qui est mesuré.

À vérifier au premier lancement, dans cet ordre :

1. Codex voit-il le skill ? (`/skills` doit lister `montage`)
2. Lit-il bien `AGENTS.md` à travers le lien symbolique ? (sinon : remplacer le lien par une copie)
3. `command -v ffmpeg` répond-il après le setup ?
4. `bash outils/recuperer.sh "<lien iCloud>"` fait-il entrer un fichier ?

Si l'un des quatre casse, c'est réparable en quelques minutes — mais tant que les quatre n'ont pas
été faits, **ce portage est une proposition, pas un résultat.**
