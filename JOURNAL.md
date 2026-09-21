# JOURNAL — une entrée par session

> Append-only : on ajoute en haut, on ne réécrit pas le passé.
> Une entrée = ce qui a été fait, ce qui a été décidé, ce qui a été appris.
> L'état courant, lui, vit dans [`ETAT.md`](ETAT.md) et se réécrit.

---

## 21/09/2026 — FORMATS.md : les formats ne se perdent plus

Nabil : « tu as pas mis les idées de format Bakhal Man, l'exploit sportif… j'ai ouvert une autre
session mais il a pas trouvé les 2 formats dans le dépôt. Crée un fichier md et mets dans le dépôt
le format annexe qu'on peut viser sur mon compte TikTok. »

**Le diagnostic** : les formats existaient bien, mais introuvables. Ils étaient enterrés au milieu de
`08-concepts-duo.md`, sous les noms « mythomètre » et « interview d'après-match » — pas sous les noms
que Nabil emploie (**Bakhal Man**, **l'exploit sportif / le journaliste**). Un `grep bakhal` ne
renvoyait que deux fichiers, et rien à la racine.

**Fait**

- [`FORMATS.md`](FORMATS.md) **à la racine** : le catalogue des sept formats (le sketch solo comme
  format de fond, puis Bakhal Man, Le Journaliste, La Note cachée, Le GPS de la vie, Le Contrôle
  technique, la tier list). Chacun avec son principe, ses rôles, son objet signature, son épisode de
  référence intégral et ses réserves d'épisodes. Les **noms officiels sont ceux de ce fichier**, avec
  une ligne de mots-clés de recherche (mythomètre, exploit sportif, conférence de presse…) pour qu'un
  grep sur n'importe quel alias tombe dessus.
- **Quatre points d'entrée** pour qu'aucune session ne les rate : une section en tête d'`ETAT.md`
  (injecté automatiquement au démarrage), une consigne dans `CLAUDE.md` (chargé automatiquement),
  une ligne dans la structure du `README.md`, et **un bloc dans le hook de démarrage** qui liste les
  sept noms à l'écran à chaque nouvelle session.
- Documenté aussi ce qui est **brûlé**, pour qu'aucune IA ne le repropose, et **le fil rouge des huit
  euros de dette de Sady**, qui circule entre le Business Bro, Le Journaliste et Le Contrôle
  technique : c'est le running gag du compte.

**Appris**

- Un format écrit dans le dépôt n'existe que s'il est **retrouvable sous le nom que Nabil emploie**.
  « Le mythomètre » et « Bakhal Man » sont le même format, mais une seule de ces deux entrées est la
  bonne. Désormais : le nom de Nabil est le nom du fichier, les autres sont des alias listés.

## 17/09/2026 — Six scripts solo, calibrés au débit mesuré

Nabil en voiture, prêt à tourner 5-6 vidéos solo « dans le délire de T'inquiète », Gen Z, 50 s à
1 min, avec des indications de mise en scène.

**Fait**

- Calibrage d'abord, écriture ensuite : **3,23 mots/s** sur ses trois montages livrés (T'inquiète
  3,63 · Business Bro 3,37 · MMA de salon 2,77). Donc 60 s ≈ 195 mots. Les six scripts font 199 à
  218 mots → 62-67 s de montage, 75-85 s de rush avec ses respirations.
- [`phase-1-solo/09-scripts-solo-17-09.md`](phase-1-solo/09-scripts-solo-17-09.md) : le projet de
  groupe · le groupe WhatsApp qui prévoit rien · les ventes entre particuliers · le mariage où tu
  manges à 1 h du matin · le salaire qui dure quatre jours · « et le vrai travail ? ».
- Chaque script : hook au mot près, escalade en paliers, chute courte, indications de jeu
  (où ça monte, où ça se dit bas, où couper) et une dernière ligne *(bonus)* qui appelle le
  commentaire — le levier que le benchmark de Sady laisse sur la table.
- Six idées écartées avec leur raison (groupe WhatsApp familial, Netflix, auto-école, « ici on est
  une famille », la vanne de la mitochondrie, le pote à une seule anecdote).

**Décidé**

- Les cinq leviers de vue sont écrits en tête du fichier, pas éparpillés : le hook est la vanne, un
  chiffre précis dedans, escalade en paliers courts, chute puis SILENCE, et l'appel au commentaire.
- Le script « ventes entre particuliers » est livré avec son risque écrit noir sur blanc (l'acheteur
  à 2 € est un angle vu) et placé en dernier dans l'ordre de tournage : c'est celui qui saute.
- Le script du tonton porte une consigne inverse des autres : ne pas surjouer l'émotion finale,
  sinon la chute tombe dans le mièvre, qui est interdit par la charte.

**Le thème « vente » refait : un hook qui ouvre une question, et une descente**

Nabil sur mon script des ventes en ligne : « le thème a un potentiel mais comme ça il est vraiment
mid. Faut un vrai hook qui fait rester les gens. Autour de Vinted, les business man 2.0. Faut que ça
soit hilarant. »

Diagnostic : le script parlait de **six personnes différentes** (le négociateur, le curieux, le
photographe, le vendeur menteur…), son hook était un mème déjà vu, et le corps était une liste de
plaintes interchangeables. On peut partir à n'importe quel palier sans rien manquer.

Deux règles écrites en §2 ter de `01-persona-et-regles.md` :
1. **Le hook ouvre une question, il n'annonce pas un sujet.** « Il a lancé son entreprise. C'est un
   compte Vinted » pose « à quel point c'est pire que ce que j'imagine ? ».
