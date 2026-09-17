# Exporter depuis CapCut — les réglages, et pourquoi

> Écrit le 17/09/2026, Nabil monte lui-même dans CapCut sur un rush **Snapchat 720p**.
> Chaque ligne est adossée à une mesure faite sur ses propres fichiers.

---

## Les réglages, directement

| Réglage CapCut | Valeur | Raison |
| :--- | :--- | :--- |
| **Ultra HD par l'IA** | ⬛ **OFF** | Invente du détail qui n'existe pas. Sur un visage : peau plastique, grain effacé. Payant en prime. |
| **Résolution** | **1080P** | Format natif TikTok, donc pas de re-scale de leur côté. **Ne rend pas plus net** (mesure ci-dessous). |
| **Fréquence d'images** | **30** | La source est à 30 im/s. 60 duplique chaque image : zéro gain, double poids. |
| **Flux optique** | ⬛ OFF | Images intermédiaires inventées → bavures autour de la bouche sur la parole rapide. |
| **Débit binaire** | **12 à 20 Mbit/s** | 20 est large pour du 720p étiré. À 12, aucune différence visible, fichier divisé par ~1,7. |
| **Smart HDR** | 🔴 **OFF** | Le plus dangereux. Voir ci-dessous. |

---

## La mesure : un upscale n'ajoute aucun détail

Sur `livraisons/12sept-casser-des-nuques-HQ.mp4` (rush Snapchat, 720×1280), 30 images
échantillonnées. Aller-retour **720p → 1080p → 720p**, lanczos des deux côtés, soit le meilleur cas
possible pour un upscale :

| | |
| :--- | ---: |
| Détail du rush 720p d'origine (écart-type du passe-haut) | **3,42** |
| Détail après l'aller-retour | **3,25** (95,0 %) |
| **PSNR de l'aller-retour** | **61,8 dB** |

**Lecture :** au-dessus de 45 dB, l'image 1080p ne contenait rien que le 720p n'avait déjà. À
61,8 dB, c'est sans appel. L'upscale **étale les mêmes pixels sur 2,25× plus de surface** — il ne
fabrique pas d'information.

Corollaire, qui est la règle §5 de [`CLAUDE.md`](../CLAUDE.md) vue depuis l'export :
**aucun réglage de sortie ne rattrape un rush 720p.** Le plafond se joue à la prise.

---

## Le Smart HDR : le piège qui a déjà coûté une vidéo

Les rushs de Nabil sont en **BT.709, SDR**, plage de couleur complète (`yuvj420p` / `color_range=pc`)
— vérifié sur les deux fichiers livrés.

Convertir ça en HDR, c'est étirer les valeurs dans un contenant que la source n'a jamais rempli.
Et TikTok gère le HDR de façon inconstante d'un lecteur à l'autre : délavé chez les uns, cramé chez
les autres.

> **C'est le même mécanisme que le bug du 12/09.** Forcer une conversion de plage de couleur avait
> fait passer les noirs de **3** dans la source à **19** dans le fichier livré. Nabil : « la vidéo
> perd en qualité ». C'était exactement ça.

**Vérification après export**, si un doute : les percentiles de luminance (0,5 / 50 / 99,5 %) doivent
être identiques entre le rush et l'export.

```bash
for f in RUSH.mp4 EXPORT.mp4; do
  echo "— $f"
  ffprobe -v error -select_streams v:0 \
    -show_entries stream=pix_fmt,color_range,color_space,color_transfer \
    -of default=nw=1 "$f"
done
```

`color_transfer` doit rester `bt709` des deux côtés. S'il passe à `smpte2084` ou `arib-std-b67`,
le Smart HDR est resté allumé.

---

## Snapchat : le vrai arbitrage

Nabil filme sur Snapchat parce qu'il s'y trouve mieux — **et c'est fondé** : Snap lisse la peau à
la prise sur la caméra avant. Ce n'est pas une lubie.

Mais le prix est mesuré : **720p au lieu de 1080p ou 4K**, et aucun export ne le récupère.

**Le test à faire une fois, pas à débattre :** filmer **une seule** vanne avec l'app Caméra en
1080p, puis appliquer un peu de « Retouche » visage dans CapCut. Deux issues, les deux utiles :

- il se trouve aussi bien → il gagne le lissage **et** la définition, on bascule ;
- il se trouve moins bien → on reste sur Snapchat, et **on arrête d'en parler**. Le confort devant
  la caméra vaut plus que 360 lignes de pixels si ça l'empêche de tourner.

---

## Poids de fichier et envoi

Les réglages de la capture du 17/09 (1080p, 60 im/s, 20 Mbit/s, IA + HDR) annonçaient **129,2 Mo
pour 49 s**. En 30 im/s à 12 Mbit/s, la même vidéo tombe autour de **75 Mo**.

Dans les deux cas c'est **au-dessus des 30 Mio du chat** : pour me l'envoyer, passer par iCloud
Drive — [`README-envoyer-un-rush.md`](README-envoyer-un-rush.md). Et pour tout le travail de
montage (transcription, coupes, chaîne de sens), **l'audio seul suffit** : 872 Ko au lieu de 60 Mo,
0,04 s d'écart maximum sur les bornes de coupe.
