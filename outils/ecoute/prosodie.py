#!/usr/bin/env python3
"""Partition vocale lisible par Claude : F0 (Praat), intensité, noyaux syllabiques, pauses, qualité de voix,
stats par mot / phrase / zone, détection auto des zones molles et monotones, images PNG.
Usage: prosodie.py fichier.wav mots.json prefixe_sortie ['[["nom",deb,fin],...]']"""
import sys, json, time, math
import numpy as np
import parselmouth
from parselmouth.praat import call
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import librosa, librosa.display
from scipy.signal import find_peaks
import soundfile as sf

import os
wav, words_json, outp = sys.argv[1:4]
zones = json.loads(sys.argv[4]) if len(sys.argv) > 4 else []
CLIPPE = os.environ.get("ECOUTE_CLIPPE", "0") == "1"   # fiche captation : dynamique compressee -> seuil zone molle -4 dB au lieu de -5
t0 = time.time()
snd = parselmouth.Sound(wav); dur = snd.get_total_duration()
TS = 0.01
# F0 en deux passes (Hirst) : plage large, puis plancher/plafond adaptés au locuteur -> moins de sauts d'octave
pitch0 = snd.to_pitch(time_step=TS, pitch_floor=60, pitch_ceiling=600)
# Praat exprime l'intensite en dB re 20 uPa en supposant amplitude 1.0 = 1 Pa : 0 dBFS RMS = 20*log10(1/2e-5) = 93.98 dB.
# On soustrait cette constante pour sortir des dBFS RMS (reference 0 dBFS), meme echelle que captation.py / vision-video.py.
# Valide sur voix2.wav et reel1.wav : offset mesure 93.93 dB (mediane, ecart-type 0.9 dB), sinus -16 dBFS -> 77.98 dB Praat.
PRAAT_VERS_DBFS = 20 * math.log10(1 / 2e-5)
inten = snd.to_intensity(time_step=TS, minimum_pitch=75); ti = inten.xs(); iraw = inten.values[0] - PRAAT_VERS_DBFS
grid = np.arange(0, dur, TS)
def nearest(t_src, v_src):
    idx = np.clip(np.round((grid - t_src[0]) / TS).astype(int), 0, len(t_src) - 1)
    v = v_src[idx].astype(float)
    v[(grid < t_src[0] - TS) | (grid > t_src[-1] + TS)] = np.nan
    return v
I = nearest(ti, iraw)
# seuil de silence : -25 dB sous le max (convention Praat) MAIS jamais sous le plancher de bruit + 6 dB
# (verif bruit-arousal : bruit rose SNR 15 / musique -12 dB -> 0 pause detectee avec le seuil fixe ; p5+6 dB en retrouve 12-16)
# + seuil LOCAL (seuil.py, fenetre glissante 10 s) : un passage 10 dB plus bas que les pics (micro qui s'eloigne, aparte,
# deuxieme prise raccordee) reste de la parole au lieu de devenir une pause fantome de plusieurs secondes.
from seuil import masque_parole, pauses_dans
SP = masque_parole(I, grid, TS); speech = SP["speech"]; thr_t = SP["thr"]; thr = SP["thr_global"]; p99, p5 = SP["p99"], SP["p5"]
BRUIT_FORT = SP["bruit_fort"]               # drapeau : pauses / debit / HNR incertains
# F0 en deux passes (Hirst), plage locuteur calculee sur les trames de PAROLE seulement (gating : la musique de fond
# voisait 28,6 % de trames fantomes ; avec gating 0,2 %)
f0v0 = nearest(pitch0.xs(), pitch0.selected_array['frequency']); f0v = f0v0[(f0v0 > 0) & speech]
if len(f0v) < 10: f0v = f0v0[f0v0 > 0]
if len(f0v) < 10: f0v = np.array([100.0, 200.0])
q25, q75 = np.percentile(f0v, [25, 75]); PFLOOR, PCEIL = max(50.0, 0.75 * q25), min(700.0, 1.75 * q75)
pitch = snd.to_pitch(time_step=TS, pitch_floor=PFLOOR, pitch_ceiling=PCEIL)
f0raw = pitch.selected_array['frequency']; tp = pitch.xs()
F0 = nearest(tp, f0raw); F0[F0 <= 0] = np.nan
F0[~speech] = np.nan                          # gating : pas de F0 hors parole
ST = 12 * np.log2(F0 / np.nanmedian(F0))  # demi-tons RELATIFS à la médiane du locuteur (0 = sa hauteur habituelle)
voiced = ~np.isnan(F0)

