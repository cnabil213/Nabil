#!/usr/bin/env python3
"""sonoriser : pose des sons (sample, jingle, effet) par-dessus une vidéo, à des timecodes précis.

    python3 outils/sonoriser.py MONTAGE.mp4 -o SONORISE.mp4 \
        --son 4.05:outils/sfx/airhorn.wav:-4 \
        --son 28.30:samples/jordan-t-es-mort.wav:-1

Chaque `--son` vaut `temps:fichier[:gain_dB]` — le temps est celui du RAPPORT-ECOUTE / du montage.
La voix est automatiquement baissée sous chaque son (ducking par sidechain) : sans ça le sample
écrase la parole ou l'inverse. Les sons sont posés sur une piste séparée puis mixés une seule fois.
La vidéo n'est pas réencodée (copie du flux) : aucune perte d'image.
"""
import argparse, json, os, subprocess, sys

DUCK_DB = 4.0        # de combien la voix descend sous un son
ATTAQUE_MS = 20      # vitesse a laquelle elle descend
RELACHE_MS = 320     # vitesse a laquelle elle remonte


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def duree(f):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f])
    if r.returncode != 0:
        sys.exit(f"ERREUR : ffprobe ne lit pas {f}\n{r.stderr.strip()}")
    return float(r.stdout.strip())


def a_du_son(f):
    r = run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=codec_type", "-of", "csv=p=0", f])
    return bool(r.stdout.strip())


