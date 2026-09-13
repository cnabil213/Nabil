#!/usr/bin/env python3
"""sonoriser : pose des sons (sample, mème, jingle) par-dessus une vidéo montée, à des timecodes précis.

    python3 outils/sonoriser.py MONTAGE.mp4 -o SONORISE.mp4 \
        --son 28.40:banque-son/doumbe-jordan-tes-mort.wav:-3

Chaque `--son` vaut `temps:fichier[:écart_dB]`. L'écart se mesure par rapport à TA VOIX quand tu
parles (RMS des passages parlés) : 0 = aussi fort que toi, -3 = trois dB dessous.

Par défaut le son S'EFFACE sous ta voix : dès que tu parles il descend de `--fond` dB (10 par
défaut) et il remonte dans tes vraies pauses (>= 0,25 s). Il est donc plein dans les trous et en
fond pendant tes phrases, sans jamais te marcher dessus (il baisse 40 ms AVANT que tu reprennes).
`--sans-duck` le laisse fixe, au niveau demandé, quoi que tu fasses.

Ta voix n'est JAMAIS modifiée : même niveau, mêmes crêtes, mono si la source est mono. Pas de
renormalisation après coup (une sonorisation ajoute ~0 LU ; le montage est déjà aux normes).
Seul filet : un limiteur à -1,5 dBFS sur le mix, sans gain automatique.
La vidéo n'est pas réencodée (copie du flux) ; le son n'est encodé qu'une fois (AAC 192 kb/s).
"""
import argparse, json, math, os, re, subprocess, sys, tempfile

FOND_DB = 10.0        # de combien le son descend sous ta voix quand tu parles
AVANCE_S = 0.04       # le son baisse ce temps-là AVANT que ta voix revienne (pré-lecture)
TENUE_S = 0.25        # une pause plus courte que ça ne fait pas remonter le son (pas de pompage entre les mots)
ATTAQUE_S = 0.015     # constante de temps de la descente
RELACHE_S = 0.04      # constante de temps de la remontée (90 % en ~90 ms)
PLAFOND = 0.84        # limiteur de sécurité : 0,84 = -1,5 dBFS


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def sonde_audio(f):
    r = run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries",
             "stream=channels,sample_rate:format=duration", "-of", "json", f])
    if r.returncode != 0:
        sys.exit(f"ERREUR : ffprobe ne lit pas {f}\n{r.stderr.strip()}")
    d = json.loads(r.stdout)
    st = (d.get("streams") or [None])[0]
    return st, float(d.get("format", {}).get("duration") or 0)


def duree(f):
    return sonde_audio(f)[1]


def lire_mono(f, sr=48000):
    """Décode un fichier en mono float32 à `sr` (numpy)."""
    import numpy as np
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vn", "-ac", "1", "-ar", str(sr),
                        "-f", "f32le", "-"], capture_output=True)
    if r.returncode != 0:
        sys.exit(f"ERREUR : décodage impossible : {f}\n{r.stderr.decode(errors='replace')[-800:]}")
    return np.frombuffer(r.stdout, dtype=np.float32)


def presence_voix(x, sr, hop_s=0.01):
    """Blocs de 10 ms : RMS en dB, seuil local, présence de parole (bool par bloc), niveau parlé."""
    import numpy as np
    n = int(sr * hop_s)
    nb = len(x) // n
    b = x[: nb * n].reshape(nb, n)
    rms = 20 * np.log10(np.sqrt(np.mean(b * b, axis=1)) + 1e-9)
    plancher = float(np.percentile(rms, 10))
    fort = float(np.percentile(rms, 90))
    seuil = max(plancher + 6.0, fort - 20.0)
    pres = rms > seuil
    # les silences plus courts que TENUE_S (entre deux mots) ne comptent pas comme des pauses
    tenue = int(round(TENUE_S / hop_s))
    i = 0
    while i < nb:
        if not pres[i]:
            j = i
            while j < nb and not pres[j]:
                j += 1
            if 0 < i and j < nb and (j - i) < tenue:
                pres[i:j] = True
            i = j
        else:
            i += 1
    parle = b[pres]
    niveau = 20 * math.log10(math.sqrt(float(np.mean(parle * parle))) + 1e-9) if len(parle) else float(np.mean(rms))
    return rms, pres, niveau, seuil, hop_s


