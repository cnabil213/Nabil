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
La coupe est faite par `trim`/`concat`, donc à la frame près — pas de seek sur keyframe qui décalerait
de une à deux secondes. Le son est ensuite ramené à **−14 LUFS / −1,5 dBTP** en deux passes (mesure puis
correction linéaire) : sans ça la plateforme remonte le niveau elle-même, et le souffle avec. La rotation
du téléphone est appliquée automatiquement (un rush portrait reste portrait). `--sans-normalisation`
pour ne pas toucher au son, `--crf` pour la qualité (défaut 16, `--preset` slow), `--image` pour étalonner sans passe supplémentaire.

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

## `sonoriser.py` — poser des sons

```bash
python3 outils/sonoriser.py MONTAGE.mp4 -o SONORISE.mp4 \
    --son 4.02:outils/sfx/impact.wav:+2 \
    --son 28.28:samples/jordan-t-es-mort.wav:-1
```

Un `--son` par effet : `temps:fichier:écart_dB`. **L'écart est relatif à la voix**, pas un gain brut :
`0` = même niveau perçu, `+2` = deux dB au-dessus, `-3` = en dessous. L'outil mesure le RMS de la voix
et celui du son, puis calcule le gain. C'est indispensable — les sons de percussion sont calés en crête
mais leur RMS est 8 à 18 dB plus bas ; réglés en crête, ils sont inaudibles sous la parole.

La voix est automatiquement baissée sous chaque son (sidechain, ~4 dB, retour en 320 ms), la vidéo
n'est pas réencodée, et le mix est remis à **−14 LUFS / −1,5 dBTP** en fin de chaîne — poser des effets
fait monter le niveau, sans cette passe le fichier repasse au-dessus de 0 dBFS.

**Où poser un son.** Dans un trou : la section 7 du `RAPPORT-ECOUTE.md` liste les pauses, et
`ecoute-video` donne les timecodes des punchlines. Un son posé sur de la parole est masqué —
mesuré sur le rush du 12/09 : le riser placé sous une phrase ressortait à **−0,4 dB**, c'est-à-dire
rien. Vérifier après coup en mesurant l'effet **dans sa propre bande** (35–110 Hz pour un impact,
2,5–7 kHz pour un souffle) : la crête large bande ne dit rien, elle est déjà occupée par la voix.

**Les samples de référence** (punchline d'un rappeur, d'un combattant, son de tendance) ne sont pas
dans le kit et ne peuvent pas l'être : ils appartiennent à quelqu'un. Déposer le fichier dans
`samples/` et le passer à l'outil comme n'importe quel autre son.

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
