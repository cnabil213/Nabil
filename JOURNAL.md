# JOURNAL — une entrée par session

> Append-only : on ajoute en haut, on ne réécrit pas le passé.
> Une entrée = ce qui a été fait, ce qui a été décidé, ce qui a été appris.
> L'état courant, lui, vit dans [`ETAT.md`](ETAT.md) et se réécrit.

---

## 10/10/2026 (regroupement) — Une seule branche `main`, `phase-1-solo/` rangé en trois

Nabil : « est-ce qu'il est bien rangé ou c'est le bordel ? » Mesuré avant de répondre : la branche par
défaut (`nabil-content-strategy-2025-ihrj59`) s'arrêtait au 15/09, il lui manquait 51 commits ; le
travail du 10/10 était sur quatre branches qui ne se voyaient pas ; `livraisons/15sept-tinquiete-HQ.mp4`
y est en **720p, 36,7 s** contre **1080p, 34,7 s** sur les branches récentes (ffprobe sur les deux).

**Fait** (ok de Nabil sur la carte « Oui, regroupe »)

- `y6378j`, `jlzjd4`, `b25fqi`, `hzlxyx`, `qvwcj2` fusionnés dans `main`. Vérifié : aucune des 10 branches
  distantes n'a un commit absent de `main`. Conflits seulement dans `ETAT.md` et `JOURNAL.md` : les entrées
  des deux côtés sont gardées, et pour les objectifs la version la plus récente (coach tournage).
- `phase-1-solo/` coupé en `strategie/`, `scripts/` (avec `cartes/`), `tournage/`, renuméroté : il y avait
  deux 07, deux 08, deux 12 et trois 13. Tous les liens entre fichiers réécrits et vérifiés (0 lien cassé).
- Aucune branche supprimée, la branche par défaut n'a pas été changée : c'est Nabil qui le fait.

**Appris**

- Chaque fil crée sa branche depuis l'état qu'il trouve. Sans branche commune, on re-divise en un jour.
  Règle : toute session part de `main` et y revient.

---

## 10/10/2026 (suite) — Les relances, case fixe de chaque fiche

**Décidé par Nabil (10/10, 14h17)** : chaque vidéo préparée arrive avec son hook écrit **et des
phrases drôles sur lesquelles rebondir**. Case ⑧ ajoutée à la fiche, remplie pour les trois sketchs
du tournage #1 (4 relances chacun), dites à la fin du fichier « hooks » pour être montables sans
retourner. Écrites d'après les scripts validés du dépôt ; ses vidéos du Drive n'ont pas été vues.

---

## 10/10/2026 (suite) — Les sources du Dénicheur ouvertes une par une

**Fait** : les quatre sources du classement téléchargées (yt-dlp, API de syndication de X) et
regardées en entier : coupes de plan mesurées (ffmpeg, seuil de scène), voix transcrite
(faster-whisper), image la plus nette choisie par variance du laplacien. Captures recadrées dans
`/mnt/project-files/cnabil/coach-tournage/fond-vert/`.

**Appris** : deux miniatures sur quatre trompaient. La vidéo jointe au « menu à 15 balles » montre
des tirs d'armes à feu ; le faux Mbappé tient un pistolet. Et l'Akatsuki n'a **aucune cape visible** :
le script disait le contraire. Une trouvaille jugée sur sa miniature est non vérifiée.

---

## 10/10/2026 (suite) — La réaction fond vert

**Fait** : section 4 de `phase-1-solo/tournage/01-coach-tournage.md`. Règle photo / vidéo, choix de l'extrait (mesuré sur la
source, jamais de tête), tournage en app Caméra sans l'effet TikTok, cadre plus bas. Lot 2 du
Dénicheur classé : trois en photo ou sans image, aucun en vidéo.

**Décidé (à confirmer par Nabil)** : la fausse vidéo IA de Mbappé ne s'affiche pas, même floutée.

**Vérifié** : la superposition d'une capture sur une vidéo 1080×1920 fonctionne (ffmpeg, 10/10).
**Non vérifié** : le détourage pour un vrai fond derrière lui (mediapipe absent du conteneur).

---

## 10/10/2026 — Coach tournage : préparer pour ne jamais refaire

**Fait**

- `phase-1-solo/tournage/01-coach-tournage.md` : la fiche de préparation (à remplir la veille), le protocole
  sur place, et les fiches du tournage #1 (pote au volant, pote qui a jamais perdu, père au
  téléphone), plus la fiche express de l'actu et six questions pour que Nabil raconte ses storytimes.

**Appris (mesuré, mots du script ÷ 3,23 mots/s)**

- Les trois sketchs « définitifs » du 17/09 font **65 à 70 s** montés, au-dessus des 35-60 s du plan.
  Hooks : 5,9 s (volant), 5,0 s (jamais perdu), 3,4 s (père). Scripts non réécrits : un hook B à
  tourner en plus et un bloc coupable désignés par vidéo, choix au montage.
- Chaque chute est un **rappel** d'un bloc précédent (l'agneau, le débrief, « comme ça ») : ce bloc
  est le maillon qu'on ne coupe jamais. Leçon Business Bro appliquée avant le tournage, pas après.
- Ce qui a fait perdre des prises jusqu'ici (prémisse coupée, négation ratée, ventre à −8 dB,
  720p de nuit) se corrige **avant** ou **sur place** : 3 fichiers par vidéo (intégrale, hooks,
  chutes) et un contrôle de 2 minutes avant de démarrer le moteur.

---

## 10/10/2026 — Le plan recalé : démarrage ce week-end, veille du matin branchée dessus

**Fait**

