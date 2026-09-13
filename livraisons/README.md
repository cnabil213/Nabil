# livraisons — les versions finales, en haute qualité

Le chat plafonne à **30 Mio** par fichier. GitHub, non. Les montages finis sont donc déposés ici, au
débit de l'original, et se téléchargent directement depuis le dépôt.

| fichier | durée | poids | débit | détail conservé |
| :-- | --: | --: | --: | --: |
| `12sept-casser-des-nuques-HQ.mp4` | 42,9 s | 53,7 Mio | 10,3 Mb/s | **99,4 %** du rush |

Le rush d'origine fait 10,5 Mb/s : cette version est à son niveau.

**Contenu de la version du 12/09** : montage 6 coupes, son à −14 LUFS, sample « JORDAN » de Doumbé à
28,40 s (il s'efface sous la voix), bouton du nez retiré sur 1266 des 1288 images.

## Pourquoi ce fichier et pas celui du chat

Mesuré sur ce montage (43 s, 720×1280), contre le rush aux mêmes coupes :

| version | poids | débit | PSNR | **détail conservé** |
| :-- | --: | --: | --: | --: |
| rush d'origine | 98,6 Mo | 10,5 Mb/s | — | 100 % |
| H.264 CRF 19 (chat) | 27,4 Mio | 5,1 Mb/s | 44,40 dB | 92,8 % |
| H.265 CRF 16 (chat) | 28,7 Mio | 5,4 Mb/s | 45,42 dB | **91,3 %** |
| H.265 CRF 14 | 37,3 Mio | 6,9 Mb/s | 46,43 dB | 93,0 % |
| **H.264 CRF 13 (ici)** | **53,7 Mio** | **10,0 Mb/s** | 47,72 dB | **99,4 %** |

**Le PSNR ment sur cette vidéo.** Le H.265 à 28,7 Mio gagne 1 dB de PSNR sur le H.264 à 27,4 Mio et
conserve pourtant *moins* de détail (91,3 % contre 92,8 %) : x265 lisse le grain, et sur un rush de
voiture la nuit le grain EST l'image. Mesure utile = écart-type du passe-haut (σ = 1 px), rapporté à
celui du rush, pas le PSNR.

Il n'y a pas de réglage magique sous 30 Mio : à 5 Mb/s on perd 7 % de détail, point. La seule vraie
réponse, c'est le débit — donc ce dossier.

## Règle

Une seule version finale par tournage, remplacée sur place quand elle change (l'historique git garde
les anciennes, inutile d'empiler les fichiers). Pour publier sur TikTok/Reels, partir de CE fichier,
jamais de celui du chat.
