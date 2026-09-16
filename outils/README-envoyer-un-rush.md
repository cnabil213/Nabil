# Envoyer un rush sans y passer dix minutes

> Le chat plafonne à **30 Mio**. Ce n'est pas réglable : c'est le client qui le fixe, pas Claude.
> Ce qui suit est la façon la moins pénible d'y arriver quand même, avec les mesures derrière.

---

## La bonne nouvelle : la plupart du temps, l'audio suffit

**Mesuré sur `livraisons/tier-foot-HQ.mp4`** — la même analyse de dérush, sur la vidéo complète
puis sur l'audio seul extrait en AAC 64 kb/s :

| | vidéo complète | audio seul |
| :--- | ---: | ---: |
| Poids | 60 Mo | **872 Ko** (69× moins) |
| Segments proposés | 5 | 5 |
| Écart max sur les bornes de coupe | — | **0,04 s** (0,00 s sur 4 segments / 5) |
| Blanc long détecté | 3,94 s | 3,94 s |
| Seuil de silence mesuré | −37,5 dBFS | −37,2 dBFS |

Tout ce qui **décide** du montage se fait sur l'audio : la transcription, l'enveloppe, les
silences, les redites, la chaîne de sens, la liste de coupes, le choix des prises, où poser un son.

Le fichier lourd ne sert qu'à **une seule chose** : le dernier encodage. Donc il ne bouge
qu'**une fois**, à la fin, quand la liste de coupes est validée — au lieu d'à chaque aller-retour.

---

## Le réflexe : le raccourci « Audio pour Claude » (un tap)

À construire **une seule fois**, dans l'app **Raccourcis** de l'iPhone :

1. **Raccourcis** → **+** (nouveau raccourci)
2. Ajouter l'action **« Encoder le média »**
3. Déplier **Afficher plus** → activer **« Audio uniquement »**
4. Ajouter l'action **« Partager »** en dessous
5. En haut, ⓘ (Détails) → activer **« Afficher dans la feuille de partage »**
   → dans **Types accepté**, ne laisser que **Médias** / **Vidéos**
6. Le nommer **« Audio pour Claude »**

Ensuite, à chaque tournage : **Photos → sélectionner les clips → Partager → Audio pour Claude →
envoyer dans le chat.** Un clip de 2 min sort autour de 1 à 2 Mo, donc **cinq clips passent
largement** sous les 30 Mio.

Envoie-les tous d'un coup : c'est la transcription de **tous** les clips qui révèle l'ordre réel et
les prises jumelles — les horodatages des fichiers se chevauchent et mentent (mesuré le 15/09 sur
« T'inquiète »).

---

## Le fichier lourd, quand il faut vraiment : iCloud Drive

**Dans Photos :** sélectionner la vidéo → **Partager** → **« Enregistrer dans Fichiers »** →
choisir **iCloud Drive** (un dossier `Rushs`, par exemple).

**Puis dans Fichiers :** appui long sur le fichier → **Partager** → **Copier le lien**
→ vérifier que l'accès est **« Tout utilisateur disposant du lien »** → coller le lien dans le chat.

Je m'occupe du reste :

```bash
bash outils/recuperer.sh "<lien iCloud>"
```

`recuperer.sh` reconnaît le lien iCloud, passe par [`icloud.py`](icloud.py) qui interroge l'API
publique de résolution (un lien iCloud est une page JavaScript — `curl` dessus ne récupère que du
HTML), récupère l'URL signée, télécharge, puis **vérifie que c'est bien une vidéo** et pas une page
de connexion.

**Le tuyau n'est pas le goulot** : mesuré depuis le conteneur, **15 Mo/s** — une vidéo de 500 Mo
arrive en 35 secondes. Et il y a 29 Go de libre.

---

## Les trois pièges qui coûtent de la qualité

### 1. ❌ Ne pas passer par un Album partagé iCloud

Apple **ré-encode et rabote** les vidéos des albums partagés. C'est exactement le problème du rush
du 12/09, qui était une capture Snapchat en 720p là où l'iPhone filme en 1080p et 4K — et
`CLAUDE.md` §5 est sans appel : **un montage ne peut pas être plus net que son rush.**

`icloud.py` **refuse** ces liens et rappelle le bon chemin plutôt que de livrer un rush dégradé
sans le dire.

### 2. ❌ Ne pas « partager directement vers une app »

Un partage direct depuis Photos vers une app fait **reconvertir le HEVC en H.264 par iOS**. C'est
pour ça que le fichier reçu pesait 98 Mo pour la même image que 57 Mo d'original. Passer par
**« Enregistrer dans Fichiers »**, qui copie le fichier tel quel.

### 3. ❌ Ne pas envoyer une version compressée « pour que ça passe »

Ré-encoder change la crête, le true peak et le loudness. La fiche captation porterait alors sur la
compression, pas sur le tournage — et les conseils qui en sortent (« ça sature », « 4 LU sous la
cible ») seraient faux.

Si c'est trop lourd : **l'audio d'abord** (§ ci-dessus), le fichier entier ensuite par iCloud Drive.

---

## Ce qui a été essayé et écarté

| Piste | Verdict, mesuré |
| :--- | :--- |
| Augmenter la limite du chat | Impossible — fixée par le client |
| Page web d'upload (artifact) | **20 Mio** de plafond : pire que le chat |
| Connecteur Google Drive pour les octets | Rend le fichier **en base64 dans la conversation** : 100 Mo de vidéo = ~133 Mo de texte. Inutilisable |
| Connecteur Google Drive pour **trouver** un fichier | Marcherait (métadonnées seulement), mais le connecteur n'est **pas autorisé** sur ce compte |
| `transfer.sh`, `0x0.st`, `bashupload.com` | **Injoignables** depuis le conteneur |
| Hébergeurs anonymes publics (catbox, etc.) | Joignables, mais y déposer des sketchs **non publiés** sur une URL publique : non |
| Google Drive, Dropbox, WeTransfer, GitHub, iCloud | **Tous joignables** — `recuperer.sh` les gère |

---

## Rappel de tournage (le plafond se joue avant le montage)

- **Filmer avec l'app Caméra**, pas dans Snapchat/Instagram/TikTok, qui plafonnent à 720p là où
  l'iPhone fait du 1080p et du 4K.
- Si la fiche captation annonce une crête au-dessus de **−1 dBTP**, reculer le téléphone au
  prochain tournage : à −6 dBTP il n'y aurait plus rien à retenir au limiteur.
- **Premier réflexe sur un rush reçu** : `derusher.py` en sort la fiche captation, et je te la dis
  **avant** de monter — c'est le seul moment où tu peux retourner filmer.
