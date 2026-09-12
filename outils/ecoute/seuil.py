"""Seuil parole/silence PARTAGE par prosodie.py et chute.py (relecture : un seuil unique classait « silence » tout passage
~10 dB sous les pics -> pauses fantomes de 12 s, ZONES MOLLES/LENTES en cascade).
Seuil LOCAL : p99 de l'intensite sur une fenetre glissante de 10 s (pas 1 s) - 25 dB, borne :
  - jamais sous le plancher global p5 + 6 dB (bruit) ;
  - jamais au-dessus du seuil global (p99 global - 25) : le seuil local ne peut que BAISSER la barre ;
  - une fenetre sans parole nette (p99 local < plancher + 12 dB) garde le seuil global (sinon le bruit passerait pour de la parole).
Retourne le masque de parole + le seuil par trame (meme grille que I)."""
import numpy as np
FEN, PAS = 10.0, 1.0

def masque_parole(I, grid, TS=0.01):
    p99, p5 = float(np.nanpercentile(I, 99)), float(np.nanpercentile(I, 5))
    thr_g = max(p99 - 25, p5 + 6)
    dur = float(grid[-1]) if len(grid) else 0.0
    centres = np.arange(0, dur + 1e-9, PAS)
    loc = []
    for c in centres:
        v = I[(grid >= c - FEN / 2) & (grid < c + FEN / 2)]; v = v[np.isfinite(v)]
        p = float(np.percentile(v, 99)) if len(v) >= 50 else p99
        loc.append(p if p - p5 >= 12 else p99)
    thr_loc = np.clip(np.array(loc) - 25, p5 + 6, thr_g)
    thr_t = np.interp(grid, centres, thr_loc) if len(centres) > 1 else np.full(len(grid), thr_g)
    speech = I > thr_t
    return dict(speech=speech, thr=thr_t, thr_global=thr_g, p99=p99, p5=p5, bruit_fort=bool((p99 - p5) < 30),
                thr_min=round(float(np.min(thr_t)), 1), thr_max=round(float(np.max(thr_t)), 1))

def pauses_dans(pauses, a, b):
    """duree de pause INTERSECTEE avec [a, b] (une pause a cheval sur une borne compte pour sa part dans la fenetre)."""
    return round(sum(max(0.0, min(p["fin"], b) - max(p["debut"], a)) for p in pauses), 2)
