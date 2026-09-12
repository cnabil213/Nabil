# Recherche « est-ce que Claude peut m'entendre ? » — mémoire des résultats

> Question de Nabil (12/09/2026) : *« Il faut que tu puisses m'entendre. Est-ce vraiment impossible ? »*
> Deux salves d'agents, ~1,5 h de machine, chaque affirmation exécutée et mesurée.
> Ce fichier existe pour qu'aucune IA ne repropose une piste déjà close.

## La réponse

**Claude n'entend pas, et rien chez Anthropic ne le permet** (vérifié le 12/09/2026, pages officielles) :
aucun bloc audio dans l'API Messages, Files API = PDF / texte / images, outil Read de Claude Code =
texte / images / PDF, et la couche compatibilité OpenAI dit *« Audio input is not supported; it will be
ignored and stripped »*. Whisper entend et écrit ; Claude lit.

**Mais « entendre » n'est pas le besoin — le besoin, c'est juger la manière de parler.** Et ça, des
mesures le font, mieux qu'un modèle qui « écoute et décrit ». C'est ce que fait `ecoute-video.py`.

## Ce qui marche (vérifié)

| Piste | Verdict | Preuve |
| :--- | :--- | :--- |
| **Praat / parselmouth** (F0, intensité, syllabes, pauses) | ✅ colonne vertébrale | Retrouve la zone molle construite (3,81–8,55 s) à ±0,1 s sans qu'on l'indique ; sépare voix plate / vivante à volume et débit **strictement égaux** (écart-type F0 2,3 → 0,3 → 3,5 st) ; 4 s par clip |
| **Partition vocale (image)** | ✅ pour *confirmer*, ❌ pour *découvrir* | Test en aveugle : un Claude ignorant trouve le vrai défaut 3/3 (début à 0,01 s près)… mais signale des « retombées » sur 6/6 clips sains en question ouverte (fins de phrase normales). Lecture des dB sur le graphe biaisée de ~+3 dB. **→ La détection vient des chiffres ; l'image sert à décrire une zone déjà bornée.** |
| **Arousal audeering** (wav2vec2, 661 Mo) | ✅ complément | Retrouve la zone molle ; **insensible au volume** (zone ×3 → inchangé ; volume ÷3 seul → inchangé ; tempo 0,75 seul → 0,35 → 0,26) ; réagit aussi à l'intonation seule. Toujours en relatif à la médiane de la vidéo. Licence **CC-BY-NC-SA** |
| **faster-whisper large-v3-turbo** int8 | ✅ remplace `small` partout | « ta vidéo elle fait 3 minutes 40 » là où `small` écrivait « 8 minutes cartes » ; 20/20 mots sur FLEURS ; VAD inutile (mêmes timestamps) |
| **Fiche captation** (astats + ebur128) | ✅ | Crête −0,002 dBFS / true peak +0,1 dBTP / −17,8 LUFS retrouvés exactement ; a révélé le bug « pas de saturation » de `vision-video.py` (pic calculé sur des RMS par bloc) |
| **Score de chute + comparaison de prises** | ✅ | La punchline attendue sort en tête (85/100) ; le comparateur désigne la bonne prise 3/3 avec la bonne raison (plus rapide / plus vivante / pause plus nette) |
| **Robustesse bruit** | ✅ avec réglages | Zone molle survit au bruit rose SNR 15 dB et à une musique à −12 dB ; rétrécit sur un micro de téléphone clippé. D'où : seuil de silence relatif au plancher, F0 gaté par la parole, passe-haut 80 Hz |

## Ce qui est CLOS — ne pas reproposer

| Piste | Pourquoi c'est mort |
| :--- | :--- |
| **Modèles audio-langage locaux** (Voxtral-Mini-3B, Qwen2.5-Omni-3B, Ultravox-1B via llama.cpp) | Transcrivent bien, **n'entendent pas la manière** : timecodes inventés (« de 14 à 20 s » sur 12,5 s), ÉNERGIE=5 VOLUME=fort pour le segment mou comme pour les forts, même verdict défaut présent ou retiré. En comparatif (« quelle moitié est la plus faible ? ») : **8 réponses « SECONDE » sur 8**, quel que soit l'ordre — biais de position pur. Ils brodent une description plausible à partir du texte. |
| **Classifieurs d'émotion catégoriels** (superb, emotion2vec, Lajavaness) | « neutre » à 1,00 partout, sur-confiants, entraînés sur anglais/chinois joué ; emotion2vec 3,3 Go RAM. Seul `superb` bascule neu → sad sur une voix ralentie : gardé en drapeau optionnel, rien de plus. |
| **Indice d'articulation par confiance Whisper** (p < 0,5 = mot avalé) | Rappel 8 % ; les vraies erreurs ont p ≈ 0,8. Gardé uniquement comme « mot suspect / halluciné ». |
| **Pauses déduites des mots Whisper** | Les mots après une pause démarrent 0,15–0,3 s trop tôt → pauses sous-estimées. Les pauses viennent de l'acoustique. |
| **Seuil MONOTONE à 1,5 st / 1,5 s** | Se déclenche sur des voix naturelles (78 % des fenêtres d'une lecture posée). Recalibré : < 0,8 st sur 2 s (100 % des voix aplaties, 0 % des naturelles). |
| **Hume AI Expression Measurement** (le spécialiste prosodie) | Fermeture annoncée au 14/06/2026 (sources tierces, non confirmé par Hume). |
| **OpenAI gpt-audio, Mistral Voxtral API** comme oreilles | Écoutent, mais aucune doc n'affirme qu'elles décrivent le ton (Mistral le liste en « futur »). Plan B non testé. |
| **AssemblyAI, Deepgram, ElevenLabs Scribe** | Sentiment sur le **texte** (anglais) ou événements (rires) — rien sur la manière de parler. |

## Ce qui reste ouvert

- **Gemini API** — seule API hébergée dont la doc promet *« emotion detection in speech »* ; ~0,15 c€ la minute, free tier sur 2.5-flash-lite ; joignable d'ici. **Jamais appelée** (pas de clé). Si un jour testée : second avis descriptif, **jamais** source de timecodes sans recoupement avec les mesures.
- **Speak AI** (`https://api.speakai.co/v1/mcp`, OAuth) — son endpoint `insights` = sentiment **texte** par phrase ; sa seule vraie oreille est `ask_ai_chat` sur l'enregistrement (changelog 07/08/2026, modèle multimodal sous-jacent). 30 min gratuites puis 2 $/h. Complément possible, pas la solution.
- **Aucune vraie vidéo de Nabil n'a été mesurée** : tout est calibré sur voix synthétique + 3 lecteurs FLEURS. Les seuils bougeront avec le profil.
- Non couverts : euh / faux départs / respirations, rires et événements non verbaux, plusieurs locuteurs (GENZED), bruit de rue réel.

## Chiffres de la recherche

Salve 1 : 5 agents, 185 exécutions, 48 min. Salve 2 : 10 agents (7 vérifications, construction, relecture adversariale, corrections), 167 exécutions, 69 min. Modèles téléchargés puis effacés : ~9 Go (llama.cpp + 3 GGUF).
