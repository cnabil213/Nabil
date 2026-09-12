#!/usr/bin/env python3
"""FUSION : mots (turbo) + Praat (prosodie.py) + arousal (audeering) + fiche captation -> RAPPORT-ECOUTE.md, mesures.json, arousal.png, profil.
Phrases = decoupage ACOUSTIQUE de chute.py (silence >= 0,30 s ou ponctuation), jamais les bornes whisper seules.
Verdict par phrase (seuils rapport.py) : ENVOYEE si p90 >= precedente +2 dB ou pic F0 >= +3 st ; PLATE si <= -3 dB et pic F0 < +1,5 st.
Arousal : relatif a la MEDIANE des fenetres de parole (>= 50 % couvertes par des mots) ; fenetres sans parole ignorees (le modele lit ~0,45 sur du silence)."""
import os, sys, json, time, datetime
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chute

def verdict_f0(sd): return "MONOTONE" if sd < 0.8 else ("peu varié" if sd < 1.5 else ("normal" if sd < 2.6 else "VARIÉ/expressif"))  # memes seuils que rapport.py
def verdict_debit(r): return "LENT" if r < 3.5 else ("RAPIDE" if r > 5.5 else "normal")
SEUILS = {"envoyee_db": 2.0, "envoyee_f0_st": 3.0, "plate_db": -3.0, "plate_f0_st": 1.5, "arousal_bas_pct": -20, "arousal_haut_pct": 30}

def _f(x, fmt="{:.1f}", u=""):
    return "—" if x is None else (fmt.format(x) + u)

def couverture(words, t0, t1):
    tot = 0.0
    for w in words:
        a, b = max(t0, w["start"]), min(t1, w["end"])
        if b > a: tot += b - a
    return tot / max(1e-6, t1 - t0)

def arousal_norm(aud, words):
    if not aud: return None
    win = aud.get("models", {}).get("audeering"); rms = aud.get("rms", [])
    if not win: return None
    for w, r in zip(win, rms):
        w["parole_pct"] = round(100 * couverture(words, w["t0"], w["t1"]))
        w["rms_db"] = r["rms_db"]
    parole = [w for w in win if w["parole_pct"] >= 50]
    if len(parole) < 2: return {"fenetres": win, "mediane": None, "creux": [], "pics": []}
    med = float(np.median([w["arousal"] for w in parole]))
    for w in win:
        w["pct_vs_mediane"] = None if w["parole_pct"] < 50 else round(100 * (w["arousal"] - med) / med)
    def zones(pred):
        out = []
        for w in win:
            if w["pct_vs_mediane"] is not None and pred(w["pct_vs_mediane"]):
                if out and w["t0"] <= out[-1]["fin"]: out[-1]["fin"] = w["t1"]; out[-1]["vals"].append(w["pct_vs_mediane"])
                else: out.append({"debut": w["t0"], "fin": w["t1"], "vals": [w["pct_vs_mediane"]]})
        for z in out: z["pct_moy"] = round(float(np.mean(z.pop("vals")))); z["duree"] = round(z["fin"] - z["debut"], 1)
        return [z for z in out if z["duree"] >= 2.0]
    return {"fenetres": win, "mediane": round(med, 3), "creux": zones(lambda p: p <= SEUILS["arousal_bas_pct"]), "pics": zones(lambda p: p >= SEUILS["arousal_haut_pct"])}

def verdicts(phrases):
    prev = None
    for p in phrases:
        if prev is None or p["int_p90_dbfs"] is None or prev["int_p90_dbfs"] is None: p["verdict"] = "ouverture"
        else:
            dI = p["int_p90_dbfs"] - prev["int_p90_dbfs"]; dF = (p["f0_pic_st"] or 0) - (prev["f0_pic_st"] or 0)
            if dI >= SEUILS["envoyee_db"] or dF >= SEUILS["envoyee_f0_st"]: p["verdict"] = "ENVOYÉE"
            elif dI <= SEUILS["plate_db"] and dF < SEUILS["plate_f0_st"]: p["verdict"] = "PLATE"
            else: p["verdict"] = "normale"
        prev = p
    return phrases

