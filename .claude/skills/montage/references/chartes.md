# Les deux formats — et leurs réglages de dérush

Deux formats, deux D.A., **deux jeux de règles de coupe**. Demander lequel à l'étape 2, en même
temps que la validation de la chaîne de sens.

---

## Format SOLO — face caméra, TikTok/Reels/Shorts

D.A. complète : [`phase-1-solo/04-da-tiktok.md`](../../../../phase-1-solo/04-da-tiktok.md).

```bash
python3 outils/derusher.py <rush> -o derush/ --silence-min 0.35 --marge 0.12
```

**⚠️ Cette D.A. est bloquée.** Cinq questions attendent une réponse de Nabil (section 5 du
fichier) : le nom du compte, les sous-titres, la voiture comme décor, l'ordre de sortie, les mèmes
3kh0. Tant qu'elles sont ouvertes, ne pas inventer de réponse — les reposer.

Ce qui est acquis :

- **Hook cash dans les 2 à 4 premières secondes.** Pas d'intro, pas de mise en contexte : la
  première phrase est déjà la vanne ou la promesse. Le dérush doit démarrer dessus — **mais sans
  jamais couper la prémisse qui la rend compréhensible** (c'est l'erreur du 13/09).
- **La première image gardée doit être nette** : c'est la vignette TikTok.
- Sous-titres : proposés, jamais produits. Ne pas en fabriquer sans que la question 2 soit tranchée.

---

## Format TIER LIST — Nabil × Sady, en voiture

D.A. tranchée, fondée sur un benchmark de 7 vidéos :
[`phase-1-solo/06-format-tier-list.md`](../../../../phase-1-solo/06-format-tier-list.md).

```bash
python3 outils/derusher.py <rush> -o derush/ --silence-min 0.45 --marge 0.11
```

**Ces deux valeurs reproduisent la règle §2.3 du format** — « tout silence ≥ 0,45 s est ramené à
0,22 s ». Le silence gardé dans le montage vaut `2 × marge`. Vérifié de bout en bout sur un fichier
de test à silences connus, mesuré sur la sortie encodée :

| silence dans la source | dans le montage produit | attendu |
| ---: | ---: | :--- |
| 0,20 s | 0,19 s — intact (sous le seuil) | intact ✅ |
| 0,50 s | 0,24 s | 0,22 s ✅ |
| 1,00 s | 0,21 s | 0,22 s ✅ |
| 2,00 s | 1,99 s — gardé entier | blanc long ✅ |

L'écart de ±0,02 s est la résolution des blocs de 10 ms de l'enveloppe.

Les trois règles du format qui ne se déduisent d'aucune mesure :

1. **On ne fragmente JAMAIS une tier list.** Un extrait au milieu montre un classement à moitié
   rempli et une note sans le débat qui l'a produite. **Dans une tier list, la prémisse c'est la
   liste elle-même.** (Erreur du 14/09 : deux extraits de 20 s taillés dans la tier list fruits.
   Nabil : « si tu fais ça on comprend plus rien. »)
2. **La durée est libre.** Corrélation durée/vues chez Sady : **+0,04**, c'est zéro, sur des vidéos
   de 1 min 55 à 3 min 47. On ne compresse pas pour atteindre une cible.
3. **On coupe les temps morts, rien d'autre.** Chaque item du classement garde sa discussion et son
   verdict. Rendement mesuré sur trois rushs : 11 à 15 % de temps mort.

Rendement attendu : si le dérush propose de jeter beaucoup plus de 15 %, c'est un signal
d'alarme — relire ce qu'il coupe avant d'encoder.

**Pas de sous-titres sur ce format** : le classement incrusté occupe déjà le tiers gauche.

---

## Le titre, dans les deux cas

Le benchmark est sans appel : chez Sady, les titres qui **promettent** font une médiane de
46 190 vues, ceux qui **décrivent** 22 974. **Deux fois moins**, et ce sont ses deux seules vidéos
sous 25 000.

**Un titre annonce un verdict contestable ou un aveu. Jamais le sujet.**

| ❌ | ✅ |
| :--- | :--- |
| « Tier list fruits » | « J'ai mis la fraise en 2 et j'assume » |
| « On note les joueurs » | « On a mis Messi en 7, venez nous insulter » |
