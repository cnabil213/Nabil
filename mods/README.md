# Mods pour C'Nabil-Famous (dépôt `cnabil213/Nabil`)

Six mods Claude Code construits et testés le 10/10/2026 (le HUD ajouté le même jour, à la demande de Nabil), depuis une session cloud (Claude Code 2.1.296). Source et historique : dépôt `PROFESSEUR-`, `projets/mods-cnabil-famous`.
Chacun transforme une règle écrite du `CLAUDE.md` ou du plan 100 K du dépôt Nabil en quelque chose qui agit tout seul.
Ils ne s'affichent que sur un ordinateur : terminal (Claude Code 2.1.287 ou plus) ou onglet Code de l'app Desktop (2.1.286 ou plus).
Ils ne tournent **pas** dans les fils du projet sur téléphone ni dans une session cloud.

| Mod | Règle d'origine | Ce qu'il fait | Ce qu'il touche (`claude plugin validate`) | Tests |
| --- | --- | --- | --- | --- |
| `cnabil-hud` | Demande de Nabil (10/10) : « un HUD, nombre d'abonnés, likes, la fenêtre de contexte » | Au-dessus de la saisie : « ◆ C'NABIL  TikTok 12 733 ▲33 · palier 20 K le 15/11 : +197/j │ Contexte ▰▰▰▱▱▱▱▱▱▱ 31 % │ Forfait 5 h 23 % · 7 j 41 % ». `/hud` ouvre le panneau : abonnés, vues et likes, dernière vidéo (vues, likes, % vue en entier), prochaine publication programmée, barre vers 100 K, fenêtre de contexte, forfait et coût du fil. Metricool relu au plus toutes les 15 minutes. | `$.mcp.call` (Metricool, lecture seule : getBrandSettings, getAnalyticsDataByMetrics, getScheduledPosts), `$.session.usage` | 5 réussis |
| `feu-vert-famous` | « Avant d'agir (classer, renommer, publier), on confirme » (CLAUDE.md, 10/10) | Retient toute publication Metricool, toute modification du Drive (renommer, déplacer, copier, créer, jeter) et toute dépense de crédits (Apify, ElevenLabs), et demande « Tu donnes ton feu vert ? ». Sans réponse, il bloque. | `$.ui.ask`, `$.ui.log` | 6 réussis |
| `garde-regles` | CLAUDE.md §3 bis, interdits absolus, scripts validés | Refuse un `grep`, un `tail -1` ou un `2>/dev/null` sur un outil de montage ; refuse le commit d'un mp4 de `livraisons/` pas passé par `ffprobe` depuis sa dernière écriture ; refuse « bestie » dans un script ; demande à Nabil avant de toucher à `01-scripts-valides.md`. | `$.process.run` (git diff, git status, en lecture), `$.ui.ask` | 9 réussis |
| `deux-gestes` | « ETAT.md + JOURNAL.md, jamais l'un sans l'autre » | Bandeau « Avant de finir : ETAT.md ✗ · JOURNAL.md ✗ » tant que du travail est fait sans les deux gestes ; refuse un push qui contient l'un sans l'autre ; rappel à Claude si le push ne contient aucun des deux ; `/fin` fait le bilan. | `$.process.run` (git, en lecture) | 6 réussis |
| `objectif-100k` | Plan 100 K (06-plan-croissance-100k.md) | `/abonnes 13450` note le relevé dans `phase-1-solo/strategie/08-suivi-abonnes.md` ; bandeau « 100 K : 13 450 abonnés · palier 20 000 le 15/11 : +193/jour à tenir · ton rythme : +375/jour » ; rappel du bilan le dimanche dès 20 h (heure belge). | lit et écrit ce seul fichier, lit l'heure | 7 réussis |
| `refus` | « Une idée rejetée se documente avec sa raison de refus » | `/refus idée — raison` ajoute une ligne datée au tableau « Brûlées » de `phase-1-solo/scripts/02-backlog-idees.md`, et dit si l'idée y est déjà. | lit et écrit ce seul fichier, lit l'heure | 4 réussis |

Aucun de ces mods n'appelle de modèle ni ne lit de clé secrète. Seul `cnabil-hud` sort de l'ordinateur : il lit Metricool par le connecteur déjà branché, en lecture seule. Les seuls programmes lancés sont `git diff`, `git status` et `git rev-list`, qui ne modifient rien.

Essai réel le 10/10 dans une copie du dépôt Nabil : `/refus`, `/abonnes` et `/fin` ont écrit ou répondu comme prévu, et `garde-regles` a refusé pour de vrai `ffprobe … | grep duration` en citant la règle.

## À réutiliser depuis `mods-cnabil-rich`

- `feu-vert` : e-mails, agenda partagé avec Sady, partage d'un fichier Drive. `feu-vert-famous` ne repose pas ces questions-là : installe les deux.
- `compteur-tokens` : le compteur de tokens du fil, alarme à 10 M.

## Installer : rien à faire

Les mods sont dans ce dépôt (`mods/`) et déclarés dans `.claude/settings.json` (`extraKnownMarketplaces` + `enabledPlugins`).
Sur un ordinateur, ouvre le dossier `Nabil` dans Claude Code (terminal ou onglet Code de l'app Desktop) et accepte la question « faire confiance à ce dossier ». Les six mods se chargent seuls, sans `/plugin install`.
Vérifié le 10/10/2026 sur une configuration vierge : après la confiance au dossier, `/refus` a répondu sans aucune installation.

Pour ajouter les deux mods de C'Nabil Rich (`feu-vert` pour les e-mails et l'agenda, `compteur-tokens`), ils sont dans le dépôt `PROFESSEUR-`, dossier `projets/mods-cnabil-rich`.

## Vérifier soi-même

```bash
claude plugin validate ./garde-regles   # liste ce que le mod touche
cd garde-regles && claude plugin test   # rejoue ses tests
```

## Modifier

- Ajouter une action à retenir : la liste `FAMILLES` en haut de `feu-vert-famous/hooks/register.ts`.
- Ajouter un mot interdit : la liste `INTERDITS` en haut de `garde-regles/hooks/register.ts`.
- Changer un palier du plan 100 K : `PALIERS` en haut de `objectif-100k/hooks/register.tsx`.
- Après une modification, monte la `version` dans `plugin.json`, sinon Claude Code garde l'ancienne copie.

## Le HUD et Metricool

Le HUD lit Metricool avec le connecteur Metricool de Claude Code (`/mcp` doit le montrer connecté). Il essaie les noms « claude.ai Metricool Social Media Management », puis « Metricool Social Media Management », « claude.ai Metricool » et « Metricool » : si ton connecteur porte un autre nom, ajoute-le à `SERVEURS` en haut de `cnabil-hud/hooks/register.tsx`.
Le compte TikTok a été relié à Metricool le 10/10/2026 à 16 h 57 ; Metricool donnait alors 12 733 abonnés au 09/10.

## La page HUD pour le téléphone

La page « C'Nabil HUD » (https://claude.ai/artifact/TEnGPtFY8Nptaqhbfsjchj), épinglée dans la barre latérale de Claude, lit Metricool en direct et marche sur téléphone. Elle ne montre pas la fenêtre de contexte, qui reste dans le HUD du terminal. Sa source est dans le dépôt `PROFESSEUR-`, `projets/mods-cnabil-famous/page-hud/`.
