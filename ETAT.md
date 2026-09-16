# ÉTAT — où on en est

> Ce fichier est lu **à chaque démarrage de session** (hook `.claude/hooks/session-start.sh`).
> Il est court exprès. Le détail est dans les fichiers qu'il pointe.
> **Règle : il se met à jour à la fin de chaque session, avec une entrée dans [`JOURNAL.md`](JOURNAL.md).**

**Dernière mise à jour : 16/09/2026**

---

## En une phrase

Phase 1 : **6 vidéos montées et livrées**, **rien de publié**. Le dépôt est désormais portable (Claude Code **et** Codex, même `SKILL.md`). Le montage est maintenant une
**procédure qui se lance** ([skill `montage`](.claude/skills/montage/SKILL.md)) et non plus de la
prose à relire — mais le blocage n'a pas bougé d'un centimètre : aucun compte n'est ouvert.

## Le chantier en cours

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
| **Envoi des rushs** | ✅ [`outils/README-envoyer-un-rush.md`](outils/README-envoyer-un-rush.md) — raccourci iOS « Audio pour Claude » (1 tap) + iCloud Drive pour le fichier lourd |

## En cours / pas fait

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
3. Au prochain rush : **lancer le skill `montage`** et voir où la procédure frotte. Elle n'a encore
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
