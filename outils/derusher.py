#!/usr/bin/env python3
"""derusher : propose une liste de coupes MESUREE. Il ne coupe pas, il propose.

Usage : python3 outils/derusher.py rush.mp4 [-o derush/] [--transcription prefixe_mots.json]
        [--silence-min 0.35] [--marge 0.12] [--seuil-db AUTO] [--blanc-long 1.5]

Trois choses, dans cet ordre :
 1. FICHE CAPTATION  — ce que le rush est vraiment (resolution, codec, plage de couleur,
    decalage audio, tags Snapchat). Regle CLAUDE.md §5 : on le dit a Nabil AVANT de monter.
 2. SILENCES MESURES — enveloppe RMS par blocs de 10 ms, seuil adaptatif entre le plancher
    de bruit et le niveau de parole. Jamais une borne de mot Whisper (il finit trop tot).
 3. PROPOSITION     — segments a garder + ligne --garder prete pour monter.py, chaque raccord
    verifie (niveau mesure a +/- 50 ms du point de coupe).

Ce qu'il ne fait PAS, volontairement :
 - il n'encode rien. La coupe reste a monter.py / assembler.py.
 - il ne decide pas. Les blancs longs et les reprises sont SIGNALES, pas supprimes :
    * un blanc >= --blanc-long peut porter une information (tier list foot du 14/09 :
      3,72 s ramenes a 0,22 s fabriquaient un effet qui n'avait pas eu lieu).
    * une reprise n'est une reprise que si la transcription le dit ET qu'un silence
      l'entoure. Sans silence mesure autour, on garde (CLAUDE.md §2 bis, regle 3).

Les timecodes sont dans le repere du wav extrait (instant 0 = premier echantillon audio),
soit exactement celui du RAPPORT-ECOUTE.md et celui qu'attend monter.py, qui applique
lui-meme le decalage du conteneur.

Dependances : numpy, soundfile, ffmpeg/ffprobe.
"""
import argparse, json, os, re, subprocess, sys, unicodedata

BLOC_S = 0.010          # resolution de l'enveloppe
FENETRE_RACCORD_S = 0.05  # demi-fenetre de verification d'un point de coupe


def die(msg):
    print(f"ERREUR : {msg}", file=sys.stderr); sys.exit(1)


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


# ---------------------------------------------------------------- fiche captation

def sonder(src):
    """ffprobe complet : c'est le premier reflexe sur un rush recu (CLAUDE.md §5)."""
    r = run(["ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", src])
    if r.returncode != 0:
        die(f"ffprobe a echoue sur {src} : {r.stderr.strip()}")
    d = json.loads(r.stdout)
    vid = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    aud = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    if aud is None:
        die("ce fichier n'a pas de piste audio : rien a mesurer")
    fmt = d["format"]

    rot = 0
    for sd in (vid or {}).get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(float(sd["rotation"]))
    tags = {**fmt.get("tags", {}), **(vid or {}).get("tags", {})}

    def frac(x):
        try:
            n, dd = x.split("/"); return round(int(n) / int(dd), 3) if int(dd) else None
        except Exception:
            return None

    fiche = {
        "fichier": os.path.basename(src),
        "duree_s": round(float(fmt.get("duration") or 0), 3),
        "taille_Mo": round(int(fmt.get("size") or 0) / 1e6, 1),
        "debit_Mbs": round(int(fmt.get("bit_rate") or 0) / 1e6, 2) if fmt.get("bit_rate") else None,
        "largeur": (vid or {}).get("width"), "hauteur": (vid or {}).get("height"),
        "rotation_deg": rot,
        "codec_video": (vid or {}).get("codec_name"), "pix_fmt": (vid or {}).get("pix_fmt"),
        "plage_couleur": (vid or {}).get("color_range") or "inconnue",
        "espace_couleur": (vid or {}).get("color_space") or "inconnu",
        "cadence": frac((vid or {}).get("r_frame_rate", "0/0")),
        "codec_audio": aud.get("codec_name"), "audio_hz": int(aud.get("sample_rate") or 0),
        "audio_canaux": aud.get("channels"),
        "decalage_audio_s": round(float(aud.get("start_time") or 0.0), 3),
        "tags": {k: v for k, v in tags.items() if len(str(v)) < 200},
    }
    # un rush portrait filme au telephone est souvent 1920x1080 + rotation 90
    if rot in (90, -90, 270) and fiche["largeur"] and fiche["hauteur"]:
        fiche["affichage"] = f'{fiche["hauteur"]}x{fiche["largeur"]} (portrait apres rotation)'
    elif fiche["largeur"]:
        fiche["affichage"] = f'{fiche["largeur"]}x{fiche["hauteur"]}'
    return fiche


