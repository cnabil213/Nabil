# ÉTAT — où on en est

> Ce fichier est lu **à chaque démarrage de session** (hook `.claude/hooks/session-start.sh`).
> Il est court exprès. Le détail est dans les fichiers qu'il pointe.
> **Règle : il se met à jour à la fin de chaque session, avec une entrée dans [`JOURNAL.md`](JOURNAL.md).**

**Dernière mise à jour : 13/09/2026**

---

## En une phrase

Phase 1 (short-form solo) : 3 scripts validés, 1 vidéo montée et livrée, **rien de publié**,
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

## En cours / pas fait

- **Vidéo 4** (l'otage du téléphone) : idée validée, script pas écrit.
- **Publication** : aucun compte ouvert, aucun nom arrêté, rien en ligne.
- **Sous-titres** : proposés dans la DA, jamais produits. Aucun outil ne les génère encore.
- **Sons du soundboard 3kh0** : 6 mèmes proposés à Nabil, jamais validés ni importés.
- **Prises du 30/08** : deux prises de la même vanne, jamais comparées. Les fichiers sont perdus.

## Les 3 prochaines actions

1. Poser à Nabil les 5 questions de la DA (`04-da-tiktok.md`, section 5).
2. Écrire le script de la Vidéo 4 une fois la DA tranchée.
3. Décider quelle vidéo sort en premier, et la publier.

## À savoir avant de commencer

- **Le conteneur est effacé entre deux sessions.** Rushs, montages et analyses ne survivent pas :
  seul ce qui est commité reste. Pour retravailler une vidéo, demander à Nabil de **renvoyer le fichier**.
- **Les outils ne sont pas installés d'office.** Voir [`outils/README.md`](outils/README.md) §Installation.
  Le montage et la retouche ont besoin de `numpy soundfile opencv-python-headless mediapipe` ;
  l'analyse de la voix a besoin en plus de `faster-whisper praat-parselmouth librosa` et d'un venv torch.
- **Rien ne se juge à l'œil ni à l'oreille sans un chiffre derrière.** C'est LA règle du projet
  (raisons et contre-exemples : [`CLAUDE.md`](CLAUDE.md), section « La règle qui prime »).