def niveau_rms(f):
    """Niveau RMS moyen en dBFS (ffmpeg volumedetect). On raisonne en RMS et non en crête :
    un impact normalisé à -6 dBFS crête a un RMS de -24 dBFS, soit 8 dB sous une voix au même
    niveau crête — réglé en crête, l'effet s'entend à peine."""
    r = run(["ffmpeg", "-hide_banner", "-i", f, "-af", "volumedetect", "-f", "null", "-"])
    for l in r.stderr.splitlines():
        if "mean_volume:" in l:
            try: return float(l.split("mean_volume:")[1].split("dB")[0])
            except ValueError: pass
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video")
    p.add_argument("-o", "--sortie", required=True)
    p.add_argument("--son", action="append", required=True, metavar="TEMPS:FICHIER[:ECART_DB]",
                   help="répétable ; ECART_DB est l'écart au niveau de la voix (0 = même niveau, -3 = dessous)")
    p.add_argument("--duck", type=float, default=DUCK_DB, help=f"baisse de la voix sous un son, en dB (défaut {DUCK_DB})")
    p.add_argument("--sans-duck", action="store_true")
    a = p.parse_args()

    if not os.path.isfile(a.video):
        sys.exit(f"ERREUR : vidéo introuvable : {a.video}")
    if not a_du_son(a.video):
        sys.exit("ERREUR : cette vidéo n'a pas de piste audio — rien à mixer")
    dur = duree(a.video)

    sons = []
    for s in a.son:
        m = s.split(":")
        if len(m) < 2:
            sys.exit(f"ERREUR : « {s} » attendu au format temps:fichier[:gain_dB]")
        try:
            t = float(m[0])
        except ValueError:
            sys.exit(f"ERREUR : « {s} » : le temps doit être un nombre de secondes")
        f = ":".join(m[1:-1]) if len(m) > 2 else m[1]
        gain = 0.0
        if len(m) > 2:
            try:
                gain = float(m[-1])
            except ValueError:
                f, gain = ":".join(m[1:]), 0.0
        if not os.path.isfile(f):
            sys.exit(f"ERREUR : son introuvable : {f}")
        if t < 0 or t > dur:
            sys.exit(f"ERREUR : {t} s est hors de la vidéo (0–{dur:.2f} s)")
        d = duree(f)
        if t + d > dur + 0.05:
            print(f"   ⚠ {os.path.basename(f)} à {t} s dépasse la fin ({t + d:.2f} > {dur:.2f}) : il sera coupé", file=sys.stderr)
        sons.append((t, f, gain, d))
    sons.sort()

    # Le gain donné est un ECART A LA VOIX, en dB : 0 = même niveau perçu, -3 = trois dB dessous.
    # L'outil mesure la voix et chaque son, puis calcule le gain réel à appliquer.
    voix_db = niveau_rms(a.video)
    if voix_db is None:
        print("   ⚠ niveau de la voix non mesurable : les gains sont appliqués tels quels", file=sys.stderr)
    print(f"Vidéo : {a.video} — {dur:.2f} s" + (f" — voix {voix_db:.1f} dBFS RMS" if voix_db is not None else ""))
    reglés = []
    for t, f, ecart, d in sons:
        son_db = niveau_rms(f)
        gain = ecart if (voix_db is None or son_db is None) else (voix_db + ecart) - son_db
        gain = max(min(gain, 30.0), -40.0)
        reglés.append((t, f, gain, d))
        print(f"   {t:6.2f} s  {os.path.basename(f):30s} {d:4.2f} s  visé voix{ecart:+.0f} dB"
              + (f"  (son {son_db:.1f} dBFS -> gain {gain:+.1f} dB)" if son_db is not None else ""))
    sons = reglés

    # chaque son est décalé à son timecode puis tous sont additionnés en une piste "effets"
    ent = ["-i", a.video] + sum([["-i", f] for _, f, _, _ in sons], [])
    ch = []
    for i, (t, _, g, _) in enumerate(sons, start=1):
        ch.append(f"[{i}:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,"
                  f"volume={g}dB,adelay={int(t*1000)}|{int(t*1000)}[s{i}]")
    # amix exige au moins 2 entrées : avec un seul son on le passe tel quel
    melange = f"amix=inputs={len(sons)}:duration=longest:normalize=0," if len(sons) > 1 else ""
    ch.append("".join(f"[s{i}]" for i in range(1, len(sons) + 1)) + melange + f"apad,atrim=0:{dur}[fxsrc]")
    ch.append("[fxsrc]asplit=2[fxduck][fxmix]")
    ch.append("[0:a]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[voix]")
    if a.sans_duck:
        ch.append("[voix]anull[vx]")
    else:
        # la voix est compressée par la piste effets : elle recule pendant le son, revient après
        ratio = max(1.0 + a.duck / 2.0, 1.5)
        ch.append(f"[voix][fxduck]sidechaincompress=threshold=0.08:ratio={ratio:.1f}"
                  f":attack={ATTAQUE_MS}:release={RELACHE_MS}:makeup=1[vx]")
    ch.append("[vx][fxmix]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.7[out]")

    cmd = ["ffmpeg", "-v", "error", "-y"] + ent + ["-filter_complex", ";".join(ch),
           "-map", "0:v", "-map", "[out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", a.sortie]
    print("→ mixage…")
    r = run(cmd)
    if r.returncode != 0 or not os.path.exists(a.sortie):
        sys.exit(f"ERREUR : mixage échoué\n{r.stderr[-1500:]}")
    # remise aux normes plateforme : ajouter des effets fait monter le mix, il faut le recadrer
    import re as _re
    r = run(["ffmpeg", "-hide_banner", "-i", a.sortie, "-af",
             "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = _re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, _re.S)
    if m:
        j = json.loads(m.group(0)); tmp2 = a.sortie + ".norm.mp4"
        af = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}"
              f":measured_LRA={j['input_lra']}:measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true")
        r2 = run(["ffmpeg", "-v", "error", "-y", "-i", a.sortie, "-map", "0:v", "-map", "0:a",
                  "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", tmp2])
        if r2.returncode == 0 and os.path.exists(tmp2):
            os.replace(tmp2, a.sortie)
            print(f"   niveau : {float(j['input_i']):.1f} -> -14 LUFS, true peak ramené sous -1,5 dBTP")
        elif os.path.exists(tmp2):
            os.remove(tmp2)
    print(f"\n✅ {a.sortie} — {os.path.getsize(a.sortie)/1048576:.1f} Mo, {duree(a.sortie):.2f} s")
    print(f"   Relire :  python3 outils/ecoute-video.py \"{a.sortie}\"")


if __name__ == "__main__":
    main()
