# JOURNAL — une entrée par session

> Append-only : on ajoute en haut, on ne réécrit pas le passé.
> Une entrée = ce qui a été fait, ce qui a été décidé, ce qui a été appris.
> L'état courant, lui, vit dans [`ETAT.md`](ETAT.md) et se réécrit.

---

## 16/09/2026 (suite) — Les 30 Mio du chat : contournés par l'audio, pas par un tuyau plus gros

Nabil : « à chaque fois je dois t'envoyer une vidéo de 30 Mo maximum (…) faire un lien WeTransfer
c'est trop, trop chiant. »

**Mesuré d'abord, proposé ensuite**

| Piste | Verdict |
| :--- | :--- |
| Augmenter la limite du chat | **Impossible** — fixée par le client, pas par Claude |
| Page web d'upload (artifact, capacité `assets`) | **20 Mio** de plafond : pire que le chat |
| Connecteur Google Drive pour les octets | Rend le fichier **en base64 dans la conversation** : 100 Mo → ~133 Mo de texte. Inutilisable |
| Connecteur Google Drive pour *trouver* un fichier | Marcherait (métadonnées), mais **pas autorisé** : `Insufficient scope` |
| `transfer.sh`, `0x0.st`, `bashupload.com` | **Injoignables** depuis le conteneur |
| Hébergeurs anonymes publics | Joignables, mais y déposer des sketchs non publiés : non (et refusé par la politique de session) |
| iCloud, Drive, Dropbox, WeTransfer, GitHub | **Tous joignables**. Débit mesuré : **15 Mo/s**, 29 Go de libre |

**La vraie trouvaille : le tuyau n'était pas le problème.**

Pour **décider** d'un montage, la vidéo ne sert à rien. Mesuré sur `tier-foot-HQ.mp4`, dérush sur la
vidéo complète contre l'audio seul (AAC 64 kb/s) :

- **60 Mo → 872 Ko** (69× moins)
- **0,04 s d'écart maximum** sur les bornes de coupe, **0,00 s sur 4 segments / 5**
- blanc long détecté à l'identique (3,94 s), seuil de silence à 0,3 dB près

Donc : les étapes 0 à 3 du skill tournent sur l'audio, et **le fichier lourd ne bouge qu'une fois**,
à la fin, quand la liste de coupes est validée — au lieu d'à chaque aller-retour.

**Fait**

- Nabil a choisi **iCloud** (son réflexe iPhone). Écrit `outils/icloud.py` : un lien de partage
  iCloud est une page JavaScript, `curl` n'y voit que du HTML. L'outil extrait le *shortGUID* et
  interroge l'API publique CloudKit (`ckdatabasews.icloud.com/.../records/resolve`). Branché dans
  `recuperer.sh` sur tout lien `icloud.com`.
- **`icloud.py` REFUSE les liens d'album partagé** et explique le bon chemin : Apple y ré-encode et
  rabote les vidéos. C'était le rush Snapchat du 12/09 prêt à se reproduire.
- Écrit [`outils/README-envoyer-un-rush.md`](outils/README-envoyer-un-rush.md) : le raccourci iOS
  « Audio pour Claude » (un tap, ~1 Mo/clip), le chemin iCloud Drive pour le fichier lourd, et les
  trois pièges qui coûtent de la qualité.
- Skill `montage` étape 0 complétée : **ne pas réclamer la vidéo avant l'étape 4.**

**Pas vérifié**

- **Le chemin de succès d'`icloud.py` n'a jamais tourné sur un vrai lien.** Les trois chemins
  d'erreur sont testés (album partagé, lien sans GUID, GUID inconnu → l'API répond
  « Cannot resolve shortGUID »), le succès non. À faire au premier rush envoyé par iCloud, et à
  corriger tout de suite si la forme de la réponse diffère.

## 16/09/2026 — Le montage devient un skill (et un outil qui refuse de couper)

**Fait**

- Nabil envoie une vidéo de Lucas Reverdy, *« Comment Automatiser ses Montages Vidéo avec Claude »*
  (14 min 11). Transcription récupérée par `yt-dlp` — **le client `web_embedded` est le seul qui passe**
  l'anti-bot YouTube, avec `--ignore-no-formats-error` (les autres : 429 puis « Sign in to confirm
  you're not a bot »).
