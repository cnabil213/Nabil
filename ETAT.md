# ÉTAT — où on en est

> Ce fichier est lu **à chaque démarrage de session** (hook `.claude/hooks/session-start.sh`).
> Il est court exprès. Le détail est dans les fichiers qu'il pointe.
> **Règle : il se met à jour à la fin de chaque session, avec une entrée dans [`JOURNAL.md`](JOURNAL.md).**

**Dernière mise à jour : 17/09/2026**

---

## En une phrase

Phase 1 : **6 vidéos montées et livrées**, **rien de publié**. Le dépôt est désormais portable (Claude Code **et** Codex, même `SKILL.md`). Le montage est maintenant une
**procédure qui se lance** ([skill `montage`](.claude/skills/montage/SKILL.md)) et non plus de la
prose à relire — mais le blocage n'a pas bougé d'un centimètre : aucun compte n'est ouvert.

## Le chantier en cours

**Nabil tourne.** La vanne sur la clope est **dans la boîte** (tournée au feeling, rushs pas encore envoyés).
**Série 3 écrite** : [`08-serie-3-adresse-directe.md`](phase-1-solo/08-serie-3-adresse-directe.md) — six sujets
en adresse directe, **55 à 58 s** chacun, zéro « on a tous ce pote ». C'est la correction du défaut que Nabil a
identifié sur la série 2.

**Série 2 : six scripts, dont 5 en attente d'arbitrage.** [`07-serie-2-six-scripts.md`](phase-1-solo/07-serie-2-six-scripts.md)
— calibrés à 3,9 mots/s, 57 à 63 s chacun. Au retour des rushs : transcrire tout, mesurer, choisir les
prises, liste de coupes à valider. C'est le premier vrai test du skill `montage` et d'`icloud.py`.

**Publier.** C'est le seul vrai blocage, et il l'est depuis six montages.
Juste derrière : **la DA solo**, bloquée sur 5 questions fermées
([`phase-1-solo/04-da-tiktok.md`](phase-1-solo/04-da-tiktok.md) §5) — à poser dès le début de
session. Tant qu'elles sont ouvertes, les sous-titres ne peuvent pas être produits.

## Fait

| | |
| :--- | :--- |
| Scripts validés | Vidéo 1 (école), Vidéo 2 (MMA de salon), Vidéo 3 (Business Bro) |
| **Vidéo 2 — MMA de salon** | ✅ [`livraisons/12sept-casser-des-nuques-HQ.mp4`](livraisons/) — 43 s, 6 coupes, « JORDAN » de Doumbé à 28,40 s, bouton retiré sur 1266/1288 images |
| **Vidéo 3 — Business Bro** | ✅ [`livraisons/30aout-business-bro-HQ.mp4`](livraisons/) — 36,5 s |
| **Vidéo 4 — L'otage du téléphone** | ✅ [`livraisons/30aout-otage-du-telephone-HQ.mp4`](livraisons/) — 41,7 s |
| **Vidéo 5 — « T'inquiète »** | ✅ [`livraisons/15sept-tinquiete-HQ.mp4`](livraisons/) — 36,7 s, 5 clips assemblés |
| **Tier list fruits** (avec Sady) | ✅ Montée et livrée — 1 min 42 |
| **Tier list footballeurs** (avec Sady) | ✅ Montée et livrée — 1 min 47 |
| Benchmark du compte de Sady | ✅ 7 vidéos relevées : [`phase-1-solo/05-benchmark-rodman.md`](phase-1-solo/05-benchmark-rodman.md) |
| D.A. du format tier list | ✅ Tranchée : [`phase-1-solo/06-format-tier-list.md`](phase-1-solo/06-format-tier-list.md) |
| **Skill `montage`** | ✅ [`.claude/skills/montage/`](.claude/skills/montage/SKILL.md) — 7 étapes, 2 points d'arrêt où Nabil tranche |
| **`outils/derusher.py`** | ✅ Propose les coupes mesurées. **Il n'encode rien, il ne décide rien.** |
| **Portage Codex (OpenAI)** | ✅ Préparé, **jamais testé** : [`outils/README-portage-codex.md`](outils/README-portage-codex.md) — `AGENTS.md` et `.agents/skills/` sont des liens symboliques, donc zéro dérive |
| **Série 2 — six scripts** | ✅ Écrits, calibrés, filtrés. **Le 5 (clope) réécrit sur l'idée de Nabil** — « vous allez bien ? », adresse directe à l'audience. Les 5 autres jugés « pas ouf » : formule « on a tous ce pote » ×6. **À trancher : tourner ou réécrire.** |
| **Série 3 — adresse directe** | ✅ Six scripts, **55-58 s**, **narration pure** : voiture · abonnements · tonton · vocaux · peur d'appeler · colis. Six mécaniques d'adresse différentes. **Pas encore tournés.** |
| **Envoi des rushs** | ✅ [`outils/README-envoyer-un-rush.md`](outils/README-envoyer-un-rush.md) — raccourci iOS « Audio pour Claude » (1 tap) + iCloud Drive pour le fichier lourd |