def ligne(p, med_ar):
    ar = "" if p.get("arousal") is None or not med_ar else f" · arousal {100*(p['arousal']-med_ar)/med_ar:+.0f} %"
    dI = "" if p.get("d_db") is None else f" ({p['d_db']:+.1f} vs précédente)"
    mots_s = p["n_mots"] / max(0.05, p["duree_s"])
    return (f"[{p['debut']:.1f}–{p['fin']:.1f} s] « {p['texte']} » — {_f(p['int_p90_dbfs'])} dBFS-RMS{dI} · {mots_s:.1f} mots/s · "
            f"F0 étendue {_f(p['f0_etendue_st'])} st{ar} → {p['verdict']}" + (f" · chute {p['score_chute']:.0f}/100" if p["score_chute"] >= 60 else ""))

def tracer_arousal(A, out_png, dur):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    win = A["fenetres"]; tc = [(w["t0"] + w["t1"]) / 2 for w in win]
    fig, ax = plt.subplots(figsize=(15, 3.6), dpi=100); fig.subplots_adjust(left=0.05, right=0.99, top=0.88, bottom=0.16)
    ar = [w["arousal"] for w in win]; ok = [w["parole_pct"] >= 50 for w in win]
    ax.plot(tc, ar, "-", color="#bbb", lw=0.8)
    ax.plot([t for t, o in zip(tc, ok) if o], [a for a, o in zip(ar, ok) if o], "o", color="#d62728", ms=4, label="arousal (fenêtre 2 s, parole)")
    ax.plot([t for t, o in zip(tc, ok) if not o], [a for a, o in zip(ar, ok) if not o], "x", color="#999", ms=4, label="fenêtre sans parole (ignorée)")
    if A["mediane"]:
        ax.axhline(A["mediane"], color="#333", ls=":", lw=0.8, label=f"médiane parole {A['mediane']:.2f}")
        ax.axhline(A["mediane"] * 0.8, color="#1f77b4", ls="--", lw=0.6, label="−20 % (creux)"); ax.axhline(A["mediane"] * 1.3, color="#2ca02c", ls="--", lw=0.6, label="+30 % (pic)")
    for z in A["creux"]: ax.axvspan(z["debut"], z["fin"], color="#1f77b4", alpha=0.15)
    for z in A["pics"]: ax.axvspan(z["debut"], z["fin"], color="#2ca02c", alpha=0.15)
    ax.set_xlim(0, dur); ax.set_ylim(0, 1); ax.set_xlabel("temps (s)"); ax.set_ylabel("arousal audeering"); ax.grid(alpha=0.3)
    ax.set_title("ÉNERGIE D'ARTICULATION (arousal, insensible au volume — mesure débit/prosodie) : bleu = creux, vert = pic", fontsize=10); ax.legend(loc="lower right", fontsize=7, ncol=5)
    fig.savefig(out_png); plt.close(fig)

CLES_PROFIL = ["f0_mediane_hz", "f0_ecart_type_st", "int_p90_db", "syll_par_s", "arousal_med"]
def _percentiles(hist):
    out = {}
    for k in CLES_PROFIL:
        v = [h[k] for h in hist if h.get(k) is not None]
        if v: out[k] = {"n": len(v), "p25": round(float(np.percentile(v, 25)), 3), "mediane": round(float(np.median(v)), 3), "p75": round(float(np.percentile(v, 75)), 3)}
    return out

