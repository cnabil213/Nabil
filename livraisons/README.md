# livraisons — les versions finales, en haute qualité

Le chat plafonne à **30 Mio** par fichier. GitHub, non. Les montages finis sont donc déposés ici, au
débit de l'original, et se téléchargent directement depuis le dépôt.

| fichier | durée | poids | débit | détail conservé |
| :-- | --: | --: | --: | --: |
| `12sept-casser-des-nuques-HQ.mp4` | 42,9 s | 53,7 Mio | 10,3 Mb/s | **99,4 %** du rush |
| `30aout-business-bro-HQ.mp4` | 36,5 s | 46,8 Mio | 10,8 Mb/s | **99,5 %** du rush |
| `30aout-otage-du-telephone-HQ.mp4` | 41,7 s | 50,7 Mio | 10,2 Mb/s | **99,2 %** du rush |
| `tier-fruits-HQ.mp4` | 1 min 42 | 58,6 Mio | 4,8 Mb/s | tier list, temps morts retirés |
| `15sept-tinquiete-HQ.mp4` | 36,7 s | 28,5 Mio | 6,2 Mb/s | 5 clips assemblés en un seul montage |
| `tier-foot-HQ.mp4` | 1 min 47 | 59,6 Mio | 4,7 Mb/s | tier list, temps morts retirés (blanc après Musiala conservé) |
| `15sept-tinquiete-HQ.mp4` | 34,7 s | 78,1 Mio | 18,9 Mb/s | **87,9 %** du rush ramené en 1080p (voir ci-dessous) |

Le rush d'origine fait 10,5 Mb/s : cette version est à son niveau.

**Contenu de « T'inquiète » (15/09)** : trois rushs 4K (38 s + 12 s + 16 s) recollés en 34,7 s, huit
segments, chaque source décodée séparément (synchro son/image mesurée à −1,7 et −3,3 ms aux entrées de
fichier). Coupé : les trois blancs de réflexion dans la liste (ramenés à 0,38 s), la fin cherchée à voix
haute du premier fichier, la deuxième formulation du « 9 ans d'études », et le second final « algorithme »
qui venait après la chute mesurée 91/100. Détail dans
[`02-scripts-valides.md`](../phase-1-solo/02-scripts-valides.md#-vidéo-5--tinquiète).

**Pourquoi 1080p et pas 4K.** Le rush est en 2160×3840 à 25 Mb/s. Le même montage en 4K à CRF 18
conserve 99,4 % du détail mais pèse **194 Mio à 46,8 Mb/s** (x264 garde tout le grain de jour de
l'iPhone) : GitHub refuse au-delà de 100 Mio. En 1080×1920 (la résolution que TikTok affiche de toute
façon), CRF 16 fait encore 100,3 Mio ; CRF 18 fait 78,1 Mio et conserve 87,9 % du détail de la source
ramenée en 1080p (lanczos), contre 85,7 % à CRF 20. C'est ce fichier. Le 4K n'existe que dans le conteneur
de la session, il n'est pas versionné.

**Contenu de l'otage du téléphone (30/08, rush B)** : 61 s ramenées à 41,7 s, six coupes, toutes
sur des silences mesurés. La chaîne de sens est gardée entière : le pote vient chez toi → il ricane
déjà parce qu'il a vu la vidéo → elle fait trois minutes → tu rigoles pour lui faire comprendre que
c'est bon → **il reste comme ça** (le meilleur moment, chute 95/100) → tu restes comme ça jusqu'où ?
→ il recommence quatre fois → « j'ai déjà vu la vidéo… j'ai déjà vu ». Coupé : les six premières
secondes d'annonce (plates, F0 à la moitié de sa variation habituelle), « toi tu regardes la
vidéo », « donc famille tu sais bien / bon tu regardes avec lui », « famille il faut… », et quatre
des six répétitions finales.

**À savoir** : la section « on connaît tous ces humains-là → une fois, deux fois, trois fois »
retombe de 8 dB sous ses pics et son débit tombe à 56 %. C'est un maillon de la chaîne, donc elle
reste — mais si Nabil la retourne avec de l'énergie, la vidéo change de niveau.

**Contenu de la version du 30/08 (Business Bro)** : 3 coupes dans le rush A, 59 s ramenées à 36,5 s.
La mise en place est gardée **entière** — une première version qui démarrait sur l'imitation a été
refusée par Nabil (« on comprend pas le contexte »), voir [`CLAUDE.md`](../CLAUDE.md) §2 bis. Les
coupes sont à l'intérieur : la triple redite sur « s'immiscent » (6,86–10,70), la redite sur les
conseils (28,76–30,70), et les 7 s de mou avant la fin (39,98–47,12). Fin nette sur « mais rends
8 balles ! ». Son : gain fixe +2,5 dB puis limiteur, −15,4 LUFS, true peak −1,2 dBTP.

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

## Le vrai plafond : le rush

Ce rush est une capture **Snapchat** (métadonnée `com.apple.quicktime.description`), donc **1280×720**,
alors que l'iPhone qui l'a filmé fait du 1080p et du 4K. La version livrée ici conserve 99,4 % du détail
du rush : elle est au maximum de ce que le rush contient. Le reste se gagne à la prise de vue, pas au
montage — app Caméra, 1080p, puis AirDrop ou WeTransfer, jamais Snapchat.

## Contrôle obligatoire avant d'annoncer une livraison

Le 14/09, deux tier lists ont été livrées **corrompues** : `mdat` sans atome `moov`. Des fichiers de
la bonne taille, illisibles par tous les lecteurs. ffmpeg était mort en fin d'encodage sans le dire
(code de retour 0), et rien ne l'avait vérifié.

`monter.py` relit désormais le fichier qu'il vient d'écrire et refuse d'annoncer un succès s'il est
illisible ou si sa durée ne correspond pas. **Ne jamais annoncer une livraison sans un `ffprobe` sur
le fichier final.** Le défaut est intermittent : la même commande aboutit une fois sur deux.

## Règle

Une seule version finale par tournage, remplacée sur place quand elle change (l'historique git garde
les anciennes, inutile d'empiler les fichiers). Pour publier sur TikTok/Reels, partir de CE fichier,
jamais de celui du chat.