2. **Le corps est une descente sur UN seul type de personne**, pas une liste. Test : si deux paliers
   s'échangent sans rien changer, c'est une liste, donc c'est mid.

Écrits : **le businessman 2.0** (le stock sous le lit, la mère comme logistique, le service client à
3 h du matin, le Black Friday à moins un euro, la PlayStation vendue pour 40 pulls dont 2 vendus) et
**le mec qui a « économisé »** (la raquette de tennis à moins 50 %, les économies additionnées comme
des gains, la banque qui appelle, le ticket perdu). Contrôle anti-doublon avec le Business Bro
(Vidéo 3) : aucun palier commun, vérifié terme par terme.

**Correction majeure, le même jour : il est NARRATEUR, pas acteur**

Après mes quatre scripts de remplacement (bourrés d'indications de jeu : mimer un volant, tenir
trois voix, jouer le prof), Nabil : « je tourne pas, je parle juste avec ma bouche. Je joue pas de
personnage. Je suis narrateur. J'ai pas un jeu d'acteur pour pouvoir jouer, caresser la voiture,
faire tout ce que tu me dis. C'est pas ça mon but. »

**Il a raison et c'est vérifiable sur ses cinq vidéos tournées : aucune scène jouée.** Ce qu'il fait,
c'est de la narration à la troisième personne, des citations jetées dans sa propre voix (« il te dit
t'inquiète ») et des apostrophes au mec absent (« frère, redescends sur terre », « diversifie déjà
ton frigo »). L'apostrophe est son moteur, pas le jeu.

Ma règle de la veille (« la loi du personnage : Nabil joue et imite quelqu'un ») était fausse sur sa
conclusion. Ce qui restait juste : **le sujet doit être un type de personne** (7/7 des gardés, 0/4
des rejetés). Mais une personne dont il PARLE. §2 bis de `01-persona-et-regles.md` est réécrit en
conséquence, avec ses formes de hook relevées sur ses vidéos et l'interdiction explicite de toute
indication de jeu dans un script.

Les six scripts sont réécrits en mode narrateur dans
[`10-scripts-narrateur-17-09.md`](10-scripts-narrateur-17-09.md) : 187 à 228 mots, 58 à 71 s, zéro
indication de jeu (vérifié automatiquement). Le fichier `09-…` devient de l'historique.

**Appris (et c'est la leçon du jour)** : il ne suffit pas de trouver la corrélation, il faut trouver
la bonne cause. « Ses scripts gardés ont tous un personnage » était vrai ; « donc il joue des
personnages » était faux. La même donnée, deux lectures, et une seule qui correspond à ce qu'il fait
vraiment devant la caméra. Sur ce projet, quand une règle est inférée d'un refus, elle se vérifie
contre les rushs avant d'être écrite comme loi.

**Le tri de Nabil, et ce qu'il a révélé**

Il garde le projet de groupe et le tonton. Les quatre autres : « vraiment bof, je me sens pas de
faire rire tout le monde avec ça. »

Test appliqué à ses 11 scripts connus : **7/7** de ceux qu'il a validés, tournés ou gardés ont un
personnage qu'il joue ; **0/4** des rejetés. Les quatre parlaient d'un groupe WhatsApp, d'une appli,
d'un mariage et d'un compte en banque : des situations, personne à imiter. C'est devenu la
**LOI DU PERSONNAGE**, écrite dans `01-persona-et-regles.md` §2 bis, et elle passe devant les autres
filtres. Corollaire : le personnage doit lui faire quelque chose À LUI, et sa voix se joue, elle ne
se rapporte pas (l'imitation du Business Bro reste le meilleur moment jamais mesuré : +22,3 dB,
chute 100/100).

Quatre remplaçants écrits dans la foulée, un personnage chacun : **le pote qui change quand il
conduit** (se joue assis dans la voiture, le décor devient le sujet), **le prof qui rend les copies
par ordre de note**, **le daron au téléphone**, **le pote qui a jamais perdu** (la manette, le lag,
le fil débranché du pied). Programme final : six vidéos, six personnages, trois registres (pote,
école, famille), aucun doublon.

**Appris**

- La question « combien de mots pour une minute ? » se règle par la mesure, pas au feeling : ses
  trois montages varient de 2,77 à 3,63 mots/s selon l'énergie de la prise. La moyenne pondérée est
  la seule base honnête pour écrire une longueur.
- **Un script peut cocher tous les filtres de la charte et être refusé quand même.** Les quatre
  rejetés avaient hook, chiffre, escalade et chute. Il manquait la seule chose que la charte ne
  disait pas encore : quelqu'un à jouer. Une règle de plus, tirée d'un refus.

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

**Troisième passe** : « très très drôle les deux ». Deux de plus sur le même moule (Nabil =
l'institution, Sady = le véhicule) : **le GPS de la vie** (« Recalcul de l'itinéraire », « vous êtes
arrivé : chez vos parents, comme depuis 2019 ») et **le contrôle technique** (« défaillance majeure »,
« interdiction de circuler », contre-visite avec les huit euros). Et le **script complet de la note
cachée** sur les fast-foods, avec les deux notes scandaleuses décidées avant (3 à McDo, 5 au grec du
quartier) et la chute « il rentre à pied ».

**Ce qui tient la ligne des cinq formats** : un objet (carton, déo, planchette, la voiture), un rôle
fixe chacun, Nabil qui ne rit jamais, une chute qui est une sentence, et le public qui fournit
l'épisode suivant. Les huit euros de dette circulent d'un format à l'autre : c'est le running gag du
compte.

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
