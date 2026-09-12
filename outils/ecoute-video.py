#!/usr/bin/env python3
"""ecoute-video : Claude « écoute » une vidéo par les chiffres.
Usage : python3 ecoute-video.py <video|wav> [-o dossier] [--profil nabil.json] [--sans-arousal]
Étapes : (1) ffmpeg -> wav 16 kHz mono (passe-haut 80 Hz) + fiche captation sur l'original ; (2) faster-whisper large-v3-turbo int8 sans VAD, mots + probabilités ;
(3) Praat (prosodie.py) global + fenêtres de 15 s + alertes molle/lente/monotone ; (4) arousal audeering 2 s / pas 1 s dans le venv torch (sous-processus) ;
(5) fusion par phrase + score de chute ; (6) RAPPORT-ECOUTE.md, RAPPORT-PROSODIE.txt, partitions PNG (≤ 1500 px), arousal.png, mesures.json, temps.json.
Tout tourne dans le python système sauf l'arousal (venv). Chaque étape est chronométrée (temps + RAM pic, machine partagée)."""
import os, sys, json, time, argparse, subprocess, shutil, math
ICI = os.path.dirname(os.path.abspath(__file__)); PK = os.path.join(ICI, "ecoute")
sys.path.insert(0, PK)
# python du venv arousal (torch) : ECOUTE_VENV_PY, sinon <dossier de l'outil>/venv-arousal/bin/python, sinon ~/venv-ecoute-arousal/bin/python
CANDIDATS_VENV = [os.environ.get("ECOUTE_VENV_PY"), os.path.join(ICI, "venv-arousal", "bin", "python"), os.path.expanduser("~/venv-ecoute-arousal/bin/python")]
VENV_PY = next((c for c in CANDIDATS_VENV if c and os.path.exists(c)), None)

def die(msg): print(f"ERREUR : {msg}", file=sys.stderr); sys.exit(2)

