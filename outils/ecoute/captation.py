#!/usr/bin/env python3
"""Fiche captation : saturation, loudness, plancher de bruit, dynamique, silences.

Usage : captation.py fichier.(wav|mp4|...) [-o dossier] [--silence-db -40] [--silence-s 0.4]
Sort  : <dossier>/<base>_captation.json + <base>_captation.md, et affiche le tableau.
Import : from captation import fiche, markdown ; d = fiche(chemin) ; print(markdown(d))

Echelle unique :
  - crete echantillon / true peak : dBFS / dBTP (0 = pleine echelle)
  - RMS, plancher de bruit        : dBFS RMS (reference 0 dBFS = sinus pleine echelle -> -3 dBFS... non :
                                    ffmpeg astats 'RMS level' = 20*log10(rms), sinus pleine echelle = -3.01 dBFS)
  - loudness                      : LUFS (EBU R128, integre), LRA en LU
Ne depend que de ffmpeg (astats, ebur128, silencedetect) et numpy (recoupement de la crete).
"""
import argparse, json, os, re, subprocess, sys
import numpy as np

CIBLE_LUFS = -14.0      # cible plateformes (TikTok/IG/YT normalisent autour de -14)
TOL_LUFS = 2.0

def _ff(args):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-v", "info"] + args + ["-f", "null", "-"],
                       capture_output=True, text=True)
    return r.stderr

def _num(pattern, txt, default=None, flags=0):
    m = re.search(pattern, txt, flags)
    if not m: return default
    v = m.group(1)
    if v in ("-inf", "inf"): return float(v)
    try: return float(v)
    except ValueError: return default

def astats(f):
    txt = _ff(["-i", f, "-af", "astats=measure_perchannel=none:measure_overall=all"])
    # bloc Overall (ffmpeg ecrit 'Overall' puis les lignes)
    ov = txt.split("Overall", 1)[-1]
    return {
        "crete_dbfs": _num(r"Peak level dB:\s*(-?[\d.]+|-inf)", ov),
        "rms_dbfs": _num(r"RMS level dB:\s*(-?[\d.]+|-inf)", ov),
        "rms_pic_dbfs": _num(r"RMS peak dB:\s*(-?[\d.]+|-inf)", ov),
        "rms_creux_dbfs": _num(r"RMS trough dB:\s*(-?[\d.]+|-inf)", ov),
        "plancher_bruit_dbfs": _num(r"Noise floor dB:\s*(-?[\d.]+|-inf)", ov),
        "flat_factor": _num(r"Flat factor:\s*(-?[\d.]+)", ov),
        "peak_count": _num(r"Peak count:\s*(-?[\d.]+)", ov),
        "crest_factor": _num(r"Crest factor:\s*(-?[\d.]+|-inf|inf)", ov),
        "duree_s": _num(r"Number of samples:\s*(\d+)", ov),  # converti plus bas
        "_txt": txt,
    }

def ebur128(f):
    txt = _ff(["-i", f, "-af", "ebur128=peak=true"])
    fin = txt.rsplit("Summary:", 1)[-1]
    return {
        "lufs_integre": _num(r"I:\s*(-?[\d.]+|-inf)\s*LUFS", fin),
        "lra_lu": _num(r"LRA:\s*(-?[\d.]+)\s*LU", fin),
        "lra_bas_lufs": _num(r"LRA low:\s*(-?[\d.]+|-inf)\s*LUFS", fin),
        "lra_haut_lufs": _num(r"LRA high:\s*(-?[\d.]+|-inf)\s*LUFS", fin),
        "true_peak_dbtp": _num(r"True peak:\s*\n?\s*Peak:\s*(-?[\d.]+|-inf)\s*dBFS", fin),
    }

def silences(f, seuil_db=-40.0, mini_s=0.4):
    txt = _ff(["-i", f, "-af", f"silencedetect=n={seuil_db}dB:d={mini_s}"])
    deb = [float(x) for x in re.findall(r"silence_start:\s*(-?[\d.]+)", txt)]
    fin = [float(x) for x in re.findall(r"silence_end:\s*(-?[\d.]+)", txt)]
    z = []
    for i, d in enumerate(deb):
        e = fin[i] if i < len(fin) else None
        z.append({"debut": round(d, 2), "fin": None if e is None else round(e, 2),
                  "duree": None if e is None else round(e - d, 2)})
    return z

