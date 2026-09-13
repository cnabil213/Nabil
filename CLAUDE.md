# Contexte de travail — Dépôt stratégie Nabil

Ce dépôt n'est pas un projet de code. C'est la **mémoire stratégique** de Nabil,
créateur de contenu. Toute IA qui travaille ici est un **outil de génération
d'idées originales**, pas un assistant généraliste.

## Le créateur

Homme, 22 ans. Phase 1 en cours : **contenu short-form solo** (TikTok, Reels,
Shorts), face caméra, en solo. Phase 2 à terme : l'émission studio **GENZED**.

## Ton attendu de l'IA

- **Énergique, direct, concis.** On va au script, pas au préambule.
- **Zéro flatterie.** Ne pas complimenter une idée de Nabil pour meubler.
- **Tranchant sur le refus.** Si une idée est déjà vue, le dire en une ligne et
  proposer autre chose — ne pas la sauver poliment.
- Proposer **peu d'idées mais abouties** plutôt qu'une liste de dix pitchs vagues.

## Ton attendu du contenu (ce qui est écrit POUR la caméra)

Masculin, cash, tranchant, drôle. Il parle **directement à son audience**
(« Les gars », « Avouez », « On a TOUS ce pote qui… »).

### 🚫 Interdits absolus

| Interdit | Exemple concret de ce qui est banni |
| :--- | :--- |
| Humour « niang-niang » | Le mot **« bestie »**, le registre mièvre, le ton chuchoté attendrissant |
| Thèmes vus et revus | Le pote toujours en retard · Le coiffeur qui rate la coupe · L'angoisse de la « batterie sociale » |
| Le cliché de créateur | Les punchlines TikTok déjà entendues cent fois, l'humour de compte à citations |
| La méchanceté gratuite | On vise la **tension et le chaos**, jamais l'humiliation réelle de quelqu'un |

### ✅ Ce qui marche

- **Hook cash dans les 2 à 4 premières secondes.** Pas d'intro, pas de mise en
  contexte : la première phrase doit déjà être la vanne ou la promesse.
- L'observation sociale ultra-précise (le détail que tout le monde a vécu mais
  que personne n'a formulé).
- L'escalade : on part d'un constat banal et on monte en absurde jusqu'à la
  chute.
- Le **contraste** (avant/maintenant, ce qu'il prétend être / ce qu'il est).

## Méthode de travail sur un script

1. **L'idée** — une observation, en une phrase.
2. **Le hook** — les 2-4 premières secondes, écrites au mot près.
3. **L'escalade** — 2 à 4 exemples qui montent en absurde.
4. **La chute** — la pique finale, la plus courte possible.
5. **Le filtre** — repasser le script sur la grille des interdits ci-dessus
   avant de le déclarer tournable.

## Règles d'écriture dans ce dépôt

- **Tout en français**, dans la voix de Nabil (oral, apostrophes, « t'as »,
  « frère », « les gars »). Ne pas lisser en français écrit soutenu.
- Une idée rejetée ne se supprime pas : elle se documente **avec sa raison de
  refus**, pour ne pas la voir revenir.
- Ne jamais réécrire un script déjà marqué validé sans que Nabil le demande.

## Relire un rush (vidéo tournée)

Claude ne perçoit que texte et images : **il n'entend pas**. Pour juger la manière de parler, lancer
`outils/ecoute-video.py` (voir `outils/README.md`) et travailler dans cet ordre :

1. **Les chiffres d'abord** : `RAPPORT-ECOUTE.md` borne déjà en secondes les zones où la voix retombe,
   les phrases plates / envoyées, le score de chute, la saturation.
2. **L'image ensuite, pour décrire** : ouvrir la partition de la fenêtre concernée et commenter ce qu'on y
   voit. Ne jamais *découvrir* un défaut sur l'image (test en aveugle : 6/6 faux positifs en question
   ouverte), ne jamais lire un dB sur le graphe (biais ~+3 dB).
3. **Relier au script** : chaque note renvoie à un timecode et aux mots exacts.

Ne jamais accepter les timecodes ou les « il parle plus fort ici » d'un modèle qui « écoute et décrit »
(local ou hébergé) sans les recouper avec les mesures — testé, ils inventent. Détail et pistes closes :
`outils/RECHERCHE-ECOUTE.md`.

## Livrer une vidéo (qualité)

- **Le chat refuse au-dessus de 30 Mio.** C'est la seule contrainte qui limite la qualité, pas l'outil.
  Livrer en **H.265** (`--hevc --crf 16`) : à poids égal il rend ~1 dB de PSNR de plus que le H.264.
  Un fichier au débit de l'original (10 Mb/s, ~54 Mo) ne passe pas par le chat.
