# ÉTAT — où on en est

> Ce fichier est lu **à chaque démarrage de session** (hook `.claude/hooks/session-start.sh`).
> Il est court exprès. Le détail est dans les fichiers qu'il pointe.
> **Règle : il se met à jour à la fin de chaque session, avec une entrée dans [`JOURNAL.md`](JOURNAL.md).**

**Dernière mise à jour : 14/09/2026**

---

## En une phrase

Phase 1 : **5 vidéos montées et livrées** (3 solo + 2 tier lists avec Sady), **rien de publié**.
Le format tier list a sa D.A. tranchée ; la D.A. solo attend encore 5 décisions de Nabil.

## Le chantier en cours

**La DA TikTok.** Proposition complète écrite dans
[`phase-1-solo/04-da-tiktok.md`](phase-1-solo/04-da-tiktok.md). Les 5 questions de sa section 5
sont à poser à Nabil dès le début de la session ; tant qu'elles sont ouvertes, la DA est bloquée.

## Fait

| | |
| :--- | :--- |
| Scripts validés | Vidéo 1 (école), Vidéo 2 (MMA de salon), Vidéo 3 (Business Bro) |
| Vidéo montée | MMA de salon, tournée le 12/09 en voiture — 6 coupes, 43 s |
| Son | normalisé à −14 LUFS, sample « JORDAN » de Doumbé à 28,40 s |
| Image | bouton du nez retiré sur 1266 des 1288 images |
| Livré | [`livraisons/12sept-casser-des-nuques-HQ.mp4`](livraisons/) — 53,7 Mio, 10,3 Mb/s |
| **Vidéo 3 — Business Bro** | ✅ **Montée et livrée** : [`livraisons/30aout-business-bro-HQ.mp4`](livraisons/) — 36,5 s |
| **Vidéo 4 — L'otage du téléphone** | ✅ **Montée et livrée** : [`livraisons/30aout-otage-du-telephone-HQ.mp4`](livraisons/) — 41,7 s |
| **Tier list fruits** (avec Sady) | ✅ Montée et livrée — 1 min 42 |
| **Tier list footballeurs** (avec Sady) | ✅ Montée et livrée — 1 min 43 |
| **Benchmark du compte de Sady** | ✅ 7 vidéos relevées : [`phase-1-solo/05-benchmark-rodman.md`](phase-1-solo/05-benchmark-rodman.md) |
| **D.A. du format tier list** | ✅ Tranchée : [`phase-1-solo/06-format-tier-list.md`](phase-1-solo/06-format-tier-list.md) |

## En cours / pas fait

- **Le montage de l'otage du téléphone garde un point faible assumé** : la section « on connaît tous
  ces humains-là → une fois, deux fois, trois fois » retombe de 8 dB et ralentit à 56 % du débit.
  C'est un maillon du sens, donc elle reste. À retourner avec de l'énergie si Nabil veut la hisser.
- **Publication** : aucun compte ouvert, aucun nom arrêté, rien en ligne.
- **Sous-titres** : proposés dans la D.A. solo, jamais produits. Écartés sur le format tier list
  (le classement incrusté occupe déjà le tiers gauche). À trancher : une identité visuelle ou deux.
- **Tier list sport du 13/09 : écartée de la publication**, deux passages non coupables proprement.
  À retourner. Raison dans [`06-format-tier-list.md`](phase-1-solo/06-format-tier-list.md) §5.
  Un montage **perso** (blancs resserrés, 1 min 33) a été fait à la demande de Nabil ; il n'est
  volontairement pas dans `livraisons/`, qui est le dossier des vidéos destinées à sortir.
- **Sons du soundboard 3kh0** : 6 mèmes proposés à Nabil, jamais validés ni importés.
- **Les trois montages sont prêts, aucun n'est publié.** C'est le seul vrai blocage de la Phase 1.

## Les 3 prochaines actions

1. **Publier.** Cinq montages prêts dans [`livraisons/`](livraisons/). Rien n'est en ligne, aucun
   compte n'est ouvert : c'est le seul blocage de la Phase 1.
2. Poser à Nabil les 5 questions de la DA (`04-da-tiktok.md`, section 5).
3. Écrire la chute de la Vidéo 4, à partir de ce qu'il a trouvé en improvisant.

## À savoir avant de commencer

- **Le conteneur est effacé entre deux sessions.** Rushs, montages et analyses ne survivent pas :
  seul ce qui est commité reste. Pour retravailler une vidéo, demander à Nabil de **renvoyer le fichier**.
- **Les outils ne sont pas installés d'office.** Voir [`outils/README.md`](outils/README.md) §Installation.
  Le montage et la retouche ont besoin de `numpy soundfile opencv-python-headless mediapipe` ;
  l'analyse de la voix a besoin en plus de `faster-whisper praat-parselmouth librosa` et d'un venv torch.
- **Rien ne se juge à l'œil ni à l'oreille sans un chiffre derrière.** C'est LA règle du projet
  (raisons et contre-exemples : [`CLAUDE.md`](CLAUDE.md), section « La règle qui prime »).