def enveloppe_duck(pres, hop_s, sr, n_total, fond_db):
    """Gain (linéaire, par échantillon) qui descend de fond_db quand la voix est là, pré-lecture comprise."""
    import numpy as np
    nb = len(pres)
    avance = int(round(AVANCE_S / hop_s))
    cible = np.zeros(nb)
    idx = np.flatnonzero(pres)
    if len(idx):
        marque = np.zeros(nb, dtype=bool)
        for k in range(avance + 1):
            marque[np.clip(idx - k, 0, nb - 1)] = True
        cible[marque] = -fond_db
    a_att = math.exp(-hop_s / ATTAQUE_S)
    a_rel = math.exp(-hop_s / RELACHE_S)
    g = np.empty(nb)
    cur = 0.0
    for i in range(nb):
        c = cible[i]
        coef = a_att if c < cur else a_rel
        cur = coef * cur + (1 - coef) * c
        g[i] = cur
    n = int(sr * hop_s)
    lin = np.repeat(10 ** (g / 20.0), n)
    if len(lin) < n_total:
        lin = np.concatenate([lin, np.full(n_total - len(lin), lin[-1] if len(lin) else 1.0)])
    return lin[:n_total].astype(np.float32), g


def intervalles(pres, hop_s, t0, t1):
    """Liste (debut, fin, parle?) des plages de présence/absence de voix entre t0 et t1."""
    i0, i1 = int(t0 / hop_s), min(int(math.ceil(t1 / hop_s)), len(pres))
    out = []
    if i1 <= i0:
        return out
    cur = bool(pres[i0]); deb = i0
    for i in range(i0 + 1, i1):
        if bool(pres[i]) != cur:
            out.append((deb * hop_s, i * hop_s, cur)); cur = bool(pres[i]); deb = i
    out.append((deb * hop_s, i1 * hop_s, cur))
    return out


def niveau_rms_db(f):
    """RMS moyen d'un son (dBFS), silences compris — les samples de la banque n'en ont pas."""
    import numpy as np
    x = lire_mono(f)
    return 20 * math.log10(math.sqrt(float(np.mean(x * x))) + 1e-9) if len(x) else -99.0


