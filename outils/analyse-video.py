#!/usr/bin/env python3
"""
Analyse une vidéo short-form pour la relecture éditoriale.

Produit :
  - la transcription horodatée (mot par mot)
  - l'analyse du hook (les 4 premieres secondes, regle non negociable)
  - les blancs / temps morts a couper
  - le debit de parole
  - des images extraites, denses sur le hook, pour la relecture visuelle

Usage :
    python3 outils/analyse-video.py ma-video.mp4 [-o dossier_sortie] [-m small]
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

# Un blanc au-dela de ce seuil est signale comme temps mort a couper.
SEUIL_BLANC = 0.45
# Duree du hook : la fenetre ou tout se joue.
FENETRE_HOOK = 4.0


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def sonde(video):
    """Metadonnees via ffprobe."""
    r = run(["ffprobe", "-v", "quiet", "-print_format", "json",
             "-show_format", "-show_streams", video])
    if r.returncode != 0:
        sys.exit(f"ffprobe a echoue sur {video}\n{r.stderr}")
    data = json.loads(r.stdout)
    v = next((s for s in data["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in data["streams"] if s["codec_type"] == "audio"), None)
    if v is None:
        sys.exit("Pas de piste video dans ce fichier.")

    num, den = (v.get("avg_frame_rate") or "0/1").split("/")
    fps = float(num) / float(den) if float(den) else 0.0
    return {
        "duree": float(data["format"]["duration"]),
        "taille_mo": float(data["format"]["size"]) / 1_048_576,
        "largeur": v["width"],
        "hauteur": v["height"],
        "fps": fps,
        "codec": v["codec_name"],
        "audio": a["codec_name"] if a else None,
    }


def extrait_audio(video, sortie):
    """Piste audio 16 kHz mono, le format attendu par le modele."""
    r = run(["ffmpeg", "-y", "-v", "error", "-i", video,
             "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", sortie])
    if r.returncode != 0:
        sys.exit(f"Extraction audio impossible :\n{r.stderr}")
    return sortie


def transcrit(wav, taille_modele):
    from faster_whisper import WhisperModel
    modele = WhisperModel(taille_modele, device="cpu", compute_type="int8")
    segments, info = modele.transcribe(
        wav, language="fr", word_timestamps=True, vad_filter=False,
    )
    segs = []
    for s in segments:
        segs.append({
            "debut": s.start,
            "fin": s.end,
            "texte": s.text.strip(),
            "mots": [{"mot": w.word.strip(), "debut": w.start, "fin": w.end}
                     for w in (s.words or [])],
        })
    return segs, info



def detecte_silences(wav, seuil_db=-32, duree_min=SEUIL_BLANC):
    """Silences reels mesures sur le signal audio.

    Les timestamps de Whisper etirent les mots pour absorber les blancs :
    ils sous-estiment donc les temps morts. On mesure l'acoustique a la place.
    """
    r = run(["ffmpeg", "-v", "info", "-i", wav, "-af",
             f"silencedetect=noise={seuil_db}dB:d={duree_min}", "-f", "null", "-"])
    silences, debut = [], None
    for ligne in r.stderr.splitlines():
        m = re.search(r"silence_start:\s*(-?[\d.]+)", ligne)
        if m:
            debut = max(float(m.group(1)), 0.0)
        m = re.search(r"silence_end:\s*([\d.]+)", ligne)
        if m and debut is not None:
            fin = float(m.group(1))
            silences.append({"debut": debut, "fin": fin, "duree": fin - debut})
            debut = None
    return silences


def analyse_rythme(segments, duree, silences):
    mots = [m for s in segments for m in s["mots"]]
    if not mots:
        return None

    # Temps mort avant le premier mot : le tueur de hook numero un.
    # Mesure acoustique si un silence ouvre la video, sinon repli sur Whisper.
    retard = mots[0]["debut"]
    for s in silences:
        if s["debut"] <= 0.15:
            retard = s["fin"]
            break

    # Ce qui est reellement dit dans la fenetre du hook.
    hook = [m["mot"] for m in mots if m["debut"] < FENETRE_HOOK]

    # Blancs internes : silences acoustiques, hors silence d'amorce et de fin.
    blancs = []
    for s in silences:
        if s["debut"] <= 0.15 or s["fin"] >= duree - 0.15:
            continue  # amorce et queue traitees a part
        avant = max((m for m in mots if m["fin"] <= s["debut"] + 0.25),
                    key=lambda m: m["fin"], default=None)
        apres = min((m for m in mots if m["debut"] >= s["fin"] - 0.25),
                    key=lambda m: m["debut"], default=None)
        blancs.append({"a": s["debut"], "duree": s["duree"],
                       "avant": avant["mot"] if avant else "…",
                       "apres": apres["mot"] if apres else "…"})

    # Queue morte : du dernier son a la fin du fichier.
    queue = next((s["duree"] for s in silences if s["fin"] >= duree - 0.15), 0.0)

    silence_total = sum(s["duree"] for s in silences)
    parle = max(duree - silence_total, 0.0)
    return {
        "nb_mots": len(mots),
        "retard_hook": retard,
        "mots_hook": hook,
        "blancs": sorted(blancs, key=lambda b: -b["duree"]),
        "temps_mort_total": sum(b["duree"] for b in blancs),
        "queue_morte": queue,
        "recuperable": retard + queue + sum(b["duree"] for b in blancs),
        "debit": len(mots) / (duree / 60) if duree else 0,
        "taux_parole": parle / duree if duree else 0,
    }


def extrait_images(video, duree, dossier):
    """Dense sur le hook (toutes les 0,5 s), puis reparti sur le reste."""
    os.makedirs(dossier, exist_ok=True)
    instants = [round(t * 0.5, 1) for t in range(int(FENETRE_HOOK * 2) + 1)]
    reste = duree - FENETRE_HOOK
    if reste > 0:
        pas = max(reste / 6, 3.0)
        t = FENETRE_HOOK + pas
        while t < duree - 0.3:
            instants.append(round(t, 1))
            t += pas
    fichiers = []
    for t in instants:
        if t >= duree:
            continue
        nom = os.path.join(dossier, f"t{t:06.2f}s.jpg".replace(".", "_", 1))
        r = run(["ffmpeg", "-y", "-v", "error", "-ss", str(t), "-i", video,
                 "-frames:v", "1", "-q:v", "3", nom])
        if r.returncode == 0 and os.path.exists(nom):
            fichiers.append((t, nom))
    return fichiers


def rapport(video, meta, segments, ryt, images, chemin):
    L = []
    A = L.append
    nom = os.path.basename(video)
    A(f"# Analyse — {nom}\n")

    A("## Fiche technique\n")
    A("| | |")
    A("| :--- | :--- |")
    A(f"| Durée | **{meta['duree']:.1f} s** |")
    ratio = meta["largeur"] / meta["hauteur"]
    verdict = "✅ vertical 9:16" if ratio < 0.65 else "⚠️ **pas vertical** — à recadrer pour TikTok"
    A(f"| Format | {meta['largeur']}×{meta['hauteur']} — {verdict} |")
    A(f"| FPS | {meta['fps']:.2f} |")
    A(f"| Codec | {meta['codec']} / audio {meta['audio'] or 'AUCUN'} |")
    A(f"| Poids | {meta['taille_mo']:.1f} Mo |\n")

    if not ryt:
        A("> ⚠️ Aucune parole detectee. Verifier la piste audio.\n")
    else:
        A("## Le hook (les 4 premières secondes)\n")
        r = ryt["retard_hook"]
        if r > 0.8:
            A(f"🔴 **{r:.2f} s de silence avant le premier mot.** C'est autant de hook perdu — à couper au montage.\n")
        elif r > 0.3:
            A(f"🟡 {r:.2f} s avant le premier mot. Acceptable, mais ça peut se resserrer.\n")
        else:
            A(f"✅ Attaque à {r:.2f} s. Tu rentres direct dedans.\n")
        A(f"**Ce qui est dit dans les 4 premières secondes :**\n")
        A(f"> {' '.join(ryt['mots_hook']) if ryt['mots_hook'] else '(rien)'}\n")

        A("## Rythme\n")
        A("| Indicateur | Valeur | Lecture |")
        A("| :--- | :--- | :--- |")
        d = ryt["debit"]
        lect_d = "✅ rythme soutenu" if d >= 170 else ("🟡 un peu posé pour du short" if d >= 130 else "🔴 trop lent, ça va scroller")
        A(f"| Débit | {d:.0f} mots/min | {lect_d} |")
        tp = ryt["taux_parole"] * 100
        A(f"| Temps de parole | {tp:.0f} % | {'✅' if tp >= 65 else '🟡 beaucoup de vide'} |")
        tm = ryt["temps_mort_total"]
        A(f"| Blancs internes | {tm:.1f} s | {'✅ propre' if tm < 1.0 else '🔴 à couper'} |")
        A(f"| Mots | {ryt['nb_mots']} | |\n")
        rec = ryt["recuperable"]
        if rec >= 0.8:
            pct = rec / meta["duree"] * 100
            A(f"> ⏱️ **{rec:.1f} s récupérables au montage** ({pct:.0f} % de la vidéo) : "
              f"{ryt['retard_hook']:.1f} s d'amorce + {tm:.1f} s de blancs + "
              f"{ryt['queue_morte']:.1f} s de queue. Sur du short, c'est énorme.\n")

        if ryt["blancs"]:
            A(f"### Blancs à couper (≥ {SEUIL_BLANC} s)\n")
            A("| À | Durée | Entre |")
            A("| :--- | :--- | :--- |")
            for b in ryt["blancs"][:12]:
                A(f"| {b['a']:.2f} s | **{b['duree']:.2f} s** | « …{b['avant']} » → « {b['apres']}… » |")
            A("")

    A("## Transcription horodatée\n")
    for s in segments:
        A(f"**[{s['debut']:6.2f} → {s['fin']:6.2f}]**  {s['texte']}\n")

    if images:
        A("## Images extraites\n")
        A(f"{len(images)} images dans `{os.path.basename(os.path.dirname(images[0][1]))}/` — ")
        A("denses sur le hook (toutes les 0,5 s) puis réparties sur le reste.\n")
        for t, f in images:
            A(f"- `{t:.1f} s` → `{os.path.basename(f)}`")
        A("")

    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))
    return chemin


def main():
    p = argparse.ArgumentParser(description="Analyse une video short-form.")
    p.add_argument("video")
    p.add_argument("-o", "--sortie", default=None)
    p.add_argument("-m", "--modele", default="small",
                   help="tiny/base/small/medium (defaut: small)")
    args = p.parse_args()

    if not os.path.exists(args.video):
        sys.exit(f"Fichier introuvable : {args.video}")
    for outil in ("ffmpeg", "ffprobe"):
        if not shutil.which(outil):
            sys.exit(f"{outil} manquant. Installer avec : apt-get install -y ffmpeg")

    base = os.path.splitext(os.path.basename(args.video))[0]
    sortie = args.sortie or os.path.join(os.path.dirname(args.video) or ".",
                                         f"analyse-{base}")
    os.makedirs(sortie, exist_ok=True)

    print(f"[1/5] Sonde       {args.video}")
    meta = sonde(args.video)
    print(f"      {meta['duree']:.1f}s · {meta['largeur']}x{meta['hauteur']} · {meta['taille_mo']:.1f} Mo")

    print("[2/5] Audio")
    wav = extrait_audio(args.video, os.path.join(sortie, "audio.wav"))

    print(f"[3/5] Transcription (modele '{args.modele}')")
    segments, _ = transcrit(wav, args.modele)
    print(f"      {len(segments)} segments")

    print("[4/5] Rythme")
    silences = detecte_silences(wav)
    ryt = analyse_rythme(segments, meta["duree"], silences)
    print(f"      {len(silences)} silences detectes")

    print("[5/5] Images")
    images = extrait_images(args.video, meta["duree"], os.path.join(sortie, "images"))
    print(f"      {len(images)} images")

    chemin = rapport(args.video, meta, segments, ryt, images,
                     os.path.join(sortie, "RAPPORT.md"))
    os.remove(wav)
    print(f"\n==> {chemin}")


if __name__ == "__main__":
    main()
