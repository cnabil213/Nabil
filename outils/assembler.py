#!/usr/bin/env python3
"""assembler : monte UNE vidéo à partir de MORCEAUX pris dans PLUSIEURS fichiers.

    python3 outils/assembler.py -o MONTAGE.mp4 \
        prise1.mp4:0.30-5.63  prise1.mp4:7.49-12.82  prise2.mp4:0.15-8.75

Chaque morceau vaut `FICHIER:DEBUT-FIN`, en secondes, **dans l'ordre du montage**. Un même fichier
peut revenir autant de fois qu'on veut. C'est le complément de `monter.py`, qui ne sait couper que
dans un seul fichier : ici on tourne en plusieurs prises et on assemble la meilleure de chacune.

Comme `monter.py` :
  * **un seul réencodage** — coupe, raccord et encodage dans la même passe ;
  * la **plage de couleur de la source est conservée** (un rush d'iPhone est en plage complète) ;
  * le son est ramené à la cible par un **gain fixe + limiteur**, jamais par loudnorm dynamique ;
  * la **sortie est relue** avant d'annoncer quoi que ce soit (un encodage tué laisse un mp4 de la
    bonne taille, sans atome moov, illisible partout — et ffmpeg peut sortir en code 0).

Les morceaux doivent partager la même taille d'image et la même cadence. L'outil le vérifie et
refuse sinon, plutôt que de livrer un montage qui saute.
"""
import argparse, json, os, re, subprocess, sys

CIBLE_LUFS, CIBLE_TP, CIBLE_LRA = -14.0, -1.5, 11.0


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def sonde(f):
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", f])
    if r.returncode != 0:
        sys.exit(f"ERREUR : ffprobe ne lit pas {f}\n{r.stderr.strip()}")
    d = json.loads(r.stdout)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    return v, a, float(d["format"]["duration"])