# ---- pauses (>= 0.15 s non-parole)
pauses = []; i = 0; n = len(grid)
while i < n:
    if not speech[i]:
        j = i
        while j < n and not speech[j]: j += 1
        d = (j - i) * TS
        if d >= 0.15: pauses.append({"debut": round(grid[i], 2), "fin": round(grid[min(j, n-1)], 2), "duree": round(d, 2)})
        i = j
    else: i += 1

# ---- noyaux syllabiques (De Jong & Wempe simplifié : pics d'intensité proéminents, voisés)
Ifill = np.where(np.isnan(I), np.nanmin(I), I)
pk, prop = find_peaks(Ifill, prominence=2.0, distance=int(0.08 / TS), height=thr_t)
nuclei = np.array([grid[p] for p in pk if voiced[max(0, p-1):p+2].any()])

# ---- qualité de voix (Praat)
pp = call(snd, "To PointProcess (periodic, cc)", PFLOOR, PCEIL)
jitter = call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
shimmer = call([snd, pp], "Get shimmer (local)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
harm = snd.to_harmonicity_cc(time_step=TS, minimum_pitch=75)
hnr = call(harm, "Get mean", 0, 0)

# ---- mots
W = json.load(open(words_json))
words = []
for s in W["segments"]:
    for w in s["words"]:
        m = (grid >= w["start"]) & (grid <= w["end"])
        if m.sum() == 0: continue
        st = ST[m]; ii = I[m]
        words.append({"mot": w["w"].strip(), "debut": round(w["start"], 2), "fin": round(w["end"], 2),
                      "duree": round(w["end"] - w["start"], 2),
                      "f0_moy_hz": None if np.all(np.isnan(st)) else round(float(np.nanmean(F0[m])), 1),
                      "f0_etendue_st": None if np.all(np.isnan(st)) else round(float(np.nanmax(st) - np.nanmin(st)), 1),
                      "f0_max_st": None if np.all(np.isnan(st)) else round(float(np.nanmax(st)), 1),
                      "int_moy_db": round(float(np.nanmean(ii)), 1), "int_max_db": round(float(np.nanmax(ii)), 1),
                      "voise_pct": round(100 * float(np.mean(~np.isnan(st))), 0),
                      "syllabes": int(((nuclei >= w["start"]) & (nuclei <= w["end"])).sum())})
# score d'accentuation = z(intensité max) + z(F0 max)
im = np.array([w["int_max_db"] for w in words]); fm = np.array([np.nan if w["f0_max_st"] is None else w["f0_max_st"] for w in words])
if len(words) > 1:
    zi = (im - im.mean()) / (im.std() + 1e-9); zf = (fm - np.nanmean(fm)) / (np.nanstd(fm) + 1e-9)
    for k, w in enumerate(words): w["accent"] = round(float(zi[k] + (0 if np.isnan(zf[k]) else zf[k])), 2)
top_accent = sorted([w for w in words if w["duree"] >= 0.12], key=lambda w: -w["accent"])[:6]
plats = sorted([w for w in words if w["duree"] >= 0.12], key=lambda w: w["accent"])[:4]

# ---- phrases (segments whisper) : débit
phrases = []
for s in W["segments"]:
    m = (grid >= s["start"]) & (grid <= s["end"]); d = s["end"] - s["start"]
    nw = len(s["words"]); nsy = int(((nuclei >= s["start"]) & (nuclei <= s["end"])).sum())
    ptime = pauses_dans(pauses, s["start"], s["end"])
    stm = ST[m]
    prev_end = phrases[-1]["fin"] if phrases else 0.0
    phrases.append({"debut": round(s["start"], 2), "fin": round(s["end"], 2), "texte": s["text"].strip(), "pause_avant_s": round(max(0.0, s["start"] - prev_end), 2),
                    "int_p90_db": round(float(np.nanpercentile(I[m & speech], 90)), 1) if (m & speech).any() else None,
                    "f0_pic_st": round(float(np.nanmax(stm)), 1) if voiced[m].any() else None,
                    "f0_pic_rel_mediane_st": round(float(np.nanmax(stm) - np.nanmedian(ST)), 1) if voiced[m].any() else None,
                    "mots": nw, "mots_par_s": round(nw / d, 2) if d > 0 else None,
                    "syll_par_s": round(nsy / d, 2) if d > 0 else None,
                    "syll_par_s_articulation": round(nsy / (d - ptime), 2) if d - ptime > 0.2 else None,
                    "int_moy_db": round(float(np.nanmean(I[m & speech])), 1) if (m & speech).any() else None,
                    "f0_moy_hz": round(float(np.nanmean(F0[m])), 1) if voiced[m].any() else None,
                    "f0_ecart_type_st": round(float(np.nanstd(stm)), 2) if voiced[m].sum() > 5 else None,
                    "f0_etendue_st": round(float(np.nanmax(stm) - np.nanmin(stm)), 1) if voiced[m].sum() > 5 else None})

# ---- passages monotones : fenêtre glissante 2,0 s (pas 0,1 s, >= 50 % parole, >= 30 % voisé), écart-type F0 en demi-tons
# Calibration (verif intonation, PSOLA plat/vivant sur reel1/reel3) : < 0,8 st = MONOTONE (100 % des fenetres plat, 0 % des voix naturelles),
# 0,8-1,3 st = PEU VARIE, et regle relative CHUTE D'INTONATION si sd < 0,5 x mediane des fenetres du clip (seulement si cette mediane >= 1,6 st).
WIN, STEP, SEUIL_MONO, SEUIL_PEU = 2.0, 0.1, 0.8, 1.3
mono_flags = []
for t in np.arange(0, max(0.0, dur - WIN) + 1e-9, STEP):
    m = (grid >= t) & (grid < t + WIN)
    if m.sum() == 0 or speech[m].mean() < 0.5 or voiced[m].sum() < 0.3 * m.sum(): continue
    sd = float(np.nanstd(ST[m]))
    mono_flags.append((t, t + WIN, sd))
sd_med_fen = float(np.median([x[2] for x in mono_flags])) if mono_flags else None
def _fusion_flags(pred, cle):
    out = []
    for a, b, sd in mono_flags:
        if pred(sd):
            if out and a <= out[-1]["fin"] - WIN + STEP + 1e-6:
                out[-1]["fin"] = round(b, 2); out[-1]["sds"].append(sd)
            else: out.append({"debut": round(a, 2), "fin": round(b, 2), "sds": [sd], "type": cle})
    for mo in out: mo["f0_ecart_type_st"] = round(float(np.mean(mo.pop("sds"))), 2)
    fus = []   # fusionne les intervalles qui se chevauchent (fenetres glissantes) pour ne pas lister 5 fois la meme zone
    for mo in sorted(out, key=lambda z: z["debut"]):
        if fus and mo["debut"] <= fus[-1]["fin"]: fus[-1]["fin"] = max(fus[-1]["fin"], mo["fin"]); fus[-1]["f0_ecart_type_st"] = round(min(fus[-1]["f0_ecart_type_st"], mo["f0_ecart_type_st"]), 2)
        else: fus.append(mo)
    for mo in fus: mo["duree"] = round(mo["fin"] - mo["debut"], 2)
    return [mo for mo in fus if mo["duree"] >= WIN + 0.5]   # au moins 6 fenetres consecutives (2,5 s)
monotones = _fusion_flags(lambda sd: sd < SEUIL_MONO, "MONOTONE")
peu_varies = _fusion_flags(lambda sd: SEUIL_MONO <= sd < SEUIL_PEU, "PEU VARIÉ")
chutes_intonation = _fusion_flags(lambda sd: sd < 0.5 * sd_med_fen, "CHUTE D'INTONATION") if (sd_med_fen is not None and sd_med_fen >= 1.6) else []

# ---- zones molles (auto) : intensité de parole lissée 1 s vs médiane globale, et débit local
Isp = np.where(speech, I, np.nan)
def _windows(x, w):
    k = int(w / TS); pad = np.full(k // 2, np.nan)
    xp = np.concatenate([pad, x, pad])
    return np.lib.stride_tricks.sliding_window_view(xp, k)[:len(x)], k
def roll_nanmean(x, w):
    V, k = _windows(x, w); ok = np.isfinite(V).sum(1) >= k // 4
    with np.errstate(all="ignore"): out = np.nanmean(V, axis=1)
    out[~ok] = np.nan; return out
def roll_nanpct(x, w, q):
    V, k = _windows(x, w); ok = np.isfinite(V).sum(1) >= k // 4
    with np.errstate(all="ignore"): out = np.nanpercentile(V, q, axis=1)
    out[~ok] = np.nan; return out
Ism = roll_nanmean(Isp, 1.0); med = float(np.nanmedian(Isp))
Ip90 = roll_nanpct(Isp, 1.0, 90); p90g = float(np.nanpercentile(Isp, 90))   # enveloppe des pics (1 s) vs pics globaux
SEUIL_MOU = 4.0 if CLIPPE else 5.0   # verif bruit : telephone clippe compresse la dynamique (zone molle -6,3 au lieu de -8,5 dB)
DUREE_MOU_MIN = 1.5                 # verif aveugle : les declinaisons de fin de phrase durent 0,3-1,1 s -> exiger >= 1,5 s
soft = Ip90 < p90g - SEUIL_MOU
molles = []; i = 0
while i < n:
    if soft[i]:
        j = i
        while j < n and (soft[j] or (np.isnan(Ip90[j]) and j + 1 < n and (soft[j+1] or np.isnan(Ip90[j+1])))): j += 1
        d = (j - i) * TS; nsy_z = int(((nuclei >= grid[i]) & (nuclei < grid[min(j, n-1)])).sum())
        if d >= DUREE_MOU_MIN and nsy_z >= 2: molles.append({"debut": round(grid[i], 2), "fin": round(grid[min(j, n-1)], 2), "duree": round(d, 2), "syllabes": nsy_z,
                                    "int_moy_db": round(float(np.nanmean(Isp[i:j])), 1), "ecart_moy_vs_mediane_db": round(float(np.nanmean(Isp[i:j]) - med), 1),
                                    "int_p90_db": round(float(np.nanpercentile(Isp[i:j], 90)), 1), "ecart_pics_vs_global_db": round(float(np.nanpercentile(Isp[i:j], 90) - p90g), 1)})
        i = max(j, i + 1)
    else: i += 1

# ---- zones lentes (auto) : debit d'ARTICULATION local = noyaux / temps de parole de la fenetre glissante 1,5 s (les silences de la
# fenetre ne comptent plus : relecture, le clip de 4 s etait « lent » 0-2 s a cause de 0,49 s de silence initial), lent si < 65 % du debit
# d'articulation global ; fenetres a < 30 % de parole ignorees ; zones distantes de < 1 s fusionnees ; duree >= 2,5 s exigee (comme MONOTONE).
rate_g = len(nuclei) / max(0.5, (nuclei.max() - nuclei.min())) if len(nuclei) > 1 else 0
rate_art_g = len(nuclei) / max(0.5, float(speech.sum()) * TS)
DUREE_LENTE_MIN, WL = 2.5, 1.5
lentes = []; cur = None
for t in np.arange(0, dur - WL + 1e-9, 0.1):
    mw = (grid >= t) & (grid < t + WL); tsp = float(speech[mw].sum()) * TS
    if tsp < 0.3 * WL: continue
    r = ((nuclei >= t) & (nuclei < t + WL)).sum() / tsp
    if r < 0.65 * rate_art_g:
        if cur and t <= cur["fin"] - WL + 0.05 + 1e-6: cur["fin"] = round(t + WL, 2); cur["rates"].append(r)
        else: cur = {"debut": round(t, 2), "fin": round(t + WL, 2), "rates": [r]}; lentes.append(cur)
for z in lentes: z["syll_par_s"] = float(np.mean(z.pop("rates")))
merged = []
for z in lentes:
    if merged and z["debut"] <= merged[-1]["fin"] + 1.0: merged[-1]["fin"] = max(merged[-1]["fin"], z["fin"]); merged[-1]["syll_par_s"] = min(merged[-1]["syll_par_s"], z["syll_par_s"])
    else: merged.append(dict(z))
lentes = [z for z in merged if z["fin"] - z["debut"] >= DUREE_LENTE_MIN]
# Le debit annonce doit porter sur TOUTE la zone fusionnee. Garder le min des fenetres de 1,5 s
# faisait passer une zone de 9 s pour aussi lente que sa pire fenetre (rush du 12/09 : 1,45 syll/s
# annonce contre 3,79 mesures sur la zone entiere, soit 27 % au lieu de 71 %). On recalcule donc
# noyaux / temps de parole sur la zone entiere, et une zone qui ne tient plus le critere sur toute
# sa duree n'est pas une zone lente : la fusion etait trop large, on la retire.
qual = []
for z in lentes:
    z["syll_par_s_min_fenetre"] = round(z.pop("syll_par_s"), 2)
    z["duree"] = round(z["fin"] - z["debut"], 2)
    z["syllabes"] = int(((nuclei >= z["debut"]) & (nuclei < z["fin"])).sum())
    mz = (grid >= z["debut"]) & (grid < z["fin"]); tsp = float(speech[mz].sum()) * TS
    if tsp <= 0.2: continue
    z["syll_par_s"] = round(z["syllabes"] / tsp, 2)
    z["ratio_vs_global"] = round(z["syll_par_s"] / max(0.1, rate_art_g), 2)
    if z["ratio_vs_global"] < 0.65: qual.append(z)
lentes = qual

# ---- stats par zone (fournies + molles auto)
def zone_stats(nom, a, b):
    m = (grid >= a) & (grid < b); ms = m & speech
    d = b - a; nw = sum(1 for w in words if a <= (w["debut"] + w["fin"]) / 2 < b)
    nsy = int(((nuclei >= a) & (nuclei < b)).sum()); ptime = pauses_dans(pauses, a, b)
    return {"zone": nom, "debut": a, "fin": b, "duree": round(d, 2),
            "int_moy_db": round(float(np.nanmean(I[ms])), 1) if ms.any() else None,
            "int_max_db": round(float(np.nanmax(I[ms])), 1) if ms.any() else None,
            "int_p90_db": round(float(np.nanpercentile(I[ms], 90)), 1) if ms.any() else None,
            "f0_moy_hz": round(float(np.nanmean(F0[m])), 1) if voiced[m].any() else None,
            "f0_ecart_type_st": round(float(np.nanstd(ST[m])), 2) if voiced[m].sum() > 5 else None,
            "f0_etendue_st": round(float(np.nanmax(ST[m]) - np.nanmin(ST[m])), 1) if voiced[m].sum() > 5 else None,
            "syllabes": nsy, "syll_par_s": round(nsy / d, 2), "syll_par_s_articulation": round(nsy / (d - ptime), 2) if d - ptime > 0.2 else None,
            "mots": nw, "mots_par_s": round(nw / d, 2), "part_parole_pct": round(100 * float(speech[m].mean()), 0),
            "pauses_s": round(ptime, 2)}
zones_out = [zone_stats(z[0], z[1], z[2]) for z in zones]

glob = {"duree_s": round(dur, 2), "seuil_silence_db": round(float(thr), 1), "seuil_silence_local_min_max_db": [SP["thr_min"], SP["thr_max"]], "plancher_p5_db": round(p5, 1), "pics_p99_db": round(p99, 1), "bruit_fort": bool(BRUIT_FORT), "clippe": bool(CLIPPE),
        "f0_sd_mediane_fenetres_2s_st": None if sd_med_fen is None else round(sd_med_fen, 2), "f0_plage_recherche_hz": [round(PFLOOR), round(PCEIL)],
        "int_p90_parole_db": round(p90g, 1), "echelle_intensite": "dBFS RMS (0 dBFS = pleine echelle ; Praat dB - 93.98)", "syll_par_s_global_utile": round(rate_g, 2), "syll_par_s_articulation_ref_lentes": round(rate_art_g, 2),
        "int_moy_parole_db": round(float(np.nanmean(I[speech])), 1), "int_mediane_parole_db": round(med, 1),
        "f0_moy_hz": round(float(np.nanmean(F0)), 1), "f0_mediane_hz": round(float(np.nanmedian(F0)), 1),
        "f0_ecart_type_st": round(float(np.nanstd(ST)), 2), "f0_p5_p95_hz": [round(float(np.nanpercentile(F0, 5)), 1), round(float(np.nanpercentile(F0, 95)), 1)],
        "part_voisee_pct": round(100 * float(voiced.mean()), 0), "part_parole_pct": round(100 * float(speech.mean()), 0),
        "syllabes_total": int(len(nuclei)), "syll_par_s_global": round(len(nuclei) / dur, 2),
        "syll_par_s_articulation": round(len(nuclei) / (speech.sum() * TS), 2),
        "mots_total": len(words), "mots_par_s": round(len(words) / dur, 2),
        "pauses_n": len(pauses), "pauses_total_s": round(sum(p["duree"] for p in pauses), 2),
        "pause_max": max(pauses, key=lambda p: p["duree"]) if pauses else None,
        "jitter_local_pct": round(100 * jitter, 2), "shimmer_local_pct": round(100 * shimmer, 2), "hnr_db": round(hnr, 1)}
t_mes = time.time() - t0

# ================= IMAGES =================
def word_labels(ax, y0, y1, fs=9):
    # étiquettes de mots au bon timecode, hauteurs alternées pour éviter le chevauchement
    for k, w in enumerate(words):
        xm = (w["debut"] + w["fin"]) / 2
        ax.axvline(w["debut"], color="#555", lw=0.4, alpha=0.6)
        ax.text(xm, y1 if k % 2 == 0 else y0, w["mot"], color="#ffd166", fontsize=fs, ha="center", va="top", rotation=0, clip_on=True)
t1 = time.time()
plt.rcParams.update({"axes.facecolor": "#14161c", "figure.facecolor": "#0d0f14", "axes.edgecolor": "#888", "axes.labelcolor": "#ddd",
                     "xtick.color": "#ddd", "ytick.color": "#ddd", "text.color": "#eee", "grid.color": "#333"})
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 7.5), dpi=100, sharex=True, gridspec_kw={"height_ratios": [1.15, 1]})
fig.subplots_adjust(left=0.05, right=0.99, top=0.93, bottom=0.08, hspace=0.08)
# piste F0
ax1.plot(grid, F0, ".", ms=2.5, color="#4cc9f0")
ax1.plot(nuclei, np.interp(nuclei, grid, np.nan_to_num(F0, nan=np.nanmin(F0))), "v", ms=5, color="#f72585", alpha=0.7, label="noyau syllabique")
for p in pauses:
    ax1.axvspan(p["debut"], p["fin"], color="#777", alpha=0.25); ax2.axvspan(p["debut"], p["fin"], color="#777", alpha=0.25)
    if p["duree"] >= 0.25: ax2.text((p["debut"]+p["fin"])/2, thr + 1, f"pause\n{p['duree']:.2f}s", color="#bbb", fontsize=7, ha="center", va="bottom")