- `phase-1-solo/strategie/06-plan-croissance-100k.md` mis à jour : le compte n'est pas encore créé, et la veille du 10/10 a
  trouvé une tendance France-Belgique qu'aucun Belge n'a prise. Le lancement passe au week-end
  (V1 samedi ou dimanche 19h, stitch « Réponse d'un Belge » le dimanche), le stock glisse de deux
  jours, 16 vidéos au 25/10 au lieu de 14.
- Nouvelle section §5 bis : ce que la veille de 7h26 cherche (actu < 24 h non prise par un Belge,
  type de personne qui revient dans les plus partagées, durée et forme qui font partager) et à quelle
  case du mix chaque idée sert. Metricool pour les stats, captures TikTok Studio pour la rétention.

**Décidé par Nabil (10/10, 12h43)**

- **Cible : toute la francophonie**, « de Bruxelles à Marseille ». Pas d'angle belge. Le stitch
  « Réponse d'un Belge » et le sketch « Le Belge de mauvaise foi » sont écartés : ils le rangent dans
  la case « le Belge ». Test ajouté au §3 : un Marseillais et un Bruxellois comprennent la vanne sans
  explication.

- **« C'est pas l'actu, c'est la trend. »** (12h55) Nabil ne traite pas l'actualité, il n'est pas
  journaliste : il reprend ce qui marche sur TikTok, X et Instagram, à sa sauce, au second degré. Le
  mot « actu » est retiré du plan, remplacé par « trend » (§3 ter, §5 bis).

**Appris**

- Nabil : « j'ai l'impression qu'on avance à l'aveugle ». Le plan existait mais n'était pas relié à
  la veille ni validé par lui. Un outil sans case dans le plan, c'est ça qu'il appelle avancer à l'aveugle.

## 09/10/2026 (suite) — Le plan de croissance 0 → 100 K

**Fait**

- Plan d'exécution complet : [`phase-1-solo/strategie/06-plan-croissance-100k.md`](phase-1-solo/strategie/06-plan-croissance-100k.md).
  Rythme, mix de formats, règles de hook, routine quotidienne, seuils par vidéo, et les deux
  premières semaines jour par jour (12/10 → 25/10), stock d'abord, puis trois tournages.

**Décidé (par défaut, à faire confirmer)**

- Échéance **31/01/2027**, pas le 09/01 : c'est ce que Nabil a écrit (« fin janvier »).
- T'inquiète sort en version 1080p (la plus nette) ; L'otage du téléphone passe en dernier du stock.
- Sous-titres automatiques de TikTok dès le départ, en attendant qu'il tranche la question de la DA.
- Instagram à partir du 26/10, en repost du fichier de `livraisons/`.

**Appris**

- Au niveau de Sady (38 K de médiane) sur 112 vidéos, on finit vers 21 à 42 K abonnés (hypothèse de
  conversion 0,5 à 1 %). Les 100 K se jouent sur 4 à 8 vidéos au-delà du million : d'où le volume et
  la règle « suite dans les 48 h » quand une vidéo fait 10 fois la médiane.
- TikTok (page officielle) : ni le nombre d'abonnés ni les vidéos passées ne sont des facteurs directs,
  et le pays est un signal faible. Un compte belge touche la France.
- Creator Rewards : aucune source ne liste la Belgique. On ne rallonge pas les vidéos au-delà d'une
  minute pour une monétisation qu'il ne touchera peut-être pas.

---

## 10/10/2026 (suite 3) — Repartir de @hitmakingz (12 700 abonnés) ?

Nabil propose de repartir d'un vieux compte de mèmes au lieu d'un compte neuf.

**Mesuré** : créé le 24/12/2021, 12 700 abonnés, 5 vidéos publiques (reposts de micro-trottoirs) toutes
entre le 25/12/2021 et le 17/01/2022, 77 % des vues sur une seule (2,5 M). Pseudo jamais changé.

**Avis** : oui, si le statut du compte est propre (à vérifier par capture). TikTok dit que le nombre
d'abonnés et les anciens succès ne sont pas des critères directs de recommandation (Newsroom, 2020) :
le compte ne bloque rien, et il apporte la preuve sociale et le LIVE débloqué. Détail :
`phase-1-solo/strategie/07-compte-hitmakingz.md`.

---

## 10/10/2026 (suite 2) — Le pseudo, deuxième tour : C'Nabil

Nabil : « Justenabil j'aime pas et cnabil c pas mon compte. » On garde son nom de rappeur, C'Nabil, en
variante libre. Vérifié sur TikTok à 14:27 : **@cnabil.tv** (proposé en premier), @yacnabil,
@levraicnabil libres. @cnabiil est pris (1 747 abonnés) : toute variante à lettre doublée enverrait les
gens chez lui. Instagram toujours non vérifiable sans connexion.

---

## 10/10/2026 (suite) — Le pseudo : vérifié sur TikTok

Nabil : « on n'a toujours pas inventé de pseudo pour Insta, etc. » Son pseudo de rappeur : Cnabil_213.

**Mesuré** (page publique TikTok, étalonnée sur un compte connu et un pseudo au hasard)

- Pris : @cnabil (privé, « nabil H », 78 abonnés), @cestnabil, @nabiltoutcourt, @c.nabil, @c_nabil,
  @cnabil_, @lenabil. **Le premier choix d'hier était pris** : on l'aurait su avant en vérifiant.
- Libres : **@justenabil**, @nabilenvrai.
- @cnabil_213 : privé, « C'Nabil🚸 », **1 152 abonnés** (pas 2 000-3 000 comme noté fin septembre).
- Instagram : impossible à consulter sans connexion. Non vérifié.

**Décidé (proposé)** : @justenabil, repli @nabilenvrai, @cnabil seulement s'il est à lui. L'ancien compte
rap est gardé, pas réutilisé : un post de passage vers le nouveau, puis il dort.

---

## 10/10/2026 — Blow Up, et premier passage du dossier Drive

**Fait**

- Enquête Blow Up : aucune des deux apps ne nomme son IA, leurs « vues prédites » ne sont pas des
  mesures. Rapport : [`outils/RECHERCHE-BLOWUP.md`](outils/RECHERCHE-BLOWUP.md).
- Dossier Drive de Nabil (11 vidéos) lu par son lien public avec `recuperer.sh` ; inventaire, rangement
  proposé et premier rapport coach (« arrêté de fumer ») :
  [`phase-1-solo/tournage/02-drive-inventaire-et-coach-fumer.md`](phase-1-solo/tournage/02-drive-inventaire-et-coach-fumer.md).

**Appris**

- Le connecteur Google Drive répond « Forbidden » sur ce dossier : lecture possible par le lien public,
  pas de renommage tant que le connecteur n'y a pas accès.
- Les .mov du Drive sont des **exports CapCut** (`TEEditor`, `DreaminaMetaInfo`), pas des originaux ;
  les trois tier lists du 14/09 y sont en **540×960**.
- **Erreur de rangement corrigée** : j'avais classé les exports CapCut comme rushs. Un export CapCut =
  un montage de Nabil. Ne jamais déduire l'état d'une vidéo de ses métadonnées seules : demander, ou
  mesurer (coupes franches, durée par rapport au rush).
- `faster-whisper` installé par pip casse sur `av` récent (`metadata_errors`) : passer un tableau numpy
  lu depuis un wav extrait par ffmpeg.

## 10/10/2026 — Branding : francophone, pas belge

Nabil : « je veux être connu dans la francophonie. J'ai pas de problématique avec le contenu belge,
mais je veux toucher un maximum de monde. Je veux qu'on me connaisse de Bruxelles à Marseille. »

**Décidé**

- Plus aucun marqueur belge dans la marque : 🇧🇪 retiré de la bio, @nabil.be et @nabilunefois retirés
  des pseudos (remplacés par @nabiltoutcourt et @nabilenvrai). @cnabil reste le premier choix.
- Règle d'écriture : une référence que seul un Belge comprend ne porte jamais la vanne. L'actu traitée
  est celle de toute la francophonie.
- Le compte reste déclaré en Belgique, où il vit : pas de faux pays.

**À vérifier** : la part de vues venues de France, dans les stats d'audience par pays, dès les 10
premières vidéos. L'idée que la langue et le sujet comptent plus que le pays déclaré est déduite, pas
mesurée.

---

## 09/10/2026 (suite 2) — Le branding recadré : un compte centré sur Nabil

Nabil, quelques minutes après la première version : « je veux que dans mon contenu je puisse tout
faire. L'actualité, une story time, un sketch. Que les gens me suivent pour moi. »

**Décidé (proposé, à valider)**

- Le mytho n'est plus le thème du compte, c'est un angle. Positionnement : « Nabil raconte tout ce qu'il
  voit, les gens, sa vie, l'actu, et il dit le verdict que personne n'ose dire. »
- Bio : « Je raconte tout ce que je vois. Même sur moi. / 🇧🇪 Sady me doit 8 € » (67 caractères).
- Signature : la note de fin devient « VERDICT x/10 », posée sur **tous** les formats, lui compris dans
  ses storytimes. C'est le fil rouge commun.
- Ordre : sketchs prêts d'abord, storytime vers la 5e vidéo, actu en dernier et légère (pas de
  politique, religion, guerre ni faits divers graves : risque de restriction).

