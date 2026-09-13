#!/usr/bin/env python3
"""Fabrique un petit kit de sons de ponctuation, synthétisés de zéro (donc libres de droits).

    python3 outils/sfx/generer.py            # écrit les .wav dans ce dossier

Les sons suivent la charte sonore de la bible GENZED : air horn sur la vanne, Windows-error sur
le malaise, bass drop sur la transition. Ils sont volontairement courts et calés à -6 dBFS crête,
pour que `sonoriser.py` n'ait qu'à ajuster le gain.
"""
import os
import numpy as np
from scipy import signal
import soundfile as sf

SR = 48000
ICI = os.path.dirname(os.path.abspath(__file__))


def env(n, attaque, chute, forme=3.0):
    """Enveloppe attaque/decroissance exponentielle, en secondes."""
    a, d = max(int(attaque * SR), 1), max(int(chute * SR), 1)
    e = np.ones(n)
    e[:a] = np.linspace(0, 1, a) ** 0.6
    fin = np.exp(-forme * np.linspace(0, 1, n - a)) if n > a else np.array([])
    e[a:] = fin
    return e


def bp_glissant(x, f0, f1, q=2.0, blocs=256):
    """Passe-bande dont la fréquence centrale glisse de f0 à f1 (traitement par blocs)."""
    y = np.zeros_like(x)
    freqs = np.geomspace(f0, f1, blocs)
    bornes = np.linspace(0, len(x), blocs + 1).astype(int)
    zi = None
    for i, f in enumerate(freqs):
        a, b = bornes[i], bornes[i + 1]
        if b <= a:
            continue
        f = min(max(f, 30.0), SR / 2 * 0.95)
        sos = signal.butter(2, [max(f / q, 20) / (SR / 2), min(f * q, SR / 2 * 0.98) / (SR / 2)], btype="band", output="sos")
        if zi is None:
            zi = signal.sosfilt_zi(sos) * x[a]
        y[a:b], zi = signal.sosfilt(sos, x[a:b], zi=zi)
    return y


def norm(x, crete_db=-6.0):
    x = x - x.mean()
    p = np.abs(x).max()
    return (x / p * 10 ** (crete_db / 20)) if p > 0 else x


def ecrire(nom, x):
    x = norm(x).astype(np.float32)
    # 3 ms de fondu aux deux bouts : jamais de clic à la pose
    f = int(0.003 * SR)
    x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
    sf.write(os.path.join(ICI, nom), x, SR)
    print(f"  {nom:16s} {len(x)/SR:.2f} s")


def t(d):
    return np.arange(int(d * SR)) / SR


def impact():
    """Coup sourd : sub qui descend + transient claqué. Pour une punchline."""
    x = t(0.60)
    f = 90 * np.exp(-9 * x) + 42
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(x), 0.002, 0.58, 5)
    cl = np.random.default_rng(1).normal(0, 1, len(x))
    sos = signal.butter(2, 1800 / (SR / 2), btype="high", output="sos")
    cl = signal.sosfilt(sos, cl) * env(len(x), 0.0005, 0.05, 60) * 0.5
    return sub + cl


def airhorn():
    """Corne de brume : empilement d'harmoniques légèrement désaccordées. La vanne."""
    x = t(0.95)
    e = env(len(x), 0.012, 0.9, 1.2)
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.5 * x)
    out = np.zeros(len(x))
    for base in (415.0, 415.0 * 1.003, 415.0 * 0.997):
        for h, amp in ((1, 1.0), (2, 0.75), (3, 0.5), (4, 0.32), (5, 0.2), (6, 0.12)):
            out += amp * np.sin(2 * np.pi * base * h * np.cumsum(vib) / SR)
    return out * e


def riser():
    """Montée : bruit filtré qui grimpe + sinus qui monte. Avant une chute."""
    x = t(1.40)
    n = np.random.default_rng(2).normal(0, 1, len(x))
    br = bp_glissant(n, 320, 7000, q=1.6) * np.linspace(0.15, 1.0, len(x)) ** 2
    f = np.geomspace(220, 1700, len(x))
    ton = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.linspace(0, 0.5, len(x)) ** 2
    return (br * 1.0 + ton) * np.concatenate([np.ones(len(x) - int(0.05 * SR)), np.linspace(1, 0, int(0.05 * SR))])


def whoosh():
    """Souffle de transition : bruit dont la bande balaye vers le haut puis retombe."""
    x = t(0.55)
    n = np.random.default_rng(3).normal(0, 1, len(x))
    y = bp_glissant(n, 500, 5200, q=1.8)
    cloche = np.sin(np.pi * np.linspace(0, 1, len(x))) ** 1.5
    return y * cloche


def boom808():
    """Bass drop : sinus qui plonge. Transition, ou appui sur un mot."""
    x = t(0.90)
    f = 150 * np.exp(-14 * x) + 45
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(len(x), 0.004, 0.88, 3.2)


def error():
    """Deux bips descendants facon erreur systeme. Le malaise."""
    out = []
    for freq, d in ((760, 0.16), (570, 0.26)):
        x = t(d)
        s = np.sign(np.sin(2 * np.pi * freq * x)) * 0.35 + np.sin(2 * np.pi * freq * x)
        out.append(s * env(len(x), 0.004, d - 0.004, 1.5))
        out.append(np.zeros(int(0.03 * SR)))
    return np.concatenate(out[:-1])


if __name__ == "__main__":
    print("Kit de sons (synthétisés, libres de droits) :")
    for nom, fn in (("impact.wav", impact), ("airhorn.wav", airhorn), ("riser.wav", riser),
                    ("whoosh.wav", whoosh), ("boom808.wav", boom808), ("error.wav", error)):
        ecrire(nom, fn())
