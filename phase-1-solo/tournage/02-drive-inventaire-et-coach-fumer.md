# Dossier Drive : inventaire, rangement proposé, et 1re analyse coach

*10/10/2026. Dossier : `drive.google.com/drive/folders/12IZK8pL9zUFRs4GW-CWEWgFhOkHCZVWH`, 11 fichiers vus à 13:13.*

## 1. Ce que je peux faire sur ce dossier

| | |
| :--- | :--- |
| Lire la liste et télécharger | ✅ par le lien public (`outils/recuperer.sh`), 11/11 fichiers téléchargés entiers, vérifiés par ffprobe |
| Renommer, déplacer, créer des sous-dossiers | ❌ pas pour l'instant : le connecteur Google Drive me répond « accès refusé » sur ce dossier |

Pour que je range moi-même, il faut que le connecteur Google Drive ait accès à ce dossier (c'est
réglable dans Paramètres → Connecteurs sur claude.ai). Sinon tu renommes à la main avec la liste du §3.

## 2. Ce qu'il y a dedans (mesuré)

Tous les `.mov` sont des **exports CapCut** (leurs métadonnées le disent : `TEEditor`,
`te_is_reencode=1`, `DreaminaMetaInfo`), pas les originaux de l'iPhone.

| Fichier | Contenu (transcription) | Tourné le | Durée | Résolution |
| :--- | :--- | :--- | ---: | :--- |
| `copy_A39B…mov` | Solo « Ceux qui ont arrêté de fumer, vous allez bien ? » | 17/09 | 47,3 s | 720×1280 |
| `copy_DD6F…mov` | Solo « 4 minutes sans répondre, 3 messages ? » | 17/09 | 41,0 s | 720×1280 |
| `copy_EFFD…mov` | Solo « Ceux qui disent "non j'ai pas faim" » (les frites) | 17/09 | 33,5 s | 720×1280 |
| `copy_2523…mov` | Solo « Les potes qui ont 3-4 ans de moins que vous » | 17/09 | 28,4 s | 720×1280 |
| `c7df…mov` | Extrait « fête foraine » | 09/10 | 10,1 s | **1080×1920** |
| `3478…mov` | Tier list footballeurs avec Sady (Salah, Drogba) | 14/09 | 83,0 s | **540×960** |
| `575b…mov` | Tier list pays avec Sady | 14/09 | 81,3 s | **540×960** |
| `b334…mov` | Tier list dessins animés avec Sady (Donald, Popeye) | 14/09 | 78,7 s | **540×960** |
| `OTAGE-TEL-chat.mp4` | Notre montage « L'otage du téléphone » (version chat) | — | 41,7 s | 720×1280 |
| `TIER-FOOT-chat.mp4` | Notre montage tier list foot (version chat) | — | 106,7 s | 720×1280 |
| `TIER-SPORT-chat.mp4` | Notre montage tier list sport (version chat) | — | 93,1 s | 720×1280 |

**À retenir :**
- Les trois tier lists du 14/09 sont en **540p** : c'est moins que la moitié des pixels du 720p, et un
  montage ne sera jamais plus net que ça. Si tu as les originaux dans Photos, mets plutôt ceux-là.
- Les 4 solos du 17/09 et la tier list pays/dessins animés ne sont **pas encore montés** chez nous.
- `OTAGE-TEL-chat` et `TIER-FOOT-chat` existent déjà en meilleure qualité dans `livraisons/` du dépôt.
  `TIER-SPORT-chat`, c'est ton montage perso, celui qu'on a volontairement laissé hors publication.

## 3. Rangement proposé (rien n'est touché tant que tu n'as pas dit oui)

Nom = `date_format_sujet_état`. Trois sous-dossiers : `1-rushs`, `2-montés`, `3-publiés`.

| Actuel | Nouveau nom | Dossier |
| :--- | :--- | :--- |
| `copy_A39B…mov` | `2026-09-17_solo_arrete-de-fumer_export.mov` | 1-rushs |
| `copy_DD6F…mov` | `2026-09-17_solo_4min-sans-repondre_export.mov` | 1-rushs |
| `copy_EFFD…mov` | `2026-09-17_solo_pas-faim-frites_export.mov` | 1-rushs |
| `copy_2523…mov` | `2026-09-17_solo_potes-plus-jeunes_export.mov` | 1-rushs |
| `c7df…mov` | `2026-10-09_extrait_fete-foraine.mov` | 1-rushs |
| `3478…mov` | `2026-09-14_tier_footballeurs_sady_540p.mov` | 1-rushs |
| `575b…mov` | `2026-09-14_tier_pays_sady_540p.mov` | 1-rushs |
| `b334…mov` | `2026-09-14_tier_dessins-animes_sady_540p.mov` | 1-rushs |
| `OTAGE-TEL-chat.mp4` | `2026-08-30_solo_otage-du-telephone_monte-chat.mp4` | 2-montés |
| `TIER-FOOT-chat.mp4` | `2026-09-14_tier_footballeurs_monte-chat.mp4` | 2-montés |
| `TIER-SPORT-chat.mp4` | `2026-09-13_tier_sport_monte-chat.mp4` | 2-montés |