**Appris**

- Dit franchement à Nabil : à 0 abonné, TikTok pousse une vidéo, pas une personne. Le « pour moi » se
  gagne par la répétition d'un mec reconnaissable : même cadre, même attitude, même fin, une bande
  récurrente (Sady, les 8 €), des réponses aux commentaires, les LIVE.

---

## 09/10/2026 (suite) — Le branding TikTok

Nabil : « Je veux que Nabil soit connu. La révélation humoristique de Belgique l'année prochaine. »
Décidé avant : nouveau compte en Belgique, TikTok d'abord, Instagram ensuite, pas YouTube.

**Fait**

- [`phase-1-solo/strategie/05-branding-tiktok.md`](phase-1-solo/strategie/05-branding-tiktok.md) : positionnement, 5 pseudos
  classés, bio prête à copier (74 caractères), photo, couvertures, signature, monétisation.

**Décidé (proposé, à valider par Nabil)**

- Positionnement : **« Nabil démasque les mythos que t'as tous autour de toi. »** Il relie le solo
  (contraste prétend/est) et les formats duo (Bakhal Man = mythomètre). Les mythos sortent en premier.
- Pseudo : @cnabil, puis @cestnabil, @justenabil, @nabil.be, @nabilunefois. Nom affiché : « Nabil ».
- Signature : le carton de fin muet « TAUX DE MYTHO x/10 », incrusté au montage. Jugé à la 10e vidéo
  sur les commentaires qui citent la note.

**Appris**

- 3 des 4 solos montés et ~10 des 21 sujets en stock sont des mythos (comptage sur les titres, à
  revérifier sur les textes).
- Creator Rewards : la Belgique n'apparaît dans aucune liste de pays publiée en 2026 (recherche du
  09/10), et le programme exige d'y résider. Pas de faux pays.

---

## 09/10/2026 — Tout regroupé : cinq branches fusionnées en une

Nabil ouvre le projet « C'Nabil-FAMOUS » pour tout centraliser, avec un objectif : **100 000 abonnés
en 3 mois**.

**Fait**

- Inventaire du dépôt : **5 branches** de sessions (stratégie, idées vidéos, Montpellier, agenda,
  automatisation montage), jamais fusionnées entre elles. Fusionnées dans `claude/project-thread-qvwcj2`.
- Conflits ETAT / JOURNAL / backlog résolus en gardant les deux côtés. Le journal est refondu par date :
  l'entrée « 5 clips » du 15/09, perdue par une fusion précédente, est revenue.
- `15sept-tinquiete-5clips-HQ.mp4` récupéré depuis l'historique : la version 1080p l'avait écrasé sous le
  même nom.
- Lecture des anciennes sessions Claude Code : tout le contenu y est déjà commité, sauf le montage perso
  de la tier list sport (perdu, jamais versionné).
- Synthèse dans `/mnt/project-files/cnabil/SYNTHESE.md`.

**Appris**

- **Des sessions parallèles sur des branches séparées écrivent des doublons et se contredisent.** Deux
  séries de scripts le même jour, deux montages de « T'inquiète » sous le même nom. Une seule branche
  de référence à partir de maintenant.
- **Compte TikTok** : une session business parle d'un ancien compte rap de 2 000 à 3 000 abonnés, ce
  dépôt disait « aucun compte ». À confirmer.

---

## 21/09/2026 (suite 3) — L'histoire de Sady : « Le bus »

Deuxième vocal de Nabil : le bus. En vrai, bus en retard, iPhone à plat, son gars Steve qui sortait du
taf, des gens qui toussaient. Trois mensonges par-dessus : bus sponsorisé Apple, Steve Jobs, zombies
stade 10. Écrit dans `phase-1-solo/scripts/09-bakhal-man-montpellier.md` § Histoire 2, 100 mots, 30-35 s. L'épisode complet
tient dans 1 min 20 à 1 min 30, pile le plafond.

**Décidé**

- « Allez, t'as menti » du vocal devient « Bon allez » + carton : le format interdit « tu mens », et
  « bon allez » est déjà le tic de Nabil dans les deux vocaux.
- Chaque palier a sa question de chiffre : « Steve Jobs est mort en 2011 » (ajouté), « ils faisaient
  quoi, les zombies ? » → « ils toussaient » (la grippe du vocal, rendue par Sady lui-même).
- **Le ton du carton est agacé, blasé** (« presque même agacé : bon allez, huit »), pas neutre-poli comme
  FORMATS.md le disait. Corrigé dans FORMATS.md § A1.
- La question « quel est le rapport entre plus de batterie et Apple ? » posée par Nabil dans le vocal :
  le rapport, c'est que la concession est plus nulle que prévu. « J'avais juste mon iPhone. Et il était
  à plat. »

**Appris** : la meilleure concession est un jeu de mots sur le mensonge lui-même (« Steve Jobs » →
« Steve, il sortait du job »). À chercher dans les prochains épisodes : le mensonge et sa version vraie
partagent un mot.

---

## 21/09/2026 (suite 2) — Relecture du vocal : trois erreurs de lecture corrigées

Nabil a renvoyé la transcription en demandant de la relire, parce qu'ils tournent bientôt en voiture.
La relecture ligne par ligne a montré que ma première version lisait le vocal de travers :

| Ce que j'avais écrit | Ce que le vocal dit |
| :--- | :--- |
| « Bruxelles » = du bruit, coupé | **Le vrai trajet : Bruxelles–Montpellier, en avion.** Ils partent de Belgique (les studios de la Phase 2 sont à Bruxelles). « bosser Montpellier » = « Bruxelles–Montpellier » |
| « 23 questions » | « deux-trois questions » |
| « neuf » = Sady concède neuf douanières | « bon allez, toi, neuf » = **le carton à 9** |
| Sady raconte, Nabil tient le carton, pas de deuxième histoire | **Nabil raconte Montpellier, Sady tient le carton, puis on inverse.** C'est la construction de Nabil, elle prime sur les rôles fixes de FORMATS.md |
| le TGV direct | l'avion (« je prends l'avion ») : « y'a un vol direct Charleroi–Montpellier » |

**Fait** : le fichier `phase-1-solo/scripts/09-bakhal-man-montpellier.md` réécrit avec une section 0 qui liste ces corrections,
une **version courte** pour l'épisode à deux histoires (Montpellier 4 → 10 → 0 → 2, mots comptés, 45-50 s,
il reste 30-35 s à Sady) et la **version longue** de secours. FORMATS.md § A1 note que le carton change de
mains à chaque histoire. Deux vrais détails du vocal récupérés : « t'as attendu ta valise » (dans le récap)
et « ils m'ont quand même mis sur le côté » (la défense finale, mot pour mot).

**Appris** : une transcription vocale ne se lit pas une fois. « Bosser », « avallée », « 23 » étaient des mots
réels déformés, pas du bruit, et le seul moyen de le voir était de relire avec le contexte (Belgique). Avant
de jeter une ligne d'un vocal, chercher le mot réel derrière.

