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
