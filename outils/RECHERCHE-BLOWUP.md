# Blow Up : ce que c'est, comment ça marche, et notre version à nous

*Enquête du 10/10/2026.*

## 1. La réponse courte

- **Blow Up n'a pas d'IA secrète.** C'est très probablement un modèle du marché (type Gemini ou GPT)
  à qui on envoie ta vidéo avec un long prompt de « coach TikTok ». Aucune des deux apps ne dit
  laquelle elle utilise (vérifié sur les deux fiches App Store), donc c'est une **déduction**,
  pas un fait.
- **Ses « vues prédites » et sa « courbe de rétention » sont une estimation du modèle, pas une
  mesure.** Personne n'a accès aux données de l'algo TikTok depuis l'extérieur. Ça peut donner de bons
  conseils, mais le chiffre de vues, c'est du théâtre.
- **On a déjà 80 % de l'outil dans ton dépôt**, construit en septembre : `outils/recuperer.sh` règle
  le problème des 30 Mo, et `outils/vision-video.py` fait « regarder » la vidéo à Claude image par
  image. Ce qui manque, c'est la partie **coach** : une grille de lecture qui transforme ces mesures
  en verdict. Ça, on peut l'écrire.

## 2. Ce que fait Blow Up (d'après les fiches App Store)

Il y a **deux apps différentes** qui portent ce nom :

| | Blow Up AI : Deviens Viral | Blow Up – Go viral using AI |
| :--- | :--- | :--- |
| Éditeur | Mountains Studio LLC (Wyoming, contact en France) | Prescient Apps |
| Note | 4,5 / 5 sur ~13 000 avis (FR) | 3,8 / 5 sur 26 avis (US) |
| Ce qu'elle fait | Analyse de profil, idées de vidéos, scripts, analyse de vidéo, republication multi-plateforme | Tu importes un brouillon, elle « simule » vues, likes, partages, rétention, et propose légende + hashtags |
| Prix | 16,99 € à 84 € selon l'offre, ~30 €/mois selon un avis | 6,99 $/semaine ou 39,99 $/an |
| IA utilisée | Non dite | Non dite |

Vu la note et le public français, celle que tu as testée est très probablement **la première**
(Mountains Studio). À confirmer : c'est toi qui l'as sur ton téléphone.

## 3. Comment une IA « regarde » une vidéo

Il n'y a que deux façons de faire, et Blow Up utilise forcément l'une des deux :

1. **Un modèle qui avale la vidéo entière.** Gemini (Google) le fait nativement : il découpe la vidéo
   en **1 image par seconde** et écoute le son en même temps. Limites officielles : 2 Go par fichier en
   gratuit, jusqu'à 1 h de vidéo. C'est le plus probable pour Blow Up, parce que c'est le plus simple à
   brancher.
2. **Découper la vidéo en images et les montrer à un modèle qui lit les images** (Claude, GPT).
   C'est ce que fait déjà `vision-video.py`, et en mieux sur le point qui compte pour toi : **4 images
   par seconde sur le hook** (les 4 premières secondes), 2 ensuite, contre 1 par seconde chez Gemini par défaut (réglable, mais plus cher).
   Sur un hook de 3 secondes, Gemini voit 3 images, nous 12.

Claude ne prend pas de fichier vidéo directement : il lit des images. Donc quand tu dis « tu sais juste
sortir la transcription », c'est vrai **dans le chat**, mais pas avec les outils du dépôt.

## 4. Les 30 Mo : déjà réglé

Le chat plafonne, le conteneur non. La méthode, déjà écrite dans `outils/README.md` :

1. Tu mets ta vidéo **originale** sur Google Drive (ou WeTransfer, Dropbox).
2. Partage → « Tout utilisateur disposant du lien ».
3. Tu colles le lien dans le fil.
4. Je lance `bash outils/recuperer.sh "<lien>"` : le fichier arrive entier, sans compression, et le
   script vérifie que c'est bien une vidéo lisible.

Vérifié aujourd'hui : le conteneur joint bien les serveurs de téléchargement de Google Drive.

## 5. Ce qu'on construit pour avoir « notre Blow Up »

**Étape 1, la grille de coach (gratuit, à faire maintenant).** Un rapport fixe que Claude sort sur
chaque vidéo, à partir des planches et des mesures audio, avec une note par critère :

- **Hook (0-3 s)** : la première phrase est-elle déjà la vanne ou la promesse ? Est-ce qu'il y a du
  mouvement ou un texte à l'écran dès la première image ? La première image est-elle nette (c'est la
  vignette) ?
- **Points de décrochage** : les zones où la voix retombe (chiffre de `ecoute-video.py`) et où l'image
  ne bouge plus, bornées en secondes.
- **Chaîne de sens** : est-ce que la vanne se comprend sans contexte (règle du 13/09) ?
- **Chute** : sa longueur, et le blanc avant.
- **Les interdits** de `CLAUDE.md` repassés un par un.
- **3 corrections concrètes**, au timecode près.

**Étape 2, un deuxième avis Gemini (optionnel, quelques centimes par vidéo).** Avec une clé API
Google gratuite mise dans les secrets de l'environnement, on envoie la même vidéo à Gemini, qui
« regarde » son et image ensemble. On compare son avis à nos mesures. Utile pour le ressenti global ;
pas pour les chiffres.

**Étape 3, la vraie rétention.** Le seul juge, c'est TikTok Studio une fois la vidéo publiée : la
courbe de rétention réelle, en capture d'écran. On compare ce que la grille avait prédit à ce qui
s'est passé, vidéo après vidéo. Au bout de 10 vidéos, notre grille sera calibrée sur **ton** public,
ce que Blow Up ne fera jamais.

**Ce qu'on ne fait pas :** coder une app ou un SaaS. Ça coûte des semaines pour un seul utilisateur,
alors que le dépôt + le fil font déjà le travail.
