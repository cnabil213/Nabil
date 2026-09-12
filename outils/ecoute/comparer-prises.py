#!/usr/bin/env python3
"""COMPARAISON DE DEUX PRISES du même texte : comparer-prises.py A.wav B.wav [--phrase "texte de la chute"] [--arousal] [--json out.json]
1. transcription faster-whisper large-v3-turbo (int8, CPU ; cache ~/.cache/ecoute-prises/<nom>_<taille>_<date>_turbo_mots.json)
2. alignement mot à mot (difflib sur mots normalisés) -> similarité, mots qui diffèrent
3. mesures globales (chute.py) : durée parlée, p90 dBFS, débit syll/s, étendue F0 st, arousal (optionnel, audeering via le venv mesures-emotion)
4. chute = --phrase (meilleure correspondance floue dans chaque prise) ou, par défaut, la DERNIÈRE phrase ; score chute de chute.py
5. rapport de diff : plus forte / plus rapide / plus vivante / pause avant la chute plus nette / plus courte / chute mieux envoyée ; verdict + confiance.
VERDICT (poids documentés) : marge = 0.40*Δscore_chute/20 + 0.20*ΔdB/6 + 0.20*ΔF0étendue/3 + 0.10*Δsyll/s/1 + 0.10*(−Δdurée %)/20, chaque terme borné à ±1.
   marge > 0 -> A ; confiance = 50 + 100*|marge| + 10*(critères pour − critères contre), bornée 50-98 %.
   Seuils pour déclarer un critère : dB 1,5 ; syll/s 0,3 ; F0 1,0 st ; pause 0,15 s ; durée 5 % ; score chute 5 pts."""
import sys, os, json, time, argparse, difflib, re, subprocess, unicodedata
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import chute
# Cache hors du paquet (le dépôt reste propre) et clé nom + taille + date : deux exports nommés
# pareil (« rush.mp4 ») ne se contaminent pas.
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "ecoute-prises"); os.makedirs(CACHE, exist_ok=True)
def cle_cache(wav):
    st = os.stat(wav); return f"{os.path.basename(wav).rsplit('.', 1)[0]}_{st.st_size}_{int(st.st_mtime)}"
VENV = os.path.join(HERE, "..", "..", "mesures-emotion")

def transcrire(wav, model_holder, log):
    out = os.path.join(CACHE, cle_cache(wav) + "_turbo_mots.json")
    if os.path.exists(out): log.append(f"transcription {os.path.basename(wav)} : cache"); return out
    from faster_whisper import WhisperModel
    if model_holder[0] is None:
        t0 = time.time(); model_holder[0] = WhisperModel("deepdml/faster-whisper-large-v3-turbo-ct2", device="cpu", compute_type="int8", cpu_threads=4); log.append(f"chargement turbo {time.time()-t0:.1f} s")
    t1 = time.time(); segs, _ = model_holder[0].transcribe(wav, language="fr", word_timestamps=True, beam_size=5, vad_filter=False)
    res = [{"start": s.start, "end": s.end, "text": s.text, "words": [{"w": w.word, "start": w.start, "end": w.end, "p": w.probability} for w in (s.words or [])]} for s in segs]
    dt = time.time() - t1; json.dump({"wav": wav, "model": "turbo int8", "transcribe_s": dt, "segments": res}, open(out, "w"), ensure_ascii=False, indent=1)
    log.append(f"transcription {os.path.basename(wav)} : {dt:.1f} s ({sum(len(s['words']) for s in res)} mots)"); return out

def arousal_json(wav, log):
    out = os.path.join(CACHE, cle_cache(wav) + "_aud")
    if not os.path.exists(out + ".json"):
        t0 = time.time(); subprocess.run([os.path.join(VENV, "venv/bin/python"), os.path.join(VENV, "emotion_windows.py"), wav, "--models", "audeering", "--no-plot", "--out", out], check=True, capture_output=True); log.append(f"arousal {os.path.basename(wav)} : {time.time()-t0:.1f} s")
    return out + ".json"