def mesure_loudness(f):
    r = run(["ffmpeg", "-hide_banner", "-i", f, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"])
    m = re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r.stderr, re.S)
    return json.loads(m.group(0)) if m else None


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video")
    p.add_argument("-o", "--sortie", required=True)
    p.add_argument("--son", action="append", required=True, metavar="TEMPS:FICHIER[:ECART_DB]",
                   help="répétable ; ECART_DB par rapport à ta voix parlée (0 = même niveau, -3 = dessous)")
    p.add_argument("--fond", type=float, default=FOND_DB, help=f"de combien le son descend quand tu parles, en dB (défaut {FOND_DB:.0f})")
    p.add_argument("--sans-duck", action="store_true", help="le son reste fixe, même pendant que tu parles")
    p.add_argument("--piste-effets", metavar="FICHIER.wav", help="écrit aussi la piste des sons seule (pour la mesurer)")
    a = p.parse_args()

    if not os.path.isfile(a.video):
        sys.exit(f"ERREUR : vidéo introuvable : {a.video}")
    st, dur = sonde_audio(a.video)
    if not st:
        sys.exit("ERREUR : cette vidéo n'a pas de piste audio — rien à mixer")
    layout = "mono" if int(st.get("channels") or 1) == 1 else "stereo"

    sons = []
    for s in a.son:
        m = s.split(":")
        if len(m) < 2:
            sys.exit(f"ERREUR : « {s} » attendu au format temps:fichier[:écart_dB]")
        try:
            t = float(m[0])
        except ValueError:
            sys.exit(f"ERREUR : « {s} » : le temps doit être un nombre de secondes")
        f, ecart = m[1], 0.0
        if len(m) > 2:
            try:
                ecart = float(m[-1]); f = ":".join(m[1:-1])
            except ValueError:
                f = ":".join(m[1:])
        if not os.path.isfile(f):
            sys.exit(f"ERREUR : son introuvable : {f}")
        if t < 0 or t > dur:
            sys.exit(f"ERREUR : {t} s est hors de la vidéo (0–{dur:.2f} s)")
        d = duree(f)
        if t + d > dur + 0.05:
            print(f"   ⚠ {os.path.basename(f)} à {t} s dépasse la fin ({t + d:.2f} > {dur:.2f}) : il sera coupé", file=sys.stderr)
        sons.append((t, f, ecart, d))
    sons.sort()

    # --- ta voix : où tu parles, à quel niveau
    import numpy as np
    sr = int(st.get("sample_rate") or 48000)   # on reste au taux de la source : pas de rééchantillonnage
    voix = lire_mono(a.video, sr)
    rms, pres, voix_db, seuil, hop = presence_voix(voix, sr)
    print(f"Vidéo : {a.video} — {dur:.2f} s, {layout} — voix parlée {voix_db:.1f} dBFS RMS "
          f"(parole au-dessus de {seuil:.0f} dBFS : {100 * pres.mean():.0f} % du temps)")

    # --- gains : l'écart demandé est relatif à la voix parlée
    regles = []
    for t, f, ecart, d in sons:
        son_db = niveau_rms_db(f)
        gain = max(min((voix_db + ecart) - son_db, 30.0), -40.0)
        regles.append((t, f, gain, d))
        print(f"   {t:6.2f} s  {os.path.basename(f):32s} {d:4.2f} s  visé voix{ecart:+.0f} dB  (son {son_db:.1f} dBFS -> gain {gain:+.1f} dB)")
        for deb, fin, parle in intervalles(pres, hop, t, min(t + d, dur)):
            if fin - deb >= 0.08:
                etat = ("tu parles : son en fond" if not a.sans_duck else "tu parles : son fixe") if parle else "trou : son plein"
                print(f"             {deb:6.2f}–{fin:6.2f} s  {etat}")
    sons = regles

    tmpdir = tempfile.mkdtemp(prefix="sonoriser-")
    gain_wav = None
    if not a.sans_duck:
        import soundfile as sf
        lin, g_db = enveloppe_duck(pres, hop, sr, len(voix), a.fond)
        gain_wav = os.path.join(tmpdir, "duck.wav")
        sf.write(gain_wav, lin, sr, subtype="FLOAT")

    ent = ["-i", a.video] + sum([["-i", f] for _, f, _, _ in sons], [])
    if gain_wav:
        ent += ["-i", gain_wav]
    ch = []
    for i, (t, _, g, _) in enumerate(sons, start=1):
        ch.append(f"[{i}:a]aformat=sample_fmts=fltp:sample_rates={sr}:channel_layouts={layout},"
                  f"volume={g:.2f}dB,adelay={int(round(t * 1000))}:all=1[s{i}]")
    melange = f"amix=inputs={len(sons)}:duration=longest:normalize=0," if len(sons) > 1 else ""
    ch.append("".join(f"[s{i}]" for i in range(1, len(sons) + 1)) + melange + f"apad,atrim=0:{dur:.3f}[fxsrc]")
    if gain_wav:
        # le gain de ducking est un signal (wav 32 bits) multiplié échantillon par échantillon
        k = len(sons) + 1
        ch.append(f"[{k}:a]aformat=sample_fmts=fltp:sample_rates={sr}:channel_layouts={layout},apad,atrim=0:{dur:.3f}[duck]")
        ch.append("[fxsrc][duck]amultiply[fx]")
    else:
        ch.append("[fxsrc]anull[fx]")
    if a.piste_effets:
        ch.append("[fx]asplit=2[fxmix][fxout]")
    else:
        ch.append("[fx]anull[fxmix]")
    ch.append(f"[0:a]aformat=sample_fmts=fltp:sample_rates={sr}:channel_layouts={layout}[voix]")
    # apad : la piste son fait exactement la durée de la vidéo (sinon l'AAC s'arrête ~50 ms avant l'image)
    ch.append(f"[voix][fxmix]amix=inputs=2:duration=first:normalize=0,"
              f"alimiter=limit={PLAFOND}:level=0:latency=1,apad=whole_dur={dur:.3f}[out]")

    cmd = ["ffmpeg", "-v", "error", "-y"] + ent + ["-filter_complex", ";".join(ch),
           "-map", "0:v", "-map", "[out]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", a.sortie]
    if a.piste_effets:
        cmd += ["-map", "[fxout]", "-c:a", "pcm_s16le", a.piste_effets]
    print("→ mixage (un seul encodage AAC, vidéo copiée)…")
    r = run(cmd)
    for fch in (gain_wav,):
        if fch and os.path.exists(fch):
            os.remove(fch)
    try:
        os.rmdir(tmpdir)
    except OSError:
        pass
    if r.returncode != 0 or not os.path.exists(a.sortie):
        sys.exit(f"ERREUR : mixage échoué\n{r.stderr[-1500:]}")

    m = mesure_loudness(a.sortie)
    print(f"\n✅ {a.sortie} — {os.path.getsize(a.sortie) / 1048576:.1f} Mo, {duree(a.sortie):.2f} s")
    if m:
        I, tp = float(m["input_i"]), float(m["input_tp"])
        alerte = "" if (abs(I + 14) <= 2.0 and tp <= -1.0) else "  ⚠ hors normes plateforme : normaliser le MONTAGE d'abord (outils/monter.py)"
        print(f"   niveau : {I:.1f} LUFS, true peak {tp:+.1f} dBTP{alerte}")
    if a.piste_effets:
        print(f"   piste des sons seule : {a.piste_effets}")
    print(f"   Relire :  python3 outils/ecoute-video.py \"{a.sortie}\"")


if __name__ == "__main__":
    main()
