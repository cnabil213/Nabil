#!/usr/bin/env python3
"""MÉTRIQUE DE CHUTE (timing comique) — une ligne par phrase + score 0-100 expliqué.
Usage : chute.py fichier.wav mots.json [--arousal X_audeering.json] [--t 8.6] [--json sortie.json] [--quiet]
  mots.json : format prosodie/transcribe.py ou transcribe_turbo.py (segments[].words[] {w,start,end})
  --t       : timecode (s) d'une phrase à détailler (celle qui contient t)
Phrases    : mots regroupés ; coupure quand un silence ACOUSTIQUE >= 0,30 s tombe entre deux mots, ou ponctuation finale (. ? !).
Mesures    : pause AVANT (silence acoustique juste avant le 1er mot), durée, int p90 dBFS (trames RMS 20 ms, parole seule),
             débit syll/s (noyaux = pics d'intensité voisés, hors pauses), étendue F0 p5-p95 en demi-tons, arousal (audeering, fenêtres dont le centre tombe dans la phrase),
             silence APRÈS (jusqu'à la prochaine parole ; fin de fichier = propre).
SCORE CHUTE 0-100 (poids documentés) :
  CONTRASTE vs phrase précédente : 50 pts = 50 * clip(0.4*ΔdB/6 + 0.2*ΔF0étendue/4st + 0.2*|Δsyll/s|/2 + 0.2*Δarousal/0.15, 0, 1)
      (sans arousal : 0.5*ΔdB/6 + 0.25*ΔF0/4 + 0.25*|Δsyll|/2). Signé : une chute PLUS FORTE / plus haute que ce qui précède compte, plus molle = 0.
      Limite connue : une chute volontairement chuchotée sera sous-notée.
  PAUSE AVANT : 25 pts = 25 * f(pause) ; f = 0 sous 0,15 s, monte linéairement jusqu'à 1 à 0,40 s, plateau jusqu'à 1,2 s, redescend à 0 à 2,5 s (trou = temps mort).
  NETTETÉ APRÈS : 25 pts = 25 * g(silence après) ; g = 0 sous 0,10 s (reprise immédiate = la chute est écrasée), 1 dès 0,30 s (respiration) ou fin de fichier.
  Première phrase : pas de précédente -> contraste 0 (étiquette 'ouverture').
"""
import sys, json, argparse, re, os
import numpy as np, parselmouth
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seuil import masque_parole   # MEME seuil local que prosodie.py (relecture : chute.py gardait p99-25 sans plancher ni gating)
from scipy.signal import find_peaks

TS = 0.01
W = {"contraste": 50, "pause": 25, "apres": 25}
WC = {"db": 0.4, "f0": 0.2, "syll": 0.2, "ar": 0.2}
NORM = {"db": 6.0, "f0": 4.0, "syll": 2.0, "ar": 0.15}

def clip(x, a, b): return max(a, min(b, x))
def f_pause(p):
    if p is None or p < 0.15: return 0.0
    if p < 0.40: return (p - 0.15) / 0.25
    if p <= 1.2: return 1.0
    if p < 2.5: return (2.5 - p) / 1.3
    return 0.0
def g_apres(s):
    if s is None: return 1.0  # fin de fichier
    if s < 0.10: return 0.0
    if s >= 0.30: return 1.0
    return (s - 0.10) / 0.20

def load_words(path):
    d = json.load(open(path))
    if "segments" in d:
        return [{"w": w["w"].strip(), "start": w["start"], "end": w["end"]} for s in d["segments"] for w in s["words"] if w["w"].strip()]
    return [{"w": w["word"].strip(), "start": w["start"], "end": w["end"]} for w in d["words"] if w["word"].strip()]

