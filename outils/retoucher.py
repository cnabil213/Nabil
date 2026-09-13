#!/usr/bin/env python3
"""retoucher : efface un defaut de peau (bouton, rougeur) sur TOUTE une video, en le suivant sur le visage.

    python3 outils/retoucher.py rush.mov -o SORTIE.mp4 --garder 6.40-12.20 40.20-50.10 \
        --repere 346:299:840 --rayon 11 --audio MONTAGE.mp4

Le point se donne UNE fois : `--repere IMAGE:X:Y`, les coordonnees du defaut sur l'image IMAGE du
montage (image = numero dans le montage coupe, pas dans le rush). Le visage est detecte a chaque
image (MediaPipe FaceLandmarker, 478 points) et le defaut est replace dans le repere de trois points
du maillage : il suit la tete quand elle tourne, s'approche ou s'eloigne, sans derive.

La correction est un « spot heal » : la tache est reconstruite a partir de la peau autour (inpainting),
puis le grain de l'image est remis par-dessus pour ne pas laisser un disque lisse. Le masque exclut
les pixels sombres (monture, narine, ombre) : la retouche ne mord jamais sur un contour.

Un SEUL reencodage : la coupe, la retouche et l'encodage se font dans la meme passe (decodage ->
python -> libx264). La plage de couleur de la source est conservee (voir monter.py).
"""
import argparse, json, os, subprocess, sys

CRF, PRESET = 19, "slow"


def run(c, **k):
    return subprocess.run(c, capture_output=True, text=True, **k)


def sonde(f):
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", f])
    if r.returncode != 0:
        sys.exit(f"ERREUR : ffprobe ne lit pas {f}\n{r.stderr.strip()}")
    d = json.loads(r.stdout)
    v = next((s for s in d["streams"] if s["codec_type"] == "video"), None)
    a = next((s for s in d["streams"] if s["codec_type"] == "audio"), None)
    return v, a, float(d["format"]["duration"])


def taille_affichee(v):
    w, h = int(v["width"]), int(v["height"])
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    return (h, w) if abs(rot) % 180 == 90 else (w, h)


def soigne_plan(plan, cx, cy, R, grain, seuil_sombre=True):
    """Repare un disque sur UN plan 8 bits (Y, U ou V) a partir de ce qui l'entoure.
    Le masque exclut ce qui est nettement plus sombre que la peau autour (monture, narine, ombre) :
    la retouche ne mord jamais sur un contour."""
    import numpy as np, cv2
    H, W = plan.shape[:2]
    x0, y0 = int(cx - 3 * R), int(cy - 3 * R)
    x1, y1 = int(cx + 3 * R), int(cy + 3 * R)
    if x0 < 0 or y0 < 0 or x1 > W or y1 > H or (x1 - x0) < 6 or (y1 - y0) < 6:
        return None
    z = plan[y0:y1, x0:x1]
    L = z.astype(np.float32)
    ell = np.zeros(z.shape[:2], np.uint8)
    cv2.ellipse(ell, (int(cx - x0), int(cy - y0)), (max(1, int(R)), max(1, int(R * 0.85))), 0, 0, 360, 255, -1)
    couronne = cv2.dilate(ell, np.ones((max(3, int(R)), max(3, int(R))), np.uint8)) - ell
    if seuil_sombre and (couronne > 0).any():
        med = float(np.median(L[couronne > 0])); ec = float(np.std(L[couronne > 0]))
        masque = ((ell > 0) & (L > med - 1.6 * ec)).astype(np.uint8)
    else:
        masque = (ell > 0).astype(np.uint8)
    if masque.sum() < 4:
        return None
    repare = cv2.inpaint(z, cv2.dilate(masque, np.ones((3, 3), np.uint8)), 5, cv2.INPAINT_TELEA)
    if grain > 0:
        hf = z.astype(np.float32) - cv2.GaussianBlur(z, (0, 0), 1.2).astype(np.float32)
        repare = np.clip(repare.astype(np.float32) + grain * hf, 0, 255)
    alpha = cv2.GaussianBlur(masque.astype(np.float32) * 255, (0, 0), max(0.8, R * 0.42)) / 255.0
    m = float(alpha.max())
    if m <= 1e-6:
        return None
    alpha = np.clip(alpha / m, 0, 1)
    return (x0, y0, x1, y1, (alpha * repare.astype(np.float32) + (1 - alpha) * z.astype(np.float32)).astype(np.uint8))