---

## 21/09/2026 (suite) — Bakhal Man, épisode 2 : « Montpellier »

Nabil a envoyé la transcription vocale d'un brainstorming à deux (« je suis passé par le Monténégro »,
dix douanières, trafic d'humains, la valise qui bipe, le doudou) et demandé : le script au propre, un
hook pensé pour le concept, deux-trois avis, des blagues, 1 min à 1 min 30 max.

**Fait**

- **Fusion de la branche `video-ideas-social-media`** dans celle-ci : le concept n'existait que là-bas
  (FORMATS.md, `phase-1-solo/scripts/08-concepts-duo.md`, les cartons). Sur les conflits (ETAT, JOURNAL, « T'inquiète »), la
  version de l'autre branche a été gardée : elle est postérieure et plus complète.
- [`phase-1-solo/scripts/09-bakhal-man-montpellier.md`](phase-1-solo/scripts/09-bakhal-man-montpellier.md) : chaîne de
  sens en cinq maillons, script avec le carton à chaque réplique (trajet 4 · 6 · 7 · 3 · 9 · 9 · 5 · 10 ·
  10 · 0 · 2), hook, avis, blagues de réserve, titres, filtre des interdits. Lien ajouté dans FORMATS.md § A1.
- **200 mots de dialogue** (comptés), soit 62 s de parole au débit mesuré de 3,23 mots/s et 1 min 15 à
  1 min 30 avec les temps du carton. Plan de coupe si ça dépasse : le maillon Suisse–Lyon.

**Décidé**

- **Le récap est la chute et tient en une respiration** : quatre faits, « Zéro. C'est vrai. Et c'est nul. »
  Nabil l'avait dit lui-même dans le vocal (« c'est trop long ») ; c'est la formule fixe du format.
- **Une seule histoire par vidéo, et c'est Sady qui raconte.** Le « après toi tu fais pareil » du vocal
  est refusé : la durée, et la règle du 17/09 (Nabil ne joue pas de personnage ; s'il raconte le
  Monténégro, il joue).
- Jeté du vocal : « Bruxelles » (incompréhensible), « 10 filles » (→ douanières), l'avion (→ TGV direct,
  meilleure pique et vrai trajet plus minable).

**Appris**

- **Chaque épisode a besoin d'une question de chiffre qui tue** (« il pesait combien ? », comme « deux
  mètres » dans La bagarre). C'est la seule arme de Nabil, et c'est Sady qui produit lui-même le chiffre
  qui tue son histoire. À trouver avant d'écrire le reste.
- **La première phrase de Sady contient déjà le mensonge** (Montpellier / Monténégro) et le carton
  répond sans un mot : le format s'explique tout seul, jamais par une intro.

---

## 21/09/2026 — FORMATS.md : les formats ne se perdent plus

Nabil : « tu as pas mis les idées de format Bakhal Man, l'exploit sportif… j'ai ouvert une autre
session mais il a pas trouvé les 2 formats dans le dépôt. Crée un fichier md et mets dans le dépôt
le format annexe qu'on peut viser sur mon compte TikTok. »

**Le diagnostic** : les formats existaient bien, mais introuvables. Ils étaient enterrés au milieu de
`phase-1-solo/scripts/08-concepts-duo.md`, sous les noms « mythomètre » et « interview d'après-match » — pas sous les noms
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

---

## 17/09/2026 — Six scripts solo, calibrés au débit mesuré

Nabil en voiture, prêt à tourner 5-6 vidéos solo « dans le délire de T'inquiète », Gen Z, 50 s à
1 min, avec des indications de mise en scène.

**Fait**

- Calibrage d'abord, écriture ensuite : **3,23 mots/s** sur ses trois montages livrés (T'inquiète
  3,63 · Business Bro 3,37 · MMA de salon 2,77). Donc 60 s ≈ 195 mots. Les six scripts font 199 à
  218 mots → 62-67 s de montage, 75-85 s de rush avec ses respirations.
- [`phase-1-solo/scripts/06-scripts-solo-17-09.md`](phase-1-solo/scripts/06-scripts-solo-17-09.md) : le projet de
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

Deux règles écrites en §2 ter de `phase-1-solo/strategie/01-persona-et-regles.md` :
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
des rejetés). Mais une personne dont il PARLE. §2 bis de `phase-1-solo/strategie/01-persona-et-regles.md` est réécrit en
conséquence, avec ses formes de hook relevées sur ses vidéos et l'interdiction explicite de toute
indication de jeu dans un script.

Les six scripts sont réécrits en mode narrateur dans
[`phase-1-solo/scripts/07-scripts-narrateur-17-09.md`](phase-1-solo/scripts/07-scripts-narrateur-17-09.md) : 187 à 228 mots, 58 à 71 s, zéro
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
**LOI DU PERSONNAGE**, écrite dans `phase-1-solo/strategie/01-persona-et-regles.md` §2 bis, et elle passe devant les autres
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

---

## 17/09/2026 — Le planning de Nabil posé dans l'agenda partagé avec Sady

**Fait**

- Connecteur **Google Calendar** branché par Nabil (il n'était pas installé ; la connexion OAuth
  ne peut pas être faite par l'IA, c'est lui qui clique).
- Agenda **SADY NABIL** (`Europe/Brussels`) rempli : il était vide. **36 événements** posés.
- Le roulement 2×8 : **20 shifts 6h-14h + 15 shifts 14h-22h**, lun-ven, alternance une semaine
  sur deux, du 14/09 au 30/10. Ancré sur la semaine du 14/09 en 6h-14h, celle que Nabil a faite.
- **Samedi 26/09, 9h-18h** : événement jeune entrepreneur Odoo, Nabil + Sady.
- Dispos reportées dans [`ETAT.md`](ETAT.md) : elles décident des créneaux de tournage.

**Appris**

- **Poser 35 shifts en 2 événements récurrents, pas en 35 événements.** Deux `RRULE`
  `FREQ=WEEKLY;INTERVAL=2;WKST=MO;BYDAY=MO,TU,WE,TH,FR` décalées d'une semaine suffisent à
  décrire toute l'alternance. Si le planning bouge, on modifie la série une fois.
- **Le changement d'heure est un piège sur une série qui traverse octobre.** L'heure d'hiver tombe
  le 25/10 ; la dernière semaine est de l'autre côté. Vérifié dans l'agenda après écriture :
  `2026-10-26T06:00:00+01:00` — le décalage passe de +02:00 à +01:00 et **6h reste 6h**. C'est ce
  que donne le champ `timeZone` ; un horaire écrit en offset fixe aurait dérivé d'une heure.
- **La règle « rien sans mesure » vaut aussi hors vidéo.** Avant de répondre « je ne peux pas me
  connecter », j'ai listé les connecteurs plutôt que de le supposer ; avant d'annoncer l'agenda
  rempli, je l'ai relu événement par événement pour vérifier l'alternance. Le jour de la semaine
  du 26/09 (samedi) a été vérifié en commande, pas de tête : c'est lui qui décidait s'il y avait
  conflit avec le shift.
- **Demander avant d'écrire chez quelqu'un d'autre.** L'agenda est partagé : un shift posé le
  mauvais jour, c'est Sady qui planifie sur une dispo fausse. Trois questions (jours travaillés,
  horizon, horaire de l'Odoo) ont évité de deviner.