ylo, yhi = np.nanpercentile(F0, 1) * 0.8, np.nanpercentile(F0, 99) * 1.25
ax1.set_ylim(ylo, yhi); ax1.set_ylabel("Hauteur F0 (Hz)")
word_labels(ax1, yhi - (yhi-ylo)*0.10, yhi - (yhi-ylo)*0.01)
ax1.grid(True, lw=0.3); ax1.legend(loc="lower right", fontsize=8, facecolor="#222")
ax1.set_title(f"PARTITION VOCALE — {wav.rsplit('/',1)[-1]} — F0 méd. {glob['f0_mediane_hz']} Hz, écart-type {glob['f0_ecart_type_st']} st · "
              f"intensité moy. {glob['int_moy_parole_db']} dB · {glob['syll_par_s_articulation']} syll/s (articulation) · {glob['pauses_n']} pauses", fontsize=10)
# piste intensité
ax2.fill_between(grid, np.nan_to_num(I, nan=thr-10), thr - 10, color="#80ed99", alpha=0.35)
ax2.plot(grid, I, color="#80ed99", lw=1.2)
ax2.plot(grid, Ip90, color="#ffffff", lw=1.0, ls="--", alpha=0.8, label="enveloppe des pics (p90, 1 s)")
ax2.axhline(p90g, color="#ffb703", lw=0.8, ls=":", label=f"pics globaux p90 {p90g:.0f} dB"); ax2.plot(grid, thr_t, color="#f55", lw=0.6, ls=":", label=f"seuil silence local {SP['thr_min']:.0f}…{SP['thr_max']:.0f} dB")
ax2.set_ylim(SP["thr_min"] - 8, np.nanmax(I) + 6); ax2.set_ylabel("Intensité (dBFS RMS)"); ax2.set_xlabel("temps (s)")
ax2.set_xlim(0, dur); ax2.set_xticks(np.arange(0, dur + 0.01, 0.5 if dur <= 20 else 1.0)); ax2.grid(True, lw=0.3); ax2.legend(loc="lower right", fontsize=8, facecolor="#222", ncol=3)
fig.savefig(outp + "_partition.png")
# clips > 15 s : une image par fenêtre de 15 s, MEME regle que ecoute-video.py (nf = ceil(dur/15) > 1) — relecture : un clip de 18 s
# n'avait qu'une image pour deux fenetres -> IndexError dans fusion.py
if dur > 15:
    for k, a in enumerate(np.arange(0, dur, 15.0)):
        b = min(a + 15.0, dur); ax2.set_xlim(a, b); ax2.set_xticks(np.arange(a, b + 0.01, 0.5))
        ax1.set_title(f"PARTITION VOCALE — {wav.rsplit('/',1)[-1]} — fenêtre {a:.0f}–{b:.0f} s", fontsize=10)
        fig.savefig(outp + f"_partition_p{k+1}.png")
