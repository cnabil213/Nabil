# MÉMOIRE CENTRALISÉ — STRATÉGIE DE CRÉATION NABIL (2025)

Base de connaissance de la stratégie de contenu de **Nabil**. Ce dépôt sert de
mémoire unique et versionnée : il remplace les fichiers mémoires éparpillés entre
les différentes IA (ChatGPT, Gemini, Claude).

## 🎯 Vision globale

La stratégie se déploie en **deux étapes**, dans cet ordre. La Phase 2 ne démarre
pas avant que la Phase 1 ait produit de la notoriété.

| | Phase | Statut | Objectif |
| :-- | :--- | :--- | :--- |
| **1** | Contenu **short-form solo** (TikTok / Reels / Shorts) | 🟢 **En cours** | Percer, construire une communauté forte, acquérir de la notoriété |
| **2** | **GENZED** — émission studio multi-caméras | 🟡 Préparé, en attente | Capitaliser sur la notoriété : clashs amicaux, tension, chaos organisé |

## 📂 Structure du dépôt

### Phase 1 — Création solo (priorité actuelle)

| Fichier | Contenu |
| :--- | :--- |
| [`phase-1-solo/01-persona-et-regles.md`](phase-1-solo/01-persona-et-regles.md) | Le persona, le ton, les interdits absolus, l'anatomie d'un script |
| [`phase-1-solo/02-scripts-valides.md`](phase-1-solo/02-scripts-valides.md) | Les scripts finaux tournables + l'historique de leurs itérations |
| [`phase-1-solo/03-backlog-idees.md`](phase-1-solo/03-backlog-idees.md) | Pipeline des idées : en cours, à creuser, brûlées |

### Phase 2 — Émission GENZED

| Fichier | Contenu |
| :--- | :--- |
| [`phase-2-genzed/01-bible-production.md`](phase-2-genzed/01-bible-production.md) | Concept GENZED, FITNA WAR, les formats courts, la grille des programmes |
| [`phase-2-genzed/02-direction-artistique.md`](phase-2-genzed/02-direction-artistique.md) | DA visuelle (couleurs, typo, plateau) + branding sonore |
| [`phase-2-genzed/03-technique-et-budget.md`](phase-2-genzed/03-technique-et-budget.md) | Setup multi-cam, workflow de tournage, studios en Belgique, budgets |
| [`phase-2-genzed/04-historique-concepts.md`](phase-2-genzed/04-historique-concepts.md) | Tous les concepts proposés, validés ou rejetés — **et pourquoi** |

### Outils

| Fichier | Contenu |
| :--- | :--- |
| [`outils/ecoute-video.py`](outils/ecoute-video.py) | **L'oreille** : transcription, captation, prosodie, verdicts par phrase, alertes horodatées, score de chute |
| [`outils/ecoute/comparer-prises.py`](outils/ecoute/comparer-prises.py) | Deux prises de la même vanne → laquelle garder, et pourquoi |
| [`outils/vision-video.py`](outils/vision-video.py) | **Les yeux** : planches contact horodatées, forme d'onde |
| [`outils/README.md`](outils/README.md) · [`outils/README-ecoute.md`](outils/README-ecoute.md) | Installation, usage, vocabulaire du rapport, limites |
| [`outils/RECHERCHE-ECOUTE.md`](outils/RECHERCHE-ECOUTE.md) | Pourquoi Claude n'entend pas, ce qui marche à la place, et les pistes closes |

### Contexte IA

[`CLAUDE.md`](CLAUDE.md) — les règles de travail chargées automatiquement par
Claude Code dans ce dépôt : ton, interdits, méthode de proposition d'idées.

## 🤖 Comment s'en servir avec une IA

**Avec Claude Code, dans ce dépôt :** rien à faire, `CLAUDE.md` est chargé tout seul.

**Avec une autre IA (ChatGPT, Gemini…) :** coller au minimum
`CLAUDE.md` + `phase-1-solo/01-persona-et-regles.md` + `phase-1-solo/02-scripts-valides.md`
avant de demander des idées. Sans ces trois fichiers, l'IA repart sur de l'humour
générique et des thèmes déjà vus.

**Rôle attendu de l'IA** (arbitré par Nabil) : outil personnel de génération
d'idées **originales**. Ton énergique, réponses concises, zéro flatterie, on va
droit au script.

## ✍️ Convention de mise à jour

- Un script passe de `03-backlog-idees.md` → `02-scripts-valides.md` uniquement
  quand il est **tournable en l'état**.
- Une idée rejetée n'est **jamais supprimée** : elle descend dans les sections
  « brûlées » / « historique » avec la raison du refus. C'est ce qui empêche les
  IA de reproposer la même chose trois mois plus tard.
- Un commit = une décision éditoriale.
