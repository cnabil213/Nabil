# Outils

Trois outils, un principe : **Claude ne perçoit que texte et images, donc tout ce qui compte dans un rush
est converti en chiffres, en phrases et en planches qu'il lit.** La détection vient des mesures ; les images
servent à décrire, jamais à deviner. Le pourquoi de chaque choix est dans
[`RECHERCHE-ECOUTE.md`](RECHERCHE-ECOUTE.md).

| Outil | Rôle | Doc |
| :--- | :--- | :--- |
| [`ecoute-video.py`](ecoute-video.py) | **L'oreille.** Transcription juste (whisper turbo), fiche captation (saturation, loudness, bruit), carte d'identité vocale (Praat), ligne de temps par phrase avec verdict ENVOYÉE / PLATE, alertes horodatées (tu retombes, monotone, trop lent), score de chute, mots appuyés, énergie d'articulation | [`README-ecoute.md`](README-ecoute.md) |
| [`ecoute/comparer-prises.py`](ecoute/comparer-prises.py) | **Deux prises de la même vanne** → laquelle est la plus forte, la plus vivante, la plus rapide, la pause avant la chute la plus nette — verdict + pourquoi | ci-dessous |
| [`vision-video.py`](vision-video.py) | **Les yeux.** Planches contact horodatées (4 images/s sur le hook, 2 ensuite), forme d'onde, fiche captation | ci-dessous |
| [`monter.py`](monter.py) | **Le montage.** Coupe le rush sur les segments à garder (à la frame près) et normalise le son pour les plateformes | ci-dessous |
| [`sonoriser.py`](sonoriser.py) | **Le son.** Pose des samples et des effets à des timecodes précis, avec ducking automatique de la voix | ci-dessous |
| [`banque-son.py`](banque-son.py) | **La banque de sons de Nabil.** Nettoie un clip reçu (découpe, silences retirés, niveau calé) et le catalogue dans `banque-son/` pour tous les montages suivants | ci-dessous |
| [`sfx/`](sfx/) | Kit de six sons de ponctuation synthétisés (libres de droits) | [`sfx/README.md`](sfx/README.md) |
| [`recuperer.sh`](recuperer.sh) | **Faire entrer un rush trop lourd pour le chat** à partir d'un lien de partage (Drive, Dropbox, WeTransfer, lien direct) | ci-dessous |

## Installation (à refaire à chaque nouvelle session : le container est neuf)

```bash
apt-get update && apt-get install -y --no-install-recommends ffmpeg
pip3 install --break-system-packages numpy scipy soundfile librosa praat-parselmouth matplotlib faster-whisper==1.2.1
# venv séparé pour l'énergie d'articulation (torch CPU) — optionnel : --sans-arousal pour s'en passer
python3 -m venv ~/venv-ecoute-arousal
~/venv-ecoute-arousal/bin/pip install --index-url https://download.pytorch.org/whl/cpu torch torchaudio
~/venv-ecoute-arousal/bin/pip install transformers soundfile librosa psutil numpy
```

Les modèles (whisper turbo ~1,6 Go, audeering ~0,6 Go) se téléchargent seuls au premier lancement.
Détail, pièges (PEP 668) et emplacement du venv : [`README-ecoute.md`](README-ecoute.md) §Installation.

## `monter.py` — couper et normaliser

```bash
python3 outils/monter.py rush.mov -o MONTAGE.mp4 --garder 6.40-27.70 32.45-37.55 40.20-66.60
```

On donne les segments à **garder** (en secondes, timecodes du `RAPPORT-ECOUTE.md`) ; tout le reste saute.