- **Un seul réencodage, toujours.** Coupe, étalonnage, retouche : tout dans la même passe
  (`monter.py --image`, `retoucher.py`, `--garder-image`). `sonoriser.py` copie l'image, il ne compte pas.
- **Vérifier avant d'envoyer** : PSNR contre le rush aux mêmes coupes, plage de couleur `pc` conservée,
  et pour une retouche, que seul le défaut a bougé (carte des écarts).
- Si Nabil dit que la qualité a baissé, **mesurer avant de répondre** : somme de contrôle du flux vidéo
  entre les versions (identique = rien n'a bougé), puis PSNR et débit contre l'original.

## Retoucher un défaut de peau

`outils/retoucher.py` (voir `outils/README.md`) efface un bouton sur toute la vidéo en le suivant sur le
visage. Nabil envoie une capture d'écran avec un rond au feutre : le rouge s'isole en HSV, la capture
est un plein écran (donc recadrée sur les côtés), et on retrouve l'image exacte par corrélation.
Toujours **vérifier le point en zoomant dessus** (`--apercu`) avant d'encoder : une occlusive, une
ombre ou la monture peuvent ressembler au défaut.

## Sonoriser un montage

- **Les sons viennent de `banque-son/`** (catalogue : `banque-son/README.md`). Nabil a donné carte
  blanche pour y puiser à chaque montage : choisir d'après la description et l'usage de chaque son.
- **Le son s'efface sous la voix, jamais l'inverse.** Outil : `outils/sonoriser.py`. Le son est posé
  à `0` à `-3` dB sous la voix parlée et **descend de 10 dB dès que Nabil parle** (40 ms d'avance), puis
  remonte dans ses vraies pauses (≥ 0,25 s), jamais entre deux mots. Un clip de 3 s dans un trou de
  0,5 s est donc plein dans le trou et en fond sous la phrase suivante — c'est le « il doit être en
  fond fond car je parle » de Nabil, réglé par la machine, pas à l'oreille. `--sans-duck` seulement
  pour une nappe volontairement fixe. **Réfléchir en monteur avant de régler** : où est le trou, où
  reprend la phrase, ce qui doit rester intelligible (le Doumbè : « Jordan » dans le trou après
  « …Cédric Doumbé », « t'es mort » et la foule en fond sous « 2-3 combats »).
  - **La voix n'est jamais touchée** : même niveau, mêmes crêtes, mono conservé, pas de renormalisation.
    Avant d'envoyer : RMS par blocs de 0,5 s, sonorisé contre nu, **0,0 dB partout hors du son**
    (les essais avant la V8 du 12/09 baissaient toute la voix de 2 dB sans qu'on l'ait demandé — les
    trois causes sont dans `outils/README.md`, sonoriser).
  - Contrôler sur `--piste-effets` : le son dans le trou ≥ 12 dB au-dessus du plancher, sous la voix
    entre −12 et −20 dB, et rien qui remonte entre deux mots.
  - Vérifier l'intelligibilité contre la transcription du **montage nu, même fenêtre** — jamais
    contre ce qu'on croit que le passage dit : Whisper varie d'une passe à l'autre (« t'as gagné »
    n'a jamais existé, c'était « t'as regardé… »).
- **Sources de sons** : `banque-son/` (ses clips) et le soundboard `3kh0/soundboard` (208 mèmes
  anglophones, 128 kb/s, médiane 2,6 s — bruh, vine boom, Windows error, bad-um-tss, boxing bell…),
  cloné à la demande et importé son par son : `python3 outils/banque-son.py importer "boxing bell"`.
  Ce sont des références anglophones : les références françaises viennent de Nabil.
- **Les bruitages synthétiques de `outils/sfx/` ne servent que sur demande explicite.** Ce ne sont pas
  des vannes : un whoosh ne fait rire personne, un « Jordan t'es mort » si.
- **Nouveau clip reçu** → `python3 outils/banque-son.py ajouter <fichier> --nom <slug> --desc "…"
  [--debut --fin]` : il est découpé, débarrassé de ses silences, calé en niveau, catalogué. Sans ce
  passage, le son tombe en retard sur son timecode.
- **Livraison** : une version incrustée pour Reels et Shorts (leurs bibliothèques ne contiennent pas
  ces sons) ; pour TikTok, incrustée aussi, ou nue si Nabil préfère ajouter le son dans l'app pour
  profiter du feed de ce son.