def analyse_audio(wav):
    snd = parselmouth.Sound(wav); dur = snd.get_total_duration()
    y = snd.values[0]; sr = int(snd.sampling_frequency)
    p0 = snd.to_pitch(time_step=TS, pitch_floor=60, pitch_ceiling=600)
    v = p0.selected_array["frequency"]; v = v[v > 0]
    q25, q75 = (np.percentile(v, [25, 75]) if len(v) else (80, 300))
    pitch = snd.to_pitch(time_step=TS, pitch_floor=max(50.0, 0.75 * q25), pitch_ceiling=min(700.0, 1.75 * q75))
    inten = snd.to_intensity(time_step=TS, minimum_pitch=75)
    grid = np.arange(0, dur, TS)
    def nearest(t_src, v_src):
        idx = np.clip(np.round((grid - t_src[0]) / TS).astype(int), 0, len(t_src) - 1)
        out = v_src[idx].astype(float); out[(grid < t_src[0] - TS) | (grid > t_src[-1] + TS)] = np.nan; return out
    F0 = nearest(pitch.xs(), pitch.selected_array["frequency"]); F0[F0 <= 0] = np.nan
    I = nearest(inten.xs(), inten.values[0])
    SP = masque_parole(I, grid, TS); speech = SP["speech"]; thr = SP["thr"]
    F0[~speech] = np.nan                       # gating : pas de F0 hors parole (comme prosodie.py)
    ST = 12 * np.log2(F0 / np.nanmedian(F0))
    # RMS dBFS par trame 20 ms centrée sur la grille
    win = int(0.02 * sr); dbfs = np.full(len(grid), np.nan)
    for k, t in enumerate(grid):
        a = int(t * sr) - win // 2; b = a + win
        seg = y[max(0, a):max(0, b)]
        if len(seg): dbfs[k] = 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1e-9)
    Ifill = np.where(np.isnan(I), np.nanmin(I), I)
    pk, _ = find_peaks(Ifill, prominence=2.0, distance=int(0.08 / TS), height=thr)
    voiced = ~np.isnan(F0)
    nuclei = np.array([grid[p] for p in pk if voiced[max(0, p - 1):p + 2].any()])
    return dict(dur=dur, grid=grid, speech=speech, ST=ST, dbfs=dbfs, nuclei=nuclei, f0med=float(np.nanmedian(F0)))

def coupures(words, A, gap=0.30):
    """indices i tels qu'on coupe entre le mot i et le mot i+1"""
    """phrases = listes de mots ; coupure si le plus long silence acoustique entre le CENTRE du mot i et max(centre du mot i+1, début i+1 + 0,30 s) borné à sa fin est >= gap
    (les bornes whisper se touchent souvent, d'où la fenêtre centre à centre), ou ponctuation finale (. ? !)."""
    speech = A["speech"]; n = len(speech)
    cuts = set()
    for i, (w0, w1) in enumerate(zip(words, words[1:])):
        a = int(clip((w0["start"] + w0["end"]) / 2, 0, A["dur"]) / TS); b = min(n, int(clip(min(w1["end"], max((w1["start"] + w1["end"]) / 2, w1["start"] + 0.30)), 0, A["dur"]) / TS) + 1)
        longest = 0; run = 0
        for s in speech[a:b]:
            run = 0 if s else run + 1; longest = max(longest, run)
        if longest * TS >= gap or re.search(r"[.?!]$", w0["w"]): cuts.add(i)
    return cuts
def segmenter(words, A, gap=0.30, cuts=None):
    cuts = coupures(words, A, gap) if cuts is None else set(cuts)
    phrases, cur = [], [words[0]]
    for i, w1 in enumerate(words[1:]):
        if i in cuts: phrases.append(cur); cur = [w1]
        else: cur.append(w1)
    phrases.append(cur); return phrases

def silence_avant(A, t):
    """silence acoustique qui précède l'attaque de la phrase (t = début whisper du 1er mot, tolérance ±0,30 s) ; None si début de fichier."""
    sp = A["speech"]; n = len(sp); i = int(clip(t, 0, A["dur"]) / TS)
    if i < n and sp[i]:  # whisper a démarré en retard : remonter jusqu'à l'attaque réelle (max 0,30 s)
        k = 0
        while i > 0 and sp[i - 1] and k < int(0.30 / TS): i -= 1; k += 1
    else:                # whisper a démarré en avance : avancer jusqu'à la 1re trame de parole
        while i < n and not sp[i]: i += 1
    j = i
    while j > 0 and not sp[j - 1]: j -= 1
    return None if j == 0 else (i - j) * TS