def alertes_captation(f):
    """Ce qui plafonne la qualite AVANT le montage. Chaque alerte cite sa mesure."""
    a = []
    h = min(x for x in (f["largeur"], f["hauteur"]) if x) if f["largeur"] else 0
    if h and h < 1080:
        a.append(f"RUSH EN {h}p — un montage ne sera jamais plus net que son rush. "
                 f"Filmer avec l'app Camera (1080p/4K), pas dans une app tierce.")
    blob = " ".join(str(v).lower() for v in f["tags"].values())
    for app, nom in (("snap", "Snapchat"), ("instagram", "Instagram"), ("tiktok", "TikTok")):
        if app in blob:
            a.append(f"CAPTURE {nom} detectee dans les metadonnees — l'original dans Photos est "
                     f"meilleur. Le demander a Nabil avant de monter.")
            break
    if f["decalage_audio_s"] >= 0.05:
        a.append(f"Decalage audio de {f['decalage_audio_s']:.3f} s — les timecodes ci-dessous sont "
                 f"dans le repere du wav ; monter.py applique ce decalage tout seul, ne pas le refaire.")
    if f["plage_couleur"] in ("pc", "full") or f["pix_fmt"] == "yuvj420p":
        a.append(f"Plage de couleur COMPLETE ({f['plage_couleur']}/{f['pix_fmt']}) — a conserver. "
                 f"Forcer yuv420p ecraserait les noirs (mesure le 12/09 : noirs de 3 a 19).")
    return a


# ---------------------------------------------------------------- enveloppe

def extraire_wav(src, out):
    """Meme extraction que ecoute-video.py : mono, passe-haut 80 Hz, pas de -ss.
    Donc instant 0 du wav = premier echantillon audio = repere du RAPPORT-ECOUTE."""
    wav = os.path.join(out, re.sub(r"\.[^.]+$", "", os.path.basename(src)) + "_env.wav")
    r = run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "48000",
             "-af", "highpass=f=80", "-c:a", "pcm_s16le", wav])
    if r.returncode != 0 or not os.path.exists(wav):
        die(f"extraction audio echouee : {r.stderr.strip()}")
    return wav


def enveloppe(wav):
    import numpy as np, soundfile as sf
    x, sr = sf.read(wav, dtype="float32")
    if x.ndim > 1:
        x = x.mean(axis=1)
    n = max(1, int(round(BLOC_S * sr)))
    nb = len(x) // n
    if nb < 2:
        die("clip trop court pour une enveloppe")
    b = x[:nb * n].reshape(nb, n)
    rms = np.sqrt((b.astype(np.float64) ** 2).mean(axis=1))
    db = 20 * np.log10(np.maximum(rms, 1e-10))
    return db, sr, n / sr


def seuil_adaptatif(db):
    """Entre le plancher de bruit et le niveau de parole, biaise vers le bas.
    Sur un rush iPhone typique (plancher -55, p95 -15) ca tombe vers -41 dBFS,
    soit le -40 dBFS de CLAUDE.md — mais ca s'adapte a un rush de voiture bruyant."""
    import numpy as np
    plancher = float(np.percentile(db, 5))
    parole = float(np.percentile(db, 95))
    s = plancher + 0.35 * (parole - plancher)
    s = min(s, parole - 18.0)          # jamais si haut qu'on couperait dans la parole
    s = max(s, plancher + 4.0)         # jamais noye dans le bruit de fond
    return round(s, 1), round(plancher, 1), round(parole, 1)


