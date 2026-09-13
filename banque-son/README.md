# Banque de sons

Les sons de Nabil, prêts à poser : silences retirés, crête à −3 dBFS, WAV 48 kHz.
Claude choisit dans ce catalogue à chaque montage et les pose dans les trous de la parole
(`outils/sonoriser.py`). Ajouter un son : `python3 outils/banque-son.py ajouter <fichier> --nom <slug> --desc "…"`.

Clips courts uniquement (quelques secondes) : c'est un dépôt git, pas un disque dur.

_Vide pour l'instant — envoie les clips, ils apparaîtront ici._

## Poser un son

```bash
python3 outils/sonoriser.py MONTAGE.mp4 -o SONORISE.mp4 --son 28.28:banque-son/<fichier>:-1
```

L'écart (`-1`) est relatif à la voix : `0` même niveau, `-3` dessous, `+2` au-dessus.
Le son démarre exactement au timecode donné : la banque a déjà retiré le silence de tête.
