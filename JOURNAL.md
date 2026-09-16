# JOURNAL — une entrée par session

> Append-only : on ajoute en haut, on ne réécrit pas le passé.
> Une entrée = ce qui a été fait, ce qui a été décidé, ce qui a été appris.
> L'état courant, lui, vit dans [`ETAT.md`](ETAT.md) et se réécrit.

---

## 16/09/2026 — Six concepts pour le duo avec Sady

Nabil : « cette fois je suis pas tout seul mais avec Sady… trouve un concept drôle, divertissant, qui
pourrait marcher, soit inventer, soit prendre un truc qui marche et l'améliorer. »

**Fait** : [`phase-1-solo/08-concepts-duo.md`](phase-1-solo/08-concepts-duo.md), six concepts, chacun
avec sa mécanique, ses rôles, deux titres et sa fin qui appelle le commentaire. Le n° 3 (le pote joué
par Sady) a son premier script écrit au mot près. Cinq idées écartées, avec la raison.

**Décidé** : les cinq règles du duo en tête du fichier (format répétable, conflit fabriqué, un rôle
chacun, appel au commentaire, titre qui accuse). Elles viennent toutes du benchmark de Sady.

**Retour de Nabil** : « Le 1 est très drôle, le reste vraiment pas. » Quatre concepts brûlés d'un
coup. Ce qu'il retient de la note cachée : une mécanique qui fait rire toute seule et un objet qui
signe le format. Deuxième passe, deux concepts écrits jusqu'au script : **l'interview d'après-match
de la vie** (Nabil journaliste au déo-micro, Sady en footballeur en langue de bois) et **le
mythomètre** (Sady raconte, Nabil monte un carton 0-10, l'histoire se dégonfle en direct).

**Appris** : mes quatre concepts refusés étaient des *formats* (mécanique, rôles, titres) mais pas
des *vannes*. Nabil juge un concept sur la première réplique qui fait rire, pas sur sa structure.
La prochaine fois : écrire le premier échange avant de décrire le format.

**À retenir** : la vidéo d'aujourd'hui doit être la première publiée. Sixième rappel.

## 15/09/2026 (soir) — Nabil a retourné « T'inquiète » et l'a montée lui-même

« J'ai monté moi-même finalement, tu en penses quoi ? » Le fichier reçu n'est pas un montage de mes
trois rushs : c'est une **nouvelle prise** (1080×1920, 60 i/s, export d'app, son 44,1 kHz), texte
remanié, veste différente, 46 s.

**Mesuré**

- **Quatre coupes**, repérées par les pics d'écart image-à-image (54 à 71 contre 8 à 12 de base) :
  10,15 · 19,38 · 28,13 · 35,45 s. **Toutes dans un silence mesuré.** Bien posées.
- **Hook meilleur que la prise de l'après-midi** : « On a tous ce pote-là… » +5,8 dB, chute 90/100
  (77/100 sur le rush 7370).
- **Trois doublons gardés** : « Il connaît que le nom de la rue. Voilà. Il connaît que le nom de la rue »
  (16,1–19,1 s) · « il a fait des études pour ça. Oui. Il a fait 9 ans d'études pour s'inquiéter. Oui »
  (25,2–27,8 s, la deuxième formulation PLATE, −4,4 dB) · le dialogue « t'inquiète / je m'inquiète pas /
  vas-y » répété quatre fois (39,6–45,5 s).
- **La fin s'éteint** : niveau −6,1 dB sur la dernière seconde, derniers mots « Vas-y. Vas-y. » PLATE,
  puis la main qui attrape le téléphone est dans le montage (image 2733, noir ensuite).
