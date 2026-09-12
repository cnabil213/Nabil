# ecoute-video — Claude « écoute » tes rushs par les chiffres

Claude ne perçoit que du texte et des images. Cet outil transforme la **manière** de parler d'une vidéo
(énergie, volume, intonation, débit, pauses, timing des chutes) en un rapport lisible + des partitions PNG.
Tout ce que dit le rapport vient de **mesures** (ffmpeg, Praat, faster-whisper, audeering) : Claude ne
« devine » rien sur l'image, il commente des zones déjà bornées par les chiffres.

## Installation sur une machine neuve (Linux, CPU seul, ~4 Go de RAM libre, ~6 Go de disque)

```bash
# 1. système
sudo apt install -y ffmpeg python3 python3-pip python3-venv          # ffmpeg >= 6 (astats, ebur128, silencedetect)

# 2. python principal : mesure + transcription
pip3 install numpy scipy soundfile librosa praat-parselmouth matplotlib faster-whisper==1.2.1
#    Debian 12 / Ubuntu >= 23.04 refusent ce pip3 (PEP 668 « externally-managed-environment »). Deux issues :
#      pip3 install --user ...                              (python système, puis `python3 ecoute-video.py ...`)
#    ou python3 -m venv ~/venv-ecoute && ~/venv-ecoute/bin/pip install ...   puis TOUJOURS lancer avec ce python :
#       ~/venv-ecoute/bin/python ecoute-video.py rush.mp4   (les sous-étapes whisper/Praat/rapport tournent avec le même python
#       que celui qui lance ecoute-video.py — sys.executable — donc jamais avec un python système sans faster-whisper)

# 3. venv séparé pour l'arousal (torch CPU isolé, ~1,4 Go RAM à l'exécution)
python3 -m venv ~/venv-ecoute-arousal
~/venv-ecoute-arousal/bin/pip install --index-url https://download.pytorch.org/whl/cpu torch torchaudio
~/venv-ecoute-arousal/bin/pip install transformers soundfile librosa psutil numpy

# 4. modèles (téléchargés une fois dans ~/.cache/huggingface/hub, au premier lancement ou à la main)
python3 -c "from faster_whisper import WhisperModel; WhisperModel('deepdml/faster-whisper-large-v3-turbo-ct2', device='cpu', compute_type='int8')"   # ~1,6 Go
~/venv-ecoute-arousal/bin/python -c "from transformers import Wav2Vec2Processor, Wav2Vec2Model; n='audeering/wav2vec2-large-robust-12-ft-emotion-msp-dim'; Wav2Vec2Processor.from_pretrained(n); Wav2Vec2Model.from_pretrained(n)"   # ~0,63 Go

# 5. où l'outil cherche le python du venv arousal, dans l'ordre :
#    (a) $ECOUTE_VENV_PY  (b) <dossier de ecoute-video.py>/venv-arousal/bin/python  (c) ~/venv-ecoute-arousal/bin/python
#    Avec l'étape 3 ci-dessus, (c) suffit : rien à exporter. Sinon :
export ECOUTE_VENV_PY=/chemin/vers/venv/bin/python
#    Si aucun n'existe (ou si le modèle audeering ne se charge pas : cache HF absent, hors ligne), l'étape est SAUTÉE
#    proprement et RAPPORT-ECOUTE.md l'écrit en gras (« Énergie d'articulation : non calculée — raison »). Le reste du rapport est produit.
```

Fichiers : `ecoute-video.py` (point d'entrée) + paquet `ecoute/` (captation.py, transcribe.py, prosodie.py, seuil.py, rapport.py,
arousal_windows.py, chute.py, fusion.py, _run.py). Copier le dossier entier. Tests : `bash tests/lance_tests.sh` (chemins relatifs au script).

## Usage

```bash
python3 ecoute-video.py rush.mp4                       # sortie dans ./ecoute-rush/
python3 ecoute-video.py rush.mp4 -o sortie/ --profil nabil.json   # profil créateur mis à jour à chaque rush
python3 ecoute-video.py prise.wav --sans-arousal       # sans le venv torch (plus rapide, pas d'arousal)
```

Entrées acceptées : mp4/mov/mkv/wav/m4a… (tout ce que ffmpeg lit) ; stéréo / 48 kHz converti en mono 16 kHz ;
vidéo sans piste audio → « cette vidéo n'a PAS de piste audio » ; fichier introuvable → erreur nette (code 2).
Toute durée ≥ 1 s : ≤ 15 s = une seule partition, > 15 s = une partition par fenêtre de 15 s (p1, p2…) — les shorts de 16–20 s
sont testés (tests/clip18s.wav).

Budget : ~90 s et 2,1 Go de RAM par minute de vidéo sur 4 cœurs sans GPU **partagés avec d'autres processus**
(whisper turbo = 60 % du temps). Étapes séquentielles, jamais en parallèle (pour rester sous 4 Go).

## Ce que produit un lancement (`-o sortie/`)

| fichier | contenu |
| :-- | :-- |
| `RAPPORT-ECOUTE.md` | LE rapport à donner à Claude : fiche captation, carte d'identité vocale, ligne de temps par phrase, alertes horodatées (les 10 plus graves ; le reste dans `mesures.json` → `alertes_toutes`), top phrases envoyées / plates / chutes, mots appuyés / suspects, pauses avant chutes, fenêtres de 15 s |
| `<base>_partition_p1.png`, `_p2.png`… | partition F0 + intensité + mots, une image par fenêtre de 15 s (1500 × 750 px) ; `<base>_partition.png` = clip entier |
| `arousal.png` | énergie d'articulation (audeering) par fenêtre de 2 s, creux / pics colorés, silences masqués |
| `mesures.json` | tout en chiffres (phrases, alertes, arousal, mots, captation, temps) |
| `RAPPORT-PROSODIE.txt` | rapport Praat détaillé (rapport.py) ; `<base>_mesures.json` = sortie brute de prosodie.py |
| `captation.md/json`, `<base>_mots.json`, `<base>_audeering.json`, `<base>_mel.png`, `temps.json`, `journal.log` | intermédiaires |

