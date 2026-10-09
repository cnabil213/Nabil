#!/usr/bin/env python3
"""icloud : transforme un lien de partage iCloud Drive en URL de telechargement direct.

Usage : python3 outils/icloud.py "https://www.icloud.com/iclouddrive/0abCdEf..."
        -> ecrit sur stdout l'URL directe (et le nom du fichier sur stderr)

Pourquoi ce detour : un lien iCloud est une page JavaScript. `curl` dessus recupere du HTML,
pas la video. Mais iCloud expose une API publique de resolution (CloudKit) qui, a partir du
« shortGUID » contenu dans le lien, rend le nom du fichier, sa taille et une URL signee.

**iCloud Drive, PAS Album partage.** Un album partage iCloud re-encode et rabote les videos
(Apple les replafonne) : c'est exactement le probleme du rush Snapchat du 12/09, et
`CLAUDE.md` §5 est clair — un montage ne peut pas etre plus net que son rush. Le chemin qui
conserve l'original, c'est Photos -> « Enregistrer dans Fichiers » -> iCloud Drive, puis
partager CE fichier.
"""
import base64, json, re, sys, urllib.parse, urllib.request

API = ("https://ckdatabasews.icloud.com/database/1/com.apple.cloudkit/production/public"
       "/records/resolve")


def die(msg, code=1):
    print(f"ERREUR : {msg}", file=sys.stderr); sys.exit(code)


def short_guid(lien):
    """Le shortGUID est le segment apres /iclouddrive/, avant un éventuel # ou ?."""
    m = re.search(r"/iclouddrive/#?([A-Za-z0-9_\-]+)", lien)
    if not m:
        m = re.search(r"icloud\.com/?#?([A-Za-z0-9_\-]{10,})", lien)
    return m.group(1) if m else None


def resoudre(lien, timeout=30):
    if "sharedalbum" in lien or "share.icloud.com/photos" in lien:
        die("c'est un lien d'ALBUM PARTAGÉ iCloud, pas un lien de fichier.\n"
            "         Apple ré-encode et rabote les vidéos des albums partagés — le rush\n"
            "         arriverait dégradé, et un montage n'est jamais plus net que son rush.\n"
            "         À faire à la place, dans Photos :\n"
            "           Partager → « Enregistrer dans Fichiers » → iCloud Drive\n"
            "           puis, dans Fichiers : appui long sur le fichier → Partager → Copier le lien", 2)

    g = short_guid(lien)
    if not g:
        die(f"je ne trouve pas de shortGUID dans ce lien : {lien}\n"
            "         Attendu : https://www.icloud.com/iclouddrive/<GUID>#nom", 2)

    corps = json.dumps({"shortGUIDs": [{"value": g}]}).encode()
    req = urllib.request.Request(API, data=corps, method="POST", headers={
        "Content-Type": "application/json",
        "Origin": "https://www.icloud.com",
        "User-Agent": "Mozilla/5.0"})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=timeout))
    except Exception as e:
        die(f"l'API iCloud n'a pas répondu : {e}")

    res = (d.get("results") or [{}])[0]
    if res.get("serverErrorCode") or res.get("reason"):
        die(f"iCloud refuse ce lien : {res.get('reason') or res.get('serverErrorCode')}\n"
            "         Le partage est-il bien actif, et réglé sur « Tout utilisateur disposant du lien » ?")

    rec = res.get("rootRecord") or {}
    champs = rec.get("fields") or {}
    fc = (champs.get("fileContent") or {}).get("value") or {}
    url = fc.get("downloadURL")
    if not url:
        die("réponse iCloud sans URL de téléchargement — le lien pointe peut-être sur un dossier.\n"
            f"         Champs reçus : {', '.join(sorted(champs)) or '(aucun)'}")

    nom = None
    brut = (champs.get("filename") or {}).get("value")
    if brut:
        try:
            nom = base64.b64decode(brut).decode("utf-8", "replace")
        except Exception:
            nom = str(brut)
    nom = nom or f"rush-{g[:8]}.mp4"

    # l'URL signee porte un gabarit ${f} a remplacer par le nom du fichier
    url = url.replace("${f}", urllib.parse.quote(nom))

    taille = fc.get("size")
    print(f"fichier : {nom}" + (f" ({int(taille)/1e6:.1f} Mo)" if taille else ""), file=sys.stderr)
    return url, nom


if __name__ == "__main__":
    if len(sys.argv) < 2:
        die("usage : python3 outils/icloud.py \"<lien iCloud Drive>\"", 2)
    u, n = resoudre(sys.argv[1])
    print(u)
