# MÉMOIRE CENTRALE — STRATÉGIE DE CRÉATION NABIL

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

```
ETAT.md            ← OÙ ON EN EST. Lu automatiquement au démarrage de chaque session
JOURNAL.md         ← une entrée par session : fait / décidé / appris
CLAUDE.md          ← les règles de travail, chargées automatiquement par Claude Code
README.md          ← ce fichier : l'index

phase-1-solo/      01-persona-et-regles · 02-scripts-valides · 03-backlog-idees
                   04-da-tiktok  ← la direction artistique + la passation
phase-2-genzed/    01-bible-production · 02-direction-artistique
                   03-technique-et-budget · 04-historique-concepts

outils/            ecoute-video.py   l'oreille : transcription, prosodie, alertes horodatées
                   monter.py         couper un rush, normaliser le son, en un seul réencodage
                   sonoriser.py      poser un sample qui s'efface sous la voix
                   retoucher.py      effacer un défaut de peau, suivi sur le visage
                   vision-video.py   les yeux : planches contact horodatées
                   banque-son.py     alimenter la banque de sons
                   README.md         installation, usage, et les pièges déjà mesurés
banque-son/        les samples de Nabil, dans le dépôt (clips courts uniquement)
livraisons/        LES MONTAGES FINIS, en haute qualité — le chat plafonne à 30 Mio, pas GitHub
.claude/hooks/     session-start.sh : injecte ETAT.md au démarrage de chaque session
```

## 🧠 La mémoire, d'une session à l'autre

Le conteneur de travail est **effacé entre deux sessions**. Ce dépôt est donc la seule chose qui
survit, et il est fait pour ça.

**Au démarrage**, le hook `.claude/hooks/session-start.sh` affiche [`ETAT.md`](ETAT.md) et la
dernière entrée du [`JOURNAL.md`](JOURNAL.md) : la session commence chargée, sans que Nabil ait
à réexpliquer quoi que ce soit.

**À la fin**, deux gestes obligatoires : réécrire `ETAT.md` (il se remplace) et ajouter une entrée
en haut de `JOURNAL.md` (il s'empile). C'est ce couple qui fait la mémoire — l'un dit *où on en
est*, l'autre *comment on y est arrivé*.

**Ce qui ne survit pas** : les rushs, les montages intermédiaires, les analyses. Pour reprendre le
travail sur une vidéo, Nabil renvoie le fichier. Seul le montage fini, dans `livraisons/`, est
permanent.

## 🤖 Comment s'en servir avec une IA

**Avec Claude Code, dans ce dépôt :** rien à faire. `CLAUDE.md` et `ETAT.md` se chargent seuls.

**Avec une autre IA (ChatGPT, Gemini…) :** coller `CLAUDE.md` + `ETAT.md` +
`phase-1-solo/01-persona-et-regles.md` + `phase-1-solo/02-scripts-valides.md` avant de demander
des idées. Sans ça, l'IA repart sur de l'humour générique et des thèmes déjà vus.

**Rôle attendu de l'IA** (arbitré par Nabil) : outil personnel de génération d'idées
**originales**, et monteur. Ton énergique, réponses concises, zéro flatterie, on va droit au script.

## ✍️ Convention de mise à jour

- Un script passe de `03-backlog-idees.md` → `02-scripts-valides.md` uniquement
  quand il est **tournable en l'état**.
- Une idée rejetée n'est **jamais supprimée** : elle descend dans les sections
  « brûlées » / « historique » avec la raison du refus. C'est ce qui empêche les
  IA de reproposer la même chose trois mois plus tard.
- Un commit = une décision éditoriale, avec un message qui dit **pourquoi**, pas seulement quoi :
  c'est ce message que la session suivante lira.
- Fin de session = `ETAT.md` réécrit + une entrée dans `JOURNAL.md`. Sans ça, la mémoire s'arrête.
