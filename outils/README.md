# Outils

## `analyse-video.py` — relecture d'un rush

Transforme une vidéo en un rapport lisible : transcription horodatée, analyse du
hook, temps morts à couper, images extraites.

### Installation (à refaire à chaque nouvelle session)

Le container est neuf à chaque fois. Une seule commande :

```bash
apt-get update && apt-get install -y --no-install-recommends ffmpeg
pip3 install --break-system-packages faster-whisper
```

Le modèle de transcription (~480 Mo) se télécharge tout seul au premier lancement,
en une dizaine de secondes.

### Usage

```bash
python3 outils/analyse-video.py /mnt/user-data/working/ma-video.mp4
```

Options : `-o dossier_sortie` · `-m tiny|base|small|medium` (défaut `small`).

### Ce que ça sort

```
analyse-ma-video/
├── RAPPORT.md      ← le rapport complet
└── images/         ← images extraites, denses sur les 4 premières secondes
```

Le rapport contient :

| Section | Ce qu'on y lit |
| :--- | :--- |
| **Fiche technique** | Durée, format (alerte si pas 9:16), fps, poids |
| **Le hook** | Le silence avant le premier mot + le texte exact des 4 premières secondes |
| **Rythme** | Débit en mots/min, temps de parole, secondes récupérables au montage |
| **Blancs à couper** | Chaque temps mort, son timecode, les mots qui l'encadrent |
| **Transcription** | Tout le texte, horodaté segment par segment |
| **Images** | La liste des captures, à ouvrir pour la relecture visuelle |

### Note technique

Les temps morts sont mesurés par **détection acoustique** (`silencedetect`), pas
par les timestamps de Whisper. Whisper étire la durée des mots pour absorber les
silences : il sous-estime massivement les blancs. Testé — un blanc réel de 1,35 s
était rapporté à `0.0 s` via Whisper, correctement détecté via l'acoustique.

### Limites, honnêtement

- La transcription n'est pas parfaite sur l'argot et les noms propres. Elle sert à
  analyser la **structure**, pas à être publiée telle quelle en sous-titres.
- L'analyse porte sur le **texte, le rythme et les images fixes**. Le jeu d'acteur,
  l'énergie, le timing comique d'une mimique — ça, ça ne se lit pas dans un rapport.
