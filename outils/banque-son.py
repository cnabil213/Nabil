#!/usr/bin/env python3
"""banque-son : la banque de sons de Nabil, dans le dépôt, réutilisable à chaque montage.

    python3 outils/banque-son.py ajouter <audio ou vidéo> --nom doumbe-jordan-tes-mort \
        --desc "Doumbè à Zébo, pesée : « Jordan, t'es mort »" [--debut 12.3 --fin 14.1] [--tags mma,menace]
    python3 outils/banque-son.py lister

`ajouter` prend n'importe quel fichier (mp3, m4a, wav, mp4, mov…), en extrait le passage demandé,
retire le silence au début et à la fin (sinon le son tombe en retard sur son timecode), cale la
crête à -3 dBFS, et l'enregistre en WAV 48 kHz dans banque-son/. Le catalogue (JSON + tableau du
README) est régénéré à chaque ajout : c'est lui que Claude lit pour choisir un son.
"""
import argparse, json, os, re, subprocess, sys, unicodedata

import numpy as np
import soundfile as sf

ICI = os.path.dirname(os.path.abspath(__file__))
BANQUE = os.path.join(os.path.dirname(ICI), "banque-son")
CATALOGUE = os.path.join(BANQUE, "catalogue.json")
README = os.path.join(BANQUE, "README.md")
SR = 48000
SEUIL_SILENCE_DB = -40.0   # sous ce niveau (par rapport à la crête), c'est du silence à retirer
PRE_ROLL_S = 0.03          # on garde 30 ms avant l'attaque : un plosif coupé net, ça s'entend
POST_ROLL_S = 0.06
CRETE_DB = -3.0


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def slug(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "son"


def charger_catalogue():
    if os.path.exists(CATALOGUE):
        with open(CATALOGUE, encoding="utf-8") as fh:
            return json.load(fh)
    return []


def sauver_catalogue(cat):
    cat.sort(key=lambda e: e["nom"])
    with open(CATALOGUE, "w", encoding="utf-8") as fh:
        json.dump(cat, fh, ensure_ascii=False, indent=1)
    ecrire_readme(cat)


def ecrire_readme(cat):
    L = ["# Banque de sons", "",
         "Les sons de Nabil, prêts à poser : silences retirés, crête à −3 dBFS, WAV 48 kHz.",
         "Claude choisit dans ce catalogue à chaque montage et les pose dans les trous de la parole",
         "(`outils/sonoriser.py`). Ajouter un son : `python3 outils/banque-son.py ajouter <fichier> --nom <slug> --desc \"…\"`.",
         "", "Clips courts uniquement (quelques secondes) : c'est un dépôt git, pas un disque dur.", ""]
    if not cat:
        L += ["_Vide pour l'instant — envoie les clips, ils apparaîtront ici._", ""]
    else:
        L += ["| Son | Durée | Ce que c'est | Quand l'utiliser | Tags |", "| :--- | ---: | :--- | :--- | :--- |"]
        for e in cat:
            L.append(f"| `{e['fichier']}` | {e['duree_s']:.2f} s | {e['desc']} | {e.get('usage') or '—'} | {', '.join(e.get('tags', [])) or '—'} |")
        L.append("")
        L.append("Niveaux (RMS) : " + " · ".join(f"{e['nom']} {e['rms_dbfs']:.0f} dBFS" for e in cat))
        L.append("")
    L += ["## Poser un son", "",
          "```bash", "python3 outils/sonoriser.py MONTAGE.mp4 -o SONORISE.mp4 --son 28.28:banque-son/<fichier>:-1", "```", "",
          "L'écart (`-1`) est relatif à la voix : `0` même niveau, `-3` dessous, `+2` au-dessus.",
          "Le son démarre exactement au timecode donné : la banque a déjà retiré le silence de tête.", ""]
    with open(README, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))


