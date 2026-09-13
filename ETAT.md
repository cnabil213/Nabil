# ÉTAT — où on en est

> Ce fichier est lu **à chaque démarrage de session** (hook `.claude/hooks/session-start.sh`).
> Il est court exprès. Le détail est dans les fichiers qu'il pointe.
> **Règle : il se met à jour à la fin de chaque session, avec une entrée dans [`JOURNAL.md`](JOURNAL.md).**

**Dernière mise à jour : 13/09/2026 (soir)**

---

## En une phrase

Phase 1 (short-form solo) : **3 vidéos tournées**, 1 montée et livrée, **rien de publié**,
et la direction artistique TikTok attend 5 décisions de Nabil.

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
| **Rush A du 30/08** | Vidéo 3 (Business Bro), 59 s, analysée. **Montable**, la fin est à couper |
| **Rush B du 30/08** | Vidéo 4 (l'otage du téléphone), 61 s, analysée. Chute et hook manquants |

## En cours / pas fait

- **Vidéo 3 et Vidéo 4** : tournées le 30/08, jamais montées. **Les fichiers sont perdus**
  (conteneur effacé) : demander à Nabil de renvoyer `prise-A-30aout.mp4` et `prise-B-30aout.mp4`.
  Tout ce qu'on sait d'elles est dans [`02-scripts-valides.md`](phase-1-solo/02-scripts-valides.md).
- **Publication** : aucun compte ouvert, aucun nom arrêté, rien en ligne.
- **Sous-titres** : proposés dans la DA, jamais produits. Aucun outil ne les génère encore.
- **Sons du soundboard 3kh0** : 6 mèmes proposés à Nabil, jamais validés ni importés.
- **Vidéo 4** : la chute n'existe pas (six répétitions de « j'ai déjà vu la vidéo » à la fin) et le
  hook est une mise en contexte, donc un interdit. À réécrire, puis à retourner ou à remonter.

## Les 3 prochaines actions

1. **Faire renvoyer les deux rushs du 30/08** — il y a une vidéo montable dedans (Business Bro),
   et c'est peut-être elle qui doit sortir en premier, pas celle du 12/09.
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