def profil_maj(chemin, g, ar_med, fichier):
    """Charge/ecrit le profil createur : historique + medianes personnelles. Retourne (profil, texte comparaison, entree).
    Cle de dedoublonnage = (nom, duree arrondie, taille en octets) : un createur qui exporte toujours « rush.mp4 » n'ecrase plus
    l'entree precedente. La comparaison « aujourd'hui vs ta mediane » se fait sur les rushs PRECEDENTS (le rush courant n'est pas
    dans sa propre mediane) ; le profil ecrit contient ensuite l'historique complet."""
    prof = {"historique": []}
    if chemin and os.path.exists(chemin):
        try: prof = json.load(open(chemin))
        except Exception: prof = {"historique": []}
    try: taille = os.path.getsize(fichier)
    except OSError: taille = None
    entree = {"fichier": os.path.basename(fichier), "duree_s": round(float(g["duree_s"])), "taille_octets": taille, "date": datetime.datetime.now().isoformat(timespec="seconds"),
              "f0_mediane_hz": g["f0_mediane_hz"], "f0_ecart_type_st": g["f0_ecart_type_st"], "int_p90_db": g["int_p90_parole_db"],
              "syll_par_s": g["syll_par_s_articulation"], "arousal_med": ar_med}
    def meme(h):   # meme rush = meme nom ET meme duree ET meme taille ; une entree ancienne (sans duree/taille) est reconnue par le nom seul
        return h.get("fichier") == entree["fichier"] and (h.get("duree_s") is None or h.get("duree_s") == entree["duree_s"]) and (h.get("taille_octets") is None or h.get("taille_octets") == entree["taille_octets"])
    prev = [h for h in prof.get("historique", []) if not meme(h)]
    P_prev = _percentiles(prev); n_prev = len(prev)
    prof["historique"] = (prev + [entree])[-50:]
    prof["percentiles"] = _percentiles(prof["historique"])
    prof["n_rushes"] = len(prof["historique"]); prof["calibre"] = n_prev >= 3
    if chemin:
        json.dump(prof, open(chemin, "w"), ensure_ascii=False, indent=1)
    if not prof["calibre"]:
        txt = f"⚠️ NON CALIBRÉ : {n_prev} rush(s) précédent(s) dans le profil (il en faut ≥ 3 avant celui-ci) — seuils par défaut (calibrés sur 3 lecteurs FLEURS + espeak, pas sur ta voix)."
    else:
        lignes = []
        for k, lab, fmt in [("f0_mediane_hz", "hauteur", "{:+.0f} Hz"), ("f0_ecart_type_st", "variation F0", "{:+.2f} st"), ("int_p90_db", "volume pics", "{:+.1f} dB"), ("syll_par_s", "débit", "{:+.2f} syll/s"), ("arousal_med", "arousal", "{:+.3f}")]:
            if entree.get(k) is not None and k in P_prev: lignes.append(f"{lab} {fmt.format(entree[k] - P_prev[k]['mediane'])} vs ta médiane ({P_prev[k]['mediane']}, n={P_prev[k]['n']} rushs précédents)")
        txt = f"Profil calibré sur {n_prev} rushs précédents — aujourd'hui : " + " ; ".join(lignes)
    return prof, txt, entree

def _fusionner_proches(zs, gap=1.0):
    """fusionne les zones d'un meme type distantes de < gap s ; les autres champs viennent de la zone la plus longue."""
    out = []
    for z in sorted(zs, key=lambda z: z["debut"]):
        if out and z["debut"] <= out[-1]["fin"] + gap:
            a = out[-1]; dom = z if (z["fin"] - z["debut"]) > (a["fin"] - a["debut"]) else a
            n = dict(dom); n["debut"] = a["debut"]; n["fin"] = max(a["fin"], z["fin"]); n["duree"] = round(n["fin"] - n["debut"], 2)
            if "syllabes" in a and "syllabes" in z: n["syllabes"] = a["syllabes"] + z["syllabes"]
            out[-1] = n
        else: out.append(dict(z))
    return out
GRAVITE = {"MONOTONE": 5, "ZONE MOLLE": 4, "CHUTE D'INTONATION": 4, "NIVEAU": 4, "CREUX": 3, "ZONE LENTE": 3, "PIC": 2, "PEU VARIÉ": 2, "mot suspect": 1}
MAX_ALERTES = 10

