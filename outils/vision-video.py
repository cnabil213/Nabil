#!/usr/bin/env python3
"""
Donne a Claude une vision quasi complete d'une video short-form.

Principe : une video, c'est une suite d'images. Claude sait lire les images.
On extrait donc la video a cadence elevee et on assemble les vignettes en
planches contact horodatees, dimensionnees pour ne pas etre redimensionnees
a la lecture (donc sans perte de detail sur les visages).

Produit :
  - des planches contact horodatees, denses sur le hook
  - la courbe d'energie vocale (forme d'onde + mesures par fenetre)
  - la transcription alignee sur les planches

Usage :
    python3 outils/vision-video.py ma-video.mp4 [--fps 2] [--fps-hook 4]
"""

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import wave

import numpy as np

# Une planche = 4 colonnes x 3 lignes. Cellule 264x470 (9:16) + bandeau.
# Total 1080x1500 : sous la limite de redimensionnement, donc plein detail.
COLS, LIGNES = 4, 3
CELL_L, CELL_H = 264, 470
PAR_PLANCHE = COLS * LIGNES

FENETRE_HOOK = 4.0
POLICE = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def duree_de(video):
    r = run(["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", "-show_streams", video])
    if r.returncode != 0:
        sys.exit(f"ffprobe a echoue :\n{r.stderr}")
    d = json.loads(r.stdout)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    if v is None:
        sys.exit("Pas de piste video.")
    return float(d["format"]["duration"]), v["width"], v["height"]


def extrait_vignettes(video, dossier, fps, debut=None, fin=None, prefixe="v"):
    """Extraction a cadence fixe, horodatee en dur sur chaque vignette.

    Le timecode est reconstruit avec un decalage explicite : `-ss` remet le PTS
    a zero, donc `%{pts}` afficherait un temps faux sur tout segment ne
    commencant pas a 0. Un timecode faux rend toutes les notes inexploitables.
    `%{pts:flt:offset}` corrige bien le decalage mais ignore la precision
    demandee et sort six decimales illisibles : on formate donc a la main.
    """
    os.makedirs(dossier, exist_ok=True)
    off = debut or 0
    tc = (f"%{{eif\\:trunc(t+{off})\\:d}}."
          f"%{{eif\\:trunc(mod((t+{off})*10\\,10))\\:d}}s")
    vf = (
        f"fps={fps},scale={CELL_L}:{CELL_H}:force_original_aspect_ratio=decrease,"
        f"pad={CELL_L}:{CELL_H}:(ow-iw)/2:(oh-ih)/2:color=0x0A0A0A,"
        f"drawtext=fontfile={POLICE}:text='{tc}':"
        f"fontcolor=0xCCFF00:fontsize=26:box=1:boxcolor=0x0A0A0A@0.85:boxborderw=5:"
        f"x=6:y=6"
    )
    cmd = ["ffmpeg", "-y", "-v", "error"]
    if debut is not None:
        cmd += ["-ss", str(debut)]
    if fin is not None:
        cmd += ["-to", str(fin)]
    cmd += ["-i", video, "-vf", vf, "-q:v", "2",
            os.path.join(dossier, f"{prefixe}%05d.jpg")]
    r = run(cmd)
    if r.returncode != 0:
        sys.exit(f"Extraction des vignettes impossible :\n{r.stderr}")
    return sorted(f for f in os.listdir(dossier) if f.startswith(prefixe))


def monte_planches(dossier_vignettes, noms, dossier_sortie, etiquette):
    """Assemble les vignettes en planches contact via le filtre tile."""
    os.makedirs(dossier_sortie, exist_ok=True)
    planches = []
    for i in range(0, len(noms), PAR_PLANCHE):
        lot = noms[i:i + PAR_PLANCHE]
        liste = os.path.join(dossier_vignettes, f"_lot_{etiquette}_{i}.txt")
        with open(liste, "w") as fh:
            for n in lot:
                fh.write(f"file '{os.path.abspath(os.path.join(dossier_vignettes, n))}'\n")
                fh.write("duration 1\n")
        sortie = os.path.join(dossier_sortie,
                              f"planche-{etiquette}-{i // PAR_PLANCHE + 1:02d}.jpg")
        r = run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0",
                 "-i", liste, "-vf",
                 f"tile={COLS}x{LIGNES}:margin=8:padding=6:color=0x0A0A0A",
                 "-frames:v", "1", "-q:v", "2", sortie])
        os.remove(liste)
        if r.returncode == 0 and os.path.exists(sortie):
            planches.append((sortie, lot))
    return planches