- **Skill [`montage`](.claude/skills/montage/SKILL.md) écrit** : 7 étapes, dont **2 qui s'arrêtent et
  attendent Nabil** (la chaîne de sens, la sonorisation). Deux fiches de référence :
  `chartes.md` (solo vs tier list) et `verification.md` (les commandes de mesure avant livraison).
- **`outils/derusher.py` écrit** : fiche captation + silences mesurés à l'enveloppe + proposition de
  segments avec le niveau vérifié à chaque raccord. **Il n'encode rien et ne décide rien.**
- Hook de session : ffmpeg s'installe désormais **en fond** au démarrage au lieu d'être seulement signalé.

**Ce qu'on a pris de sa vidéo, et ce qu'on a refusé**

Pris : l'**architecture** (des étapes nommées, chacune suivie d'une relecture de son propre travail),
le **point d'arrêt humain à un endroit défini** (lui fait valider sa liste de plans ; nous, la chaîne
de sens), le **choix de la charte au démarrage**, et l'idée qu'une procédure doit être un skill et
pas de la prose.

Refusé : sa règle numéro un, *« couper tous les blancs et toutes les reprises, cut chirurgical »*.
Elle marche sur une vidéo explicative ; **sur un sketch c'est exactement ce qui a cassé deux
montages** (Business Bro du 13/09, tier list foot du 14/09). Et il juge son résultat à l'œil — « là
on voit que les cuts sont absolument parfaits », zéro mesure. C'est l'interdit du dépôt.

**Appris / mesuré**

- **Le seuil de silence n'a pas besoin d'être fixé à la main.** `plancher + 0,35 × (parole − plancher)`
  tombe à **−39,1 dBFS** sur « T'inquiète » et **−37,5 dBFS** sur la tier list foot, soit le −40 dBFS
  de `CLAUDE.md` — mais il s'adapte à un rush bruyant, ce qu'une constante ne fait pas.