## En cours / pas fait

- 🎙️ **NABIL EST UN NARRATEUR, PAS UN ACTEUR.** Il raconte, il cite, il imite les VOIX. Il ne mime
  rien. Test : **si la vanne ne marche plus les yeux fermés, elle est fausse.** La D.A. affirmait
  l'inverse (« hook acting, mimique muette ») — c'était inventé : il parle dès 0,05-0,15 s sur ses
  4 vidéos. Corrigé le 17/09, détail dans `01-persona-et-regles.md` §3 bis.
- 🎬 **Nabil monte lui-même dans CapCut.** Réglages d'export : **Ultra HD par l'IA OFF, Smart HDR
  OFF, 30 im/s (pas 60)**. Mesuré : l'aller-retour 720p→1080p→720p sort à 61,8 dB, donc l'upscale
  n'ajoute **aucun** détail. Détail : [`outils/README-export-capcut.md`](outils/README-export-capcut.md).
- **Il a refilmé sur Snapchat** (« je suis plus beau sur snap »). Ses 4 anciennes vidéos : **720p,
  30/1**, et `monter.py` ne touche pas la cadence → ça vient bien de Snapchat. **Le nouveau rush n'a
  jamais été mesuré** : réclamer 2 s exportées depuis CapCut (~2 Mo).
  **3 pistes à tester, dans cet ordre :** (1) `Snapchat → Paramètres avancés → Qualité vidéo`, la
  mettre sur **Automatique** (si elle est sur « Faible », il perd de la définition sans le savoir) ;
  (2) `iOS → Réglages → Appareil photo → **Miroir photo de face**` — s'il est désactivé, la vidéo est
  enregistrée inversée, ce qui explique peut-être tout le « je suis moins bien » ; (3) une vanne à
  l'app Caméra 1080p + « Retouche » CapCut. Test proposé, pas encore fait : une vanne à l'app Caméra 1080p + « Retouche » CapCut.
  S'il se trouve aussi bien → on bascule. Sinon → on reste sur Snap et on n'en reparle plus.
- **PLAFOND : 60 s maximum par vidéo** (Nabil, 17/09). À 3,87 mots/s mesurés, ça fait **232 mots**.
  Compter avant de livrer un script, jamais estimer à l'œil.