def silence_apres(A, t):
    """silence acoustique après la dernière trame de parole de la phrase (t = fin whisper du dernier mot, tolérance ±0,30 s) ; None si fin de fichier."""
    sp = A["speech"]; n = len(sp); i = min(n - 1, int(t / TS))
    if sp[i]:            # whisper a fini trop tôt : avancer jusqu'à la fin réelle de la parole (max 0,30 s)
        k = 0
        while i + 1 < n and sp[i + 1] and k < int(0.30 / TS): i += 1; k += 1
    else:                # whisper a fini trop tard : reculer jusqu'à la dernière trame de parole
        while i > 0 and not sp[i]: i -= 1
    j = i + 1
    while j < n and not sp[j]: j += 1
    return None if j >= n else (j - i - 1) * TS
def mesures_phrase(A, ph, arousal):
    d0, d1 = ph[0]["start"], ph[-1]["end"]
    a, b = int(d0 / TS), int(d1 / TS) + 1
    sp = A["speech"][a:b]; db = A["dbfs"][a:b][sp]; st = A["ST"][a:b]
    n_nuc = int(((A["nuclei"] >= d0) & (A["nuclei"] < d1)).sum()); t_parole = max(0.05, float(sp.sum()) * TS)
    ar = None
    if arousal:
        c = [w["arousal"] for w in arousal if d0 <= (w["t0"] + w["t1"]) / 2 < d1]
        if not c: c = [w["arousal"] for w in arousal if w["t1"] > d0 and w["t0"] < d1]
        ar = round(float(np.mean(c)), 3) if c else None
    stv = st[~np.isnan(st)]
    return dict(debut=round(d0, 2), fin=round(d1, 2), duree_s=round(d1 - d0, 2), texte=" ".join(w["w"] for w in ph).replace(" '", "'"),
                pause_avant_s=(None if (pa := silence_avant(A, d0)) is None else round(pa, 2)),
                silence_apres_s=(None if (sa := silence_apres(A, d1)) is None else round(sa, 2)),
                int_p90_dbfs=(round(float(np.percentile(db, 90)), 1) if len(db) else None),
                syll_par_s=round(n_nuc / t_parole, 2), n_syll=n_nuc,
                f0_etendue_st=(round(float(np.percentile(stv, 95) - np.percentile(stv, 5)), 1) if len(stv) > 3 else None),
                f0_pic_st=(round(float(np.percentile(stv, 95)), 1) if len(stv) > 3 else None), arousal=ar)

def scorer(phrases):
    prev = None
    for p in phrases:
        expl = []
        if prev is None or p["int_p90_dbfs"] is None or prev["int_p90_dbfs"] is None:
            p.update(d_db=None, d_f0=None, d_syll=None, d_ar=None, pts_contraste=0.0); expl.append("ouverture : pas de phrase précédente -> contraste 0")
        else:
            d_db = p["int_p90_dbfs"] - prev["int_p90_dbfs"]
            d_f0 = (p["f0_etendue_st"] or 0) - (prev["f0_etendue_st"] or 0)
            d_sy = p["syll_par_s"] - prev["syll_par_s"]
            d_ar = None if p["arousal"] is None or prev["arousal"] is None else p["arousal"] - prev["arousal"]
            if d_ar is None: wc = {"db": 0.5, "f0": 0.25, "syll": 0.25, "ar": 0.0}
            else: wc = WC
            raw = wc["db"] * clip(d_db / NORM["db"], -1, 1) + wc["f0"] * clip(d_f0 / NORM["f0"], -1, 1) + wc["syll"] * clip(abs(d_sy) / NORM["syll"], 0, 1) + (wc["ar"] * clip(d_ar / NORM["ar"], -1, 1) if d_ar is not None else 0)
            p.update(d_db=round(d_db, 1), d_f0=round(d_f0, 1), d_syll=round(d_sy, 2), d_ar=(None if d_ar is None else round(d_ar, 3)), pts_contraste=round(W["contraste"] * clip(raw, 0, 1), 1))
            expl.append(f"contraste {p['pts_contraste']}/50 : ΔdB {d_db:+.1f} (poids {wc['db']}, sat ±6), ΔF0 {d_f0:+.1f} st (poids {wc['f0']}, sat ±4), |Δdébit| {abs(d_sy):.2f} syll/s (poids {wc['syll']}, sat 2)" + (f", Δarousal {d_ar:+.3f} (poids {wc['ar']}, sat ±0.15)" if d_ar is not None else ", arousal absent"))
        p["pts_pause"] = round(W["pause"] * f_pause(p["pause_avant_s"]), 1)
        expl.append(f"pause avant {p['pts_pause']}/25 : " + ("début de fichier" if p["pause_avant_s"] is None else f"{p['pause_avant_s']:.2f} s (idéal 0,40-1,2 s)"))
        p["pts_apres"] = round(W["apres"] * g_apres(p["silence_apres_s"]), 1)
        sa = p["silence_apres_s"]
        p["apres"] = "fin du fichier (propre)" if sa is None else ("respiration après la chute" if sa >= 0.30 else ("reprise immédiate (chute écrasée)" if sa < 0.10 else "reprise rapide"))
        expl.append(f"netteté après {p['pts_apres']}/25 : {p['apres']}" + ("" if sa is None else f" ({sa:.2f} s)"))
        p["score_chute"] = round(p["pts_contraste"] + p["pts_pause"] + p["pts_apres"], 1); p["explication"] = " | ".join(expl)
        prev = p
    return phrases