def energie(wav, duree, fenetre=0.5):
    """Courbe d'energie vocale : ce qui s'approche le plus du 'tu envoies ou pas'."""
    with wave.open(wav, "rb") as w:
        sr = w.getframerate()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    if data.size == 0:
        return None
    x = data.astype(np.float32) / 32768.0
    n = max(int(sr * fenetre), 1)
    nb = len(x) // n
    if nb == 0:
        return None
    blocs = x[:nb * n].reshape(nb, n)
    rms = np.sqrt((blocs ** 2).mean(axis=1)) + 1e-9
    db = 20 * np.log10(rms)  # enveloppe en dBFS RMS par bloc (reference 0 dBFS)
    parle = db[db > db.max() - 35]  # on ignore les silences
    # crete = max(|x|) sur les echantillons, PAS le max du RMS par bloc
    # (le RMS d'un bloc de 0,5 s est 10 a 20 dB sous la crete : il ne peut pas detecter la saturation)
    crete = float(20 * np.log10(np.abs(x).max() + 1e-9))
    return {
        "db": db,
        "fenetre": fenetre,
        "pic": crete,
        "moyen": float(parle.mean()) if parle.size else float(db.mean()),
        "dynamique": float(np.percentile(parle, 90) - np.percentile(parle, 10))
        if parle.size > 1 else 0.0,
    }