## Lire le rapport (vocabulaire)

- **Échelle de volume unique** : dBFS RMS, 0 dBFS = pleine échelle (Praat dB − 93,98) ; true peak en dBTP ; loudness en LUFS.
  Ne jamais lire un dB « sur le graphe » : la lecture visuelle est biaisée d'environ +3 dB (vérif en aveugle).
- **ENVOYÉE** : phrase dont les pics (p90) sont ≥ +2 dB au-dessus de la précédente, ou pic de F0 ≥ +3 demi-tons.
  **PLATE** : ≤ −3 dB et pas de montée de F0. **normale** sinon. **ouverture** = première phrase.
- **ZONE MOLLE (tu retombes)** : pics sur 1 s ≥ 5 dB sous les pics de la vidéo pendant ≥ 1,5 s (≥ 2 syllabes).
- **ZONE LENTE** : débit d'articulation (syllabes / temps de parole, silences exclus) < 65 % de ton débit d'articulation global
  sur une fenêtre de 1,5 s, pendant ≥ 2,5 s (zones distantes de < 1 s fusionnées). Une fin de phrase seule ne suffit plus.
- **NIVEAU QUI CHANGE** : pics (p90) d'une fenêtre de 15 s ≥ 6 dB sous ceux d'une autre → micro qui s'éloigne, aparté, prise raccordée.
- **Parole / silence** : seuil LOCAL (p99 sur 10 s glissantes − 25 dB, jamais sous le plancher + 6 dB, jamais au-dessus du seuil global) ;
  un passage 10 dB plus bas que les pics reste de la parole. Même seuil dans le découpage en phrases (`ecoute/seuil.py`).
  Les pauses à cheval sur une borne de fenêtre comptent pour leur part dans chaque fenêtre.
- **MONOTONE** : écart-type F0 < 0,8 st sur 2 s ; **PEU VARIÉ** 0,8–1,3 st ; **CHUTE D'INTONATION** : moitié de ta variation habituelle.
- **arousal** (audeering) : énergie d'articulation, insensible au volume (mesure le tempo). Toujours en % vs la médiane
  de la vidéo ; fenêtres sans parole ignorées (le modèle lit ~0,45 sur du silence). CREUX = ≤ −20 %, PIC = ≥ +30 %.
- **score de chute /100** : contraste avec la phrase d'avant (50) + pause avant 0,4–1,2 s (25) + respiration après ≥ 0,3 s (25).
- **mot suspect** (confiance whisper < 0,5) = mal transcrit ou halluciné ; ce n'est PAS un détecteur de mot avalé (rappel 8 %).
- **Profil créateur** (`--profil`) : historique des rushs + percentiles personnels (F0 médiane, écart-type F0, pics dBFS,
  syll/s, arousal). Un rush est identifié par (nom, durée arrondie, taille) : ré-analyser le même fichier ne crée pas de doublon,
  mais deux exports nommés pareil (`rush.mp4`) comptent bien pour deux. Sous 3 rushs PRÉCÉDENTS le rapport affiche
  « NON CALIBRÉ » ; ensuite chaque mesure est comparée à la médiane des rushs précédents (le rush du jour n'est pas dans sa propre médiane).
- **Arousal absent** : `--sans-arousal`, venv introuvable ou modèle non chargé → ligne en gras « non calculée — raison » en section 2
  et 9, pas d'`arousal.png`, pas de creux/pics, score de chute sans arousal (poids 0,5/0,25/0,25).

## Limites honnêtes

- **Seuils non calibrés sur Nabil** : calibrés sur 3 lecteurs FLEURS (lecture posée) + une voix espeak avec défaut construit.
  Une voix short-form énergique peut déplacer les seuils (d'où le profil). Aucune vraie vidéo de Nabil n'a été mesurée.
- **Un seul locuteur** : pas de diarisation ; un duo, un extrait de film, une musique forte faussent tout.
- **Euh, faux départs, respirations, rires** : invisibles (whisper les gomme, Praat les compte comme parole).
- **Bruit** : testé sur bruit rose SNR 15 dB, musique −12 dB, simulation téléphone ; pas sur bruit de rue réel.
  Sous ~15 dB de SNR, pauses / débit / HNR deviennent incertains (drapeau « bruit de fond fort »).
- **Mots horodatés** : les mots qui suivent une pause démarrent 0,15–0,3 s trop tôt chez whisper ; les pauses sont donc
  mesurées sur l'acoustique, jamais déduites des mots.
- **Timing comique** : la métrique de chute n'a jamais été confrontée à un jugement humain ; une chute chuchotée est sous-notée.
- **Oreille locale (LLM audio)** : Qwen2.5-Omni / Voxtral / Ultravox ont été testés et écartés (hallucinent, biais de position 8/8).
- **Licence** : le modèle audeering `wav2vec2-large-robust-12-ft-emotion-msp-dim` est sous **CC-BY-NC-SA 4.0** — usage non
  commercial uniquement ; `--sans-arousal` pour s'en passer. faster-whisper (MIT), modèle turbo (MIT), Praat/parselmouth (GPL-3).
- Temps mesurés sur une machine partagée (4 cœurs, autres agents actifs) : whisper turbo 18–52 s selon la charge pour 12–60 s d'audio.