def sonde(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,sample_rate,channels:format=duration", "-of", "json", f], capture_output=True, text=True)
    if r.returncode != 0: die(f"ffprobe ne lit pas ce fichier : {f}\n{r.stderr.strip()}")
    d = json.loads(r.stdout); aud = [s for s in d.get("streams", []) if s.get("codec_type") == "audio"]
    return aud, float(d.get("format", {}).get("duration") or 0)

def etape(nom, cmd, temps, log):
    t = time.time(); print(f"--- {nom} : {' '.join(os.path.basename(c) if os.sep in c else c for c in cmd)[:160]}", flush=True)
    r = subprocess.run([sys.executable, os.path.join(PK, "_run.py")] + cmd, capture_output=True, text=True)
    mes = {}
    for l in r.stdout.splitlines()[::-1]:
        if l.startswith('{"MESURE"'): mes = json.loads(l)["MESURE"]; break
    log.write(f"===== {nom}\n{r.stdout}\n{r.stderr}\n"); log.flush()
    temps[nom] = {"s": round(time.time() - t, 2), "ram_pic_mb": mes.get("ram_pic_mb"), "exit": r.returncode}
    print(f"    {temps[nom]['s']} s, RAM pic {mes.get('ram_pic_mb')} MB, exit {r.returncode}", flush=True)
    if r.returncode != 0: print(r.stderr[-1500:], file=sys.stderr)
    return r.returncode == 0

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fichier"); ap.add_argument("-o", "--sortie"); ap.add_argument("--profil"); ap.add_argument("--sans-arousal", action="store_true")
    a = ap.parse_args()
    T0 = time.time(); temps = {}
    if not os.path.isfile(a.fichier): die(f"fichier introuvable : {a.fichier}")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"): die("ffmpeg/ffprobe absents (apt install ffmpeg)")
    src = os.path.abspath(a.fichier); base = os.path.splitext(os.path.basename(src))[0]
    out = os.path.abspath(a.sortie or os.path.join(os.path.dirname(src), "ecoute-" + base)); os.makedirs(out, exist_ok=True)
    log = open(os.path.join(out, "journal.log"), "w")
    aud, dur = sonde(src)
    if not aud: die(f"cette vidéo n'a PAS de piste audio : {src} — rien à écouter")
    print(f"Entrée : {src} — {dur:.1f} s, audio {aud[0].get('codec_name')} {aud[0].get('sample_rate')} Hz {aud[0].get('channels')} canal/aux → sortie {out}")
    # (1) fiche captation sur l'ORIGINAL + conversion
    t = time.time(); import captation
    try: cap = captation.fiche(src)
    except Exception as e: cap = None; print(f"    fiche captation impossible : {e!r}", file=sys.stderr)
    cap_json = os.path.join(out, "captation.json")
    if cap:
        json.dump(cap, open(cap_json, "w"), ensure_ascii=False, indent=1); open(os.path.join(out, "captation.md"), "w").write(captation.markdown(cap) + "\n")
        v = cap["verdicts"]; print("    captation : " + " | ".join(f"{v[k]['icone']} {k}" for k in v))
    temps["1a_captation"] = {"s": round(time.time() - t, 2)}
    wav = os.path.join(out, base + "_16k.wav"); t = time.time()
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-af", "highpass=f=80", "-c:a", "pcm_s16le", wav], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(wav): die(f"conversion ffmpeg échouée : {r.stderr.strip()}")
    temps["1b_ffmpeg_wav16k"] = {"s": round(time.time() - t, 2)}
    dur_w = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav], capture_output=True, text=True).stdout.strip() or dur)
    if dur_w < 1.0: die(f"audio trop court ({dur_w:.2f} s) : rien à mesurer")
    clippe = bool(cap and (cap.get("flat_factor") or 0) > 0 and (cap.get("crete_dbfs") or -99) > -1.0)
    # (2) transcription
    prefix = os.path.join(out, base)
    if not etape("2_whisper_turbo", [sys.executable, os.path.join(PK, "transcribe.py"), wav, prefix], temps, log): die("transcription échouée")
    mots = prefix + "_mots.json"
    if sum(len(s["words"]) for s in json.load(open(mots))["segments"]) == 0: die("aucun mot reconnu : piste muette ou sans parole ?")
    # (3) Praat, fenêtres de 15 s
    nf = max(1, math.ceil(dur_w / 15.0)); zones = [[f"{k*15:.0f}–{min((k+1)*15, dur_w):.0f} s", k * 15.0, min((k + 1) * 15.0, dur_w)] for k in range(nf)]
    env = dict(os.environ, ECOUTE_CLIPPE="1" if clippe else "0")
    t = time.time(); print("--- 3_praat_prosodie", flush=True)
    r = subprocess.run([sys.executable, os.path.join(PK, "_run.py"), sys.executable, os.path.join(PK, "prosodie.py"), wav, mots, prefix, json.dumps(zones)], capture_output=True, text=True, env=env)
    mes = next((json.loads(l)["MESURE"] for l in r.stdout.splitlines()[::-1] if l.startswith('{"MESURE"')), {})
    log.write(f"===== 3_praat_prosodie\n{r.stdout[-3000:]}\n{r.stderr}\n"); temps["3_praat_prosodie"] = {"s": round(time.time() - t, 2), "ram_pic_mb": mes.get("ram_pic_mb"), "exit": r.returncode}
    print(f"    {temps['3_praat_prosodie']['s']} s, RAM pic {mes.get('ram_pic_mb')} MB, exit {r.returncode}")
    if r.returncode != 0: print(r.stderr[-1500:], file=sys.stderr); die("prosodie échouée")
    mesures = prefix + "_mesures.json"
    images = sorted([os.path.join(out, f) for f in os.listdir(out) if f.startswith(base + "_partition_p") and f.endswith(".png")], key=lambda p: int(p.rsplit("_p", 1)[1][:-4])) or [prefix + "_partition.png"]
    # (4) arousal (venv torch, sous-processus)
    aud_json = prefix + "_audeering.json"; arousal_raison = None
    if a.sans_arousal: aud_json = None; arousal_raison = "--sans-arousal demandé"; temps["4_arousal_audeering"] = {"s": 0, "saute": True}
    elif VENV_PY is None:
        arousal_raison = "venv arousal introuvable (ni ECOUTE_VENV_PY, ni " + ", ni ".join(c for c in CANDIDATS_VENV[1:]) + ") — voir README §3"
        print(f"    {arousal_raison} : étape 4 sautée", file=sys.stderr); aud_json = None; temps["4_arousal_audeering"] = {"s": 0, "saute": True}
    else:
        ok4 = etape("4_arousal_audeering", [VENV_PY, os.path.join(PK, "arousal_windows.py"), wav, "--models", "audeering", "--no-plot", "--out", prefix + "_audeering"], temps, log)
        err = None
        try:
            J = json.load(open(aud_json)) if os.path.exists(aud_json) else {}
            err = (J.get("infos", {}).get("audeering") or {}).get("error"); ok_json = bool(J.get("models", {}).get("audeering"))
            if err and len(err) > 160: err = err[:160] + "… (message complet dans journal.log / " + os.path.basename(aud_json) + ")"
        except Exception as e: ok_json = False; err = f"JSON illisible ({e!r})"
        if not ok4 or not ok_json:   # relecture : modele non charge -> JSON avec models vide et exit 0 -> KeyError tardif ; ici saut PROPRE et explique
            arousal_raison = "modèle audeering non chargé dans le venv" + (f" : {err}" if err else "") + " (cache HF absent / hors ligne / torch ? voir README §3-4)"
            print(f"    AROUSAL NON CALCULÉ — {arousal_raison}", file=sys.stderr); aud_json = None
    if aud_json and not os.path.exists(aud_json): aud_json = None
    # (5) rapport Praat + fusion
    t = time.time(); r = subprocess.run([sys.executable, os.path.join(PK, "rapport.py"), mesures], capture_output=True, text=True)
    if r.returncode == 0: shutil.move(prefix + "_RAPPORT.txt", os.path.join(out, "RAPPORT-PROSODIE.txt"))
    temps["5a_rapport_praat"] = {"s": round(time.time() - t, 2), "exit": r.returncode}
    t = time.time(); import fusion
    temps_courts = {k: v["s"] for k, v in temps.items()}
    md = fusion.fusionner(wav, mots, mesures, aud_json, cap_json if cap else None, out, a.profil, src, temps_courts, images, arousal_raison)
    if arousal_raison: print(f"    (rapport : arousal non calculé — {arousal_raison})", file=sys.stderr)
    temps["5b_fusion"] = {"s": round(time.time() - t, 2)}
    temps["TOTAL"] = {"s": round(time.time() - T0, 2)}
    json.dump({"fichier": src, "duree_s": dur_w, "temps": temps, "note": "machine partagée (4 cœurs, autres agents actifs), RAM pic = ru_maxrss du sous-processus"}, open(os.path.join(out, "temps.json"), "w"), indent=1, ensure_ascii=False)
    print("\n" + md)
    print("TEMPS : " + " | ".join(f"{k} {v['s']} s" + (f" ({v['ram_pic_mb']} MB)" if v.get("ram_pic_mb") else "") for k, v in temps.items()))
    print(f"==> {os.path.join(out, 'RAPPORT-ECOUTE.md')}")

if __name__ == "__main__": main()