---

## 17/09/2026 (suite) — Un chemin de réglage donné sans le vérifier : corrigé

Nabil : « je trouve pas tes paramètres, je comprends rien (…) y'a moyen d'améliorer la capture
Snapchat ou pas ? »

**Erreur de ma part, et du type exact que `CLAUDE.md` interdit.** Je lui avais donné
`Snapchat → Paramètres avancés → Qualité vidéo` comme s'il était établi. En réalité ça venait
d'articles SEO de **vendeurs de logiciels de réparation vidéo** (EaseUS, HitPaw, iMyFone,
Wondershare, Tenorshare), qui se contredisent entre eux, et dont aucun n'est la doc de Snapchat.
Recherche refaite : **aucune source primaire ne confirme ce réglage sur iOS.** Et le fait que Nabil
ne le trouve pas est une donnée plus fiable que ces articles.

**Réponse rendue : non, la capture Snapchat ne s'améliore pas.** 720p, pas de réglage, et changer
de méthode de sauvegarde ne récupère rien puisque la perte est à la prise.

**Le vrai déblocage, et il annule tout le débat** : ce que Nabil aime chez Snapchat, c'est le
**lissage de peau** — et **CapCut le fait**, alors qu'il y est déjà (clip → barre du bas, défiler à
droite → « Retoucher » → « Lisser la peau »). Donc filmer à l'app Caméra en 1080p et lisser dans
CapCut lui donne le look **et** la définition.

**Leçon de méthode** : la règle « rien sans mesure » vaut aussi pour les chemins d'interface. Un
chemin de réglage se cite depuis la doc de l'éditeur, ou se donne comme non vérifié. Un article de
vendeur de logiciel n'est pas une source.

---

## 17/09/2026 (suite) — « 30 fps c'est le pire truc nan ? » — il a raison sur le principe, pas sur son fichier

Nabil conteste la recommandation « 30 im/s, pas 60 », et demande de me renseigner sur la sauvegarde
Snapchat.

**Il a raison, et ma réponse précédente était trop sèche.** 60 im/s est effectivement meilleur que
30 comme format de *capture*. Ce que je n'avais pas expliqué : ça se gagne **à la prise**, pas à
l'export.

**Mesuré** : les **quatre** vidéos solo livrées sont en `30/1` (`r_frame_rate` et `avg_frame_rate`),
cadence constante. Et `grep -n "fps\|-r "` sur `monter.py` ne renvoie **rien** : l'outil ne touche
jamais à la cadence. Donc les 30 im/s viennent bien de Snapchat, pas du pipeline de montage.
Exporter en 60 depuis du 30 duplique les images (identique, deux fois plus lourd) ou les invente
(bavures sur la parole rapide).

**Recherché sur la sauvegarde Snapchat** — trois trouvailles utiles :

1. **Un réglage de qualité vidéo existe** : `Réglages → Paramètres avancés → Qualité vidéo`
   (Automatique / Standard / Faible). Un compte en « Faible » perd de la définition sans prévenir.
   **Jamais vérifié chez Nabil** — c'est la première chose à regarder.
2. **L'export depuis Memories ne dégrade ni ne récupère** : « Exporting Memories does not increase
   resolution or bitrate; it preserves what Snapchat stored. » La perte est **à la capture**, donc
   chercher un meilleur chemin d'export est une impasse.
3. **Snapchat n'utilise pas le pipeline caméra natif d'iOS** : il lit le flux capteur et le traite
   lui-même. C'est ce qui permet le lissage en direct, et ce qui coûte la définition.

**La piste la plus prometteuse, et elle est gratuite :** le « plus beau sur Snap » a trois causes —
lissage de peau + yeux éclaircis appliqués par défaut, saturation poussée, et **le miroir**. iOS a
`Réglages → Appareil photo → Miroir photo de face` ; désactivé, la vidéo est enregistrée inversée
par rapport au retour écran. On se connaît en miroir, donc la version non-miroir paraît étrange.
**Un bouton, et il récupère peut-être le 1080p sans perdre sa tête.**

**Non mesuré, et demandé** : son NOUVEAU rush Snapchat. Les mesures ci-dessus portent sur les
anciens fichiers. Demandé 2 s exportées depuis CapCut (~2 Mo, ça passe dans le chat) pour relever
résolution, cadence, codec et débit réels.

---

## 17/09/2026 (suite) — Réglages d'export CapCut : l'upscale IA ne fabrique rien

Nabil a **refilmé sur Snapchat** — « j'ai l'impression que je suis plus beau sur snap » — et demande
les meilleurs réglages d'export dans CapCut. Capture d'écran : Ultra HD par l'IA ON, 1080p, 60 im/s,
20 Mbit/s, Smart HDR ON, 129,2 Mo estimés pour 49 s.

**Mesuré avant de répondre.** Ses deux rushs livrés : **720×1280, 30 im/s, h264, `yuvj420p`,
`color_range=pc`, `color_transfer=bt709`**. Donc CapCut lui propose de fabriquer du 1080p, du
60 im/s et du HDR à partir d'une source qui n'a aucun des trois.

**Le test de l'upscale**, sur `12sept-casser-des-nuques-HQ.mp4`, 30 images, aller-retour
720p → 1080p → 720p en lanczos (meilleur cas possible) :

| | |
| :--- | ---: |
| Détail du rush 720p (écart-type du passe-haut) | 3,42 |
| Détail après l'aller-retour | 3,25 (95,0 %) |
| **PSNR** | **61,8 dB** |

Au-dessus de 45 dB, l'image 1080p ne contenait rien que le 720p n'avait déjà. À 61,8 dB c'est sans
appel : **l'upscale étale les mêmes pixels sur 2,25× plus de surface, il ne crée pas d'information.**

**Réglages donnés** : Ultra HD par l'IA OFF · 1080p (pour le format natif TikTok, **pas** pour la
netteté) · **30 im/s pas 60** (la source est à 30, 60 duplique) · flux optique OFF · 12-20 Mbit/s ·
**Smart HDR OFF**.

**Le Smart HDR est le point dur**, et c'est un récidiviste : convertir du BT.709 SDR en HDR étire
les valeurs dans un contenant que la source n'a jamais rempli. C'est le mécanisme exact du bug du
12/09 (noirs de 3 → 19, « la vidéo perd en qualité »). Commande de vérification écrite dans le doc :
`color_transfer` doit rester `bt709` après export.

**Sur Snapchat, arbitrage posé sans moraliser.** Sa préférence est fondée — Snap lisse la peau à la
prise. Le prix (720p) est mesuré et irrécupérable. Proposition : filmer **une seule** vanne à l'app
Caméra en 1080p + « Retouche » dans CapCut. S'il se trouve aussi bien, il gagne les deux. Sinon on
reste sur Snap et **on arrête d'en parler** — le confort devant la caméra vaut plus que 360 lignes
si ça l'empêche de tourner.

**Écrit** : [`outils/README-export-capcut.md`](outils/README-export-capcut.md), plus une ligne dans
`CLAUDE.md` §5.

---

## 17/09/2026 (suite) — « Je ne suis pas un acteur » : une règle inventée dans la D.A., corrigée par la mesure