def trouver_silences(db, pas, seuil, mini):
    """Plages continues sous le seuil, d'au moins `mini` secondes."""
    import numpy as np
    bas = db < seuil
    sil, i, n = [], 0, len(bas)
    while i < n:
        if bas[i]:
            j = i
            while j < n and bas[j]:
                j += 1
            d = (j - i) * pas
            if d >= mini:
                sil.append({"debut": round(i * pas, 3), "fin": round(j * pas, 3), "duree": round(d, 3),
                            "niveau_db": round(float(np.mean(db[i:j])), 1)})
            i = j
        else:
            i += 1
    return sil


def niveau_a(db, pas, t):
    """Niveau moyen mesure autour d'un instant — pour verifier un raccord."""
    import numpy as np
    i0 = max(0, int((t - FENETRE_RACCORD_S) / pas))
    i1 = min(len(db), int((t + FENETRE_RACCORD_S) / pas) + 1)
    if i1 <= i0:
        return None
    return round(float(np.mean(db[i0:i1])), 1)


def construire_segments(sil, duree, marge, blanc_long):
    """Les segments a garder = ce qui reste entre les silences coupables.
    Un blanc >= blanc_long n'est PAS coupe : il est garde et signale."""
    coupables = [s for s in sil if s["duree"] < blanc_long]
    longs = [s for s in sil if s["duree"] >= blanc_long]
    segs, t = [], 0.0
    for s in coupables:
        # on entre dans le silence de `marge`, sans jamais depasser sa moitie
        m = min(marge, s["duree"] / 2 - 0.01)
        a, b = t, s["debut"] + max(m, 0.0)
        if b - a > 0.15:
            segs.append([round(a, 2), round(b, 2)])
        t = s["fin"] - max(m, 0.0)
    if duree - t > 0.15:
        segs.append([round(t, 2), round(duree, 2)])
    return segs, longs, coupables


# ---------------------------------------------------------------- reprises

def _norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9 ]", " ", s).split()


