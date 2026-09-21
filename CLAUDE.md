# Contexte de travail — Dépôt stratégie Nabil

Ce dépôt n'est pas un projet de code. C'est la **mémoire de travail de Nabil**, créateur de
contenu, et elle est faite pour le suivre d'une session à l'autre. Toute IA qui travaille ici
est un **outil de génération d'idées originales** et un **monteur**, pas un assistant généraliste.

---

## Démarrer et finir une session

**Au démarrage** — [`ETAT.md`](ETAT.md) est injecté automatiquement par le hook de session.
Il dit où on en est, ce qui est en cours, et les prochaines actions. Le lire avant toute chose.

**Les formats du compte sont catalogués dans [`FORMATS.md`](FORMATS.md)** (racine du dépôt) :
**Bakhal Man**, **Le Journaliste**, La Note cachée, Le GPS de la vie, Le Contrôle technique, la tier
list. **Le lire avant de proposer un format ou d'écrire un épisode** — ne jamais réinventer un format
qui existe déjà, ni reproposer un concept brûlé.

**À la fin** — deux gestes, jamais l'un sans l'autre :

1. Réécrire [`ETAT.md`](ETAT.md) pour qu'il colle à la réalité (il se remplace, il ne s'empile pas).
2. Ajouter une entrée en haut de [`JOURNAL.md`](JOURNAL.md) : ce qui a été fait, ce qui a été
   décidé, ce qui a été appris.

**Le conteneur est effacé entre deux sessions.** Rushs, montages et analyses ne survivent pas.
Seul ce qui est commité reste. Un commit = une décision ou un livrable, avec un message qui dit
*pourquoi*, pas seulement *quoi* : c'est ce message que la session suivante lira.

---

## Le créateur

Homme, 22 ans. Phase 1 en cours : **contenu short-form solo** (TikTok, Reels, Shorts), face
caméra, en solo. Phase 2 à terme : l'émission studio **GENZED**.

## Ton attendu de l'IA

- **Énergique, direct, concis.** On va au script, pas au préambule.
- **Zéro flatterie.** Ne pas complimenter une idée de Nabil pour meubler.
- **Tranchant sur le refus.** Si une idée est déjà vue, le dire en une ligne et proposer autre
  chose — ne pas la sauver poliment.
- Proposer **peu d'idées mais abouties** plutôt qu'une liste de dix pitchs vagues.
- **Annoncer ce qui va prendre du temps.** Un travail de fond est bienvenu, une attente non
  annoncée ne l'est pas : prévenir avant, et donner d'abord la version rapide si elle existe.

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

- **Hook cash dans les 2 à 4 premières secondes.** Pas d'intro, pas de mise en contexte : la
  première phrase doit déjà être la vanne ou la promesse.
- L'observation sociale ultra-précise (le détail que tout le monde a vécu mais que personne n'a
  formulé).
- L'escalade : on part d'un constat banal et on monte en absurde jusqu'à la chute.
- Le **contraste** (avant/maintenant, ce qu'il prétend être / ce qu'il est).

## Méthode de travail sur un script

1. **L'idée** — une observation, en une phrase.
2. **Le hook** — les 2-4 premières secondes, écrites au mot près.
3. **L'escalade** — 2 à 4 exemples qui montent en absurde.
4. **La chute** — la pique finale, la plus courte possible.
5. **Le filtre** — repasser le script sur la grille des interdits ci-dessus avant de le déclarer
   tournable.

## Règles d'écriture dans ce dépôt

- **Tout en français**, dans la voix de Nabil (oral, apostrophes, « t'as », « frère »,
  « les gars »). Ne pas lisser en français écrit soutenu.
- Une idée rejetée ne se supprime pas : elle se documente **avec sa raison de refus**, pour ne
  pas la voir revenir.
- Ne jamais réécrire un script déjà marqué validé sans que Nabil le demande.

---

## La règle qui prime : rien sans mesure

**On ne juge rien à l'œil ni à l'oreille sans un chiffre derrière.** Claude n'entend pas, et se
trompe quand il « regarde » une image sans mesure préalable. Les contre-exemples, tous vécus sur
ce projet :

