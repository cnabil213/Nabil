---
name: montage
description: Monter une vidéo de Nabil de bout en bout — du rush reçu au fichier livré. À déclencher dès qu'un rush, un clip ou plusieurs prises arrivent à monter, dérusher, couper, resserrer, sonoriser ou livrer ; y compris sur « monte-moi ça », « voilà le rush », « tu peux couper les blancs », « prends les meilleurs moments », « fais-moi un montage », « assemble ces clips ». Contient la procédure mesurée du dépôt, les points d'arrêt où Nabil tranche, et les garde-fous qui ont coûté deux montages ratés.
---

# Monter une vidéo de Nabil

Sept étapes. **Deux d'entre elles s'arrêtent et attendent Nabil** (étapes 2 et 6). Les autres
s'enchaînent toutes seules. Après chaque étape, une passe de relecture de son propre travail.

**La règle qui prime, rappelée ici parce que c'est ici qu'on la viole :** on ne juge rien à l'œil
ni à l'oreille sans un chiffre derrière. Pas de « les cuts sont parfaits » — un `ffprobe`, un
niveau mesuré, une transcription relue.

---

## Étape 0 — Ce que le rush est vraiment (avant de monter, pas après)

```bash
python3 outils/derusher.py <rush> -o derush/
```

La section 1 du rapport est la fiche captation. **La dire à Nabil tout de suite**, avant toute
proposition de montage : un montage ne sera jamais plus net que son rush, et c'est le seul moment
où il peut retourner filmer.