## 4. Coach : « Ceux qui ont arrêté de fumer, vous allez bien ? »

Mesures : planches à 4 images/s sur le hook et 2 images/s ensuite, transcription mot à mot, netteté
par image, niveau sonore.

| Critère | Mesure | Verdict |
| :--- | :--- | :--- |
| Démarrage | 1er mot à **0,0 s** | ✅ zéro temps mort |
| Hook | « Ceux qui ont décidé d'arrêter de fumer, vous allez bien ? Non, je pose la question ! » | ✅ ouvre une question, parle à l'audience |
| Vignette (1re image) | netteté 192 contre 53 de médiane : **l'image la plus nette de toute la vidéo** | ✅ |
| Rythme global | **4,25 mots/s** (la prise retenue de « T'inquiète » était à 6,86) | 🟡 lent pour du face cam |
| Creux | **3,6 mots/s entre 5 et 15 s**, pile sur « Macron / la Belgique de Philippe / l'essence est chère » | 🔴 c'est là qu'on scrolle |
| Blancs | le plus long fait 0,5 s | ✅ déjà serré, rien à couper dans les silences |
| Son | −16,4 LUFS, pas de saturation | 🟡 à remonter à −14 au montage |
| Texte à l'écran | aucun sur les planches | 🟡 un titre sur le hook aide ceux qui regardent sans le son |
| Fin | la vanne tombe à **30,5-33,5 s** (« même s'ils veulent retourner fumer, le paquet coûte 13 balles, comment tu vas faire ? ») ; les **13 s d'après** la redisent sans monter | 🔴 la vidéo continue après sa chute |

**Les 3 corrections**

1. **Couper après « comment tu vas faire ? » (~34,5 s).** On passe de 47 à environ 35 s, et la vidéo
   finit sur sa meilleure phrase. « Affronte tes problèmes comme on affronte tout le monde » ne monte
   pas plus haut : elle dilue.
2. **Resserrer 5-15 s** à une seule phrase de contexte (« vous avez arrêté avant que tout devienne
   cher ») au lieu de Macron + Philippe + l'essence + les voitures. En plus, « la Belgique de Philippe »
   ne parle pas à un Français : ça va contre la cible francophonie.
3. **Remonter à −14 LUFS et mettre le hook en texte** sur les 3 premières secondes.

**Pour le tournage (ce que la vidéo t'apprend)** : écris ta chute **avant** de tourner et **arrête-toi
dès qu'elle est dite**. Ici elle existait, tu as continué 13 s par élan. Et une seule phrase de contexte,
pas quatre.

*Limite : la transcription est automatique ; deux passages sont peut-être mal entendus (16-19 s,
« il faut passer aux étudiants, aux commerciaux », et la dernière phrase). Les chiffres de rythme et de
blanc, eux, ne dépendent pas de ça.*

## 5. Rangement fait (10/10, 13:52, validé par Nabil)

15 vidéos renommées et rangées, rien de supprimé. La racine du dossier ne contient plus que
`1-rushs` (11 vidéos), `2-montés` (4) et `3-publiés` (vide).

Les 4 vidéos arrivées après le premier inventaire :

| Nouveau nom | Contenu (transcription) | Durée | Résolution |
| :--- | :--- | ---: | :--- |
| `2026-09-14_tier_red-flags-copine_sady_540p.mov` | Tier list des comportements de copine (elle check tes followers, elle veut te quitter à chaque dispute) | 101,7 s | 540×960 |
| `2026-09-14_tier_rappeurs_sady_540p.mov` | Tier list rappeurs (Jul, Alonzo…) | 111,7 s | 540×960 |
| `2026-09-17_solo_tinquiete_export.mov` | « T'inquiète », export CapCut d'une seule prise | 46,1 s | 720×1280 |
| `2026-09-12_solo_casser-des-nuques_monte-HQ.mp4` | Notre montage livré « Casser des nuques » | 42,9 s | 720×1280 |

Convention pour la suite : `date-de-tournage_format_sujet_état`, état = `export` (CapCut), `rush`
(original iPhone), `monte-…` (fini). Une vidéo publiée passe dans `3-publiés`.

## 6. Correction (10/10, 14:06) : les exports CapCut sont TES montages

**Erreur de classement.** J'avais rangé les 6 exports CapCut du 17/09 et du 09/10 dans `1-rushs` en
partant du principe qu'« export CapCut » voulait dire « rush pas encore monté ». C'était une
supposition, pas une mesure : un export CapCut, c'est une vidéo que Nabil a **montée lui-même**.
Nabil les a déplacés dans `2-montés` ; je les ai renommés `…_monte-capcut.mov`.

Le §2 (« les 4 solos du 17/09 ne sont pas encore montés ») et le §4 sont donc à lire autrement : le
rapport coach sur « arrêté de fumer » porte sur **son montage**, pas sur un rush. Les conseils restent
valables (couper après « comment tu vas faire ? », resserrer 5-15 s).

Les 5 tier lists du 14/09 restent dans `1-rushs` : Nabil ne les a pas montées. Elles sont quand même
passées par CapCut (métadonnées) et en sont ressorties en 540p.