def extraire(source, debut, fin, sortie):
    """Passage demandé -> WAV 48 kHz float, canaux conservés (mono reste mono)."""
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if debut is not None:
        cmd += ["-ss", str(debut)]
    cmd += ["-i", source]
    if fin is not None:
        cmd += ["-to", str(fin - (debut or 0))]
    cmd += ["-vn", "-ar", str(SR), "-c:a", "pcm_f32le", sortie]
    r = run(cmd)
    if r.returncode != 0 or not os.path.exists(sortie):
        sys.exit(f"ERREUR : extraction impossible\n{r.stderr.strip()[-800:]}")


def nettoyer(x, sr):
    """Retire le silence aux deux bouts, garde un pré-roll, cale la crête, pose des fondus."""
    mono = x if x.ndim == 1 else x.mean(axis=1)
    crete = np.abs(mono).max()
    if crete <= 0:
        sys.exit("ERREUR : le passage est muet")
    seuil = crete * 10 ** (SEUIL_SILENCE_DB / 20)
    fort = np.where(np.abs(mono) > seuil)[0]
    a = max(int(fort[0] - PRE_ROLL_S * sr), 0)
    b = min(int(fort[-1] + POST_ROLL_S * sr), len(mono))
    y = x[a:b].astype(np.float32)
    y = y / np.abs(y).max() * 10 ** (CRETE_DB / 20)
    f = int(0.003 * sr)
    rampe = np.linspace(0, 1, f, dtype=np.float32)
    if y.ndim == 1:
        y[:f] *= rampe; y[-f:] *= rampe[::-1]
    else:
        y[:f] *= rampe[:, None]; y[-f:] *= rampe[::-1][:, None]
    return y, a / sr, (len(mono) - b) / sr


def ajouter(a):
    if not os.path.isfile(a.source):
        sys.exit(f"ERREUR : fichier introuvable : {a.source}")
    if (a.debut is None) != (a.fin is None):
        sys.exit("ERREUR : --debut et --fin vont ensemble")
    if a.debut is not None and a.fin <= a.debut:
        sys.exit("ERREUR : --fin doit suivre --debut")
    nom = slug(a.nom)
    os.makedirs(BANQUE, exist_ok=True)
    dest = os.path.join(BANQUE, nom + ".wav")
    cat = charger_catalogue()
    if any(e["nom"] == nom for e in cat) and not a.force:
        sys.exit(f"ERREUR : « {nom} » existe déjà (--force pour remplacer)")

    tmp = dest + ".brut.wav"
    extraire(a.source, a.debut, a.fin, tmp)
    x, sr = sf.read(tmp, dtype="float32")
    os.remove(tmp)
    y, coupe_debut, coupe_fin = nettoyer(x, sr)
    sf.write(dest, y, sr, subtype="PCM_16")

    mono = y if y.ndim == 1 else y.mean(axis=1)
    entree = {
        "nom": nom, "fichier": nom + ".wav", "desc": a.desc, "usage": a.usage or "",
        "tags": [t.strip() for t in (a.tags or "").split(",") if t.strip()],
        "duree_s": round(len(mono) / sr, 2),
        "rms_dbfs": round(float(20 * np.log10(np.sqrt((mono ** 2).mean()) + 1e-9)), 1),
        "crete_dbfs": CRETE_DB, "canaux": 1 if y.ndim == 1 else y.shape[1],
        "source": os.path.basename(a.source),
        "passage": [a.debut, a.fin] if a.debut is not None else None,
    }
    cat = [e for e in cat if e["nom"] != nom] + [entree]
    sauver_catalogue(cat)
    print(f"✅ banque-son/{nom}.wav — {entree['duree_s']:.2f} s, RMS {entree['rms_dbfs']:.1f} dBFS, "
          f"{entree['canaux']} canal/aux")
    print(f"   silence retiré : {coupe_debut:.2f} s en tête, {coupe_fin:.2f} s en queue")
    print(f"   {len(cat)} son(s) au catalogue → banque-son/README.md")
    print(f"   poser :  --son <temps>:banque-son/{nom}.wav:-1")


