#!/usr/bin/env python3
"""monter : coupe un rush sur des segments à garder et normalise le son pour les plateformes.

    python3 outils/monter.py rush.mov -o sortie.mp4 --garder 6.40-27.75 32.05-37.60 40.10-66.90

Les coupes sont à la frame près (trim + concat, pas de seek sur keyframe) : les poser dans un
silence (voir les pauses de RAPPORT-ECOUTE.md) pour qu'elles ne s'entendent pas.
Le son est ramené à -14 LUFS / -1,5 dBTP en deux passes (mesure puis correction linéaire),
la cible des plateformes : sans ça elles remontent le niveau elles-mêmes, et le souffle avec.
La rotation du téléphone est appliquée automatiquement par ffmpeg (un rush portrait reste portrait).
"""
import argparse, json, os, re, subprocess, sys

CIBLE_LUFS, CIBLE_TP, CIBLE_LRA = -14.0, -1.5, 11.0


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def sonde(f):
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", f])
    if r.returncode != 0:
        sys.exit(f"ERREUR : ffprobe ne lit pas {f}\n{r.stderr.strip()}")
    d = json.loads(r.stdout)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    return v, a, float(d["format"]["duration"])


def mesure_loudness(f):
    """Passe 1 de loudnorm : mesure sur le fichier réel (JSON en fin de stderr)."""
    r = run(["ffmpeg", "-hide_banner", "-i", f, "-af",
             f"loudnorm=I={CIBLE_LUFS}:TP={CIBLE_TP}:LRA={CIBLE_LRA}:print_format=json",
             "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    if not m:
        return None
    return json.loads(m.group(0))


def segments(specs, duree):
    out = []
    for s in specs:
        if "-" not in s:
            sys.exit(f"ERREUR : segment « {s} » attendu au format debut-fin (en secondes)")
        a, b = s.split("-", 1)
        try:
            a, b = float(a), float(b)
        except ValueError:
            sys.exit(f"ERREUR : segment « {s} » : bornes non numériques")
        if b <= a:
            sys.exit(f"ERREUR : segment « {s} » : la fin doit suivre le début")
        if a < 0 or b > duree + 0.05:  # duree conteneur ; le decalage audio est applique plus tard
            sys.exit(f"ERREUR : segment « {s} » hors du fichier (0–{duree:.2f} s)")
        out.append((a, min(b, duree)))
    out.sort()
    for (a1, b1), (a2, b2) in zip(out, out[1:]):
        if a2 < b1:
            sys.exit(f"ERREUR : segments qui se chevauchent : {a1}-{b1} et {a2}-{b2}")
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fichier")
    p.add_argument("-o", "--sortie", required=True)
    p.add_argument("--garder", nargs="+", required=True, metavar="DEBUT-FIN",
                   help="segments à garder, en secondes (ex. 6.40-27.75)")
    p.add_argument("--crf", type=int, default=16, help="qualité vidéo, plus bas = meilleur (défaut 16 ; 18 reste très bon, 23 se voit)")
    p.add_argument("--preset", default="slow", help="préréglage x264 (défaut slow : meilleure qualité à débit égal)")
    p.add_argument("--image", default=None, metavar="FILTRE",
                   help="filtre ffmpeg d'étalonnage appliqué DANS la même passe que la coupe "
                        "(ex. \"eq=brightness=0.06:contrast=1.10,curves=m='0/0 0.25/0.33 1/1'\"). "
                        "Le faire après coûterait un réencodage entier.")
    p.add_argument("--sans-normalisation", action="store_true", help="ne pas toucher au niveau sonore")
    a = p.parse_args()

    if not os.path.isfile(a.fichier):
        sys.exit(f"ERREUR : fichier introuvable : {a.fichier}")
    v, aud, dur = sonde(a.fichier)
    if v is None:
        sys.exit("ERREUR : pas de piste vidéo")
    if aud is None:
        sys.exit("ERREUR : pas de piste audio — rien à normaliser ni à recoller")
    segs = segments(a.garder, dur)
    garde = sum(b - x for x, b in segs)
    print(f"Source : {a.fichier} — {dur:.2f} s")
    for x, b in segs:
        print(f"   garder {x:7.2f} – {b:7.2f} s  ({b - x:5.2f} s)")
    print(f"   => {garde:.2f} s gardées, {dur - garde:.2f} s coupées ({100 * (dur - garde) / dur:.0f} %)")

    # --- recalage : sur un rush de telephone la piste audio ne demarre pas a 0 (iPhone : ~0,28 s).
    # Les timecodes du RAPPORT-ECOUTE viennent du wav extrait, dont l'instant 0 est le premier
    # echantillon audio ; trim/atrim, eux, travaillent sur les PTS du conteneur. Sans ce decalage
    # les coupes tombent ~0,3 s trop tot, en pleine queue de mot (constate : -16 dBFS au raccord au
    # lieu du silence). On decale donc video ET audio de la meme valeur : la synchro est preservee.
    off = float(aud.get("start_time") or 0.0)
    if abs(off) > 0.005:
        print(f"   (recalage : la piste audio demarre a {off:.3f} s, les coupes sont decalees d'autant)")
    # --- coupe : trim/atrim + concat (précision à la frame, contrairement à un seek sur keyframe)
    parts, lab = [], []
    img = ("," + a.image) if a.image else ""
    for i, (x, b) in enumerate(segs):
        xo, bo = round(x + off, 3), round(b + off, 3)
        parts.append(f"[0:v]trim={xo}:{bo},setpts=PTS-STARTPTS{img}[v{i}];[0:a]atrim={xo}:{bo},asetpts=PTS-STARTPTS[a{i}]")
        lab.append(f"[v{i}][a{i}]")
    fc = ";".join(parts) + ";" + "".join(lab) + f"concat=n={len(segs)}:v=1:a=1[v][a]"
    tmp = a.sortie + ".coupe.mp4"
    print("→ coupe…")
    r = run(["ffmpeg", "-v", "error", "-y", "-i", a.fichier, "-filter_complex", fc,
             "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", str(a.crf), "-preset", a.preset,
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp])
    if r.returncode != 0 or not os.path.exists(tmp):
        sys.exit(f"ERREUR : coupe échouée\n{r.stderr[-1200:]}")

    if a.sans_normalisation:
        os.replace(tmp, a.sortie)
    else:
        print("→ mesure du niveau…")
        m = mesure_loudness(tmp)
        if not m:
            print("   (mesure impossible : le son est laissé tel quel)", file=sys.stderr)
            os.replace(tmp, a.sortie)
        else:
            print(f"   avant : {float(m['input_i']):.1f} LUFS, true peak {float(m['input_tp']):+.1f} dBTP, LRA {float(m['input_lra']):.1f}")
            print("→ normalisation…")
            af = (f"loudnorm=I={CIBLE_LUFS}:TP={CIBLE_TP}:LRA={CIBLE_LRA}"
                  f":measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
                  f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=summary")
            r = run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-map", "0:v", "-map", "0:a",
                     "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k",
                     "-movflags", "+faststart", a.sortie])
            if r.returncode != 0 or not os.path.exists(a.sortie):
                sys.exit(f"ERREUR : normalisation échouée\n{r.stderr[-1200:]}")
            os.remove(tmp)

    v2, _, dur2 = sonde(a.sortie)
    apres = mesure_loudness(a.sortie)
    print(f"\n✅ {a.sortie}")
    br_src = (os.path.getsize(a.fichier) * 8 / dur) / 1e6
    br_out = (os.path.getsize(a.sortie) * 8 / dur2) / 1e6
    print(f"   {dur2:.2f} s · {v2['width']}×{v2['height']} · {os.path.getsize(a.sortie) / 1048576:.1f} Mo")
    print(f"   débit : {br_src:.2f} Mb/s (source) -> {br_out:.2f} Mb/s"
          + ("  ⚠ perte marquée, baisser --crf" if br_out < br_src * 0.45 else "  ✅"))
    if apres:
        print(f"   après : {float(apres['input_i']):.1f} LUFS, true peak {float(apres['input_tp']):+.1f} dBTP")
    print(f"\n   Relire le résultat :  python3 outils/ecoute-video.py \"{a.sortie}\"")


if __name__ == "__main__":
    main()