- **Le silence gardé dans le montage vaut `2 × --marge`.** Je l'avais d'abord lu à l'envers dans mon
  propre calcul (j'ai pris ce qui est *retiré* pour ce qui *reste*). Corrigé en **mesurant le fichier
  de sortie** sur un test à silences connus : 0,20 s → 0,19 s intact · 0,50 s → 0,24 s · 1,00 s →
  0,21 s · 2,00 s → 1,99 s gardé entier. D'où : `--silence-min 0.45 --marge 0.11` **reproduit
  exactement** la règle §2.3 du format tier list.
- **Contrôle de non-régression utile** : sur un montage déjà serré, l'outil doit proposer très peu.
  Mesuré : 5 % sur `15sept-tinquiete-HQ.mp4`, 1 % sur `tier-foot-HQ.mp4`. S'il propose beaucoup plus,
  c'est lui qui a tort.
- **La règle du 14/09 est maintenant dans le code, pas seulement dans un document** : sur
  `tier-foot-HQ.mp4`, `derusher.py` retrouve le blanc de **3,94 s** (à 4,17 s) que Nabil avait fait
  remettre, et **refuse de le couper**. Même logique pour une redite sans silence mesuré autour.

**Pas fait**

- Les sous-titres. Lui les sort automatiquement, nous jamais — et la question 2 de la D.A. solo
  (police Monument Extended ou native TikTok) est toujours ouverte. C'est le vrai trou restant.
- Le montage sur fichier allégé (proxy) puis retour en pleine résolution. Utile chez lui (vidéos
  YouTube de 20-30 min) ; sur des sketchs de 40 s à 1 min 45, ça ne rapporte rien pour l'instant.
- Toujours **rien de publié**. Six montages prêts, aucun compte ouvert.


## 15/09/2026 — « T'inquiète » : 5 clips assemblés en une vidéo

**Fait**

- Cinq clips reçus (1 min 44 au total), tournés en 3 minutes : une prise principale, une escalade
  sur le médecin, et **trois prises de la même fin**. Nabil : « ya des moments où je bug dans ma
  tête, prends les meilleurs moments les plus drôles. »
- **`outils/assembler.py` écrit** : monte une vidéo à partir de morceaux `FICHIER:DEBUT-FIN` venus
  de plusieurs fichiers, en un seul encodage. `monter.py` ne savait couper que dans un seul fichier.
- Montage livré : **36,7 s** gardées sur 1 min 44, soit 65 % jeté.

**Appris**

- **Transcrire tous les clips AVANT de décider.** Les horodatages des fichiers se chevauchaient et
  donnaient un ordre faux ; seule la transcription a révélé l'ordre réel et les trois prises
  jumelles de la fin.
- **Quand plusieurs prises disent la même chose, mesurer avant de choisir.** Débit : 6,86 mots/s
  pour la retenue, 6,56 et 5,21 pour les autres. Et surtout : une des trois ratait la négation de la
  chute (« je m'inquiète » au lieu de « je m'inquiète pas »).
- **Ne pas couper un mot au ras du raccord.** Deux raccords finissaient pile sur la fin d'un mot
  (−33 dBFS au point de coupe) : repoussés de 0,4 s dans le silence qui suit.

## 14/09/2026 (suite) — Tier list sport, montage perso

Nabil : « c'est pas pour TikTok, c'est pour moi, donc garde [les deux passages]. Fluidifie un peu
le truc. » Fait : blancs ≥ 0,45 s ramenés à 0,22 s, contenu intact, 1 min 50 → 1 min 33 (−15 %).

La décision d'écarter cette vidéo tient toujours : elle portait sur la **publication**. Un montage
privé d'un rush qu'il a tourné lui-même est son affaire. Le fichier n'est pas dans `livraisons/`,
qui reste le dossier des vidéos destinées à sortir.

Les cinq blancs les plus longs sont notés dans le relevé (88,7 s / 19,5 s / 7,7 s / 14,0 s /
4,3 s) : ce sont ceux qui risquent de porter une information, comme celui de Musiala.

## 14/09/2026 (suite) — Un silence qui portait une information

Nabil, sur la tier list foot : « au départ, après Musiala, je veux que tu laisses, car avec le cut
on dirait qu'on a fait exprès de dire "qui est ce mec" en même temps alors que non, même pas. »

Le blanc de 3,72 s entre « on va en mettre 5 » et le double « mais qui est ce mec ? » avait été
ramené à 0,22 s par la compression automatique. Résultat : les deux répliques se collaient et
laissaient croire à un effet préparé. **Remis entier.** 1 min 43 → 1 min 47.

Règle ajoutée à `CLAUDE.md` §2 bis et à la D.A. du format : un silence n'est pas toujours un temps
mort. Entre deux locuteurs surtout, la simultanéité se lit comme une intention.

## 14/09/2026 (suite) — Deux fichiers livrés corrompus

**Ce qui s'est passé**

Nabil : « j'arrive pas à lire les 2 vidéos ». Les fichiers étaient des `mdat` sans atome `moov` :
la bonne taille, illisibles partout. ffmpeg était mort en fin d'encodage **en sortant en code 0**,
et je n'avais pas relu le fichier écrit. Pire : j'avais filtré la sortie de l'outil avec un `grep`
qui ne gardait que la ligne de succès, donc même le message d'erreur ne me serait pas parvenu.

**Corrigé**

- `monter.py` relit sa sortie (lisibilité + durée) et refuse d'annoncer un succès sinon. Il affiche
  aussi la stderr de ffmpeg même quand le code de retour est 0.
- Méthode `select` (une seule passe de décodage) au-delà de 5 segments, au lieu de trim/concat qui
  ouvre une branche par segment.
- Les cinq fichiers de `livraisons/` ont été recontrôlés un par un : tous lisibles.

**Appris**

- Le défaut est **intermittent** : la même commande aboutit une fois sur deux. Ce n'est ni la
  mémoire (14 Go libres), ni le disque, ni le dossier de sortie — tous testés.
- **Ne jamais filtrer la sortie d'un outil sur sa ligne de succès.** C'est ce qui a caché l'erreur.
- La règle « rien sans mesure » vaut aussi pour ses propres livrables : un fichier n'est livré que
  s'il a été relu.

## 14/09/2026 — Les tier lists avec Sady, et la D.A. du format

**Fait**

- Trois tier lists reçues (sports, fruits, footballeurs), toutes en 720p, deux à deux personnes.
- **Benchmark du compte de Sady** (@rodman97.3) sur 7 vidéos : `05-benchmark-rodman.md`.
- **D.A. du format tier list tranchée** : `06-format-tier-list.md`.
- Fruits et footballeurs montées et livrées : temps morts retirés, classement intact.

**Décidé**

- **On ne fragmente jamais une tier list.** Premier essai : deux extraits de 20 s. Nabil : « vu que
  c'est une tier list, si tu fais ça on comprend plus rien. » Dans ce format, la prémisse c'est la
  liste elle-même.
- **La durée est libre** (corrélation durée/vues chez Sady : +0,04). On coupe le mort, pas la durée.
- **Le titre fait la moitié du travail** : chez Sady, titre qui promet = 2× les vues d'un titre plat.
- **La tier list sport ne sort pas.** Deux passages vérifiés en double passe, non coupables proprement
  (au cœur d'un item, pas dans une respiration). À retourner.

**Appris**

- **Ne jamais conclure sur moins de cinq mesures.** Sur deux vidéos j'avais conclu « plus long =
  mieux ». Sur sept, la corrélation est nulle. C'était du bruit, et je l'avais présenté comme un fait.
- Méthode de compression reproductible : tout silence ≥ 0,45 s ramené à 0,22 s. 11 à 15 % de gagné
  sur ces rushs, sans toucher au contenu.

## 13/09/2026 (nuit) — Les trois vidéos sont montées

**Fait**

- **L'otage du téléphone montée** : 61 s → 41,7 s, six coupes. Méthode §2 bis appliquée dès le
  départ : chaîne de sens écrite d'abord, coupes faites dedans, transcription du montage relue
  avant livraison. Elle se tient debout toute seule.
- Les six premières secondes d'annonce sautent : mesurées plates (F0 à la moitié de sa variation
  habituelle sur 0,4–3,7 s) et sémantiquement confuses. La prémisse commence à 6,0 s.
- Quatre des six répétitions finales de « j'ai déjà vu la vidéo » sautent. La dernière (« j'ai déjà
  vu », chute 98/100) devient la chute. **Elle existait, elle était juste noyée.**