**Une vanne tournée en plusieurs fichiers** (Nabil s'arrête, reprend, envoie trois `.mov`) : donner
les fichiers à la suite et préfixer chaque segment de l'index de sa source, dans l'ordre du montage :

```bash
python3 outils/monter.py IMG_7370.mov IMG_7374.mov IMG_7375.mov -o MONTAGE.mp4 \
    --garder 0:0.033-6.71 0:7.88-9.47 1:0.00-3.77 1:4.09-6.36 2:0.00-5.55
```

Chaque source est décodée une fois par son propre démultiplexeur (`select` par source, puis `concat`
des sources), donc avec sa propre liste d'édition AAC : la synchro son/image de chaque rush est
conservée (mesurée à 0,0 ms sur les deux raccords du 15/09). **Ne pas recoller les fichiers avec le
concat demuxer en copie de flux** : il ignore l'amorce AAC et décale le son de 59 ms sur le deuxième
fichier, 80 ms sur le troisième (mesuré par corrélation, 15/09). Les segments d'une même source doivent
se suivre.
La coupe est faite par `trim`/`concat`, donc à la frame près — pas de seek sur keyframe qui décalerait
de une à deux secondes. Le son est ramené à **−14 LUFS** par un **gain fixe** mesuré sur la coupe audio
(quelques secondes), puis un **limiteur** retient les crêtes à −1,5 dBFS — le tout dans la passe de coupe,
un seul encodage AAC. La rotation du téléphone est appliquée automatiquement (un rush portrait reste
portrait). `--sans-normalisation` pour ne pas toucher au son, `--cible -16` pour retenir moins de crêtes,
`--crf` pour la qualité (défaut 16, `--preset` slow), `--image` pour étalonner sans passe supplémentaire,
**`--garder-image MONTAGE.mp4`** pour reprendre l'image déjà encodée d'un montage aux mêmes coupes et ne
refaire que le son (zéro perte d'image, une dizaine de secondes ; l'outil vérifie que les durées collent).

> **Le niveau : gain fixe + limiteur, pas `loudnorm`.** Un rush iPhone sort à −16…−17 LUFS avec des
> crêtes à −0,1 dBTP (l'AGC du téléphone pousse à fond) : impossible d'atteindre −14 LUFS sans retenir
> des crêtes. `loudnorm` en deux passes, censé être linéaire, repasse alors en mode **dynamique** sans le
> dire et fait bouger le gain au fil des phrases (mesuré V6 contre rush, blocs de 0,5 s : de −0,5 à
> +1,6 dB), en rééchantillonnant à 96 kHz au passage. Maintenant : `volume=+G dB` puis
> `alimiter=limit=0.84:level=0:latency=1`. Sur le rush du 12/09 : +1,9 dB, le limiteur touche 9,9 % des
> tranches de 10 ms, au plus 3,3 dB — les syllabes les plus fortes ressortent ~1,5 dB moins fort qu'au
> rush, le reste est intact ; résultat −15,1 LUFS / −1,3 dBTP, synchro son/image à 0,3 ms. Le vrai
> remède est à la prise : si la fiche captation annonce une crête au-dessus de −1 dBTP, reculer le
> téléphone ou baisser le gain (app caméra à gain manuel) ; à −6 dBTP il n'y aurait plus rien à retenir.

> **La plage de couleur de la source, jamais convertie.** Un rush d'iPhone est en plage *complète*
> (`yuvj420p`, `color_range=pc` : noirs à 0, blancs à 255). Forcer `-pix_fmt yuv420p` le convertit en
> plage *limitée* (16–235) et, sans étiquettes couleur (`color_space=unknown`), le lecteur affiche un
> contraste écrasé. Mesuré sur le rush du 12/09 : noirs à **3** dans la source, à **19** dans le fichier
> livré — alors que le SSIM de compression était bon. C'était ça, « la vidéo perd en qualité ». L'outil
> lit maintenant la plage de la source, la conserve, étiquette BT.709 explicitement, et avertit si la
> sortie ne la respecte pas. Vérification : les percentiles de luminance (0,5 / 50 / 99,5 %) doivent être
> identiques entre la source et le montage.
>
> **Pas d'étalonnage qu'on n'a pas demandé.** Une reprise d'expo (`--image`) change l'image par
> définition : à côté de l'original, elle se lit comme une perte, et sur une vidéo sombre elle remonte
> le grain des ombres. Ne l'appliquer que sur demande, jamais d'initiative.
>
> **`--hevc`** : H.265 tient la même qualité avec ~40 % de débit en moins (CRF 15 H.265 ≈ 29,7 Mo là où
> CRF 18 H.264 fait 30,9). iPhone et TikTok le lisent ; la prévisualisation dans un navigateur, pas
> toujours. Pour un fichier que Nabil regarde dans le chat, H.264 reste le choix sûr.

> **Un seul réencodage, jamais deux.** Chaque passe h264 coûte de la qualité, et ça s'empile. Mesuré
> sur le rush du 12/09, contre un étalon sans perte construit au même `trim` : la chaîne
> coupe → étalonnage → copie d'envoi (trois passes, dont une à CRF 24) ressort à **SSIM 0,979 /
> 39,2 dB**, contre **0,988 / 40,1 dB** pour la même vidéo faite en **une seule passe à CRF 19** —
> et le débit passe de 2,95 à 5,81 Mb/s. D'où l'option `--image` : l'étalonnage se fait DANS la passe
> de coupe. Pris isolément, même CRF 24 est invisible (SSIM 0,9855) : le coupable n'est pas le CRF,
> c'est le nombre de passes. `sonoriser.py` copie le flux vidéo, il ne compte pas comme une passe.
>
> Pour mesurer une perte, construire l'étalon avec le **même `trim`** que le montage : un étalon fait
> au `-ss` cale sur une image-clé, le décalage d'une ou deux images fait chuter le SSIM à 0,88 pour
> tout le monde et la mesure ne veut plus rien dire.

> **Le décalage audio, à ne pas réintroduire.** Sur un rush de téléphone la piste audio ne démarre pas à
> zéro (iPhone : **0,283 s** sur le rush du 12/09). Les timecodes du rapport viennent du wav extrait,
> dont l'instant 0 est le premier échantillon audio, alors que `trim`/`atrim` travaillent sur les PTS du
> conteneur. Sans recalage les coupes tombent ~0,3 s trop tôt, en pleine queue de mot — mesuré :
> −16 dBFS au raccord au lieu du silence. L'outil lit `start_time` et décale **vidéo et audio de la même
> valeur**, donc la synchro lèvres/son est préservée.

**Poser une coupe.** La prendre dans un silence réel, pas sur une borne de mot : Whisper termine les mots
trop tôt (« cardi-bés » finit à 27,48 s alors que Whisper annonce 27,10). Les pauses de la section 7 du
rapport, ou une mesure d'enveloppe à −40 dBFS, donnent les bonnes bornes. Vérifier après coup que le
niveau juste avant et juste après le raccord est bien celui d'un silence.

## `banque-son.py` — la banque de sons

```bash
python3 outils/banque-son.py ajouter clip.mp4 --nom doumbe-jordan-tes-mort \
    --desc "Doumbè à Zébo : « Jordan, t'es mort »" --usage "après une menace, une punchline de combat" \
    --tags mma,menace --debut 12.3 --fin 14.1
python3 outils/banque-son.py lister
python3 outils/banque-son.py retirer doumbe-jordan-tes-mort
```

Prend n'importe quel fichier, audio ou vidéo. Extrait le passage (`--debut/--fin`), **retire le silence
en tête et en queue** (sinon le son tombe en retard sur son timecode — il garde 30 ms avant l'attaque pour
ne pas couper un plosif), cale la crête à −3 dBFS, enregistre en WAV 48 kHz dans `banque-son/`, et
régénère le catalogue (`catalogue.json` + tableau du `banque-son/README.md`) — c'est ce tableau que
Claude lit pour choisir un son à chaque montage.

La banque vit **dans le dépôt** : le container est effacé à chaque session, tout ce qui n'est pas commité
disparaît. Clips courts uniquement (quelques secondes), c'est git, pas un disque dur.

### Le soundboard 3kh0 (source externe)

[`3kh0/soundboard`](https://github.com/3kh0/soundboard) : 208 sons de mèmes (anglophones), mp3 128 kb/s,
médiane 2,6 s, catalogue `sounds.json`. GitHub est joignable depuis le container (MyInstants ne l'est pas :
Cloudflare renvoie 403 sur tout, mp3 compris). On ne le copie pas en entier dans le dépôt (49 Mo) : on
le clone à la demande et on importe son par son dans la banque, nettoyé et catalogué.

```bash
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/3kh0/soundboard ~/3kh0/soundboard
python3 outils/banque-son.py importer "boxing bell" --desc "cloche de boxe" --usage "avant un combat, une confrontation"
```

Le code du soundboard est sous Apache 2.0 ; les sons eux-mêmes sont des mèmes, au même titre que tout
son de tendance — leur usage relève de Nabil.

## `sonoriser.py` — poser des sons

```bash
python3 outils/sonoriser.py MASTER.mp4 -o MONTAGE-sonorise.mp4 \
    --son 28.40:banque-son/doumbe-jordan-tes-mort.wav:-3 [--fond 10] [--piste-effets fx.wav]
```

Un `--son` par effet : `temps:fichier:écart_dB`. **L'écart est relatif à la voix parlée** (RMS des
passages où Nabil parle, pas la moyenne du fichier silences compris) : `0` = même niveau, `-3` = en
dessous. L'outil mesure la voix et le son puis calcule le gain — indispensable, les percussions sont
calées en crête mais leur RMS est 8 à 18 dB plus bas ; réglées en crête, elles sont inaudibles.

**Le son s'efface sous la voix** (on baisse le son, jamais la voix). L'outil détecte où Nabil parle
(blocs de 10 ms, seuil local), descend le son de `--fond` dB (10) **40 ms avant** chaque reprise de
parole, et ne le laisse remonter que dans les pauses ≥ 0,25 s — entre deux mots il reste en fond, donc
pas de pompage. L'enveloppe est calculée hors ligne (numpy) et appliquée par `amultiply` : déterministe,
mesurable. Il affiche pour chaque son les plages « trou : son plein / tu parles : son en fond ».
Mesuré sur le Doumbè du 12/09 (2,98 s posé à 28,40 s, écart −3, piste seule via `--piste-effets`) :
« Jordan » à −15…−18 dBFS dans le trou de 0,5 s (+14 à +21 dB au-dessus du plancher), « t'es mort »
et la foule entre −12 et −20 dB sous « 2-3 combats », la foule qui remonte dans la pause de 0,4 s à
30,1 s puis redescend. `--sans-duck` = son fixe (nappe volontaire).

**La voix n'est jamais modifiée.** Pas de sidechain sur la voix, pas de renormalisation, disposition
(mono) et taux d'échantillonnage de la source conservés, un seul encodage AAC, vidéo copiée. Seul filet :
un limiteur à −1,5 dBFS (`alimiter=limit=0.84:level=0:latency=1`) sur le mix. Vérification avant
d'envoyer : RMS par blocs de 0,5 s, sonorisé contre nu = **0,0 dB partout hors du son** (V8 : ✅),
et somme de contrôle du flux vidéo identique. Dépendances : numpy + soundfile (déjà requis par ecoute).

> **Trois pièges mesurés, à ne pas réintroduire.** (1) `alimiter` a un **gain automatique activé par
> défaut** (`level=1`) : il multiplie la sortie par 1/limit — à `limit=0.7` la voix prenait +3 dB avant
> d'être recompressée, à 0.94 encore +0,5 dB. Toujours `level=0` (et `latency=1`, sinon 5 ms de retard).
> (2) `aformat=channel_layouts=stereo` sur une voix mono fabrique un double-mono que le mesureur R128
> compte **+3 LU** plus fort : la renormalisation qui suivait baissait alors **toute** la vidéo de 2,1 dB
> (mesuré V6 → essai, blocs de 0,5 s, constant du début à la fin). Garder la disposition de la source.
> (3) `loudnorm` « linéaire » en deux passes repasse en mode dynamique sans prévenir dès que la crête
> dépasse la cible. Plus de `loudnorm` dans cet outil : une sonorisation ajoute ~0 LU au montage.

**Où poser un son.** Dans un trou : la section 7 du `RAPPORT-ECOUTE.md` liste les pauses, et
`ecoute-video` donne les timecodes des punchlines — puis vérifier la borne réelle à l'enveloppe (blocs
de 25–50 ms) : Whisper finit les mots trop tôt. Un son posé sur de la parole sans ducking est masqué —
mesuré sur le rush du 12/09 : un riser sous une phrase ressortait à **−0,4 dB**, c'est-à-dire rien.
Mesurer un effet **dans sa propre bande** (35–110 Hz pour un impact, 2,5–7 kHz pour un souffle) : la
crête large bande ne dit rien, elle est déjà occupée par la voix.

**Les samples de référence** (punchline d'un combattant, son de tendance) passent par la banque :
`banque-son.py ajouter` les découpe, cale et catalogue ; ils appartiennent à leurs auteurs, l'usage
relève de Nabil.

## `retoucher.py` — effacer un defaut de peau sur toute la video

```bash
curl -sSL -o outils/face_landmarker.task https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
pip3 install opencv-python-headless mediapipe          # + apt : libegl1 libgles2 libgl1 libglx0 libglvnd0
python3 outils/retoucher.py rush.mov -o SORTIE.mp4 --garder 6.40-12.20 40.20-50.10 \
    --repere 346:299:840 --rayon 11 --audio MONTAGE.mp4 --suivi suivi.json [--hevc --crf 16]
```

Le point se donne **une seule fois** : `--repere IMAGE:X:Y`, les coordonnées du défaut sur une image du
montage. Le visage est détecté à chaque image (MediaPipe FaceLandmarker, 478 points) et le défaut est
replacé dans le repère de trois points du maillage : il suit la tête qui tourne, s'approche, s'éloigne.
Sur le rush du 12/09 : suivi sur 1266 des 1288 images, 29 trous de flou de bougé comblés par
interpolation, 22 images sans visage laissées telles quelles (1/30 s chacune, invisible).

La correction est un *spot heal* : le disque est reconstruit depuis la peau autour (inpainting Telea),
le grain d'origine est remis par-dessus (`--grain`), et le masque **exclut les pixels nettement plus
sombres** que la peau alentour — sans ça la retouche baverait sur la monture, la narine ou l'ombre.

**Trouver les coordonnées** quand Nabil envoie une capture d'écran annotée : le rouge du feutre est
isolable en HSV (teinte < 6 ou > 174, saturation ≥ 180) ; la capture est un plein écran, donc
`x_video = (x_capture + bord) / échelle` avec `échelle = hauteur_capture / hauteur_video` et
`bord = (largeur_video × échelle − largeur_capture) / 2`. Retrouver l'image exacte par corrélation
sur toutes les images du montage, puis vérifier le point en zoomant dessus (`--apercu`).

> **Jamais de détour par RGB.** Première version en `bgr24` : **39,0 dB** de PSNR contre la source, au
> lieu de 44,4 — l'aller-retour YUV 4:2:0 → RGB → YUV rééchantillonne la couleur deux fois. L'outil
> travaille maintenant dans le format de la source (`yuvj420p`), plan par plan : luminance en pleine
> résolution, couleur en demi-résolution, **et seuls les octets sous la retouche sont modifiés**. Tout
> le reste de l'image repart vers l'encodeur exactement tel qu'il a été décodé : 44,4 dB, soit la
> qualité d'un montage sans retouche.
>
> **Cadence fixe en sortie de `concat`.** Sans `fps=`, le flux brut sort en cadence variable et perd
> une image par rapport au montage encodé (qui, lui, en duplique une au raccord d'un segment tombant
> sur une demi-image). 1288 contre 1289 : sans conséquence sur la synchro (33 ms), mais les deux
> fichiers ne sont plus comparables image par image.

`--suivi fichier.json` garde le résultat du suivi : le refaire coûte 2 minutes, le relire coûte 0.
Indispensable pour essayer plusieurs encodages du même montage.

## Qualité de livraison : le plafond de 30 Mio

Le chat refuse tout fichier au-dessus de **30 Mio**. C'est ça, et rien d'autre, qui limitait la qualité.
Mesures sur le montage du 12/09 (43 s, 720×1280, PSNR contre le rush aux mêmes coupes) :

| fichier | poids | débit | PSNR |
| :-- | --: | --: | --: |
| rush d'origine (iPhone) | 98,6 Mo | 10,52 Mb/s | — |
| H.264 CRF 19 (ce qui était livré) | 27,4 Mo | 5,11 Mb/s | 44,40 dB |
| **H.265 CRF 16** (livré depuis) | **28,7 Mo** | 5,36 Mb/s | **45,42 dB** |
| H.265 CRF 14 | 37,3 Mo | 6,94 Mb/s | 46,43 dB |
| H.264 CRF 13 (débit de l'original) | 53,7 Mo | 10,00 Mb/s | 47,72 dB |

À poids égal, **H.265 gagne ~1 dB sur H.264** : c'est le seul levier gratuit sous le plafond. Au-delà,
il faut sortir du chat (le fichier à 53,7 Mo a été refusé à l'envoi). Le connecteur Google Drive ne
convient pas : il veut le contenu en base64 dans l'appel, impossible pour 50 Mo.
Sur une vidéo sombre et granuleuse comme un rush de voiture la nuit, c'est le grain des zones sombres
qui part en premier — d'où l'impression de « moins net » avant même de regarder les chiffres.

## `recuperer.sh` — un rush trop lourd pour le chat

L'upload du chat plafonne à quelques dizaines de Mo ; un export TikTok d'une minute peut les dépasser.
Le container, lui, télécharge sans limite pratique. Donc : déposer le fichier quelque part, m'envoyer le lien.

```bash
bash outils/recuperer.sh "<lien de partage>" [nom.mp4]
```

Le fichier atterrit dans `/mnt/user-data/working/` (ou `$RUSH_DIR`). Gère les liens **Google Drive**
(l'ID est extrait et le téléchargement passe par `drive.usercontent.google.com` avec `confirm=t`, ce qui
évite l'écran antivirus qui renvoie du HTML sur les gros fichiers), **Dropbox** (`?dl=1`), **WeTransfer**
et tout lien direct ; repli sur `yt-dlp` si `curl` échoue. Vérifie ensuite que c'est bien un média
(`ffprobe`) et **refuse explicitement une page HTML** — le cas d'un lien non public, qui renvoie une page
de connexion au lieu de la vidéo.

> **Envoyer l'original, pas une version compressée.** Ré-encoder change la crête, le true peak et le
> loudness : la fiche captation (« ça sature », « 4 LU sous la cible ») porterait alors sur la
> compression, pas sur le tournage.

## `ecoute-video.py` — relire un rush

```bash
python3 outils/ecoute-video.py /mnt/user-data/working/rush.mp4 -o ecoute-rush/ --profil profil-voix.json
```

Sort `RAPPORT-ECOUTE.md` (à lire en premier), les partitions PNG par fenêtre de 15 s, `arousal.png`, `mesures.json`.
Le `--profil` accumule les percentiles personnels de Nabil (hauteur, variation, pics, débit) : sous 3 rushs le rapport
dit « NON CALIBRÉ » ; ensuite chaque mesure est comparée à *sa* voix habituelle, pas à des seuils génériques.
Vocabulaire du rapport, seuils et limites : [`README-ecoute.md`](README-ecoute.md).

**Comment Claude s'en sert** : lire le rapport → les alertes et verdicts sont déjà bornés en secondes → ouvrir la
partition de la fenêtre concernée pour *décrire* ce qui s'y passe → relier au script. Ne jamais lire une valeur de
dB « sur le graphe » (biais ~+3 dB mesuré), ne jamais chercher un défaut sur l'image sans chiffre derrière.

## `ecoute/comparer-prises.py` — deux prises

```bash
python3 outils/ecoute/comparer-prises.py prise-A.wav prise-B.mp4
```

Transcrit les deux (turbo), aligne les mots, applique **le même découpage** aux deux prises, puis compare :
volume des pics, débit, étendue de hauteur, pause avant la chute, durée, score de chute. Verdict avec confiance
et la raison en clair (*« A est plus haute/vivante »*). Testé sur trois manipulations contrôlées : 3/3.

## `vision-video.py` — voir le rush

```bash
python3 outils/vision-video.py /mnt/user-data/working/rush.mp4
```

Planches contact 1080×1500 (sous le seuil de redimensionnement, donc les visages restent lisibles), timecode incrusté
sur chaque vignette, 4 images/s sur les 4 premières secondes, 2 ensuite ; forme d'onde ; fiche captation.

> **Bug corrigé le 12/09** : la première version annonçait « pas de saturation » sur un fichier à 0 dBFS de crête —
> le pic était calculé sur des moyennes RMS par bloc. La crête est désormais mesurée sur les échantillons et le
> true peak par `ebur128`.

### Deux pièges des planches, à ne pas réintroduire

1. **Le timecode.** `-ss` remet le PTS à zéro : `%{pts}` affichait `6.0s` sur une image réellement à `10.0s`.
   Le décalage est reconstruit explicitement (`eif`), car `%{pts:flt:offset}` ignore la précision demandée.
2. **La taille des planches.** Au-delà de ~1568 px l'image est redimensionnée à la lecture : grille 4×3 en cellules
   264×470, calibrée pour rester dessous.