def crete_numpy(f):
    """Recoupement : decode en float32 (ffmpeg) et prend max(|x|). Pour un mp4/aac le decodeur peut depasser 1.0."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-i", f, "-vn", "-f", "f32le", "-acodec", "pcm_f32le", "-"],
                       capture_output=True)
    x = np.frombuffer(r.stdout, dtype=np.float32)
    if x.size == 0: return None
    pk = float(np.abs(x).max())
    return {"crete_lin": pk, "crete_dbfs": 20 * np.log10(pk) if pk > 0 else float("-inf"),
            "rms_dbfs": float(20 * np.log10(np.sqrt(np.mean(x.astype(np.float64) ** 2)) + 1e-12)),
            "n_ech_sup_0dbfs": int((np.abs(x) >= 1.0).sum()), "n_ech": int(x.size)}

def duree_de(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                       capture_output=True, text=True)
    try: return float(r.stdout.strip())
    except ValueError: return None

def verdicts(d):
    v = {}
    tp = d["true_peak_dbtp"]; sp = d["crete_dbfs"]
    if tp is None: v["saturation"] = ("⚪", "true peak non mesuré")
    elif tp > -1.0: v["saturation"] = ("🔴", f"ça sature : true peak {tp:+.1f} dBTP (> −1) — crête échantillon {sp:.2f} dBFS")
    elif tp > -3.0: v["saturation"] = ("🟡", f"limite : true peak {tp:+.1f} dBTP (> −3), garde de la marge")
    else: v["saturation"] = ("✅", f"pas de saturation : true peak {tp:+.1f} dBTP")
    I = d["lufs_integre"]
    if I is None or I == float("-inf"): v["loudness"] = ("⚪", "loudness non mesurable (silence ?)")
    else:
        ecart = I - CIBLE_LUFS
        if abs(ecart) <= TOL_LUFS: v["loudness"] = ("✅", f"{I:.1f} LUFS, dans la cible {CIBLE_LUFS:.0f} ±{TOL_LUFS:.0f}")
        elif ecart < 0: v["loudness"] = ("🟡", f"{I:.1f} LUFS : {abs(ecart):.1f} LU sous la cible {CIBLE_LUFS:.0f} — la plateforme va remonter (et le bruit avec)")
        else: v["loudness"] = ("🟡", f"{I:.1f} LUFS : {ecart:.1f} LU au-dessus de la cible {CIBLE_LUFS:.0f} — la plateforme va baisser, risque d'écrêtage avant")
    nf = d["plancher_bruit_dbfs"]
    if nf is None: v["bruit"] = ("⚪", "plancher non mesuré")
    elif nf > -50: v["bruit"] = ("🟡", f"bruit : plancher {nf:.1f} dBFS (> −50) — souffle/ambiance audible")
    else: v["bruit"] = ("✅", f"plancher {nf:.1f} dBFS, propre")
    lra = d["lra_lu"]
    if lra is None: v["dynamique"] = ("⚪", "LRA non mesurée")
    elif lra < 4: v["dynamique"] = ("🟡", f"LRA {lra:.1f} LU : très compressé / voix sans relief (seuil indicatif)")
    elif lra > 15: v["dynamique"] = ("🟡", f"LRA {lra:.1f} LU : très large — passages très bas ou très forts, à égaliser au montage (seuil indicatif)")
    else: v["dynamique"] = ("✅", f"LRA {lra:.1f} LU : dynamique de parole normale")
    tot = sum(z["duree"] or 0 for z in d["silences"]); dur = d["duree_s"] or 0
    pct = 100 * tot / dur if dur else 0
    plus = max((z["duree"] or 0) for z in d["silences"]) if d["silences"] else 0
    if plus >= 1.5: v["silences"] = ("🟡", f"{len(d['silences'])} silence(s) ≥ {d['silence_min_s']} s ({pct:.0f} % du fichier), le plus long {plus:.1f} s")
    else: v["silences"] = ("✅", f"{len(d['silences'])} silence(s) ≥ {d['silence_min_s']} s ({pct:.0f} % du fichier)")
    return v

def fiche(f, seuil_silence_db=None, silence_min_s=0.4):
    a = astats(f); e = ebur128(f); n = crete_numpy(f)
    if seuil_silence_db is None:  # relatif : 25 dB sous le RMS global, jamais plus laxiste que -40 dBFS
        seuil_silence_db = round(min(-40.0, (a["rms_dbfs"] if a["rms_dbfs"] not in (None, float("-inf")) else -15.0) - 25.0), 1)
    s = silences(f, seuil_silence_db, silence_min_s)
    d = {"fichier": os.path.abspath(f), "duree_s": duree_de(f),
         "crete_dbfs": a["crete_dbfs"], "true_peak_dbtp": e["true_peak_dbtp"],
         "crete_numpy_dbfs": None if n is None else round(n["crete_dbfs"], 3),
         "n_ech_sup_0dbfs_numpy": None if n is None else n["n_ech_sup_0dbfs"],
         "rms_dbfs": a["rms_dbfs"], "rms_numpy_dbfs": None if n is None else round(n["rms_dbfs"], 2),
         "rms_pic_dbfs": a["rms_pic_dbfs"], "rms_creux_dbfs": a["rms_creux_dbfs"],
         "plancher_bruit_dbfs": a["plancher_bruit_dbfs"], "flat_factor": a["flat_factor"], "peak_count": a["peak_count"],
         "crest_factor": a["crest_factor"],
         "lufs_integre": e["lufs_integre"], "lra_lu": e["lra_lu"], "lra_bas_lufs": e["lra_bas_lufs"], "lra_haut_lufs": e["lra_haut_lufs"],
         "cible_lufs": CIBLE_LUFS, "silence_seuil_db": seuil_silence_db, "silence_min_s": silence_min_s, "silences": s}
    d["verdicts"] = {k: {"icone": i, "texte": t} for k, (i, t) in verdicts(d).items()}
    return d

def _f(x, fmt="{:.1f}", unit=""):
    if x is None: return "—"
    if x == float("-inf"): return "−∞" + unit
    return fmt.format(x) + unit

def markdown(d):
    V = d["verdicts"]
    L = [f"## Fiche captation — `{os.path.basename(d['fichier'])}` ({_f(d['duree_s'])} s)", "",
         "| Mesure | Valeur | Verdict |", "| :--- | :--- | :--- |",
         f"| Crête échantillon | {_f(d['crete_dbfs'], '{:.2f}', ' dBFS')} (numpy {_f(d['crete_numpy_dbfs'], '{:.2f}', ' dBFS')}, {d['n_ech_sup_0dbfs_numpy']} éch. ≥ 0) | {V['saturation']['icone']} {V['saturation']['texte']} |",
         f"| True peak | {_f(d['true_peak_dbtp'], '{:+.1f}', ' dBTP')} | ↑ |",
         f"| Loudness intégrée | {_f(d['lufs_integre'], '{:.1f}', ' LUFS')} (cible {d['cible_lufs']:.0f} ±{TOL_LUFS:.0f}) | {V['loudness']['icone']} {V['loudness']['texte']} |",
         f"| Niveau RMS global | {_f(d['rms_dbfs'], '{:.1f}', ' dBFS')} (pic RMS {_f(d['rms_pic_dbfs'], '{:.1f}')}, creux {_f(d['rms_creux_dbfs'], '{:.1f}')}) | échelle dBFS RMS, réf. 0 dBFS |",
         f"| Plancher de bruit | {_f(d['plancher_bruit_dbfs'], '{:.1f}', ' dBFS')} | {V['bruit']['icone']} {V['bruit']['texte']} |",
         f"| Dynamique (LRA) | {_f(d['lra_lu'], '{:.1f}', ' LU')} ({_f(d['lra_bas_lufs'])} → {_f(d['lra_haut_lufs'])} LUFS) | {V['dynamique']['icone']} {V['dynamique']['texte']} |",
         f"| Écrêtage (astats) | flat factor {_f(d['flat_factor'], '{:.2f}')}, peak count {_f(d['peak_count'], '{:.0f}')} | {'🔴 échantillons collés au plafond (écrêtage)' if ((d['flat_factor'] or 0) > 0 and (d['crete_dbfs'] or -99) > -1.0) else '✅ pas de plateau au plafond'} |",
         f"| Silences (< {d['silence_seuil_db']:.0f} dB, ≥ {d['silence_min_s']} s) | " +
         (" · ".join(f"{z['debut']}–{z['fin']} s" for z in d['silences']) if d['silences'] else "aucun") +
         f" | {V['silences']['icone']} {V['silences']['texte']} |"]
    return "\n".join(L)

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fichier"); p.add_argument("-o", "--sortie", default=None)
    p.add_argument("--silence-db", type=float, default=None, help="seuil absolu en dBFS (défaut : RMS global − 25 dB, plafonné à −40)"); p.add_argument("--silence-s", type=float, default=0.4)
    p.add_argument("--json-seul", action="store_true")
    a = p.parse_args()
    if not os.path.exists(a.fichier): sys.exit(f"Fichier introuvable : {a.fichier}")
    d = fiche(a.fichier, a.silence_db, a.silence_s)
    out = a.sortie or os.path.dirname(os.path.abspath(a.fichier)); os.makedirs(out, exist_ok=True)
    base = os.path.splitext(os.path.basename(a.fichier))[0]
    with open(os.path.join(out, base + "_captation.json"), "w", encoding="utf-8") as fh: json.dump(d, fh, ensure_ascii=False, indent=1)
    md = markdown(d)
    with open(os.path.join(out, base + "_captation.md"), "w", encoding="utf-8") as fh: fh.write(md + "\n")
    if not a.json_seul: print(md)
    print(f"\n==> {os.path.join(out, base + '_captation.json')}")

if __name__ == "__main__":
    main()