def trouver_reprises(tr_path, sil, mini_mots=4):
    """Une reprise = la MEME suite de >= mini_mots mots, dite deux fois de suite.
    On ne la signale que si un silence mesure l'encadre : sans silence autour,
    elle n'est pas coupable proprement (CLAUDE.md §2 bis, regle 3)."""
    d = json.load(open(tr_path, encoding="utf-8"))
    mots = [w for s in d.get("segments", []) for w in s.get("words", [])]
    if not mots:
        return []
    toks = [(_norm(w["w"])[:1] or [""])[0] for w in mots]
    trouvees, i = [], 0
    while i < len(toks) - 2 * mini_mots:
        best = 0
        for L in range(min(14, (len(toks) - i) // 2), mini_mots - 1, -1):
            if toks[i:i + L] == toks[i + L:i + 2 * L] and all(toks[i:i + L]):
                best = L; break
        if best:
            a, b = mots[i]["start"], mots[i + best - 1]["end"]
            enc = any(s["fin"] >= b - 0.35 and s["debut"] <= b + 0.6 for s in sil)
            trouvees.append({"debut": round(a, 2), "fin": round(b, 2),
                             "texte": " ".join(w["w"].strip() for w in mots[i:i + best]),
                             "silence_apres": enc})
            i += best
        else:
            i += 1
    return trouvees


# ---------------------------------------------------------------- rapport

def ecrire_rapport(out, src, fiche, alertes, stats, sil, segs, longs, reprises, db, pas, args):
    L = []; P = L.append
    P(f"# PROPOSITION DE DÉRUSH — `{fiche['fichier']}`")
    P("")
    P("> Mesuré, pas deviné. Rien n'est coupé par cet outil : ce qui suit est une **proposition**")
    P("> à valider contre la chaîne de sens (`CLAUDE.md` §2 bis) avant d'encoder quoi que ce soit.")
    P("")
    P("## 1. Fiche captation")
    P("")
    P("| | |")
    P("| :--- | :--- |")
    P(f"| Durée | {fiche['duree_s']} s |")
    P(f"| Image | {fiche.get('affichage','?')} · {fiche['codec_video']} · {fiche['cadence']} im/s · {fiche['taille_Mo']} Mo"
      + (f" · {fiche['debit_Mbs']} Mb/s |" if fiche['debit_Mbs'] else " |"))
    P(f"| Couleur | {fiche['pix_fmt']} · plage `{fiche['plage_couleur']}` · espace `{fiche['espace_couleur']}` |")
    P(f"| Son | {fiche['codec_audio']} · {fiche['audio_hz']} Hz · {fiche['audio_canaux']} canal(aux) · décalage {fiche['decalage_audio_s']} s |")
    P("")
    if alertes:
        P("**À dire à Nabil avant de monter :**")
        P("")
        for a in alertes:
            P(f"- {a}")
        P("")
    else:
        P("Aucune alerte de captation. ✅")
        P("")

    P("## 2. Ce que l'enveloppe mesure")
    P("")
    P(f"Blocs de {int(BLOC_S*1000)} ms, mono, passe-haut 80 Hz — même extraction que `ecoute-video.py`.")
    P("")
    P("| | |")
    P("| :--- | :--- |")
    P(f"| Plancher de bruit (p5) | **{stats['plancher']} dBFS** |")
    P(f"| Niveau de parole (p95) | **{stats['parole']} dBFS** |")
    P(f"| Écart parole / bruit | {round(stats['parole']-stats['plancher'],1)} dB"
      + (" — **faible, les bornes de silence sont incertaines**" if stats['parole']-stats['plancher'] < 30 else "") + " |")
    P(f"| Seuil de silence retenu | **{stats['seuil']} dBFS** ({'imposé' if args.seuil_db is not None else 'adaptatif'}) |")
    P(f"| Silences ≥ {args.silence_min} s | {len(sil)} |")
    P("")

    P("## 3. Proposition de coupes")
    P("")
    garde = sum(b - a for a, b in segs)
    P(f"**{len(segs)} segments gardés · {garde:.1f} s sur {fiche['duree_s']} s "
      f"· {100*(1-garde/max(fiche['duree_s'],0.01)):.0f} % jeté.**")
    P("")
    P("| # | garder | durée | niveau au raccord d'entrée | au raccord de sortie |")
    P("| ---: | :--- | ---: | :--- | :--- |")
    for i, (a, b) in enumerate(segs, 1):
        # debut du 1er segment et fin du dernier = bornes du fichier, pas des raccords
        na = None if i == 1 else niveau_a(db, pas, a)
        nb = None if i == len(segs) else niveau_a(db, pas, b)
        fa = "— début du rush" if na is None else (f"{na} dBFS ✅ silence" if na < stats["seuil"] else f"{na} dBFS ⚠️ PAS un silence")
        fb = "— fin du rush" if nb is None else (f"{nb} dBFS ✅ silence" if nb < stats["seuil"] else f"{nb} dBFS ⚠️ PAS un silence")
        P(f"| {i} | `{a:.2f}-{b:.2f}` | {b-a:.2f} s | {fa} | {fb} |")
    P("")
    P("Ligne prête pour `monter.py` :")
    P("")
    P("```bash")
    P(f"python3 outils/monter.py {src} -o MONTAGE.mp4 \\")
    P("    --garder " + " ".join(f"{a:.2f}-{b:.2f}" for a, b in segs))
    P("```")
    P("")

    mauvais = [i for i, (a, b) in enumerate(segs, 1)
               if any(n is not None and n >= stats["seuil"] for n in
                      ((None if i == 1 else niveau_a(db, pas, a)),
                       (None if i == len(segs) else niveau_a(db, pas, b))))]
    if mauvais:
        P(f"> ⚠️ **Raccords {', '.join(map(str, mauvais))} : le niveau mesuré au point de coupe est au-dessus du seuil.**")
        P("> C'est une coupe en pleine queue de mot. Repousser la borne dans le silence qui suit")
        P("> avant d'encoder (CLAUDE.md §2 ter, règle 4).")
        P("")

    P("## 4. Ce que l'outil REFUSE de couper tout seul")
    P("")
    if longs:
        P(f"**{len(longs)} blanc(s) ≥ {args.blanc_long} s — gardés entiers, à trancher par Nabil.**")
        P("")
        P("Un blanc long n'est pas forcément un temps mort : il porte parfois une information.")
        P("Le 14/09 sur la tier list foot, 3,72 s ramenés à 0,22 s faisaient croire à un effet")
        P("préparé qui n'avait pas eu lieu. Avant de resserrer, se demander ce que le blanc sépare —")
        P("surtout entre deux locuteurs, où la simultanéité se lit comme une intention.")
        P("")
        P("| blanc | durée | niveau |")
        P("| :--- | ---: | ---: |")
        for s in longs:
            P(f"| `{s['debut']:.2f}-{s['fin']:.2f}` | {s['duree']:.2f} s | {s['niveau_db']} dBFS |")
        P("")
    else:
        P(f"Aucun blanc ≥ {args.blanc_long} s. ✅")
        P("")

    if reprises:
        cb = [r for r in reprises if r["silence_apres"]]
        P(f"**{len(reprises)} redite(s) détectée(s) à la transcription, dont {len(cb)} entourée(s) d'un silence mesuré.**")
        P("")
        P("| passage | texte répété | coupable proprement ? |")
        P("| :--- | :--- | :--- |")
        for r in reprises:
            P(f"| `{r['debut']:.2f}-{r['fin']:.2f}` | « {r['texte']} » | "
              + ("oui — silence mesuré après" if r["silence_apres"] else "**non** — pas de silence autour, on garde") + " |")
        P("")
        P("> Une redite ne se coupe que si un silence réel l'encadre. Et **jamais un maillon entier**")
        P("> de la chaîne de sens : on coupe DANS les maillons (CLAUDE.md §2 bis).")
        P("")
    else:
        P("Redites : " + ("aucune trouvée à la transcription." if _args_tr(args) else
                          "non cherchées — relancer avec `--transcription <prefixe>_mots.json`.") )
        P("")

    P("## 5. Avant d'encoder — les trois gestes qui ne se sautent pas")
    P("")
    P("1. **Écrire la chaîne de sens** et la faire valider par Nabil : qui est le personnage → ce qu'il")
    P("   fait → ce que Nabil fait face à lui → l'escalade → la chute. Un maillon coupé casse la vanne.")
    P("2. **Vérifier que la première image gardée est nette** — sur TikTok, c'est la vignette.")
    P("3. **Relire la transcription du montage.** Si elle ne tient pas debout toute seule à la lecture,")
    P("   le montage est faux, quels que soient les chiffres.")
    P("")

    chemin = os.path.join(out, "PROPOSITION-DERUSH.md")
    open(chemin, "w", encoding="utf-8").write("\n".join(L) + "\n")
    return chemin


def _args_tr(a):
    return getattr(a, "transcription", None)


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fichier")
    p.add_argument("-o", "--sortie", default="derush", help="dossier de sortie (défaut : derush/)")
    p.add_argument("--transcription", metavar="MOTS.json",
                   help="sortie <prefixe>_mots.json d'ecoute-video.py, pour chercher les redites")
    p.add_argument("--silence-min", type=float, default=0.35, metavar="S",
                   help="durée minimale d'un silence coupable (défaut 0,35 s ; jamais sous 0,10 s)")
    p.add_argument("--marge", type=float, default=0.12, metavar="S",
                   help="marge gardée de chaque côté de la parole (défaut 0,12 s — ne pas couper un plosif)")
    p.add_argument("--seuil-db", type=float, default=None, metavar="dBFS",
                   help="seuil de silence imposé (défaut : adaptatif, mesuré sur ce rush)")
    p.add_argument("--blanc-long", type=float, default=1.5, metavar="S",
                   help="au-delà, un blanc est gardé entier et signalé (défaut 1,5 s)")
    a = p.parse_args()

    if not os.path.exists(a.fichier):
        die(f"fichier introuvable : {a.fichier}")
    for exe in ("ffmpeg", "ffprobe"):
        if not subprocess.run(["which", exe], capture_output=True).stdout.strip():
            die(f"{exe} absent (apt-get install ffmpeg)")
    if a.silence_min < 0.10:
        die("--silence-min sous 0,10 s : en dessous ce n'est pas un silence, c'est une occlusive "
            "au milieu d'un mot (CLAUDE.md §2 bis)")
    os.makedirs(a.sortie, exist_ok=True)

    print(f"→ fiche captation…")
    fiche = sonder(a.fichier)
    alertes = alertes_captation(fiche)
    print(f"  {fiche.get('affichage','?')} · {fiche['codec_video']} · {fiche['duree_s']} s · {fiche['taille_Mo']} Mo")
    for al in alertes:
        print(f"  ⚠️  {al}")

    print("→ enveloppe…")
    wav = extraire_wav(a.fichier, a.sortie)
    db, sr, pas = enveloppe(wav)
    s_auto, plancher, parole = seuil_adaptatif(db)
    seuil = a.seuil_db if a.seuil_db is not None else s_auto
    stats = {"seuil": seuil, "plancher": plancher, "parole": parole}
    print(f"  plancher {plancher} dBFS · parole {parole} dBFS · seuil {seuil} dBFS")
    if parole - plancher < 30:
        print(f"  ⚠️  écart parole/bruit de {parole-plancher:.1f} dB seulement : bornes incertaines")

    sil = trouver_silences(db, pas, seuil, a.silence_min)
    duree_wav = len(db) * pas
    segs, longs, coupables = construire_segments(sil, duree_wav, a.marge, a.blanc_long)
    print(f"  {len(sil)} silences ≥ {a.silence_min} s ({len(coupables)} coupables, {len(longs)} blancs longs gardés)")

    reprises = []
    if a.transcription:
        if not os.path.exists(a.transcription):
            die(f"transcription introuvable : {a.transcription}")
        print("→ redites…")
        reprises = trouver_reprises(a.transcription, sil)
        print(f"  {len(reprises)} redite(s), dont {sum(1 for r in reprises if r['silence_apres'])} coupable(s) proprement")

    garde = sum(b - a_ for a_, b in segs)
    chemin = ecrire_rapport(a.sortie, a.fichier, fiche, alertes, stats, sil, segs, longs, reprises, db, pas, a)

    json.dump({"fiche": fiche, "seuil_db": seuil, "plancher_db": plancher, "parole_db": parole,
               "silences": sil, "blancs_longs": longs, "segments": segs, "redites": reprises},
              open(os.path.join(a.sortie, "derush.json"), "w"), ensure_ascii=False, indent=1)

    print()
    print(f"✅ {len(segs)} segments · {garde:.1f} s gardées sur {fiche['duree_s']} s "
          f"({100*(1-garde/max(fiche['duree_s'],0.01)):.0f} % jeté)")
    print(f"   → {chemin}  ← À LIRE, ce n'est qu'une proposition")
    print()
    print("   --garder " + " ".join(f"{x:.2f}-{y:.2f}" for x, y in segs))


if __name__ == "__main__":
    main()