def lister(a):
    cat = charger_catalogue()
    if not cat:
        print("Banque vide."); return
    for e in cat:
        print(f"  {e['fichier']:36s} {e['duree_s']:5.2f} s  {e['rms_dbfs']:6.1f} dBFS  {e['desc']}"
              + (f"  [{', '.join(e['tags'])}]" if e.get("tags") else ""))


SOUNDBOARD = next((d for d in (os.environ.get("SOUNDBOARD_DIR", ""), "/home/user/3kh0/soundboard",
                                os.path.expanduser("~/3kh0/soundboard")) if d and os.path.isdir(d)),
                  "/home/user/3kh0/soundboard")   # clone anonyme : voir README (git clone --depth 1)


def importer(a):
    """Cherche un son du soundboard 3kh0 par son nom (sounds.json) et l'ajoute à la banque."""
    sj = os.path.join(SOUNDBOARD, "sounds.json")
    if not os.path.exists(sj):
        sys.exit("ERREUR : soundboard absent — cloner d'abord :\n"
                 "  GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/3kh0/soundboard ~/3kh0/soundboard")
    d = json.load(open(sj, encoding="utf-8"))
    items = d if isinstance(d, list) else list(d.values())[0]
    items = [it for it in items if isinstance(it, dict) and it.get("mp3")]
    q = a.recherche.lower()
    hits = [it for it in items if q in it["name"].lower() or q in os.path.basename(it["mp3"]).lower()]
    if not hits:
        sys.exit(f"ERREUR : aucun son du soundboard ne contient « {a.recherche} » (lister : --lister)")
    if len(hits) > 1 and not a.premier:
        print(f"{len(hits)} sons correspondent — précise, ou --premier :")
        for it in hits: print(f"   {it['name']!r:44s} {it['mp3']}")
        sys.exit(2)
    it = hits[0]
    a.source = os.path.join(SOUNDBOARD, it["mp3"])
    a.nom = a.nom or it["name"]
    a.desc = a.desc or f"{it['name']} (soundboard 3kh0)"
    a.debut = a.fin = None
    ajouter(a)


def retirer(a):
    nom = slug(a.nom); cat = charger_catalogue()
    if not any(e["nom"] == nom for e in cat):
        sys.exit(f"ERREUR : « {nom} » n'est pas au catalogue")
    f = os.path.join(BANQUE, nom + ".wav")
    if os.path.exists(f):
        os.remove(f)
    sauver_catalogue([e for e in cat if e["nom"] != nom])
    print(f"✅ « {nom} » retiré ({len(cat) - 1} son(s) restant(s))")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("ajouter", help="nettoyer un clip et l'ajouter au catalogue")
    s.add_argument("source"); s.add_argument("--nom", required=True); s.add_argument("--desc", required=True)
    s.add_argument("--usage", default=None, help="quand l'utiliser (ex. « après une menace, une punchline de combat »)")
    s.add_argument("--tags", default=None, help="mots-clés séparés par des virgules")
    s.add_argument("--debut", type=float, default=None, help="début du passage dans la source, en s")
    s.add_argument("--fin", type=float, default=None, help="fin du passage dans la source, en s")
    s.add_argument("--force", action="store_true")
    s.set_defaults(fn=ajouter)
    l = sub.add_parser("lister", help="afficher le catalogue"); l.set_defaults(fn=lister)
    r = sub.add_parser("retirer", help="retirer un son du catalogue"); r.add_argument("nom"); r.set_defaults(fn=retirer)
    i = sub.add_parser("importer", help="importer un son du soundboard 3kh0 (208 mèmes) par son nom")
    i.add_argument("recherche"); i.add_argument("--nom", default=None); i.add_argument("--desc", default=None)
    i.add_argument("--usage", default=None); i.add_argument("--tags", default="soundboard")
    i.add_argument("--premier", action="store_true", help="prendre le premier si plusieurs correspondent")
    i.add_argument("--force", action="store_true"); i.set_defaults(fn=importer)
    a = p.parse_args(); a.fn(a)


if __name__ == "__main__":
    main()