Nabil : « tu dois comprendre que je ne suis pas un acteur (…) je suis juste un narrateur (…) quand je
parlais du mec qui dit toujours "t'inquiète", c'était une narration. Je n'ai pas mimé. »

**Le dépôt disait le contraire — et c'était une invention.** `phase-1-solo/strategie/01-persona-et-regles.md` listait parmi
les mécaniques qui marchent : « **Le hook acting** — ouvrir sur une mimique muette avant même de
parler *(Vidéo 2 : l'esquive dans le vide)* ». Et la fiche de la Vidéo 2 affirmait : « Le hook est
**muet** : la mimique d'esquive démarre avant le premier mot. C'est elle qui arrête le scroll. »

**Mesure sur les quatre vidéos solo livrées — premier son de voix :**

| Vidéo | 1er son de voix |
| :--- | ---: |
| Vidéo 2 — MMA de salon | **0,12 s** |
| Vidéo 3 — Business Bro | **0,05 s** |
| Vidéo 4 — Otage du téléphone | **0,15 s** |
| Vidéo 5 — T'inquiète | **0,11 s** |

**Il parle dès la première image, à chaque fois. Aucune ouverture muette n'a jamais existé.** La
didascalie « [Hook acting] » était une proposition d'écriture qu'une session a recopiée comme un
fait observé, puis promue en « mécanique qui marche » dans la D.A. Elle a ensuite servi de base à
**neuf** des douze scripts des séries 2 et 3.

**Corrigé**

- `phase-1-solo/strategie/01-persona-et-regles.md` : nouvelle section **§3 bis « Nabil est un NARRATEUR, pas un acteur »**,
  avec la mesure, la correction explicite, et un tableau de ce qui est autorisé.
- `phase-1-solo/scripts/01-scripts-valides.md` : didascalie retirée de la Vidéo 2, note de tournage remplacée par la mesure.
- `CLAUDE.md` : une ligne de plus au tableau des contre-exemples, et une section dédiée.
- **Les douze scripts réécrits** : hooks muets refaits en hooks parlés (Clio, Pas faim, Le « ? »),
  vannes gestuelles renarrées (la fenêtre qui bloque, la main-essuie-glace, les mains vides), toutes
  les indications de jeu ramenées à **la voix**.

**La ligne qu'on garde, et elle est mesurée** : l'imitation **vocale** d'un personnage qu'on cite
reste autorisée — c'est son meilleur moment toutes vidéos confondues (Business Bro, **+22,3 dB**,
score de chute **100/100**). Ce qui est banni, c'est le **geste**, pas la voix.

**Le test ajouté à la D.A. :** *si la vanne ne marche plus les yeux fermés, elle est fausse.*
Ses quatre vidéos passent ce test ; neuf de mes douze scripts ne le passaient pas.

**Effet de bord mesuré** : un hook muet coûte 0 mot, un hook parlé en coûte ~20. Trois scripts de la
série 2 sont repassés au-dessus du plafond après réécriture, et ont été resserrés. Trois restent à
233-234 mots, soit 0,3 s au-dessus des 232 — **sous le bruit de la mesure** (3,87 mots/s viennent
d'une seule vidéo). Noté comme tel dans les fichiers au lieu d'être raboté pour faire joli.

---

## 17/09/2026 (suite) — Plafond fixé à 60 s : les douze scripts recalibrés

Nabil : « nan ça doit faire maximum 60 secondes. » La consigne précédente (« au moins 50 secondes,
une minute ») était un plancher ; c'est un **plafond**.

**Traduit en chiffre tout de suite** : 3,87 mots/s mesurés sur « T'inquiète » → **60 s = 232 mots,
maximum**. Quatre scripts dépassaient.

**Méthode de coupe** : retirer **le maillon le plus faible en entier**, jamais raboter partout.
Raboter enlève les détails précis (les chiffres, les noms) et c'est exactement ce qui fait rire.

| Retiré | De |
| :--- | :--- |
| Le palier « 9,99 de musique » | Abonnements |
| « Il écoute même pas la réponse » | Le tonton |
| « Celui qui se reprend dans le même vocal » | Les vocaux |
| « S'il appelle deux fois de suite » | La peur d'appeler |
| Le point relais à quatre kilomètres | Le colis |

Résultat : **les six de la série 3 tiennent en 55 à 58 s**, les six de la série 2 en 57 à 60 s.

**Le cas de la clope, et il est intéressant.** Le script fait **264 mots → 68 s**, et **Nabil l'a
déjà tourné**. On ne réécrit pas un script tourné. À la place, l'**ordre de sacrifice au montage**
est écrit dans sa fiche, à froid : le concert à 150 € part en premier (~12 s) — **avec** son rappel
« ah non, plus de Netflix », sinon le rappel tombe sur rien (chaîne de sens, `CLAUDE.md` §2 bis). Ne
jamais toucher à « vous êtes des moines ? », « moi j'ai jamais fumé » et la chute.

**Deux défauts attrapés par le recomptage**, invisibles à la relecture : « résilier » écrit deux fois
à trois lignes d'écart dans les abonnements, et une note de tournage qui citait encore des chiffres
supprimés du script. Les deux corrigés. **Compter force à relire vraiment.**

---

## 17/09/2026 (suite) — Série 3 : six sujets en adresse directe, zéro « on a tous ce pote »

Nabil a tourné la vanne sur la clope « au feeling » et redemande des thèmes.

**Fait** — [`phase-1-solo/scripts/05-serie-3-adresse-directe.md`](phase-1-solo/scripts/05-serie-3-adresse-directe.md),
six scripts complets, **255 à 269 mots → 60 à 70 s** de montage serré.

**La correction appliquée, et c'est la leçon de la journée.** La série 2 a été jugée « pas ouf ». Le
défaut n'était pas les sujets mais le **regard** : six fois « on a TOUS ce pote qui », soit un
personnage qu'on observe de l'extérieur — la même formule que trois des cinq vidéos déjà faites.
L'idée de Nabil sur la clope a montré l'autre voie : on parle **à** l'audience de **sa** vie.

Pour ne pas remplacer une formule par une autre, les six utilisent **six mécaniques d'adresse
différentes** : l'accusation (« Je sais ce que vous faites »), la prise de nouvelles (« Vous allez
bien ? », son format), l'aveu collectif (« Avouez »), le rappel de service public, le constat
générationnel (« On est la première génération qui… »), l'exigence d'explication (« Expliquez-moi »).

**Sujets** : seul dans ta voiture · les abonnements qu'on utilise pas · le tonton au repas de famille
· les vocaux de 7 minutes · la peur d'appeler · le colis « livré ».

**Méthode, identique à la série 2 et elle a resservi** : premier comptage → cinq scripts courts
(187 à 218 mots, le plus court à 48 s, sous le minimum). Un **vrai palier** ajouté à chacun plutôt
que du délayage — la ligne mystère « GLBL DIGITAL LIMITED » sur le relevé, le tonton qui n'écoute pas
la réponse à sa propre question, les six vocaux d'affilée (« c'est une série »), la messagerie non
écoutée qu'on préfère rappeler, le colis « reporté suite à un incident ». Recomptés : 60-70 s partout.

**Risque noté** : « la peur d'appeler » frôle le thème brûlé « angoisse de la batterie sociale ». La
ligne est écrite dans le script : rester sur l'absurde et les gestes concrets (la pizza, la phrase
répétée, le « ouais ? »), jamais sur la fatigue sociale. À vérifier au tournage.