def soigne_yuv(Y, U, V, cx, cy, R, grain):
    """Pose la retouche sur la luminance et sur les deux plans de couleur (demi-resolution).
    Tout le reste de l'image n'est jamais touche : les octets decodes repartent tels quels
    vers l'encodeur, donc aucune perte hors de la tache."""
    r = soigne_plan(Y, cx, cy, R, grain)
    if r is None:
        return False
    x0, y0, x1, y1, patch = r
    Y[y0:y1, x0:x1] = patch
    for P in (U, V):
        rc = soigne_plan(P, cx / 2.0, cy / 2.0, max(2.0, R / 2.0), 0.0, seuil_sombre=False)
        if rc is not None:
            a, b, c, d, pc = rc
            P[b:d, a:c] = pc
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("fichier")
    p.add_argument("-o", "--sortie", required=True)
    p.add_argument("--repere", required=True, metavar="IMAGE:X:Y", help="où est le défaut, sur une image du montage")
    p.add_argument("--garder", nargs="*", default=[], metavar="DEBUT-FIN", help="segments à garder (comme monter.py)")
    p.add_argument("--rayon", type=float, default=11.0, help="rayon de la retouche en pixels (défaut 11)")
    p.add_argument("--grain", type=float, default=0.55, help="part du grain d'origine remise (0 = lisse, 1 = tout)")
    p.add_argument("--audio", help="prendre la piste son de ce fichier (copiée telle quelle)")
    p.add_argument("--crf", type=int, default=CRF)
    p.add_argument("--hevc", action="store_true", help="H.265 : même qualité qu'en H.264 pour ~40 %% de débit en moins")
    p.add_argument("--suivi", metavar="FICHIER.json", help="cache du suivi du visage (réutilisé d'un encodage à l'autre)")
    p.add_argument("--preset", default=PRESET)
    p.add_argument("--apercu", metavar="DOSSIER", help="écrire des avant/après (PNG) au lieu d'encoder")
    a = p.parse_args()

    try:
        n_ref, x_ref, y_ref = a.repere.split(":")
        n_ref, x_ref, y_ref = int(n_ref), float(x_ref), float(y_ref)
    except ValueError:
        sys.exit("ERREUR : --repere attendu au format IMAGE:X:Y (ex. 346:299:840)")
    if not os.path.isfile(a.fichier):
        sys.exit(f"ERREUR : fichier introuvable : {a.fichier}")

    import numpy as np, cv2
    import mediapipe as mp
    from mediapipe.tasks import python as mpp
    from mediapipe.tasks.python import vision

    modele = os.environ.get("FACE_LANDMARKER") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "face_landmarker.task")
    if not os.path.isfile(modele):
        sys.exit("ERREUR : modèle de visage absent. Le télécharger une fois :\n"
                 "  curl -sSL -o outils/face_landmarker.task https://storage.googleapis.com/"
                 "mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task")

    v, aud, dur = sonde(a.fichier)
    W, H = taille_affichee(v)
    fps = eval(v.get("r_frame_rate", "30/1")) if "/" in str(v.get("r_frame_rate")) else float(v.get("r_frame_rate"))
    pleine = (v.get("color_range") == "pc") or str(v.get("pix_fmt", "")).startswith("yuvj")
    # On travaille dans l'espace de la source (YUV 4:2:0), jamais en RGB : un aller-retour
    # YUV -> RGB -> YUV reechantillonne la couleur et coute ~5 dB de PSNR (mesure sur le rush du 12/09).
    PIX = "yuvj420p" if pleine else "yuv420p"

    # --- decodage : coupe appliquee ici, pour ne reencoder qu'une fois
    if a.garder:
        segs = []
        for s in a.garder:
            x, b = s.split("-")
            segs.append((float(x), float(b)))
        segs.sort()
        off = float((aud or {}).get("start_time") or 0.0)
        parts = [f"[0:v]trim={x+off:.3f}:{b+off:.3f},setpts=PTS-STARTPTS[v{i}]" for i, (x, b) in enumerate(segs)]
        # fps= en fin de chaine : sans ca le flux brut sort en cadence variable et perd une image
        # par rapport au montage encode (qui, lui, passe par un encodeur en cadence fixe).
        fc = (";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(len(segs)))
              + f"concat=n={len(segs)}:v=1:a=0,fps={fps:g}[v]")
        dec = ["ffmpeg", "-v", "error", "-i", a.fichier, "-filter_complex", fc, "-map", "[v]",
               "-f", "rawvideo", "-pix_fmt", PIX, "-"]
        print(f"Source : {a.fichier} — coupe de {len(segs)} segments appliquée dans la même passe")
    else:
        dec = ["ffmpeg", "-v", "error", "-i", a.fichier, "-vf", f"fps={fps:g}",
               "-f", "rawvideo", "-pix_fmt", PIX, "-"]
        print(f"Source : {a.fichier}")
    print(f"   {W}×{H}, {fps:g} i/s, plage {'complète' if pleine else 'limitée'}")

    fl = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
        base_options=mpp.BaseOptions(model_asset_path=modele),
        running_mode=vision.RunningMode.IMAGE, num_faces=1))

    taille = W * H * 3 // 2          # YUV 4:2:0

    def points(buf):
        yuv = np.frombuffer(buf, np.uint8).reshape(H * 3 // 2, W)
        rgb = cv2.cvtColor(yuv, cv2.COLOR_YUV2RGB_I420)
        r = fl.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
        if not r.face_landmarks:
            return None
        return np.array([[l.x * W, l.y * H] for l in r.face_landmarks[0]], np.float32)

    # ---- passe 1 : suivi du visage sur toutes les images (aucun encodage, aucune ecriture)
    cache = None
    if a.suivi and os.path.isfile(a.suivi):
        C = json.load(open(a.suivi))
        if C.get("fichier") == os.path.abspath(a.fichier) and C.get("garder") == list(a.garder) and C.get("repere") == a.repere:
            cache = C
            print(f"→ passe 1 : suivi relu depuis {a.suivi} ({len(C['pos'])} images)")
        else:
            print(f"   ({a.suivi} ne correspond pas à cette commande : suivi refait)")
    print("→ passe 1 : suivi du visage…" if cache is None else "")
    reperes = []
    n = 0
    pin = None if cache else subprocess.Popen(dec, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=taille * 2)
    while pin is not None:
        buf = pin.stdout.read(taille)
        if not buf or len(buf) < taille:
            break
        reperes.append(points(buf))
        n += 1
        if n % 300 == 0:
            print(f"   {n} images…", flush=True)
    if pin is not None:
        pin.stdout.close(); pin.wait()
    if cache:
        total = len(cache["pos"])
        pos = [None if p is None else (np.array(p[0], np.float32), float(p[1])) for p in cache["pos"]]
        suivies = sum(p is not None for p in pos)
        print(f"   visage suivi sur {suivies}/{total} images (cache)")
    else:
        total = n
    if not cache and (n_ref >= total or reperes[n_ref] is None):
        sys.exit(f"ERREUR : pas de visage détecté sur l'image de repère {n_ref} (montage : {total} images)")
    if not cache:

        P0 = reperes[n_ref]
        d = np.linalg.norm(P0 - np.array([x_ref, y_ref], np.float32), axis=1)
        ANCRES = [int(i) for i in np.argsort(d)[:3]]
        A0 = P0[ANCRES]
        M = np.array([[A0[0][0], A0[1][0], A0[2][0]], [A0[0][1], A0[1][1], A0[2][1]], [1, 1, 1]], np.float64)
        BARY = np.linalg.solve(M, np.array([x_ref, y_ref, 1.0]))
        # echelle de reference : taille du triangle d'ancrage sur l'image de repere
        per0 = float(np.linalg.norm(A0[0] - A0[1]) + np.linalg.norm(A0[1] - A0[2]) + np.linalg.norm(A0[2] - A0[0]))
        print(f"   repère : image {n_ref}, points {ANCRES}, barycentriques {np.round(BARY, 3)}")

        pos = [None] * total
        for i, P in enumerate(reperes):
            if P is None:
                continue
            A = P[ANCRES]
            pos[i] = (BARY[0] * A[0] + BARY[1] * A[1] + BARY[2] * A[2],
                      float(np.linalg.norm(A[0] - A[1]) + np.linalg.norm(A[1] - A[2]) + np.linalg.norm(A[2] - A[0])) / per0)
        # trous courts (flou de bouge) : on interpole entre les deux images encadrantes
        TROU_MAX = 4
        vus = [i for i, p in enumerate(pos) if p is not None]
        comble = 0
        for a_, b_ in zip(vus, vus[1:]):
            if 1 < b_ - a_ <= TROU_MAX + 1:
                for k in range(a_ + 1, b_):
                    t = (k - a_) / (b_ - a_)
                    pos[k] = ((1 - t) * pos[a_][0] + t * pos[b_][0], (1 - t) * pos[a_][1] + t * pos[b_][1])
                    comble += 1
        # lissage median sur 3 images : enleve le tremblement du maillage sans retarder le suivi
        lisse = list(pos)
        for i in range(total):
            f = [pos[j] for j in (i - 1, i, i + 1) if 0 <= j < total and pos[j] is not None]
            if len(f) == 3:
                lisse[i] = (np.median(np.stack([x[0] for x in f]), axis=0), float(np.median([x[1] for x in f])))
        pos = lisse
        suivies = sum(p is not None for p in pos)
        print(f"   visage suivi sur {suivies}/{total} images ({comble} trous comblés, "
              f"{total - suivies} sans visage : pas de retouche sur celles-là)")
        if a.suivi:
            json.dump({"fichier": os.path.abspath(a.fichier), "garder": list(a.garder), "repere": a.repere,
                       "pos": [None if p is None else [[float(p[0][0]), float(p[0][1])], float(p[1])] for p in pos]},
                      open(a.suivi, "w"))
            print(f"   suivi enregistré dans {a.suivi} (réutilisable pour un autre encodage)")

    # ---- passe 2 : retouche + encodage (un seul reencodage)
    if a.apercu:
        os.makedirs(a.apercu, exist_ok=True)
        enc = None
        print(f"→ passe 2 : aperçus avant/après dans {a.apercu} (pas d'encodage)")
    else:
        tags = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                "-color_range", "pc" if pleine else "tv"]
        if a.hevc:
            par = f"colorprim=bt709:transfer=bt709:colormatrix=bt709:range={'full' if pleine else 'limited'}"
            codec = ["-c:v", "libx265", "-crf", str(a.crf), "-preset", a.preset, "-pix_fmt", PIX,
                     "-tag:v", "hvc1", "-x265-params", par] + tags
        else:
            codec = ["-c:v", "libx264", "-crf", str(a.crf), "-preset", a.preset, "-pix_fmt", PIX] + tags
        cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", PIX,
               "-s", f"{W}x{H}", "-r", f"{fps:g}", "-i", "-"]
        if a.audio:
            cmd += ["-i", a.audio, "-map", "0:v", "-map", "1:a", "-c:a", "copy", "-shortest"]
        cmd += codec + ["-movflags", "+faststart", a.sortie]
        enc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"→ passe 2 : retouche et encodage ({'H.265' if a.hevc else 'H.264'} CRF {a.crf} {a.preset}, un seul passage)…")
    pin = subprocess.Popen(dec, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=taille * 2)
    n = 0
    faits = 0
    while True:
        buf = pin.stdout.read(taille)
        if not buf or len(buf) < taille:
            break
        fr = bytearray(buf)                      # octets decodes, modifies seulement sous la retouche
        tab = np.frombuffer(fr, np.uint8)
        Y = tab[: W * H].reshape(H, W)
        U = tab[W * H: W * H + W * H // 4].reshape(H // 2, W // 2)
        V = tab[W * H + W * H // 4:].reshape(H // 2, W // 2)
        p = pos[n] if n < total else None
        if p is not None:
            pt, ech = p
            R = max(3.0, a.rayon * ech)
            if a.apercu:
                px, py = int(round(pt[0])), int(round(pt[1])); m = 46
                yuv = np.frombuffer(bytes(fr), np.uint8).reshape(H * 3 // 2, W)
                av = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420)[max(0, py - m):py + m, max(0, px - m):px + m].copy()
                soigne_yuv(Y, U, V, float(pt[0]), float(pt[1]), R, a.grain)
                yuv2 = np.frombuffer(bytes(fr), np.uint8).reshape(H * 3 // 2, W)
                ap = cv2.cvtColor(yuv2, cv2.COLOR_YUV2BGR_I420)[max(0, py - m):py + m, max(0, px - m):px + m].copy()
                if av.shape == ap.shape and av.size and n % 30 == 0:
                    Z = 6
                    duo = np.hstack([cv2.resize(av, None, fx=Z, fy=Z, interpolation=cv2.INTER_LANCZOS4),
                                     np.full((av.shape[0] * Z, 8, 3), 255, np.uint8),
                                     cv2.resize(ap, None, fx=Z, fy=Z, interpolation=cv2.INTER_LANCZOS4)])
                    cv2.putText(duo, f"AVANT {n/fps:.2f}s", (10, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    cv2.putText(duo, "APRES", (av.shape[1] * Z + 20, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    cv2.imwrite(os.path.join(a.apercu, f"{n:05d}.png"), duo)
            elif soigne_yuv(Y, U, V, float(pt[0]), float(pt[1]), R, a.grain):
                pass
            faits += 1
        if enc:
            enc.stdin.write(bytes(fr))
        n += 1
        if n % 300 == 0:
            print(f"   {n} images…", flush=True)
    pin.stdout.close()
    pin.wait()
    if enc:
        enc.stdin.close()
        err = enc.stderr.read().decode(errors="replace")
        if enc.wait() != 0:
            sys.exit(f"ERREUR : encodage échoué\n{err[-1200:]}")
    print(f"\n✅ {a.sortie} — {n} images, retouche posée sur {faits}")
    if not a.apercu and os.path.exists(a.sortie):
        v2, _, d2 = sonde(a.sortie)
        print(f"   {d2:.2f} s · {v2['width']}×{v2['height']} · {os.path.getsize(a.sortie)/1048576:.1f} Mo"
              f" · {v2.get('codec_name')} · plage {v2.get('color_range')}")


if __name__ == "__main__":
    main()
