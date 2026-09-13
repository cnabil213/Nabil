# Banque de sons

Les sons de Nabil, prêts à poser : silences retirés, crête à −3 dBFS, WAV 48 kHz.
Claude choisit dans ce catalogue à chaque montage et les pose dans les trous de la parole
(`outils/sonoriser.py`). Ajouter un son : `python3 outils/banque-son.py ajouter <fichier> --nom <slug> --desc "…"`.

Clips courts uniquement (quelques secondes) : c'est un dépôt git, pas un disque dur.

| Son | Durée | Ce que c'est | Quand l'utiliser | Tags |
| :--- | ---: | :--- | :--- | :--- |
| `doumbe-jordan.wav` | 0.94 s | Doumbè : « JORDAN » (mot entier, foule derrière, fondu avant « t'es mort ») | sur un nom qu'on vient de citer — 0,94 s, la fermeture du « d » resserrée pour qu'il tienne au plus près du trou | mma, menace, court |
| `doumbe-jordan-tes-mort.wav` | 2.98 s | Doumbè à Zébo, KO en 5 s (RMC Sport, sept. 2023) : « Jordan, t'es mort » + la foule qui explose | après le nom de Doumbè, après une menace, ou quand quelqu'un se croit intouchable | mma, doumbe, menace, ko, foule |

Niveaux (RMS) : doumbe-jordan -14 dBFS · doumbe-jordan-tes-mort -16 dBFS

## Poser un son

```bash
python3 outils/sonoriser.py MONTAGE.mp4 -o SONORISE.mp4 --son 28.28:banque-son/<fichier>:-1
```

L'écart (`-1`) est relatif à la voix : `0` même niveau, `-3` dessous, `+2` au-dessus.
Le son démarre exactement au timecode donné : la banque a déjà retiré le silence de tête.
