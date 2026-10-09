# Vérifier un montage — les commandes exactes

Aucune de ces vérifications ne se saute, et **aucune ne se remplace par un coup d'œil**.

---

## 1. Le fichier est-il lisible ? (obligatoire, toujours)

Un encodage interrompu produit un mp4 **de la bonne taille, sans atome `moov`, illisible partout** —
et ffmpeg peut sortir en **code 0**. Deux tier lists ont été livrées comme ça le 14/09.

```bash
ffprobe -v error -show_entries format=duration,size,bit_rate \
        -show_entries stream=codec_name,width,height,nb_frames -of json MONTAGE.mp4
```

Si ça sort une erreur ou une durée nulle : **le fichier est mort, relancer l'encodage.** Le défaut
est intermittent — la même commande aboutit une fois sur deux.

Et la vérification qui attrape le cas vicieux (conteneur lisible, flux illisible) :

```bash
ffmpeg -v error -i MONTAGE.mp4 -f null - && echo "flux décodable de bout en bout ✅"
```

> **Ne jamais filtrer la sortie d'un outil avec un `grep` qui ne garde que la ligne de succès.**
> C'est exactement comme ça que l'erreur du 14/09 est passée.

---

## 2. La plage de couleur a-t-elle été conservée ?

Forcer `yuv420p` sur un rush iPhone en plage complète écrase les noirs. Mesuré le 12/09 : noirs à
**3** dans la source, **19** dans le fichier livré. C'était ça, « la vidéo perd en qualité ».

```bash
for f in RUSH.mov MONTAGE.mp4; do
  echo "— $f"
  ffprobe -v error -select_streams v:0 -show_entries stream=pix_fmt,color_range,color_space \
          -of default=nw=1 "$f"
done
```

Les percentiles de luminance (0,5 / 50 / 99,5 %) doivent être **identiques** entre la source et le
montage.

---

## 3. La voix a-t-elle été touchée par la sonorisation ?

Le son s'efface sous la voix, **jamais l'inverse**. RMS par blocs de 0,5 s, sonorisé contre nu :
l'écart doit être **0,0 dB partout hors du son posé**.

```bash
python3 - <<'PY'
import numpy as np, soundfile as sf, subprocess
for nom, f in (("nu","MONTAGE.mp4"), ("sonorisé","MONTAGE-sonorise.mp4")):
    subprocess.run(["ffmpeg","-v","error","-y","-i",f,"-vn","-ac","1","-ar","48000",
                    "-c:a","pcm_s16le",f"/tmp/{nom}.wav"], check=True)
a,sr = sf.read("/tmp/nu.wav", dtype="float32"); b,_ = sf.read("/tmp/sonorisé.wav", dtype="float32")
n = int(0.5*sr); m = min(len(a),len(b))//n
f = lambda x: 20*np.log10(np.maximum(np.sqrt((x[:m*n].reshape(m,n).astype(np.float64)**2).mean(1)),1e-10))
d = f(b)-f(a)
for i,v in enumerate(d):
    if abs(v) > 0.15: print(f"  bloc {i*0.5:6.2f} s : {v:+.2f} dB")
print(f"écart max hors son : {np.abs(d).max():.2f} dB  (attendu ≈ 0,0 hors du son posé)")
PY
```

Vérifier aussi que **le flux vidéo est bit à bit identique** (sonoriser.py copie l'image) :

```bash
for f in MONTAGE.mp4 MONTAGE-sonorise.mp4; do
  ffmpeg -v error -i "$f" -map 0:v -c copy -f md5 - ; done
```

---

## 4. Le montage se comprend-il ?

**La seule vérification qu'aucun chiffre ne remplace.** Transcrire le montage final et le relire :

```bash
python3 outils/ecoute-video.py MONTAGE.mp4 -o ecoute-montage/
```

Si la transcription ne tient pas debout toute seule à la lecture, **le montage est faux, quels que
soient les chiffres**. Les mesures disent où ça retombe et où ça envoie ; elles ne disent pas ce
qui se comprend.

---

## 5. Le détail conservé (pas le PSNR)

Juger la qualité au **détail conservé** — écart-type du passe-haut, rapporté à la source. Le PSNR
ment : le H.265 a déjà eu un meilleur PSNR tout en conservant **moins** de détail (91,3 % contre
92,8 %).

Pour mesurer une perte, construire l'étalon avec le **même `trim`** que le montage. Un étalon fait
au `-ss` cale sur une image-clé, et le décalage d'une ou deux images fait chuter le SSIM à 0,88
pour tout le monde — la mesure ne veut alors plus rien dire.

Reporter le résultat dans le tableau de [`livraisons/README.md`](../../../../livraisons/README.md).

---

## 6. Avant d'annoncer la livraison

- [ ] `ffprobe` passé sur le fichier final, durée non nulle
- [ ] `ffmpeg -f null -` décode le flux de bout en bout
- [ ] plage de couleur identique à la source
- [ ] première image gardée **nette** (c'est la vignette TikTok)
- [ ] transcription du montage relue, elle se tient toute seule
- [ ] si sonorisé : écart RMS ≈ 0,0 dB hors du son, md5 vidéo identique
- [ ] tableau de `livraisons/README.md` rempli
- [ ] `ETAT.md` réécrit, entrée ajoutée en haut de `JOURNAL.md`

**Tant qu'une case n'est pas cochée, ne pas dire que c'est livré.**
