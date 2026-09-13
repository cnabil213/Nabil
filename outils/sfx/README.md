# Kit de sons

Six sons de ponctuation **synthétisés de zéro** par [`generer.py`](generer.py) — donc libres de droits,
aucun sample emprunté. Ils suivent la charte sonore de la bible GENZED (air horn sur la vanne,
Windows-error sur le malaise, bass drop sur la transition).

```bash
python3 outils/sfx/generer.py     # régénère les .wav (déterministe, mêmes fichiers à chaque fois)
```

| Fichier | Durée | À quoi ça sert |
| :--- | :--- | :--- |
| `impact.wav` | 0,60 s | Le coup sourd sous une punchline. Sub qui descend + transient claqué |
| `airhorn.wav` | 0,95 s | La vanne. Harmoniques désaccordées, vibrato léger |
| `boom808.wav` | 0,90 s | Bass drop. Appui sur un mot, ou transition |
| `riser.wav` | 1,40 s | Montée avant une chute. **Attention : sous de la parole il est masqué** — mesuré −0,4 dB, inaudible. À poser sur un silence ou pas du tout |
| `whoosh.wav` | 0,55 s | Souffle de transition |
| `error.wav` | 0,45 s | Le malaise. Deux bips descendants |

Tous calés à **−6 dBFS crête**, mais leur RMS va de −13 à −24 dBFS : c'est pourquoi
[`sonoriser.py`](../sonoriser.py) raisonne en **écart au niveau de la voix** et non en gain brut.
Réglé en crête, un impact s'entend à peine ; réglé en RMS, il est à sa place.

## Ce qui n'est pas là

Les **samples de référence** (une punchline de Doumbè, un extrait d'émission, un son de tendance)
ne peuvent pas être fabriqués ici et ne se téléchargent pas : c'est du contenu qui appartient à
quelqu'un. Nabil fournit le fichier, l'outil le place — voir `outils/README.md` § `sonoriser.py`.