- **La chute garde à vue a disparu** (91/100 sur la prise de l'après-midi). Le nouveau final « on est
  plus bête qu'eux » mesure 62/100 puis retombe.
- Image constamment en mouvement (écart moyen 8 à 12 par image, contre ~3 sur un plan posé) : cadrage
  qui change, mains dans le champ, flous de bougé visibles sur la planche. Netteté 190–370 à l'échelle
  540×960 contre 300–640 sur le rush de 14 h 53.
- Son : −16,1 LUFS (2 LU sous la cible), true peak −2,5, LRA 3,8 (l'app a compressé).

**Ce que j'en pense** (donné à Nabil) : la prise est plus vivante et le hook plus fort ; le montage
est propre sur ses coupes ; il manque le geste le plus dur, couper ce qu'on a dit deux fois et
s'arrêter à la chute. Pas de coupe possible dans le doublon « études » (aucun silence ≥ 0,10 s entre
24,3 et 27,9 s) : celui-là ne se sauve qu'à la prise.

## 15/09/2026 (suite) — « T'inquiète » tournée, montée, livrée

Nabil a tourné le script B en trois fichiers 4K (app Caméra, de jour : le plafond de netteté est enfin
le bon) et demandé « un montage parfait… coupe le début d'une phrase pour la coller avec le restant
d'une autre, y a des trucs que j'ai refaits ».

**Fait**

- Trois rushs analysés (`ecoute-video.py`), silences mesurés à l'enveloppe, huit segments, un seul
  encodage : [`livraisons/15sept-tinquiete-HQ.mp4`](livraisons/15sept-tinquiete-HQ.mp4), 34,7 s.
- `monter.py` accepte plusieurs sources (`k:debut-fin`), chaque source décodée par son propre
  démultiplexeur. Test de synchro : 0,0 ms sur l'essai, −1,7 et −3,3 ms sur le montage final.
- Transcription du montage relue : la chaîne de sens tient entière (hook → le pote à un mot → la liste
  → la boîte de nuit → le médecin → la police → garde à vue).

**Décidé**

- Le second final « vous connaissez mon algorithme ? la baffe ou delete » est écarté : il vient après
  une chute à 91/100 et retombe (−10,7 dB, « delete » mot le plus plat). Documenté, pas supprimé.
- Livraison en 1080×1920 CRF 18 (78 Mio, 87,9 % du détail) : le 4K à CRF 18 fait 194 Mio, GitHub
  bloque à 100. Choix mesuré, pas esthétique. Tableau dans `livraisons/README.md`.

**Appris**

- **Le concat demuxer en copie de flux désynchronise le son** : +59 ms sur le 2e fichier, +80 ms sur
  le 3e (liste d'édition AAC ignorée). Mesuré par corrélation croisée, avant de livrer. Ne plus jamais
  recoller des rushs iPhone comme ça.
- Deux des trois fichiers **démarrent en pleine parole** (−22 et −12 dBFS dès les 20 premières ms) :
  l'attaque de « Il va voir » et de « Contrôle » est tronquée à la prise. Consigne ajoutée : une
  seconde de silence avant de parler **à chaque fichier**.
- x264 sur du 4K de jour sort au double du débit de la source (46,8 Mb/s contre 25) : il encode le
  grain. Le débit ne dit rien de la qualité, la mesure de détail oui.
- Whisper a transcrit « On va là-bas, il » sur le montage alors que le « t'inquiète » est là (0,2 s,
  −18 dBFS à l'enveloppe) : vérifier à l'enveloppe avant de croire à un mot coupé.

## 15/09/2026 — Quatre scripts pour un tournage en voiture, et la question Apify

Nabil, sur le parking, avec le temps de tourner 3-4 vidéos. Il demande des thèmes, des scripts, et
si Apify (scraper TikTok) me servirait.

**Fait**

- Quatre scripts complets, au mot près, dans
  [`phase-1-solo/07-scripts-proposes-15-09.md`](phase-1-solo/07-scripts-proposes-15-09.md) :
  A le pote qui a six mois de plus · B « T'inquiète » · C le pote qui a un contact pour tout ·
  D le pote qui te corrige quand tu racontes. Ordre conseillé A → B → C → D, D en dernier parce
  qu'il frôle l'humour de couple.
- Dix angles refusés, documentés avec leur raison dans le backlog (muscu, vocaux, radin, Dubaï,
  surenchère, stagiaire, « projet », et « réagir à une vidéo » : pas à zéro abonné).

**Décidé**

- Pas de vidéo « réaction » pour l'instant : il faut le clip source et un compte qui existe.
- Les consignes de tournage tiennent en cinq lignes en tête du fichier de scripts. La plus
  importante vient des rushs du 30/08 : **après la chute, on se tait et on coupe**, on ne cherche
  pas une meilleure fin à voix haute.

**Appris**

- `api.apify.com` est **injoignable depuis le conteneur** (Connection reset, tunnel fermé côté
  proxy, deux essais). Brancher Apify passe d'abord par la politique réseau de l'environnement.
  Avant ça, aucun test possible.
- Apify servirait à deux choses mesurables : un benchmark de 5-10 comptes de sketchs français
  (titres, hooks, ratio commentaires — ce qu'on a fait à la main sur Sady avec des 403), et le
  test « ce thème est-il déjà saturé ? » par une recherche chiffrée avant d'écrire. Ça ne
  remplace ni l'écriture ni TikTok Studio (rétention, trafic : seul le compte les voit).

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