def norm(w): return re.sub(r"[^a-z0-9']", "", unicodedata.normalize("NFKD", w.lower()).encode("ascii", "ignore").decode())

def globales(wav, phrases, A):
    import numpy as np
    sp = A["speech"]; db = A["dbfs"][sp]; st = A["ST"][~np.isnan(A["ST"])]
    d0, d1 = phrases[0]["debut"], phrases[-1]["fin"]; tpar = float(sp.sum()) * chute.TS
    ar = [p["arousal"] for p in phrases if p["arousal"] is not None]
    return dict(duree_parlee_s=round(d1 - d0, 2), duree_fichier_s=round(A["dur"], 2), p90_dbfs=round(float(np.percentile(db, 90)), 1),
                syll_par_s=round(float(((A["nuclei"] >= d0) & (A["nuclei"] < d1)).sum()) / max(0.05, tpar), 2),
                f0_etendue_st=round(float(np.percentile(st, 95) - np.percentile(st, 5)), 1), f0_sd_st=round(float(np.std(st)), 2),
                pauses_total_s=round((d1 - d0) - tpar, 2), arousal=(round(sum(ar) / len(ar), 3) if ar else None))

def choisir_chute(phrases, texte):
    if not texte: return len(phrases) - 1
    t = " ".join(norm(w) for w in texte.split())
    return max(range(len(phrases)), key=lambda i: difflib.SequenceMatcher(None, t, " ".join(norm(w) for w in phrases[i]["texte"].split())).ratio())