def fusionner(wav, mots_json, mesures_json, audeering_json, captation_json, out_dir, profil=None, fichier_origine=None, temps=None, images=None, arousal_raison=None):
    t0 = time.time()
    M = json.load(open(mesures_json)); g = M["global"]
    cap = json.load(open(captation_json)) if captation_json and os.path.exists(captation_json) else None
    aud = None
    if audeering_json and os.path.exists(audeering_json):
        try: aud = json.load(open(audeering_json))
        except Exception as e: arousal_raison = arousal_raison or f"JSON arousal illisible ({e!r})"
    if aud and not aud.get("models", {}).get("audeering"):   # relecture : models vide + exit 0 -> KeyError tardif ; on explique au lieu de planter
        err = (aud.get("infos", {}).get("audeering") or {}).get("error"); arousal_raison = arousal_raison or (f"modèle audeering non chargé : {err}" if err else "modèle audeering non chargé"); aud = None
    if aud is None and not arousal_raison: arousal_raison = "étape arousal sautée (--sans-arousal ou venv introuvable, voir README §3)"
    words = chute.load_words(mots_json)
    Wraw = json.load(open(mots_json)); tous = [w for s in Wraw["segments"] for w in s["words"]]
    suspects = [w for w in tous if w.get("p", 1) < 0.5]
    phrases, A = chute.analyser(wav, mots_json, audeering_json if aud else None)
    for p in phrases: p["n_mots"] = len([w for w in words if p["debut"] - 0.01 <= w["start"] <= p["fin"] + 0.01])
    verdicts(phrases)
    AR = arousal_norm(aud, words); med_ar = AR["mediane"] if AR else None
    dur = g["duree_s"]
    if AR and AR["fenetres"]: tracer_arousal(AR, os.path.join(out_dir, "arousal.png"), dur)
    prof, prof_txt, entree = profil_maj(profil, g, med_ar, fichier_origine or wav)
    # ---------- RAPPORT ----------
    L = []; P = L.append
    nom = os.path.basename(fichier_origine or wav)
    P(f"# RAPPORT D'ÉCOUTE — {nom} — {dur:.1f} s"); P("")
    P(f"_Généré le {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} · échelle de volume unique : dBFS RMS (0 = pleine échelle), true peak en dBTP, loudness en LUFS · Claude ne lit que ce rapport + les PNG._"); P("")
    P(f"**Profil créateur** : {prof_txt}"); P("")
    # 1 captation
    P("## 1. Fiche captation (mesurée sur le fichier d'origine)")
    if cap:
        import captation as C
        P(C.markdown(cap).split("\n", 2)[2])
        v = cap["verdicts"]; P(""); P("**En clair** : " + " · ".join(f"{v[k]['icone']} {v[k]['texte']}" for k in ("saturation", "loudness", "bruit", "dynamique", "silences")))
    else: P("_fiche captation indisponible_")
    if g.get("bruit_fort"): P(f"\n🟡 **Bruit de fond fort** (pics {g['pics_p99_db']} vs plancher {g['plancher_p5_db']} dBFS, < 30 dB d'écart) : pauses, débit et HNR incertains.")
    if g.get("clippe"): P("\n🟡 **Dynamique compressée / écrêtée** : la zone molle est cherchée à −4 dB au lieu de −5 (sous-estimée sinon).")
    P("")
    # 2 carte d'identité
    P("## 2. Carte d'identité vocale (Praat)")
    P(f"- **Hauteur** : F0 médiane {g['f0_mediane_hz']} Hz, plage habituelle {g['f0_p5_p95_hz'][0]}–{g['f0_p5_p95_hz'][1]} Hz, écart-type {g['f0_ecart_type_st']} demi-tons → **{verdict_f0(g['f0_ecart_type_st'])}** (monotone < 0,8 · peu varié < 1,5 · normal < 2,6 · expressif ≥ 2,6)")
    P(f"- **Volume** : pics (p90 parole) {g['int_p90_parole_db']} dBFS-RMS, moyenne parole {g['int_moy_parole_db']} dBFS-RMS")
    P(f"- **Débit** : {g['syll_par_s_articulation']} syll/s hors pauses (**{verdict_debit(g['syll_par_s_articulation'])}**), {g['mots_par_s']} mots/s, parole {g['part_parole_pct']:.0f} % du temps")
    pm = g.get("pause_max")
    P(f"- **Pauses** : {g['pauses_n']} pauses ≥ 0,15 s, total {g['pauses_total_s']} s" + (f", la plus longue {pm['duree']} s à {pm['debut']} s" if pm else ""))
    P(f"- **Timbre** : jitter {g['jitter_local_pct']} %, shimmer {g['shimmer_local_pct']} %, HNR {g['hnr_db']} dB (indicatif ; le jitter baisse aussi quand l'intonation est plate)")
    if med_ar is not None: P(f"- **Énergie d'articulation** (arousal audeering, médiane des fenêtres de parole) : {med_ar:.3f} — à lire en relatif seulement")
    elif AR is not None: P("- **Énergie d'articulation** (arousal) : **non calculée** — moins de 2 fenêtres de 2 s avec ≥ 50 % de parole (clip trop court ou sans parole)")
    else: P(f"- **Énergie d'articulation** (arousal) : **non calculée** — {arousal_raison} → pas d'arousal.png, pas d'alertes creux/pics, score de chute sans arousal")
    loc = g.get("seuil_silence_local_min_max_db")
    if loc: P(f"- **Seuil parole/silence** : local (fenêtre 10 s) {loc[0]}…{loc[1]} dBFS, global {g['seuil_silence_db']} dBFS (plancher {g['plancher_p5_db']}, pics {g['pics_p99_db']})")
    P("")
    # 3 ligne de temps
    P("## 3. Ligne de temps par phrase (découpage acoustique : silence ≥ 0,30 s ou ponctuation)")
    P("_Volume = p90 des trames de parole en dBFS-RMS ; Δ vs phrase précédente ; ENVOYÉE = +2 dB ou pic F0 +3 st ; PLATE = −3 dB sans montée de F0 ; arousal en % vs médiane de la vidéo._"); P("")
    for p in phrases: P("- " + ligne(p, med_ar))
    P("")
    # 4 alertes
    P(f"## 4. Alertes horodatées (détectées par les chiffres, pas par lecture d'image ; {MAX_ALERTES} plus graves, le reste dans mesures.json → alertes_toutes)")
    al = []   # (t, type, gravite, duree, texte)
    def A(z, typ, txt): al.append((z["debut"], typ, GRAVITE[typ], z.get("duree", 0), txt))
    for z in _fusionner_proches(M["zones_molles_auto"]): A(z, "ZONE MOLLE", f"🔻 **ZONE MOLLE {z['debut']}–{z['fin']} s** ({z['duree']} s, {z['syllabes']} syll.) : pics {z['int_p90_db']} dBFS soit **{z['ecart_pics_vs_global_db']} dB** sous tes pics → tu retombes")
    for z in _fusionner_proches(M["zones_lentes_auto"]): A(z, "ZONE LENTE", f"🐢 **ZONE LENTE {z['debut']}–{z['fin']} s** ({z['duree']} s) : {z['syll_par_s_min']} syll/s hors silences = {int(100*z['ratio_vs_global'])} % de ton débit d'articulation")
    for z in _fusionner_proches(M["passages_monotones_auto"]): A(z, "MONOTONE", f"➖ **MONOTONE {z['debut']}–{z['fin']} s** ({z['duree']} s) : écart-type F0 {z['f0_ecart_type_st']} st (< 0,8) → tu parles sur une note")
    for z in _fusionner_proches(M.get("passages_peu_varies_auto", [])): A(z, "PEU VARIÉ", f"〰️ PEU VARIÉ {z['debut']}–{z['fin']} s ({z['duree']} s) : écart-type F0 {z['f0_ecart_type_st']} st (0,8–1,3)")
    for z in _fusionner_proches(M.get("chutes_intonation_auto", [])): A(z, "CHUTE D'INTONATION", f"📉 **CHUTE D'INTONATION {z['debut']}–{z['fin']} s** ({z['duree']} s) : F0 sd {z['f0_ecart_type_st']} st = moitié de ta variation habituelle ({g.get('f0_sd_mediane_fenetres_2s_st')} st)")
    if AR:
        for z in _fusionner_proches(AR["creux"]): A(z, "CREUX", f"🔋 CREUX D'ÉNERGIE {z['debut']}–{z['fin']} s ({z['duree']} s) : arousal {z['pct_moy']:+d} % vs médiane → débit/articulation qui s'affaissent")
        for z in _fusionner_proches(AR["pics"]): A(z, "PIC", f"⚡ PIC D'ÉNERGIE {z['debut']}–{z['fin']} s ({z['duree']} s) : arousal {z['pct_moy']:+d} % vs médiane")
    # niveau qui change entre fenetres de 15 s (micro qui s'eloigne, prise raccordee) : pics p90 des fenetres avec >= 20 % de parole
    zp = [z for z in M["zones"] if z.get("int_p90_db") is not None and (z.get("part_parole_pct") or 0) >= 20]
    niveau = None
    if len(zp) >= 2:
        zmin, zmax = min(zp, key=lambda z: z["int_p90_db"]), max(zp, key=lambda z: z["int_p90_db"]); ecart = round(zmax["int_p90_db"] - zmin["int_p90_db"], 1)
        if ecart >= 6:
            niveau = {"debut": zmin["debut"], "fin": zmin["fin"], "duree": zmin["duree"], "ecart_db": ecart, "fenetre_basse": zmin["zone"], "fenetre_haute": zmax["zone"], "p90_basse": zmin["int_p90_db"], "p90_haute": zmax["int_p90_db"]}
            A(niveau, "NIVEAU", f"🎚️ **NIVEAU QUI CHANGE de {ecart} dB** entre fenêtres : {zmin['zone']} pics {zmin['int_p90_db']} dBFS vs {zmax['zone']} pics {zmax['int_p90_db']} dBFS → micro qui s'éloigne / aparté / prise raccordée ? (seuil local appliqué ; pauses et débit de la fenêtre basse à vérifier)")
    for w in suspects: al.append((w["start"], "mot suspect", GRAVITE["mot suspect"], 0, f"❓ mot suspect « {w['w'].strip()} » à {w['start']:.1f} s (confiance whisper {w['p']:.2f} : mal transcrit / halluciné, PAS un indice d'articulation)"))
    garde = sorted(al, key=lambda x: (-x[2], -x[3], x[0]))[:MAX_ALERTES]
    if al:
        for x in sorted(garde, key=lambda x: x[0]): P("- " + x[4])
        if len(al) > len(garde):
            reste = {}
            for x in al:
                if x not in garde: reste[x[1]] = reste.get(x[1], 0) + 1
            P(f"- … + {len(al) - len(garde)} autre(s) alerte(s) moins grave(s) ({', '.join(f'{v} {k}' for k, v in reste.items())}) dans mesures.json")
    else: P("- aucune")
    alertes_toutes = [{"t": x[0], "type": x[1], "gravite": x[2], "duree": x[3], "texte": x[4], "dans_rapport": x in garde} for x in sorted(al, key=lambda x: x[0])]
    P("")
    # 5 top
    notees = [p for p in phrases if p["verdict"] != "ouverture"]
    P("## 5. Top phrases")
    env = sorted([p for p in notees if p["d_db"] is not None], key=lambda p: -p["d_db"])[:5]
    pla = sorted([p for p in notees if p["d_db"] is not None], key=lambda p: p["d_db"])[:5]
    P("**Les plus envoyées (Δ volume vs précédente)** :")
    for p in env: P(f"- [{p['debut']:.1f}–{p['fin']:.1f} s] « {p['texte'][:80]} » {p['d_db']:+.1f} dB, F0 étendue {_f(p['f0_etendue_st'])} st → {p['verdict']}")
    P(""); P("**Les plus plates** :")
    for p in pla: P(f"- [{p['debut']:.1f}–{p['fin']:.1f} s] « {p['texte'][:80]} » {p['d_db']:+.1f} dB, F0 étendue {_f(p['f0_etendue_st'])} st → {p['verdict']}")
    P(""); P("**Meilleures chutes (score 0–100 = contraste 50 + pause avant 25 + netteté après 25)** :")
    for p in sorted(phrases, key=lambda p: -p["score_chute"])[:3]:
        P(f"- [{p['debut']:.1f}–{p['fin']:.1f} s] « {p['texte'][:80]} » **{p['score_chute']:.0f}/100** — pause avant {_f(p['pause_avant_s'], '{:.2f}', ' s')}, {p['apres']}" + (f" ({p['silence_apres_s']:.2f} s)" if p["silence_apres_s"] is not None else ""))
    P("")
    # 6 mots
    P("## 6. Mots appuyés / plats (Praat : pic de volume + pic de hauteur)")
    P("- **appuyés** : " + " ; ".join(f"« {w['mot']} » @{w['debut']} s ({w['int_max_db']} dBFS, F0 pic {w['f0_max_st']} st)" for w in M["mots_les_plus_accentues"][:6]))
    P("- **plats** : " + " ; ".join(f"« {w['mot']} » @{w['debut']} s ({w['int_max_db']} dBFS, F0 pic {w['f0_max_st']} st)" for w in M["mots_les_plus_plats"][:4]))
    P("- **avalés / mal transcrits** (confiance whisper < 0,5) : " + (" ; ".join(f"« {w['w'].strip()} » @{w['start']:.1f} s (p={w['p']:.2f})" for w in suspects) if suspects else "aucun — attention, ce n'est pas un détecteur d'articulation (rappel 8 % mesuré)"))
    P("")
    # 7 pauses avant chutes
    P("## 7. Pauses avant chutes (timing)")
    pc = [p for p in phrases if p["pause_avant_s"] is not None and p["pause_avant_s"] >= 0.4]
    if pc:
        for p in pc: P(f"- pause {p['pause_avant_s']:.2f} s puis « {p['texte'][:60]} » ({p['verdict']}, {_f(p['d_db'], '{:+.1f}', ' dB')}, chute {p['score_chute']:.0f}/100) — {p['apres']}")
    else: P("- aucune pause ≥ 0,4 s avant une phrase")
    P("")
    # 8 fenêtres 15 s
    P("## 8. Fenêtres de 15 s (Praat)")
    P("| fenêtre | F0 moy Hz | F0 sd st | pics p90 dBFS | syll/s artic. | parole % | pauses s | partition |"); P("| :-- | --: | --: | --: | --: | --: | --: | :-- |")
    for k, z in enumerate(M["zones"]):
        img = images[k] if images and k < len(images) else None
        P(f"| {z['zone']} | {_f(z['f0_moy_hz'])} | {_f(z['f0_ecart_type_st'], '{:.2f}')} | {_f(z['int_p90_db'])} | {_f(z['syll_par_s_articulation'], '{:.2f}')} | {z['part_parole_pct']:.0f} | {z['pauses_s']} | {os.path.basename(img) if img else '—'} |")
    P("")
    P("## 9. Fichiers"); 
    for im in (images or []): P(f"- `{os.path.basename(im)}` — partition F0 + intensité + mots (lire APRÈS les chiffres : sert à décrire, pas à découvrir)")
    if AR: P("- `arousal.png` — énergie d'articulation par fenêtre de 2 s")
    else: P(f"- **arousal non calculé** : {arousal_raison}")
    P("- `RAPPORT-PROSODIE.txt` — rapport Praat détaillé (rapport.py) ; `mesures.json` — tout en chiffres")
    if temps: P("- temps par étape (s, machine partagée) : " + ", ".join(f"{k} {v}" for k, v in temps.items()))
    P(""); P("_Limites : seuils calibrés sur 3 lecteurs FLEURS + espeak, pas sur ta voix ; un seul locuteur ; euh / faux départs invisibles ; audeering = licence CC-BY-NC-SA 4.0 (usage non commercial)._")
    md = "\n".join(L) + "\n"
    open(os.path.join(out_dir, "RAPPORT-ECOUTE.md"), "w", encoding="utf-8").write(md)
    out = {"fichier": fichier_origine or wav, "captation": cap, "prosodie_global": g, "zones_15s": M["zones"], "alertes": {"molles": M["zones_molles_auto"], "lentes": M["zones_lentes_auto"], "monotones": M["passages_monotones_auto"],
           "peu_varies": M.get("passages_peu_varies_auto", []), "chutes_intonation": M.get("chutes_intonation_auto", []), "arousal_creux": AR["creux"] if AR else None, "arousal_pics": AR["pics"] if AR else None, "niveau_change": niveau},
           "alertes_toutes": alertes_toutes, "arousal_raison": arousal_raison,
           "phrases": phrases, "arousal": AR, "mots_suspects": suspects, "mots_appuyes": M["mots_les_plus_accentues"], "mots_plats": M["mots_les_plus_plats"], "pauses": M["pauses"],
           "profil_entree": entree, "profil_calibre": prof["calibre"], "temps_s": temps, "seuils": SEUILS, "temps_fusion_s": round(time.time() - t0, 2)}
    json.dump(out, open(os.path.join(out_dir, "mesures.json"), "w"), ensure_ascii=False, indent=1)
    return md

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("wav"); ap.add_argument("mots"); ap.add_argument("mesures"); ap.add_argument("--audeering"); ap.add_argument("--captation"); ap.add_argument("-o", default="."); ap.add_argument("--profil")
    a = ap.parse_args(); print(fusionner(a.wav, a.mots, a.mesures, a.audeering, a.captation, a.o, a.profil))