plt.close(fig)
# mel-spectrogramme annoté
y, srr = librosa.load(wav, sr=None, mono=True)
S = librosa.power_to_db(librosa.feature.melspectrogram(y=y, sr=srr, n_fft=1024, hop_length=int(0.005*srr), n_mels=96, fmax=min(8000, srr//2)), ref=np.max)
fig, ax = plt.subplots(figsize=(15, 6), dpi=100); fig.subplots_adjust(left=0.05, right=0.99, top=0.9, bottom=0.09)
librosa.display.specshow(S, sr=srr, hop_length=int(0.005*srr), x_axis="time", y_axis="mel", fmax=min(8000, srr//2), ax=ax, cmap="magma", vmin=-70, vmax=0)
ax.plot(grid, F0, color="#4cc9f0", lw=1.4, label="F0 (Hz)")
for p in pauses: ax.axvspan(p["debut"], p["fin"], color="#fff", alpha=0.12)
ymax = ax.get_ylim()[1]
for k, w in enumerate(words):
    ax.axvline(w["debut"], color="#fff", lw=0.4, alpha=0.5)
    ax.text((w["debut"]+w["fin"])/2, ymax*(0.97 if k % 2 == 0 else 0.88), w["mot"], color="#ffd166", fontsize=9, ha="center", va="top")
ax.set_xlim(0, dur); ax.set_xticks(np.arange(0, dur + 0.01, 0.5)); ax.set_xlabel("temps (s)"); ax.set_ylabel("fréquence (Hz, échelle mel)")
ax.set_title(f"MEL-SPECTROGRAMME annoté — {wav.rsplit('/',1)[-1]} (clair = fort ; trait bleu = F0 ; bandes blanches = pauses)", fontsize=10); ax.legend(loc="upper right", fontsize=8)
fig.savefig(outp + "_mel.png"); plt.close(fig)
t_img = time.time() - t1

out = {"fichier": wav, "global": glob, "zones": zones_out, "zones_molles_auto": molles, "zones_lentes_auto": lentes, "passages_monotones_auto": monotones, "passages_peu_varies_auto": peu_varies, "chutes_intonation_auto": chutes_intonation,
       "mots_les_plus_accentues": top_accent, "mots_les_plus_plats": plats, "phrases": phrases, "pauses": pauses, "mots": words,
       "noyaux_syllabiques_s": [round(float(x), 2) for x in nuclei], "temps_mesures_s": round(t_mes, 2), "temps_images_s": round(t_img, 2),
       "images": [outp + "_partition.png", outp + "_mel.png"]}
json.dump(out, open(outp + "_mesures.json", "w"), ensure_ascii=False, indent=1)
# résumé texte
L = [f"=== {wav}  (mesures {t_mes:.2f}s, images {t_img:.2f}s)", "GLOBAL: " + json.dumps(glob, ensure_ascii=False)]
L += ["ZONES:"] + ["  " + json.dumps(z, ensure_ascii=False) for z in zones_out]
L += [f"ZONES MOLLES AUTO (enveloppe des pics p90 sur 1 s < pics globaux -{SEUIL_MOU} dB, >={DUREE_MOU_MIN} s):"] + ["  " + json.dumps(z, ensure_ascii=False) for z in molles]
L += ["ZONES LENTES AUTO (débit d'articulation sur 1,5 s < 65 % du débit d'articulation global, >= 2,5 s):"] + ["  " + json.dumps(z, ensure_ascii=False) for z in lentes]
L += [f"PASSAGES MONOTONES AUTO (écart-type F0 < {SEUIL_MONO} st sur fenêtre 2 s):"] + ["  " + json.dumps(z, ensure_ascii=False) for z in monotones]
L += [f"PASSAGES PEU VARIÉS AUTO ({SEUIL_MONO} <= sd < {SEUIL_PEU} st):"] + ["  " + json.dumps(z, ensure_ascii=False) for z in peu_varies]
L += ["CHUTES D'INTONATION (sd < 0,5 x médiane des fenêtres du clip):"] + ["  " + json.dumps(z, ensure_ascii=False) for z in chutes_intonation]
L += ["MOTS LES PLUS ACCENTUÉS:"] + [f"  {w['mot']!r} @{w['debut']}-{w['fin']} int_max {w['int_max_db']} dB f0_max {w['f0_max_st']} st score {w['accent']}" for w in top_accent]
L += ["MOTS LES PLUS PLATS:"] + [f"  {w['mot']!r} @{w['debut']}-{w['fin']} int_max {w['int_max_db']} dB f0_max {w['f0_max_st']} st score {w['accent']}" for w in plats]
L += ["PHRASES:"] + ["  " + json.dumps(p, ensure_ascii=False) for p in phrases]
L += ["PAUSES:"] + ["  " + json.dumps(p, ensure_ascii=False) for p in pauses]
open(outp + "_resume.txt", "w").write("\n".join(L) + "\n"); print("\n".join(L))