| Ce qui a été affirmé | Ce que la mesure disait |
| :--- | :--- |
| « Ce défaut se voit sur l'image » (question ouverte, en aveugle) | 6 faux positifs sur 6 |
| « Il parle plus fort ici » (modèle audio local) | Timecodes inventés, biais de position 8/8 |
| « Le H.265 est meilleur, son PSNR est plus haut » | Il conservait **moins** de détail (91,3 % contre 92,8 %) |
| « Son original est en 1080p » | Ses métadonnées disaient 720p |
| « Ces deux captures montrent le même moment » | 0,17 s d'écart : l'une nette, l'autre floue |
| « La qualité a baissé » → une explication | Mesurer **d'abord**, répondre ensuite |

Corollaire : quand Nabil signale un problème, la première réponse est une mesure, pas une
hypothèse. Et quand une mesure contredit ce qu'on a affirmé plus tôt, **on se corrige
explicitement** — dans la réponse et dans le dépôt.

---

## Technique : les cinq règles, et où est le détail

Le mode d'emploi complet des outils est dans [`outils/README.md`](outils/README.md).
Ce qui suit, ce sont les règles qu'on ne redécouvre pas.

### 1. Relire un rush → [`outils/ecoute-video.py`](outils/ecoute-video.py)

Les chiffres d'abord (`RAPPORT-ECOUTE.md` borne les zones en secondes), **l'image seulement pour
décrire** ce que les chiffres ont déjà trouvé. Ne jamais lire un dB sur un graphe (biais ~+3 dB).
Vocabulaire et limites : [`outils/README-ecoute.md`](outils/README-ecoute.md). Pistes closes :
[`outils/RECHERCHE-ECOUTE.md`](outils/RECHERCHE-ECOUTE.md).

### 2. Monter → [`outils/monter.py`](outils/monter.py)