**En attente** : les rushs de la clope, tournés mais pas encore envoyés.

---

## 17/09/2026 (suite) — Nabil retourne le script 5, et met le doigt sur le défaut des six

Nabil : « les idées, je les ai vraiment pas trouvées ouf. » Puis il propose son angle sur la clope :
« Eh les gars, ceux qui ont arrêté de fumer, vous allez bien ? (…) vous avez arrêté quand l'essence
était pas chère (…) comment vous faites pour toujours pas fumer ? Moi si j'avais fumé, j'aurais fumé
là, maintenant. »

**Sa version est meilleure, et la raison est structurelle** : la mienne *décrivait un pote* (« il fume
les tiennes »), la sienne *interpelle l'audience* (« vous allez bien ? »). Le spectateur est dedans,
il se tague. Et ça révèle le défaut des six : **six fois « on a TOUS ce pote qui »**, la même formule
que trois des cinq vidéos déjà faites. Compétent, mais une formule — il l'a senti avant moi.

**Fait**

- Script 5 réécrit sur son idée : hook à contre-emploi (ton grave, « vous tenez le coup ? »),
  escalade des « depuis » (le plein à 90 balles → le grec à 9 € → Netflix qui t'a séparé de ta mère →
  le concert à 150 €), sommet « vous êtes des moines ? », aveu « moi j'ai jamais fumé de ma vie »,
  **deux chutes à tourner** : la sienne (« j'aurais fumé là, maintenant ») et un retournement
  (« 13 balles le paquet, laissez tomber, je vais pleurer, c'est encore gratuit »). 264 mots → ~68 s.
- Ma version écartée, **documentée avec sa raison** dans le fichier, pour ne pas y revenir.
- Risque plateforme noté à part : TikTok bride ce qui « représente ou promeut » le tabac. Ironie OK,
  aucune vraie cigarette à l'écran, et la chute B retourne le propos contre la clope — en réserve.

**À trancher par Nabil**

- Les cinq autres : les tourner tels quels, ou les réécrire dans son registre (adresse directe à
  l'audience, pas portrait de pote) ? Le fix dépend de ce qu'il a trouvé « pas ouf » : la formule, ou
  les sujets.
- **Proposition DA** : « Eh les gars, ceux qui [X], vous allez bien ? » peut devenir un **format
  récurrent** — un hook reconnaissable en une seconde, c'est ce qui fait abonner (cf. la tier list
  chez Sady). À valider avant d'en écrire d'autres.

---

## 17/09/2026 — Série 2 : six scripts écrits pour un tournage immédiat

Nabil, en voiture : « je vais au moins tourner les corps (…) 5-6 thèmes (…) au moins 50 secondes,
une minute (…) un peu comme "T'inquiète" (…) t'es mon manager, mon directeur artistique. »

**Fait**

- **Calibré avant d'écrire** : « T'inquiète » livré = 142 mots pour 36,7 s, soit **3,9 mots/s**.
  Donc 55-60 s de montage serré = 215-235 mots utiles. Cible d'écriture fixée à 220-260 mots pour
  laisser de la marge à la coupe (le rush de « T'inquiète » faisait 1 min 44 pour 36,7 s gardées).
- **Six scripts complets** dans [`phase-1-solo/scripts/04-serie-2-six-scripts.md`](phase-1-solo/scripts/04-serie-2-six-scripts.md),
  chacun avec hook au mot près, escalade, chute isolée, indications de tournage, titre TikTok
  (verdict, jamais le sujet) et risque au filtre. Comptés : **220 à 242 mots → 57 à 63 s**.
- Ordre de tournage donné : **la Clio d'abord**, Nabil est dedans, la voiture est l'accessoire.
- Après le premier comptage, trois scripts étaient courts (200, 200 et **178 mots → 46 s**, sous le
  minimum demandé). Un vrai palier ajouté à chacun (le sondage de dates, la paille du Coca, le
  « en ligne il y a 4 min » + l'avis de recherche dans le groupe), pas du remplissage. Recomptés.
- Filtre des interdits passé mécaniquement (`grep` sur bestie / batterie sociale / coiffeur / en
  retard / contrôle de maths) : rien.

**Décidé**

- Les six vivent dans `phase-1-solo/scripts/04-serie-2-six-scripts.md` et sont pointés depuis le backlog. Ils montent dans
  `phase-1-solo/scripts/01-scripts-valides.md` **un par un, une fois tournés et validés** — pas avant.
- Deux scripts (« Je gère », « Arrêté de fumer ») reposent sur le contraste discours/réalité, comme
  le Business Bro. Sujets sans rapport, mécanique partagée : assumé, c'est la mécanique qui marche le
  mieux chez lui.

**Appris**

- **Whisper compte 184 « mots » là où le script en compte 142** (il sépare les apostrophes). Pour
  calibrer une longueur de script, compter les mots *écrits*, pas les tokens Whisper. Le débit de
  référence est donc 3,9 mots/s, pas 5,05.
- Un thème qui se tourne **là où Nabil est** (la voiture) vaut plus qu'un meilleur thème qu'il devra
  tourner plus tard. L'ordre de tournage fait partie du script.

---

## 16/09/2026 — Six concepts pour le duo avec Sady

Nabil : « cette fois je suis pas tout seul mais avec Sady… trouve un concept drôle, divertissant, qui
pourrait marcher, soit inventer, soit prendre un truc qui marche et l'améliorer. »

**Fait** : [`phase-1-solo/scripts/08-concepts-duo.md`](phase-1-solo/scripts/08-concepts-duo.md), six concepts, chacun
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

---

## 16/09/2026 (suite) — « ChatGPT est-il meilleur que toi ? » — comparaison chiffrée, et portage préparé

Nabil : « est-ce que tu penses que ChatGPT est beaucoup plus performant que toi pour faire des
montages vidéo ? (…) prends un maximum de data, renseigne-toi. »

**La réponse, et elle n'est pas flatteuse pour moi non plus : ce n'est pas le modèle qui monte.**
C'est ffmpeg, numpy et un conteneur avec du réseau. La comparaison ne porte donc pas sur
l'intelligence mais sur l'environnement d'exécution.

| | Ici | Codex Cloud | ChatGPT (chat) |
| :--- | :--- | :--- | :--- |
| Fichier déposé dans le chat | 30 Mio | **impossible** | 512 Mo, mais vidéo/audio non supportés |
| ffmpeg | installé | oui, via le setup | pas garanti |
| Internet pendant le travail | oui, 15 Mo/s | **OFF par défaut**, activable | **aucun** |
| Persistance | git | git | session éphémère |

Sources : Help Center OpenAI (vidéo/audio non supportés à l'upload), `openai-node#1778` (pas de
vidéo dans l'API), doc Codex Cloud (« Setup scripts run with internet access » / « Agent internet
access is off by default »), doc Skills OpenAI.

**Trois trouvailles qui comptent**

1. **Le sandbox de ChatGPT n'a pas de réseau.** « Essentially an Ubuntu sandbox with no root or
   internet access. » Ça tue `recuperer.sh`, `icloud.py`, la banque de sons et l'installation de
   Whisper d'un seul coup. ChatGPT en chat est hors course pour *exécuter* un montage.
2. **Le skill est portable, et c'est une bonne nouvelle.** ChatGPT et Codex utilisent un `SKILL.md`
   avec frontmatter `name`/`description` — « built on the open agent skills standard ». C'est
   exactement le fichier écrit ce matin. Aucun enfermement.
3. **Chez Codex, aucun fichier n'entre par le chat.** « Cloud tasks (…) do not automatically receive
   additional inputs beyond what is explicitly provided in the repository. » Donc le raccourci iOS
   « Audio pour Claude » n'y servirait plus à rien : même 872 Ko d'audio devraient passer par un
   lien. **Le portage n'enlève aucun problème d'envoi de fichier, il en ajoute un.**

**Fait**

- `AGENTS.md` → lien symbolique vers `CLAUDE.md` (Codex lit `AGENTS.md`). Un seul fichier, donc
  aucune dérive possible.
- `.agents/skills/montage/` → lien symbolique vers `.claude/skills/montage/`. C'est bien
  **`.agents/skills`** que Codex balaie, pas `.codex/skills` (vieux tutos périmés). Les deux liens
  se résolvent, vérifié.
- [`outils/setup-codex.sh`](outils/setup-codex.sh) écrit : ffmpeg + deps + **pré-téléchargement du
  modèle Whisper**, parce que chez Codex le réseau n'existe que pendant le setup.
- [`outils/README-portage-codex.md`](outils/README-portage-codex.md) : les deux réglages à faire,
  la comparaison chiffrée, et la limite qu'aucun réglage ne résout.

**Non vérifié**

- **Le portage n'a jamais tourné sur un vrai Codex.** Emplacements et comportements viennent de la
  doc OpenAI, pas d'un essai. Seuls les liens symboliques sont mesurés. Quatre points à vérifier au
  premier lancement, listés en fin de `README-portage-codex.md`.
- **Le test des 512 Mo côté ChatGPT est à faire par Nabil** : uploader un mp4 de 100 Mo et demander
  un `ffprobe`. C'est le seul chiffre manquant de la comparaison, et il est falsifiable.

**Ce qui n'a pas changé**

Six montages prêts, zéro publié. Changer d'outil n'en sortira pas un de plus.

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

---

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

---

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

---

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

---

## 15/09/2026 — Quatre scripts pour un tournage en voiture, et la question Apify

Nabil, sur le parking, avec le temps de tourner 3-4 vidéos. Il demande des thèmes, des scripts, et
si Apify (scraper TikTok) me servirait.

**Fait**

- Quatre scripts complets, au mot près, dans
  [`phase-1-solo/scripts/03-scripts-proposes-15-09.md`](phase-1-solo/scripts/03-scripts-proposes-15-09.md) :
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

---

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

---

## 14/09/2026 (suite) — Tier list sport, montage perso

Nabil : « c'est pas pour TikTok, c'est pour moi, donc garde [les deux passages]. Fluidifie un peu
le truc. » Fait : blancs ≥ 0,45 s ramenés à 0,22 s, contenu intact, 1 min 50 → 1 min 33 (−15 %).

La décision d'écarter cette vidéo tient toujours : elle portait sur la **publication**. Un montage
privé d'un rush qu'il a tourné lui-même est son affaire. Le fichier n'est pas dans `livraisons/`,
qui reste le dossier des vidéos destinées à sortir.

Les cinq blancs les plus longs sont notés dans le relevé (88,7 s / 19,5 s / 7,7 s / 14,0 s /
4,3 s) : ce sont ceux qui risquent de porter une information, comme celui de Musiala.

---

## 14/09/2026 (suite) — Un silence qui portait une information

Nabil, sur la tier list foot : « au départ, après Musiala, je veux que tu laisses, car avec le cut
on dirait qu'on a fait exprès de dire "qui est ce mec" en même temps alors que non, même pas. »

Le blanc de 3,72 s entre « on va en mettre 5 » et le double « mais qui est ce mec ? » avait été
ramené à 0,22 s par la compression automatique. Résultat : les deux répliques se collaient et
laissaient croire à un effet préparé. **Remis entier.** 1 min 43 → 1 min 47.

Règle ajoutée à `CLAUDE.md` §2 bis et à la D.A. du format : un silence n'est pas toujours un temps
mort. Entre deux locuteurs surtout, la simultanéité se lit comme une intention.

---

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

---

## 14/09/2026 — Les tier lists avec Sady, et la D.A. du format

**Fait**

- Trois tier lists reçues (sports, fruits, footballeurs), toutes en 720p, deux à deux personnes.
- **Benchmark du compte de Sady** (@rodman97.3) sur 7 vidéos : `phase-1-solo/strategie/04-benchmark-rodman.md`.
- **D.A. du format tier list tranchée** : `phase-1-solo/strategie/03-format-tier-list.md`.
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

---

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

---

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

---

## 13/09/2026 (soir) — Les deux rushs du 30/08 enfin analysés

**Fait**

- Nabil demande pourquoi les deux autres vidéos du WeTransfer n'ont jamais été touchées. Réponse :
  elles ne l'ont pas été, il n'y a pas d'excuse. Elles étaient encore sur le disque : analysées.
- **Découverte : ce ne sont pas deux prises de la même vanne.** Le nom `prise-A` / `prise-B` avait
  été inventé par moi, et il a induit tout le monde en erreur pendant deux jours.
  - Rush A (18 h 55, 59 s) = la **Vidéo 3, Business Bro**, improvisée.
  - Rush B (19 h 01, 61 s) = la **Vidéo 4, l'otage du téléphone** — que le dépôt déclarait
    « script à écrire ». Elle est tournée.
- Analyse complète des deux (`ecoute-video.py`), versée dans `phase-1-solo/scripts/01-scripts-valides.md` avant que le
  conteneur ne l'efface : transcription, zones molles, scores de chute, son.

**Appris**

- **Le meilleur moment tourné à ce jour** est dans le rush A, à 16,0–22,8 s : l'imitation du faux
  investisseur. +22,3 dB sur la phrase d'avant, score de chute 100/100.
- Les deux rushs saturent en crête (−0,3 dBTP), comme celui du 12/09. C'est systématique : le gain
  automatique du téléphone. À traiter à la prise, pas au montage.
- **Ne jamais nommer un fichier d'après une hypothèse.** Nommer d'après ce qu'il contient, ou par
  sa date. Un nom inventé devient un fait dans la mémoire du projet.

---

## 13/09/2026 — Montage, son, retouche, et une leçon sur la qualité

**Fait**

- Chaîne son refaite : le sample s'efface sous la voix (ducking calculé hors ligne), la voix
  n'est plus touchée. Trois défauts ffmpeg trouvés et corrigés — ils baissaient toute la voix de 2 dB.
- Sample Doumbé découpé au mot : « JORDAN » seul, 0,94 s, la foule derrière, coupé avant « t'es mort ».
- `outils/retoucher.py` écrit : efface un défaut de peau sur toute la vidéo en le suivant sur le
  visage (MediaPipe). Bouton du nez retiré sur 1266 des 1288 images.
- `livraisons/` créé : les montages finis vivent dans le dépôt, en haute qualité.
- `phase-1-solo/strategie/02-da-tiktok.md` écrit : proposition de DA TikTok + passation.

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

---

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