Ce qui se signale sans attendre : un rush sous 1080p, une capture Snapchat/Instagram/TikTok
repérée dans les métadonnées (l'original dans Photos est meilleur — le lui demander), une crête
au-dessus de −1 dBTP (reculer le téléphone au prochain tournage).

Si le fichier est trop lourd pour le chat : `bash outils/recuperer.sh "<lien>"`.

---

## Étape 1 — Transcrire TOUT, avant de décider quoi que ce soit

```bash
python3 outils/ecoute-video.py <rush> -o ecoute/ --profil profil-voix.json
```

**Plusieurs clips = transcrire les cinq, pas trois.** Le 15/09 sur « T'inquiète », les horodatages
des fichiers se chevauchaient et donnaient un ordre faux ; seule la transcription a révélé l'ordre
réel et les trois prises jumelles de la fin.

Le `RAPPORT-ECOUTE.md` sort déjà borné en secondes : zones molles, zones lentes, punchlines,
pauses, score de chute. **Ne jamais lire un dB sur un graphe** (biais mesuré ~+3 dB) ni chercher un
défaut sur l'image sans chiffre derrière.

Installation lourde (~1,6 Go) : voir `outils/README.md` §Installation. Si le temps manque, dire à
Nabil que ça tourne et donner la version rapide en attendant.

---

## Étape 2 — 🛑 LA CHAÎNE DE SENS — s'arrêter et la faire valider

**C'est le point d'arrêt le plus important du dépôt.** Écrire, en clair, avant de toucher aux
ciseaux :

> qui est le personnage → ce qu'il fait → ce que Nabil fait face à lui → l'escalade → la chute

Puis la montrer à Nabil et attendre sa réponse. **Chaque maillon manquant casse tout.**

Le 13/09 sur le Business Bro, le meilleur moment mesuré était l'imitation (+22,3 dB, chute 100/100).
Le montage a démarré dessus. Nabil : « on comprend pas le contexte, y'a plus de sens du tout à la
vanne ». Il avait raison : sans le pote qui fait le mec business, l'imitation tombe sur rien.

**Les mesures disent où ça retombe et où ça envoie. Elles ne disent pas ce qui se comprend.**

Profiter de cet arrêt pour demander aussi **le format** — solo ou tier list : voir
[`references/chartes.md`](references/chartes.md). Les deux n'ont pas les mêmes règles.

---

## Étape 3 — Le dérush mesuré

Relancer `derusher.py` avec la transcription, pour qu'il cherche aussi les redites :

```bash
python3 outils/derusher.py <rush> -o derush/ --transcription ecoute/<prefixe>_mots.json
```

Il sort `PROPOSITION-DERUSH.md` : segments à garder, niveau mesuré à chaque raccord, blancs longs
signalés, redites détectées. **C'est une proposition, pas un montage.** La confronter à la chaîne
de sens validée à l'étape 2, puis corriger à la main.

Les quatre garde-fous, tous payés par un montage raté :

1. **Couper DANS les maillons, jamais un maillon entier.** Sur le Business Bro, « s'immiscent »
   était dit trois fois : on garde la phrase qui nomme le sujet ET son domaine, on jette les redites.
2. **Ne couper que sur un silence mesuré** (≥ 0,10 s à l'enveloppe). Whisper finit les mots trop
   tôt, et une occlusive fabrique un silence *au milieu* d'un mot. Une redite sans silence autour
   ne se coupe pas.
3. **Un blanc long porte parfois une information.** `derusher.py` refuse de les couper et les
   remonte. Avant de resserrer, se demander ce que le blanc sépare — **surtout entre deux
   locuteurs, où la simultanéité se lit comme une intention** (tier list foot, 14/09 : 3,7 s
   ramenés à 0,22 s faisaient croire à un « mais qui est ce mec ? » dit en chœur exprès).
4. **Ne pas couper un mot au ras du raccord.** Finir dans le silence qui suit. Le rapport signale
   tout raccord dont le niveau mesuré est au-dessus du seuil : les corriger avant d'encoder.

Et : **la première image gardée doit être nette.** Sur TikTok, c'est la vignette.

---

## Étape 4 — Encoder, une seule fois

**Un seul fichier source** — coupe, étalonnage et retouche dans la même passe :

```bash
python3 outils/monter.py <rush> -o MONTAGE.mp4 --garder 6.40-27.70 32.45-37.55
```

**Plusieurs fichiers** — `monter.py` ne coupe que dans un fichier, il faut assembler :

```bash
python3 outils/assembler.py clip1.mov:2.1-9.4 clip3.mov:0.5-6.8 -o MONTAGE.mp4
```

Les morceaux sont donnés **dans l'ordre du montage**. L'outil refuse des sources de taille ou de
cadence différentes.

Jamais deux passes h264 : mesuré, trois passes tombent à SSIM 0,979 là où une seule à CRF 19 tient
0,988, pour un débit deux fois moindre. L'étalonnage se fait DANS la passe de coupe (`--image`), et
**jamais d'initiative** — une reprise d'expo non demandée se lit comme une perte.

Le décalage audio du conteneur et la plage de couleur de la source sont gérés par l'outil. Ne pas
les refaire à la main.

---

## Étape 5 — Vérifier le fichier, puis relire le montage

**Deux vérifications, aucune des deux ne se saute.** Commandes exactes :
[`references/verification.md`](references/verification.md).

1. **Le fichier est-il lisible ?** Un encodage interrompu produit un mp4 de la bonne taille, sans
   atome `moov`, illisible partout — et ffmpeg peut sortir en code 0. Deux tier lists ont été
   livrées comme ça le 14/09. Le défaut est intermittent : **relancer suffit**, mais ne jamais
   annoncer une livraison sans `ffprobe` sur le fichier final.
   Corollaire : **ne jamais filtrer la sortie d'un outil avec un `grep` qui ne garde que la ligne
   de succès.** C'est comme ça que l'erreur est passée.

2. **La transcription du montage se tient-elle toute seule ?** La relire à la lecture. Si elle ne
   tient pas debout, le montage est faux, quels que soient les chiffres.

---

## Étape 6 — 🛑 Sonoriser, seulement si Nabil le demande

```bash
python3 outils/sonoriser.py MONTAGE.mp4 -o MONTAGE-sonorise.mp4 \
    --son 28.40:banque-son/doumbe-jordan-tes-mort.wav:-3
```

**Deux sons par vidéo au maximum.** Les sons viennent de `banque-son/` (carte blanche pour y
puiser, le catalogue est dans son `README.md`). Les bruitages synthétiques de `outils/sfx/` ne
servent **que sur demande explicite** : un whoosh ne fait rire personne, un « JORDAN » de Doumbé si.

Le son s'efface sous la voix, jamais l'inverse. **La voix n'est jamais touchée** — le vérifier par
RMS sur blocs de 0,5 s, sonorisé contre nu : 0,0 dB partout hors du son.

Poser le son **dans un trou mesuré**, pas sur un timecode Whisper. Un son posé sur de la parole
sans ducking est masqué : mesuré, un riser sous une phrase ressortait à −0,4 dB, c'est-à-dire rien.

---

## Étape 7 — Livrer

Les montages destinés à sortir vont dans [`livraisons/`](../../../livraisons/), au débit de la
source, et se téléchargent depuis GitHub — le chat plafonne à 30 Mio et coûte 7 % de détail.

Un montage fait pour Nabil seul (essai, version perso) **ne va pas** dans `livraisons/` : ce
dossier est celui des vidéos destinées à publier.

Juger la qualité au **détail conservé** (écart-type du passe-haut, rapporté à la source), pas au
PSNR : le H.265 a déjà eu un meilleur PSNR tout en conservant moins de détail (91,3 % contre
92,8 %). Remplir le tableau de `livraisons/README.md`.

---

## Ce qu'on ne fait pas

- **Ne jamais réécrire un script déjà marqué validé** sans que Nabil le demande.
- **Ne pas couper tous les blancs par réflexe.** C'est la règle des monteurs de vidéos explicatives ;
  sur un sketch elle détruit le timing. Le blanc est un outil comique.
- **Ne pas annoncer un succès sans mesure.** Ni « les cuts sont parfaits », ni « la qualité est
  bonne », ni « c'est livré » — sans le chiffre qui le montre.
- **Ne pas encoder avant que la chaîne de sens soit validée par Nabil.**

## Quand une mesure contredit ce qu'on a affirmé plus tôt

On se corrige explicitement, dans la réponse **et** dans le dépôt. C'est la moitié de la valeur de
ce dossier : les six contre-exemples du tableau de `CLAUDE.md` viennent tous d'une affirmation
faite sans mesure.

## Finir la session

Deux gestes, jamais l'un sans l'autre : réécrire `ETAT.md` pour qu'il colle à la réalité, et
ajouter une entrée en haut de `JOURNAL.md`. Le conteneur est effacé entre deux sessions — seul ce
qui est commité reste.