**Un seul réencodage**, toujours : coupe, étalonnage et retouche dans la même passe. Conserver la
plage de couleur de la source. Poser les coupes dans un silence réel, mesuré à l'enveloppe — pas
sur une borne de mot (Whisper finit les mots trop tôt, et une occlusive fabrique un silence *au
milieu* d'un mot). **La première image gardée doit être nette** : sur TikTok, c'est la vignette.

### 2 bis. Monter une vanne : on ne coupe JAMAIS la prémisse

**La règle du hook ne donne pas le droit de supprimer ce qui rend la vanne compréhensible.**
Erreur commise le 13/09 sur le Business Bro : le meilleur moment mesuré était l'imitation du
personnage (+22,3 dB, chute 100/100), j'ai démarré le montage dessus, et Nabil a répondu
« on comprend pas le contexte, y'a plus de sens du tout à la vanne ». Il avait raison : sans le
pote qui fait le mec business, l'imitation tombe sur rien.

La méthode, dans cet ordre :

1. **Écrire la chaîne de sens** avant de toucher aux ciseaux : qui est le personnage → ce qu'il
   fait → ce que TOI tu fais face à lui → l'escalade → la chute. Chaque maillon manquant casse tout.
2. **Couper DANS les maillons, jamais un maillon entier.** Sur ce rush, « s'immiscent » était dit
   trois fois de suite : on garde la seule phrase qui nomme le sujet ET son domaine
   (« ils s'immiscent dans les e-commerce, dans le trading »), on jette les deux redites.
3. **Ne couper que sur un silence mesuré** (≥ 0,10 s à l'enveloppe). Une redite sans silence autour
   d'elle ne se coupe pas : on la garde.
3 bis. **Un silence n'est pas toujours un temps mort : il porte parfois une information.** Resserrer
   un blanc rapproche ce qu'il sépare, et peut fabriquer un effet qui n'a pas eu lieu. Constaté le
   14/09 sur la tier list foot : le blanc de 3,7 s après Musiala, ramené à 0,22 s, faisait croire que
   Nabil et Sady avaient dit « mais qui est ce mec ? » en chœur, exprès. Nabil : « alors que non,
   même pas. » Avant de comprimer un blanc, se demander ce qu'il sépare — surtout entre deux
   locuteurs, où la simultanéité se lit comme une intention.
4. **Relire la transcription du montage** avant de livrer. Si elle ne se tient pas toute seule à la
   lecture, le montage est faux, quels que soient les chiffres.

Les mesures disent où ça retombe et où ça envoie. **Elles ne disent pas ce qui se comprend.**

### 3. Sonoriser → [`outils/sonoriser.py`](outils/sonoriser.py)

Les sons viennent de [`banque-son/`](banque-son/), carte blanche pour y puiser. **Le son s'efface
sous la voix, jamais l'inverse** : il descend de 10 dB dès que Nabil parle et remonte dans ses
vraies pauses. La voix n'est jamais touchée — le vérifier par RMS sur blocs de 0,5 s, sonorisé
contre nu : 0,0 dB partout hors du son. Deux sons par vidéo au maximum. Les bruitages
synthétiques de `outils/sfx/` ne servent que sur demande explicite : un whoosh ne fait rire
personne, un « JORDAN » de Doumbé si.

### 2 ter. Assembler plusieurs prises → [`outils/assembler.py`](outils/assembler.py)

Quand un sujet est tourné en **plusieurs clips** (une prise par idée, plusieurs prises de la même
fin), `monter.py` ne suffit pas : il ne coupe que dans un fichier. `assembler.py` prend des morceaux
`FICHIER:DEBUT-FIN` **dans l'ordre du montage**, venus de fichiers différents, et n'encode qu'une
fois. Il refuse d'assembler des sources de taille ou de cadence différentes.

Méthode, le 15/09 sur « T'inquiète » (5 clips, 1 min 44 → 36,7 s) :

1. **Transcrire tous les clips** avant de décider quoi que ce soit. C'est la transcription qui révèle
   l'ordre réel et les doublons — les horodatages des fichiers, eux, se chevauchent et mentent.
2. **Écrire la chaîne de sens** (§2 bis), puis choisir pour chaque maillon la meilleure prise.
3. **Quand plusieurs prises disent la même chose, mesurer** : débit de parole, niveau, et surtout
   si la chute est correctement dite. Sur ces trois prises, une ratait la négation.
4. **Ne pas couper un mot au ras du raccord** : finir dans le silence qui suit, pas sur la fin du
   mot. Vérifier après coup le niveau de part et d'autre de chaque raccord.

### 3 bis. Vérifier le fichier écrit, toujours

**Un encodage interrompu produit un mp4 de la bonne taille, sans atome `moov`, illisible partout —
et ffmpeg peut sortir en code 0.** Deux tier lists ont été livrées ainsi le 14/09.
`monter.py` relit maintenant sa sortie (durée + lisibilité) et refuse d'annoncer un succès sinon.
Le défaut est intermittent : la même commande aboutit une fois sur deux, donc **relancer suffit**,
mais ne jamais annoncer une livraison sans `ffprobe` sur le fichier final.

Corollaire de méthode : ne jamais filtrer la sortie d'un outil avec un `grep` qui ne garde que la
ligne de succès. C'est comme ça que l'erreur est passée.

### 4. Livrer → [`livraisons/`](livraisons/)

Le chat plafonne à **30 Mio** et coûte 7 % de détail. Les montages finis vont dans `livraisons/`,
au débit de la source, et se téléchargent depuis GitHub. Juger la qualité au **détail conservé**
(écart-type du passe-haut, rapporté à la source), pas au PSNR. Tableau de mesures :
[`livraisons/README.md`](livraisons/README.md).

### 5. Tourner : le plafond se joue avant le montage

Le rush du 12/09 est **une capture Snapchat** — sa métadonnée `com.apple.quicktime.description`
le dit en clair, et l'original dans Photos fait **720p, HEVC, 57 Mo**. Un montage ne peut pas être
plus net que son rush.

- **Filmer avec l'app Caméra**, pas dans Snapchat, qui plafonne à 720p là où l'iPhone fait du
  1080p et du 4K.
- **Envoyer le fichier tel quel** : Photos → « Enregistrer dans Fichiers », puis WeTransfer par
  Safari ou AirDrop. Un partage direct vers une app fait reconvertir le HEVC en H.264 par iOS
  (c'est pourquoi le fichier reçu pesait 98 Mo pour la même image que 57 Mo d'original).
- **Premier réflexe sur un rush reçu** : `ffprobe -v error -show_format -show_streams`, lire la
  résolution et les tags, et le dire à Nabil **avant** de monter.

### En prime : retoucher un défaut de peau → [`outils/retoucher.py`](outils/retoucher.py)

Efface un bouton sur toute la vidéo en le suivant sur le visage. Nabil envoie une capture annotée
au feutre rouge ; le rouge s'isole en HSV et l'image exacte se retrouve par corrélation. Toujours
**vérifier le point en zoomant dessus** (`--apercu`) avant d'encoder.