- Trois montages sont désormais dans `livraisons/`. Aucun n'est publié : c'est le seul blocage.

**Décidé**

- Un point faible est gardé sciemment dans l'otage du téléphone : « on connaît tous ces humains-là
  → une fois, deux fois, trois fois » retombe de 8 dB. C'est un maillon du sens, on ne le coupe pas.
  Noté dans `livraisons/README.md` pour que Nabil décide s'il le retourne.

## 13/09/2026 (nuit) — Business Bro monté, après un premier montage raté

**Fait**

- Première version : départ direct sur l'imitation, 24,5 s. **Refusée par Nabil** : « on comprend
  pas le contexte, y'a plus de sens du tout à la vanne ». Il avait raison.
- Deuxième version, livrée : 36,5 s, la mise en place gardée entière, les coupes faites à
  l'intérieur (triple redite sur « s'immiscent », redite sur les conseils, 7 s de mou avant la fin).

**Appris — la faute de méthode, écrite dans CLAUDE.md §2 bis**

J'avais pris le moment le mieux noté par les mesures (+22,3 dB, chute 100/100) et je l'avais mis en
ouverture, en invoquant la règle du hook. Mais **les mesures disent où ça retombe, elles ne disent
pas ce qui se comprend.** Une vanne est une chaîne de sens : qui est le personnage, ce qu'il fait,
ce que toi tu fais face à lui, l'escalade, la chute. On coupe DANS les maillons, jamais un maillon
entier. Et on relit la transcription du montage avant de livrer.

## 13/09/2026 (soir) — Les deux rushs du 30/08 enfin analysés

**Fait**