def analyser(wav, mots_json, arousal_json=None, cuts=None):
    words = load_words(mots_json); A = analyse_audio(wav)
    arousal = json.load(open(arousal_json)).get("models", {}).get("audeering") if arousal_json else None
    phrases = [mesures_phrase(A, ph, arousal) for ph in segmenter(words, A, cuts=cuts)]
    return scorer(phrases), A

def tableau(phrases):
    L = ["  #  [début - fin ]  pause av. | durée | p90 dBFS (Δ)   | syll/s (Δ)    | F0 étendue st (Δ) | arousal (Δ)     | après                              | SCORE | texte"]
    for k, p in enumerate(phrases, 1):
        fmt = lambda v, s="": ("  –  " if v is None else f"{v:{s}}")
        L.append(f"{k:>3}  [{p['debut']:5.2f}-{p['fin']:5.2f}]  {fmt(p['pause_avant_s'],'4.2f')} s  | {p['duree_s']:4.2f} | {fmt(p['int_p90_dbfs'],'5.1f')} ({fmt(p['d_db'],'+.1f')}) | {p['syll_par_s']:4.2f} ({fmt(p['d_syll'],'+.2f')}) | {fmt(p['f0_etendue_st'],'4.1f')} ({fmt(p['d_f0'],'+.1f')})  | {fmt(p['arousal'],'.3f')} ({fmt(p['d_ar'],'+.3f')}) | {p['apres'][:34]:34} | {p['score_chute']:5.1f} | {p['texte'][:70]}")
    best = max(range(len(phrases)), key=lambda i: phrases[i]["score_chute"])
    L.append(f"\nMEILLEURE CHUTE : phrase {best+1} « {phrases[best]['texte'][:60]} » score {phrases[best]['score_chute']}/100")
    L.append("   " + phrases[best]["explication"])
    return "\n".join(L)

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("wav"); ap.add_argument("mots"); ap.add_argument("--arousal"); ap.add_argument("--t", type=float); ap.add_argument("--json"); ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    phrases, A = analyser(a.wav, a.mots, a.arousal)
    if not a.quiet:
        print(f"CHUTE — {a.wav.rsplit('/',1)[-1]} — {A['dur']:.2f} s — {len(phrases)} phrases (coupure : silence >= 0,30 s ou ponctuation) — F0 médiane {A['f0med']:.0f} Hz")
        print(tableau(phrases))
        if a.t is not None:
            sel = [p for p in phrases if p["debut"] - 0.05 <= a.t <= p["fin"] + 0.05]
            for p in sel: print(f"\nPHRASE À {a.t} s : « {p['texte']} » -> score {p['score_chute']}/100\n   {p['explication']}")
    if a.json: json.dump(phrases, open(a.json, "w"), ensure_ascii=False, indent=1)