def mesure_loudness(f):
    r = run(["ffmpeg", "-hide_banner", "-i", f, "-af",
             f"loudnorm=I={CIBLE_LUFS}:TP={CIBLE_TP}:LRA={CIBLE_LRA}:print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    return json.loads(m.group(0)) if m else None


def fraction(txt):
    a, b = (txt.split("/") + ["1"])[:2]
    return float(a) / float(b or 1)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("morceaux", nargs="+", metavar="FICHIER:DEBUT-FIN")
    p.add_argument("-o", "--sortie", required=True)
    p.add_argument("--crf", type=int, default=18)
    p.add_argument("--preset", default="slow")
    p.add_argument("--hevc", action="store_true")
    p.add_argument("--cible", type=float, default=CIBLE_LUFS, metavar="LUFS")
    p.add_argument("--sans-normalisation", action="store_true")
    a = p.parse_args()

    # --- lecture des morceaux
    pieces = []
    for m in a.morceaux:
        if ":" not in m or "-" not in m.rsplit(":", 1)[1]:
            sys.exit(f"ERREUR : « {m} » attendu au format FICHIER:DEBUT-FIN (secondes)")
        f, bornes = m.rsplit(":", 1)
        try:
            x, b = (float(t) for t in bornes.split("-", 1))
        except ValueError:
            sys.exit(f"ERREUR : « {m} » : bornes non numériques")
        if b <= x:
            sys.exit(f"ERREUR : « {m} » : la fin doit suivre le début")
        if not os.path.isfile(f):
            sys.exit(f"ERREUR : fichier introuvable : {f}")
        pieces.append((f, x, b))

    # --- compatibilité : même image, même cadence, sinon le montage saute
    fichiers = list(dict.fromkeys(f for f, _, _ in pieces))
    infos = {}
    ref = None
    for f in fichiers:
        v, au, dur = sonde(f)
        if v is None or au is None:
            sys.exit(f"ERREUR : {f} n'a pas à la fois une image et un son")
        sig = (int(v["width"]), int(v["height"]), round(fraction(v.get("r_frame_rate", "30/1")), 3))
        if ref is None:
            ref = sig
        elif sig != ref:
            sys.exit(f"ERREUR : {f} est en {sig[0]}×{sig[1]} à {sig[2]:g} i/s, "
                     f"les autres en {ref[0]}×{ref[1]} à {ref[2]:g} i/s — montage impossible tel quel")
        infos[f] = (v, au, dur)
    W, H, FPS = ref

    print(f"Montage de {len(pieces)} morceaux pris dans {len(fichiers)} fichier(s) — {W}×{H}, {FPS:g} i/s")
    total = 0.0
    for f, x, b in pieces:
        v, au, dur = infos[f]
        off = float(au.get("start_time") or 0.0)
        if b > dur + 0.05:
            sys.exit(f"ERREUR : {f}:{x}-{b} dépasse la fin du fichier ({dur:.2f} s)")
        total += b - x
        print(f"   {os.path.basename(f)[:28]:28s} {x:7.2f} – {b:7.2f}  ({b - x:5.2f} s)"
              + (f"  [recalage audio {off:+.3f} s]" if abs(off) > 0.005 else ""))
    print(f"   => {total:.2f} s de montage")

    # --- plage de couleur : on prend celle de la source, comme monter.py
    pleine = any((infos[f][0].get("color_range") == "pc")
                 or str(infos[f][0].get("pix_fmt", "")).startswith("yuvj") for f in fichiers)
    PIX = "yuvj420p" if pleine else "yuv420p"

    # --- graphe : un trim par morceau, puis concat. Les morceaux viennent de fichiers différents,
    # donc `select` (une seule passe) n'est pas applicable ici, contrairement à monter.py.
    idx = {f: i for i, f in enumerate(fichiers)}
    pv, pa = [], []
    for k, (f, x, b) in enumerate(pieces):
        i = idx[f]
        off = float(infos[f][1].get("start_time") or 0.0)
        xo, bo = round(x + off, 3), round(b + off, 3)
        pv.append(f"[{i}:v]trim={xo}:{bo},setpts=PTS-STARTPTS,fps={FPS:g},format={PIX},"
                  f"setsar=1[v{k}]")
        pa.append(f"[{i}:a]atrim={xo}:{bo},asetpts=PTS-STARTPTS,"
                  f"aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=mono[a{k}]")
    n = len(pieces)
    fc_audio = ";".join(pa) + ";" + "".join(f"[a{k}]" for k in range(n)) + f"concat=n={n}:v=0:a=1[a]"
    fc = ";".join(pv + pa) + ";" + "".join(f"[v{k}][a{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=1[v][a]"
    ent = sum([["-i", f] for f in fichiers], [])

    # --- niveau : mesuré sur le son assemblé, puis gain fixe + limiteur dans la passe d'encodage
    out_a = "[a]"
    if not a.sans_normalisation:
        tmpwav = a.sortie + ".montage.wav"
        print("→ mesure du niveau sur le montage…")
        r = run(["ffmpeg", "-v", "error", "-y"] + ent + ["-filter_complex", fc_audio, "-map", "[a]",
                                                         "-c:a", "pcm_s16le", tmpwav])
        m = mesure_loudness(tmpwav) if r.returncode == 0 else None
        if not m:
            print("   (mesure impossible : le son est laissé tel quel)", file=sys.stderr)
        else:
            I, tp = float(m["input_i"]), float(m["input_tp"])
            gain = max(min(a.cible - I, 20.0), -20.0)
            print(f"   avant : {I:.1f} LUFS, true peak {tp:+.1f} dBTP")
            print(f"   gain fixe {gain:+.1f} dB, puis limiteur à {CIBLE_TP:+.1f} dBFS")
            fc += (f";[a]volume={gain:.2f}dB,"
                   f"alimiter=limit={10 ** (CIBLE_TP / 20):.4f}:level=0:latency=1[aout]")
            out_a = "[aout]"
        if os.path.exists(tmpwav):
            os.remove(tmpwav)

    tags = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
            "-color_range", "pc" if pleine else "tv"]
    if a.hevc:
        par = f"colorprim=bt709:transfer=bt709:colormatrix=bt709:range={'full' if pleine else 'limited'}"
        codec = ["-c:v", "libx265", "-crf", str(a.crf), "-preset", a.preset, "-pix_fmt", PIX,
                 "-tag:v", "hvc1", "-x265-params", par] + tags
    else:
        codec = ["-c:v", "libx264", "-crf", str(a.crf), "-preset", a.preset, "-pix_fmt", PIX] + tags
    print(f"→ assemblage et encodage ({'H.265' if a.hevc else 'H.264'} CRF {a.crf} {a.preset}, "
          f"plage {'complète' if pleine else 'limitée'})…")
    r = run(["ffmpeg", "-v", "error", "-y"] + ent + ["-filter_complex", fc, "-map", "[v]"] + codec +
            ["-map", out_a, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.sortie])
    if r.returncode != 0 or not os.path.exists(a.sortie):
        sys.exit(f"ERREUR : assemblage échoué\n{r.stderr[-1500:]}")

    # --- VÉRIFICATION : ne jamais annoncer un succès sans avoir relu le fichier écrit.
    ctrl = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.sortie])
    if ctrl.returncode != 0 or not ctrl.stdout.strip():
        sys.exit(f"ERREUR : {a.sortie} est illisible — encodage interrompu.\n"
                 f"  ffprobe : {ctrl.stderr.strip()[:200]}\n"
                 f"  ffmpeg (code {r.returncode}) : {(r.stderr or '(rien)').strip()[-900:]}")
    v2, _, dur2 = sonde(a.sortie)
    if abs(dur2 - total) > 0.5:
        print(f"   ⚠ durée inattendue : {dur2:.2f} s au lieu de {total:.2f} s", file=sys.stderr)
    if pleine and v2.get("color_range") != "pc":
        print(f"   ⚠ plage complète NON conservée (color_range={v2.get('color_range')})", file=sys.stderr)
    apres = mesure_loudness(a.sortie)
    print(f"\n✅ {a.sortie}")
    print(f"   {dur2:.2f} s · {v2['width']}×{v2['height']} · {os.path.getsize(a.sortie) / 1048576:.1f} Mo"
          f" · {v2.get('codec_name')} · plage {v2.get('color_range')}"
          + (f" · {float(apres['input_i']):.1f} LUFS, true peak {float(apres['input_tp']):+.1f} dBTP" if apres else ""))
    print(f"\n   Relire :  python3 outils/ecoute-video.py \"{a.sortie}\"")


if __name__ == "__main__":
    main()