- Nabil demande pourquoi les deux autres vidéos du WeTransfer n'ont jamais été touchées. Réponse :
  elles ne l'ont pas été, il n'y a pas d'excuse. Elles étaient encore sur le disque : analysées.
- **Découverte : ce ne sont pas deux prises de la même vanne.** Le nom `prise-A` / `prise-B` avait
  été inventé par moi, et il a induit tout le monde en erreur pendant deux jours.
  - Rush A (18 h 55, 59 s) = la **Vidéo 3, Business Bro**, improvisée.
  - Rush B (19 h 01, 61 s) = la **Vidéo 4, l'otage du téléphone** — que le dépôt déclarait
    « script à écrire ». Elle est tournée.
- Analyse complète des deux (`ecoute-video.py`), versée dans `02-scripts-valides.md` avant que le
  conteneur ne l'efface : transcription, zones molles, scores de chute, son.

**Appris**

- **Le meilleur moment tourné à ce jour** est dans le rush A, à 16,0–22,8 s : l'imitation du faux
  investisseur. +22,3 dB sur la phrase d'avant, score de chute 100/100.
- Les deux rushs saturent en crête (−0,3 dBTP), comme celui du 12/09. C'est systématique : le gain
  automatique du téléphone. À traiter à la prise, pas au montage.
- **Ne jamais nommer un fichier d'après une hypothèse.** Nommer d'après ce qu'il contient, ou par
  sa date. Un nom inventé devient un fait dans la mémoire du projet.

## 13/09/2026 — Montage, son, retouche, et une leçon sur la qualité

**Fait**

- Chaîne son refaite : le sample s'efface sous la voix (ducking calculé hors ligne), la voix
  n'est plus touchée. Trois défauts ffmpeg trouvés et corrigés — ils baissaient toute la voix de 2 dB.
- Sample Doumbé découpé au mot : « JORDAN » seul, 0,94 s, la foule derrière, coupé avant « t'es mort ».
- `outils/retoucher.py` écrit : efface un défaut de peau sur toute la vidéo en le suivant sur le
  visage (MediaPipe). Bouton du nez retiré sur 1266 des 1288 images.
- `livraisons/` créé : les montages finis vivent dans le dépôt, en haute qualité.
- `phase-1-solo/04-da-tiktok.md` écrit : proposition de DA TikTok + passation.

**Décidé**

- Les livraisons passent par GitHub, plus par le chat (qui plafonne à 30 Mio et coûte 7 % de détail).
- Les sous-titres seront la signature visuelle du compte — à valider par Nabil.

**Appris, à la dure**

- Une occlusive fabrique un silence **au milieu** d'un mot : couper « Jordan » sur ce silence
  donnait « JORD ». Chercher les bornes d'un mot à l'enveloppe, pas au premier blanc venu.
- Le PSNR ment sur une vidéo granuleuse. Mesurer le **détail conservé** (écart-type du passe-haut).
  Le H.265 gagnait 1 dB de PSNR et conservait *moins* de détail que le H.264.
- Deux captures d'écran « du même moment » étaient à 0,17 s d'écart, l'une nette, l'autre floue.
  **Vérifier que c'est la même image avant de comparer quoi que ce soit.**
- Le rush venait de Snapchat (720p). J'en ai conclu à tort que l'original était en 1080p ;
  ses métadonnées disaient 720p. **Lire les métadonnées avant de conclure.**

## 12/09/2026 — Premier rush analysé et monté

**Fait**

- Rush de 74 s reçu (vidéo MMA, tournée en voiture la nuit), analysé par `ecoute-video.py`.
- Monté en 6 coupes, 43 s, son normalisé à −14 LUFS.
- Deux problèmes de qualité d'image trouvés et corrigés : trois réencodages empilés (→ un seul),
  et la plage de couleur convertie de complète à limitée (→ conservée, BT.709 étiqueté).

**Appris**

- Les coupes tombaient 0,3 s trop tôt : sur un rush d'iPhone la piste audio ne démarre pas à zéro
  (0,283 s ici). Décaler **vidéo et audio** de la même valeur.
- Les bruitages synthétiques ne font rire personne. Nabil veut des mèmes et des samples réels.