- **Rushs de la vanne sur la clope : tournés le 17/09, pas encore envoyés.** Son script fait **68 s**,
  soit 8 de trop : l'ordre de coupe au montage est déjà écrit dans sa fiche (`07-serie-2` §5). À réclamer en début de
  session suivante (audio d'abord, raccourci iOS).
- **Publication : rien en ligne, aucun compte ouvert, aucun nom arrêté.** Six montages prêts.
  C'est LE blocage de la Phase 1, et il est le même depuis quatre sessions.
- **Sous-titres : jamais produits.** Bloqués par la question 2 de la DA solo (Monument Extended ou
  police native TikTok). Écartés sur le format tier list — le classement occupe déjà le tiers gauche.
- **Le montage de l'otage du téléphone garde un point faible assumé** : la section « on connaît tous
  ces humains-là → une fois, deux fois, trois fois » retombe de 8 dB et ralentit à 56 % du débit.
  C'est un maillon du sens, donc elle reste. À retourner si Nabil veut la hisser.
- **Tier list sport du 13/09 : écartée de la publication**, deux passages non coupables proprement.
  À retourner. Raison dans [`06-format-tier-list.md`](phase-1-solo/06-format-tier-list.md) §5.
  Un montage **perso** (1 min 33) existe, volontairement hors de `livraisons/`.
- **Sons du soundboard 3kh0** : 6 mèmes proposés, jamais validés ni importés.
- **Écrire la chute de la Vidéo 4**, à partir de ce qu'il a trouvé en improvisant.
- **Pas repris de la vidéo de Lucas Reverdy** : le montage sur fichier allégé (proxy) puis retour en
  pleine résolution. Utile sur du 20-30 min, inutile sur des sketchs de 40 s. À ressortir le jour où
  un format long arrive.
- **`icloud.py` n'a jamais tourné sur un vrai lien.** Les 3 chemins d'erreur sont testés, le chemin
  de succès non. **À vérifier au premier rush envoyé par iCloud** — et à corriger tout de suite si
  la forme de la réponse de l'API diffère.
- **Le portage Codex n'a jamais tourné sur un vrai Codex.** Emplacements et comportements viennent
  de la doc OpenAI. 4 points à vérifier au premier lancement (fin de `README-portage-codex.md`).
- **Test en attente côté Nabil** : uploader un mp4 de 100 Mo dans ChatGPT et demander un `ffprobe`.
  C'est le seul chiffre manquant de la comparaison ChatGPT / ici. S'il passe, ChatGPT gagne sur
  l'upload (512 Mo contre 30 Mio) et il faudra le noter ici.
- **Le connecteur Google Drive est branché mais pas autorisé** (`Insufficient scope`). Sans intérêt
  tant qu'on reste sur iCloud ; à réactiver seulement si Nabil change de stockage.

## Les 3 prochaines actions

1. **Publier.** Ouvrir le compte, arrêter un nom, sortir la première vidéo. Rien d'autre ne débloque
   la Phase 1.
2. Poser à Nabil les **5 questions** de la DA (`04-da-tiktok.md` §5) — dont celle qui débloque les
   sous-titres.
3. **Au retour des six rushs de la série 2** : lancer le skill `montage` et voir où la procédure frotte. Elle n'a encore
   jamais tourné sur un vrai rush reçu en direct — et c'est aussi le test d'`icloud.py`.

## À savoir avant de commencer

- **Un rush à monter ?** Le skill [`montage`](.claude/skills/montage/SKILL.md) contient la procédure
  complète. Ne pas la réimproviser.
- **Ne pas réclamer la vidéo tout de suite.** Les étapes 0 à 3 du montage tournent sur **l'audio
  seul** (mesuré : 60 Mo → 872 Ko, 0,04 s d'écart max sur les bornes de coupe). Le fichier lourd ne
  bouge qu'une fois, à la fin. Nabil envoie l'audio par un raccourci iOS, le reste par iCloud Drive.
- **Le conteneur est effacé entre deux sessions.** Rushs, montages et analyses ne survivent pas :
  seul ce qui est commité reste. Pour retravailler une vidéo, demander à Nabil de **renvoyer le fichier**.
- **ffmpeg s'installe en fond au démarrage** (~1 min). Avant de lancer un outil vidéo :
  `command -v ffmpeg`. Le reste des dépendances : [`outils/README.md`](outils/README.md) §Installation.
  L'analyse de la voix (`ecoute-video.py`) pèse ~1,6 Go et s'installe à la demande.
- **Rien ne se juge à l'œil ni à l'oreille sans un chiffre derrière.** C'est LA règle du projet
  (raisons et contre-exemples : [`CLAUDE.md`](CLAUDE.md), section « La règle qui prime »).