def comparer(A_wav, B_wav, phrase=None, arousal=False):
    log = []; holder = [None]
    mA, mB = transcrire(A_wav, holder, log), transcrire(B_wav, holder, log)
    aA = arousal_json(A_wav, log) if arousal else None; aB = arousal_json(B_wav, log) if arousal else None
    t0 = time.time(); wA, wB = chute.load_words(mA), chute.load_words(mB)
    sm = difflib.SequenceMatcher(None, [norm(w["w"]) for w in wA], [norm(w["w"]) for w in wB])
    # MÊME DÉCOUPAGE EN PHRASES pour les 2 prises : union des coupures acoustiques de A et de B, transportées par l'alignement mot à mot
    a2b, b2a = {}, {}
    for i1, j1, k in sm.get_matching_blocks():
        for q in range(k): a2b[i1 + q] = j1 + q; b2a[j1 + q] = i1 + q
    AA, AB = chute.analyse_audio(A_wav), chute.analyse_audio(B_wav)
    cutsA, cutsB = chute.coupures(wA, AA), chute.coupures(wB, AB)
    cutsA_all = cutsA | {b2a[i] for i in cutsB if i in b2a}; cutsB_all = cutsB | {a2b[i] for i in cutsA if i in a2b}
    arA = json.load(open(aA))["models"]["audeering"] if aA else None; arB = json.load(open(aB))["models"]["audeering"] if aB else None
    phA = chute.scorer([chute.mesures_phrase(AA, ph, arA) for ph in chute.segmenter(wA, AA, cuts=cutsA_all)])
    phB = chute.scorer([chute.mesures_phrase(AB, ph, arB) for ph in chute.segmenter(wB, AB, cuts=cutsB_all)])
    log.append(f"mesures Praat des 2 prises : {time.time()-t0:.1f} s ; coupures A {sorted(cutsA)} B {sorted(cutsB)} -> communes {sorted(cutsA_all)}")
    diffs = [(tag, " ".join(w["w"] for w in wA[i1:i2]), " ".join(w["w"] for w in wB[j1:j2])) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]
    gA, gB = globales(A_wav, phA, AA), globales(B_wav, phB, AB)
    iA, iB = choisir_chute(phA, phrase), choisir_chute(phB, phrase); cA, cB = phA[iA], phB[iB]
    R = {"A": A_wav, "B": B_wav, "similarite_texte_pct": round(100 * sm.ratio(), 1), "diffs_texte": diffs, "globales": {"A": gA, "B": gB}, "chute": {"A": cA, "B": cB}, "phrases": {"A": phA, "B": phB}, "log": log}
    # ---- critères
    crit = []  # (nom, gagnant, phrase explicative, contribution marge)
    def C(nom, va, vb, seuil, unit, higher_better=True, fmt=".1f", contrib=0.0):
        d = va - vb; win = None if abs(d) < seuil else ("A" if (d > 0) == higher_better else "B")
        crit.append(dict(critere=nom, A=va, B=vb, delta=round(d, 3), gagnant=win, texte=f"{nom} : A {va:{fmt}}{unit} vs B {vb:{fmt}}{unit} (Δ {d:+{fmt}}{unit}) -> " + (f"{win}" if win else "égalité"), marge=contrib))
    C("Plus forte (p90 dBFS parole)", gA["p90_dbfs"], gB["p90_dbfs"], 1.5, " dB", contrib=0.20 * chute.clip((gA["p90_dbfs"] - gB["p90_dbfs"]) / 6, -1, 1))
    C("Plus rapide (syll/s hors pauses)", gA["syll_par_s"], gB["syll_par_s"], 0.3, " syll/s", fmt=".2f", contrib=0.10 * chute.clip((gA["syll_par_s"] - gB["syll_par_s"]) / 1.0, -1, 1))
    C("Plus haute/vivante (étendue F0 p5-p95)", gA["f0_etendue_st"], gB["f0_etendue_st"], 1.0, " st", contrib=0.20 * chute.clip((gA["f0_etendue_st"] - gB["f0_etendue_st"]) / 3, -1, 1))
    if gA["arousal"] is not None and gB["arousal"] is not None: C("Plus d'énergie perçue (arousal audeering, insensible au volume)", gA["arousal"], gB["arousal"], 0.03, "", fmt=".3f")
    pa, pb = cA["pause_avant_s"] or 0.0, cB["pause_avant_s"] or 0.0
    fa, fb = chute.f_pause(pa), chute.f_pause(pb)
    win = None
    if abs(fa - fb) >= 0.1: win = "A" if fa > fb else "B"
    elif abs(pa - pb) >= 0.15 and max(pa, pb) <= 1.2: win = "A" if pa > pb else "B"
    crit.append(dict(critere="Pause avant la chute plus nette", A=pa, B=pb, delta=round(pa - pb, 2), gagnant=win, texte=f"Pause avant la chute : A {pa:.2f} s vs B {pb:.2f} s (Δ {pa-pb:+.2f} s ; idéal 0,40-1,2 s) -> " + (win or "égalité"), marge=0.0))
    C("Plus courte (durée parlée)", gA["duree_parlee_s"], gB["duree_parlee_s"], 0.05 * max(gA["duree_parlee_s"], gB["duree_parlee_s"]), " s", higher_better=False, fmt=".2f", contrib=0.10 * chute.clip(-(100 * (gA["duree_parlee_s"] - gB["duree_parlee_s"]) / max(gA["duree_parlee_s"], gB["duree_parlee_s"])) / 20, -1, 1))
    C("Chute mieux envoyée (score chute.py)", cA["score_chute"], cB["score_chute"], 5.0, "/100", contrib=0.40 * chute.clip((cA["score_chute"] - cB["score_chute"]) / 20, -1, 1))
    marge = sum(c["marge"] for c in crit); gagnant = "A" if marge > 0.02 else ("B" if marge < -0.02 else None)
    pour = sum(1 for c in crit if c["gagnant"] == gagnant); contre = sum(1 for c in crit if c["gagnant"] and c["gagnant"] != gagnant)
    conf = int(chute.clip(50 + 100 * abs(marge) + 10 * (pour - contre), 50, 98)) if gagnant else 50
    R.update(criteres=crit, marge=round(marge, 3), verdict=gagnant, confiance_pct=conf, pour=pour, contre=contre); return R