def fiche_captation(fichier):
    """Crete / true peak / LUFS / plancher de bruit / LRA via captation.py (ffmpeg astats + ebur128).
    Mesure sur le fichier d'origine (pas le wav 16 kHz reechantillonne, qui ecrete a 0 dBFS)."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        from ecoute import captation
    except ImportError:
        return None
    try:
        return captation.fiche(fichier)
    except Exception as e:  # ffmpeg absent d'un filtre, fichier muet...
        print(f"      (fiche captation indisponible : {e})")
        return None


def forme_onde(wav, sortie):
    r = run(["ffmpeg", "-y", "-v", "error", "-i", wav, "-filter_complex",
             "showwavespic=s=1400x300:colors=0xCCFF00|0xBF00FF:split_channels=0",
             "-frames:v", "1", sortie])
    return sortie if r.returncode == 0 and os.path.exists(sortie) else None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("video")
    p.add_argument("-o", "--sortie", default=None)
    p.add_argument("--fps", type=float, default=2.0,
                   help="cadence sur le corps de la video (defaut 2)")
    p.add_argument("--fps-hook", type=float, default=4.0,
                   help="cadence sur les 4 premieres secondes (defaut 4)")
    args = p.parse_args()

    if not os.path.exists(args.video):
        sys.exit(f"Fichier introuvable : {args.video}")
    for outil in ("ffmpeg", "ffprobe"):
        if not shutil.which(outil):
            sys.exit(f"{outil} manquant.")

    base = os.path.splitext(os.path.basename(args.video))[0]
    sortie = args.sortie or os.path.join(os.path.dirname(args.video) or ".",
                                         f"vision-{base}")
    os.makedirs(sortie, exist_ok=True)
    tmp = os.path.join(sortie, "_vignettes")

    duree, larg, haut = duree_de(args.video)
    print(f"[1/4] {duree:.1f}s · {larg}x{haut}")

    print(f"[2/4] Vignettes — hook a {args.fps_hook} i/s, corps a {args.fps} i/s")
    noms_hook = extrait_vignettes(args.video, tmp, args.fps_hook,
                                  fin=FENETRE_HOOK, prefixe="h")
    noms_corps = []
    if duree > FENETRE_HOOK:
        noms_corps = extrait_vignettes(args.video, tmp, args.fps,
                                       debut=FENETRE_HOOK, prefixe="c")
    total = len(noms_hook) + len(noms_corps)
    print(f"      {total} vignettes ({len(noms_hook)} hook + {len(noms_corps)} corps)")

    print("[3/4] Planches contact")
    planches = monte_planches(tmp, noms_hook, sortie, "hook")
    planches += monte_planches(tmp, noms_corps, sortie, "corps")
    print(f"      {len(planches)} planches de {PAR_PLANCHE} vignettes")

    print("[4/4] Energie vocale")
    wav = os.path.join(sortie, "_a.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", args.video, "-vn", "-ac", "1",
         "-ar", "16000", "-c:a", "pcm_s16le", wav])
    ndg = energie(wav, duree) if os.path.exists(wav) else None
    cap = fiche_captation(args.video)
    onde = forme_onde(wav, os.path.join(sortie, "forme-onde.png")) if os.path.exists(wav) else None

    L = [f"# Vision — {os.path.basename(args.video)}\n",
         f"Durée **{duree:.1f} s** · {larg}×{haut} · **{total} images extraites** "
         f"({args.fps_hook} i/s sur le hook, {args.fps} i/s ensuite)\n",
         "## Planches contact\n",
         "À ouvrir dans l'ordre. Chaque vignette porte son timecode en haut à gauche.\n"]
    for chemin, lot in planches:
        L.append(f"- `{os.path.basename(chemin)}` — {len(lot)} images")
    L.append("")

    if ndg:
        L.append("## Énergie vocale\n")
        L.append("Échelle : niveaux en dBFS RMS (0 dBFS = pleine échelle), crête en dBFS / dBTP, loudness en LUFS.\n")
        L.append("| Mesure | Valeur | Lecture |")
        L.append("| :--- | :--- | :--- |")
        dy = ndg["dynamique"]
        lect = ("✅ tu joues avec ta voix" if dy >= 12 else
                "🟡 dynamique moyenne, tu peux pousser les contrastes" if dy >= 7 else
                "🔴 débit plat — c'est le truc qui tue un hook")
        L.append(f"| Dynamique | {dy:.1f} dB | {lect} |")
        L.append(f"| Niveau moyen (parole) | {ndg['moyen']:.1f} dBFS | "
                 f"{'✅' if -20 <= ndg['moyen'] <= -8 else '🟡 à normaliser au montage'} |")
        if cap:
            V = cap["verdicts"]
            L.append(f"| Crête échantillon | {cap['crete_dbfs']:.2f} dBFS | "
                     f"{'🔴' if cap['crete_dbfs'] > -1.0 else '✅'} (wav 16 kHz : {ndg['pic']:.2f} dBFS) |")
            L.append(f"| True peak | {cap['true_peak_dbtp']:+.1f} dBTP | {V['saturation']['icone']} {V['saturation']['texte']} |")
            L.append(f"| Loudness intégrée | {cap['lufs_integre']:.1f} LUFS | {V['loudness']['icone']} {V['loudness']['texte']} |")
            nf = cap['plancher_bruit_dbfs']
            L.append(f"| Plancher de bruit | {'−∞' if nf == float('-inf') else f'{nf:.1f}'} dBFS | {V['bruit']['icone']} {V['bruit']['texte']} |")
            L.append(f"| Dynamique (LRA) | {cap['lra_lu']:.1f} LU | {V['dynamique']['icone']} {V['dynamique']['texte']} |\n")
        else:
            L.append(f"| Crête échantillon | {ndg['pic']:.2f} dBFS | "
                     f"{'🔴 ça sature' if ndg['pic'] > -1.0 else '🟡 limite' if ndg['pic'] > -3.0 else '✅ pas de saturation'} |\n")
        db = ndg["db"]
        seuil = np.percentile(db[db > db.max() - 35], 25) if (db > db.max() - 35).any() else db.mean()
        creux = [(i * ndg["fenetre"], float(v)) for i, v in enumerate(db)
                 if v < seuil - 4 and v > db.max() - 35]
        if creux:
            L.append("**Passages où tu redescends en énergie :** " +
                     " · ".join(f"`{t:.1f}s`" for t, _ in creux[:14]) + "\n")
    if onde:
        L.append(f"**Forme d'onde :** `{os.path.basename(onde)}` — les pics, c'est "
                 "là où tu envoies ; les plats, là où ça retombe.\n")

    chemin_rapport = os.path.join(sortie, "VISION.md")
    with open(chemin_rapport, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))

    shutil.rmtree(tmp, ignore_errors=True)
    if os.path.exists(wav):
        os.remove(wav)
    print(f"\n==> {chemin_rapport}")


if __name__ == "__main__":
    main()
