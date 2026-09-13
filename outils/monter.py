#!/usr/bin/env python3
"""monter : coupe un rush sur des segments à garder et normalise le son pour les plateformes.

    python3 outils/monter.py rush.mov -o sortie.mp4 --garder 6.40-27.75 32.05-37.60 40.10-66.90

Les coupes sont à la frame près (trim + concat, pas de seek sur keyframe) : les poser dans un
silence (voir les pauses de RAPPORT-ECOUTE.md) pour qu'elles ne s'entendent pas.
Le son est ramené à -14 LUFS (cible des plateformes) par un GAIN FIXE mesuré sur la coupe, puis un
limiteur retient les crêtes à -1,5 dBFS : ta voix garde ses contrastes d'une phrase à l'autre.
(Avant : loudnorm en deux passes, qui repassait en mode « dynamique » dès que la crête du rush
dépassait la cible — c'est le cas d'un iPhone — et faisait bouger le gain de ±1 dB pendant les
phrases ; constaté sur le rush du 12/09. Il rééchantillonnait aussi le son à 96 kHz.)
`--garder-image MONTAGE.mp4` réutilise l'image déjà encodée d'un montage aux mêmes coupes et ne
refait que le son : zéro perte d'image, quelques secondes.
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


def args_codec(v, a):
    """Arguments d'encodage qui respectent la source.

    Un rush d'iPhone est en plage COMPLETE (yuvj420p, color_range=pc : noirs a 0, blancs a 255).
    Forcer -pix_fmt yuv420p le convertit en plage limitee (16-235) : c'est lossy, et si les
    etiquettes couleur manquent (color_space=unknown), le lecteur affiche un contraste ecrase.
    Constate sur le rush du 12/09 : « la video perd en qualite », alors que le SSIM etait bon.
    On garde donc la plage de la source et on etiquette explicitement BT.709."""
    full = (v.get("color_range") == "pc") or str(v.get("pix_fmt", "")).startswith("yuvj")
    pf = "yuvj420p" if full else "yuv420p"
    tags = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-color_range", "pc" if full else "tv"]
    if a.hevc:
        params = f"colorprim=bt709:transfer=bt709:colormatrix=bt709:range={'full' if full else 'limited'}"
        c = ["-c:v", "libx265", "-crf", str(a.crf), "-preset", a.preset, "-pix_fmt", pf,
             "-tag:v", "hvc1", "-x265-params", params]
    else:
        c = ["-c:v", "libx264", "-crf", str(a.crf), "-preset", a.preset, "-pix_fmt", pf]
    if a.tune:
        c += ["-tune", a.tune]
    return c + tags, full


def stats_limiteur(wav, gain_db, plafond_db=None, tranche_s=0.01):
    """Quelle part du son le limiteur va toucher : % des tranches de 10 ms dont la crête, après le
    gain fixe, dépasse le plafond, et de combien au plus. Chaine vide si numpy/soundfile manquent."""
    try:
        import numpy as np, soundfile as sf
        x, sr = sf.read(wav)
        if x.ndim > 1:
            x = np.max(np.abs(x), axis=1)
        n = max(1, int(sr * tranche_s)); nb = len(x) // n
        if nb == 0:
            return ""
        pk = 20 * np.log10(np.max(np.abs(x[: nb * n]).reshape(nb, n), axis=1) + 1e-9) + gain_db
        plafond = CIBLE_TP if plafond_db is None else plafond_db
        sur = pk > plafond
        if not sur.any():
            return " : aucune crête à retenir"
        return f" : {100 * sur.mean():.1f} % des tranches de 10 ms retenues, au plus {float(pk.max() - plafond):.1f} dB"
    except Exception:
        return ""


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fichier")
    p.add_argument("-o", "--sortie", required=True)
    p.add_argument("--garder", nargs="+", required=True, metavar="DEBUT-FIN",
                   help="segments à garder, en secondes (ex. 6.40-27.75)")
    p.add_argument("--crf", type=int, default=16, help="qualité vidéo, plus bas = meilleur (défaut 16 ; 18 reste très bon, 23 se voit)")
    p.add_argument("--preset", default="slow", help="préréglage x264 (défaut slow : meilleure qualité à débit égal)")
    p.add_argument("--hevc", action="store_true",
                   help="encoder en H.265 : ~40 %% plus léger à qualité égale (iPhone et TikTok le lisent)")
    p.add_argument("--tune", default=None, help="tune x264/x265, ex. « grain » pour garder le grain d'une vidéo sombre")
    p.add_argument("--image", default=None, metavar="FILTRE",
                   help="filtre ffmpeg d'étalonnage appliqué DANS la même passe que la coupe "
                        "(ex. \"eq=brightness=0.06:contrast=1.10,curves=m='0/0 0.25/0.33 1/1'\"). "
                        "Le faire après coûterait un réencodage entier.")
    p.add_argument("--sans-normalisation", action="store_true", help="ne pas toucher au niveau sonore")
    p.add_argument("--garder-image", metavar="MONTAGE.mp4", help="reprend l'image de ce montage (mêmes coupes), ne refait que le son")
    p.add_argument("--cible", type=float, default=CIBLE_LUFS, metavar="LUFS", help=f"niveau visé (défaut {CIBLE_LUFS:.0f} ; -16 retient moins de crêtes)")
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

    image = None
    if a.garder_image:
        if not os.path.isfile(a.garder_image):
            sys.exit(f"ERREUR : --garder-image : fichier introuvable : {a.garder_image}")
        vi, _, di = sonde(a.garder_image)
        if vi is None:
            sys.exit(f"ERREUR : --garder-image : pas de piste vidéo dans {a.garder_image}")
        di = float(vi.get("duration") or di)   # durée du flux VIDÉO (le conteneur ajoute la queue AAC)
        if abs(di - garde) > 0.08:   # deux images
            sys.exit(f"ERREUR : --garder-image : l'image de {a.garder_image} dure {di:.2f} s et les segments gardés {garde:.2f} s : "
                     "ce ne sont pas les mêmes coupes")
        if a.image:
            print("   ⚠ --image ignoré : l'image est reprise telle quelle", file=sys.stderr)
        image = (a.garder_image, vi)
        print(f"   image reprise de {a.garder_image} ({di:.2f} s, {vi.get('codec_name')}, plage {vi.get('color_range')}) : seul le son est refait")

    # --- recalage : sur un rush de telephone la piste audio ne demarre pas a 0 (iPhone : ~0,28 s).
    # Les timecodes du RAPPORT-ECOUTE viennent du wav extrait, dont l'instant 0 est le premier
    # echantillon audio ; trim/atrim, eux, travaillent sur les PTS du conteneur. Sans ce decalage
    # les coupes tombent ~0,3 s trop tot, en pleine queue de mot (constate : -16 dBFS au raccord au
    # lieu du silence). On decale donc video ET audio de la meme valeur : la synchro est preservee.
    off = float(aud.get("start_time") or 0.0)
    if abs(off) > 0.005:
        print(f"   (recalage : la piste audio demarre a {off:.3f} s, les coupes sont decalees d'autant)")
    # --- coupe : trim/atrim + concat (précision à la frame, contrairement à un seek sur keyframe)
    pv, pa = [], []
    img = ("," + a.image) if a.image else ""
    for i, (x, b) in enumerate(segs):
        xo, bo = round(x + off, 3), round(b + off, 3)
        pv.append(f"[0:v]trim={xo}:{bo},setpts=PTS-STARTPTS{img}[v{i}]")
        pa.append(f"[0:a]atrim={xo}:{bo},asetpts=PTS-STARTPTS[a{i}]")
    n = len(segs)
    fc_audio = ";".join(pa) + ";" + "".join(f"[a{i}]" for i in range(n)) + f"concat=n={n}:v=0:a=1[a]"
    if image:
        fc = fc_audio
    else:
        fc = ";".join(pv + pa) + ";" + "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]"

    # --- niveau : mesuré sur la coupe audio seule (quelques secondes), puis gain fixe + limiteur
    # appliqués DANS la passe de coupe : un seul encodage AAC, et le gain ne bouge pas d'une phrase
    # a l'autre (contrairement a loudnorm en mode dynamique).
    out_a = "[a]"
    if not a.sans_normalisation:
        tmpwav = a.sortie + ".coupe.wav"
        print("→ mesure du niveau sur la coupe…")
        r = run(["ffmpeg", "-v", "error", "-y", "-i", a.fichier, "-filter_complex", fc_audio,
                 "-map", "[a]", "-c:a", "pcm_s16le", tmpwav])
        m = mesure_loudness(tmpwav) if r.returncode == 0 else None
        if not m:
            print("   (mesure impossible : le son est laissé tel quel)", file=sys.stderr)
        else:
            I, tp = float(m["input_i"]), float(m["input_tp"])
            gain = max(min(a.cible - I, 20.0), -20.0)
            print(f"   avant : {I:.1f} LUFS, true peak {tp:+.1f} dBTP, LRA {float(m['input_lra']):.1f}")
            print(f"   gain fixe {gain:+.1f} dB, puis limiteur à {CIBLE_TP:+.1f} dBFS" + stats_limiteur(tmpwav, gain))
            fc += f";[a]volume={gain:.2f}dB,alimiter=limit={10 ** (CIBLE_TP / 20):.4f}:level=0:latency=1[aout]"
            out_a = "[aout]"
        if os.path.exists(tmpwav):
            os.remove(tmpwav)

    ent = ["-i", a.fichier] + (["-i", image[0]] if image else [])
    if image:
        video = ["-map", "1:v", "-c:v", "copy"]
        full = image[1].get("color_range") == "pc"
        print("→ son seul (image copiée)…")
    else:
        codec, full = args_codec(v, a)
        video = ["-map", "[v]"] + codec
        print("→ coupe…")
        print(f"   codec : {'H.265' if a.hevc else 'H.264'} CRF {a.crf} {a.preset}"
              + (f" tune {a.tune}" if a.tune else "")
              + f" · plage {'complète (comme la source)' if full else 'limitée'} · BT.709 étiqueté")
    r = run(["ffmpeg", "-v", "error", "-y"] + ent + ["-filter_complex", fc] + video +
            ["-map", out_a, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.sortie])
    if r.returncode != 0 or not os.path.exists(a.sortie):
        sys.exit(f"ERREUR : coupe échouée\n{r.stderr[-1200:]}")

    v2, _, dur2 = sonde(a.sortie)
    if full and v2.get("color_range") != "pc":
        print("   ⚠ la plage complète de la source n'a PAS été conservée (color_range="
              f"{v2.get('color_range')}) : contraste écrasé à l'affichage", file=sys.stderr)
    apres = mesure_loudness(a.sortie)
    print(f"\n✅ {a.sortie}")
    br_src = (os.path.getsize(a.fichier) * 8 / dur) / 1e6
    br_out = (os.path.getsize(a.sortie) * 8 / dur2) / 1e6
    print(f"   {dur2:.2f} s · {v2['width']}×{v2['height']} · {os.path.getsize(a.sortie) / 1048576:.1f} Mo"
          f" · {v2.get('codec_name')} · plage {v2.get('color_range')} · {v2.get('color_space')}")
    if not image:
        print(f"   débit : {br_src:.2f} Mb/s (source) -> {br_out:.2f} Mb/s"
              + ("  ⚠ perte marquée, baisser --crf" if br_out < br_src * (0.27 if a.hevc else 0.45) else "  ✅"))
        # (le H.265 tient la même qualité avec ~40 % de débit en moins : le seuil d'alerte en tient compte)
    if apres:
        print(f"   après : {float(apres['input_i']):.1f} LUFS, true peak {float(apres['input_tp']):+.1f} dBTP")
    print(f"\n   Relire le résultat :  python3 outils/ecoute-video.py \"{a.sortie}\"")


if __name__ == "__main__":
    main()