def rapport(R):
    L = []; P = L.append
    nA, nB = os.path.basename(R["A"]), os.path.basename(R["B"])
    P(f"COMPARAISON DE PRISES — A = {nA} | B = {nB}"); P("=" * 78)
    P(f"Texte : similarité {R['similarite_texte_pct']} %" + (" — mêmes mots" if not R["diffs_texte"] else " — différences : " + " ; ".join(f"[{t}] A « {a} » / B « {b} »" for t, a, b in R["diffs_texte"][:6])))
    gA, gB = R["globales"]["A"], R["globales"]["B"]
    P(f"Global A : {gA['duree_parlee_s']} s parlées, p90 {gA['p90_dbfs']} dBFS, {gA['syll_par_s']} syll/s, F0 étendue {gA['f0_etendue_st']} st (sd {gA['f0_sd_st']}), pauses {gA['pauses_total_s']} s" + (f", arousal {gA['arousal']}" if gA['arousal'] is not None else ""))
    P(f"Global B : {gB['duree_parlee_s']} s parlées, p90 {gB['p90_dbfs']} dBFS, {gB['syll_par_s']} syll/s, F0 étendue {gB['f0_etendue_st']} st (sd {gB['f0_sd_st']}), pauses {gB['pauses_total_s']} s" + (f", arousal {gB['arousal']}" if gB['arousal'] is not None else ""))
    cA, cB = R["chute"]["A"], R["chute"]["B"]
    P(f"Chute A [{cA['debut']}-{cA['fin']}] « {cA['texte'][:70]} » : score {cA['score_chute']} (contraste {cA['pts_contraste']} + pause {cA['pts_pause']} + après {cA['pts_apres']}) ; ΔdB {cA['d_db']}, p90 {cA['int_p90_dbfs']} dBFS, {cA['syll_par_s']} syll/s, F0 {cA['f0_etendue_st']} st, {cA['apres']}")
    P(f"Chute B [{cB['debut']}-{cB['fin']}] « {cB['texte'][:70]} » : score {cB['score_chute']} (contraste {cB['pts_contraste']} + pause {cB['pts_pause']} + après {cB['pts_apres']}) ; ΔdB {cB['d_db']}, p90 {cB['int_p90_dbfs']} dBFS, {cB['syll_par_s']} syll/s, F0 {cB['f0_etendue_st']} st, {cB['apres']}")
    P(""); P("CRITÈRES")
    for c in R["criteres"]: P("  - " + c["texte"])
    P("")
    v = R["verdict"]
    if v is None: P(f"VERDICT : ÉGALITÉ (marge {R['marge']:+.3f}) — aucune prise ne se détache ; confiance 50 %")
    else:
        raisons = [c["critere"].split(" (")[0].lower() for c in R["criteres"] if c["gagnant"] == v]; contre = [c["critere"].split(" (")[0].lower() for c in R["criteres"] if c["gagnant"] and c["gagnant"] != v]
        P(f"VERDICT : prise {v} ({nA if v=='A' else nB}) — confiance {R['confiance_pct']} % (marge {R['marge']:+.3f}, {R['pour']} critères pour, {R['contre']} contre)")
        P(f"   POURQUOI : {v} est " + ", ".join(raisons) + (f". Mais l'autre prise est " + ", ".join(contre) + "." if contre else "."))
    P("   (poids : score chute 40 %, volume 20 %, vivacité F0 20 %, débit 10 %, brièveté 10 % ; pause avant la chute déjà comptée dans le score chute)")
    P("   Temps : " + " ; ".join(R["log"]))
    return "\n".join(L)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("A"); ap.add_argument("B"); ap.add_argument("--phrase"); ap.add_argument("--arousal", action="store_true"); ap.add_argument("--json")
    a = ap.parse_args(); t0 = time.time()
    R = comparer(os.path.abspath(a.A), os.path.abspath(a.B), a.phrase, a.arousal); txt = rapport(R); print(txt); print(f"   Total : {time.time()-t0:.1f} s (machine partagée)")
    if a.json: json.dump(R, open(a.json, "w"), ensure_ascii=False, indent=1)
