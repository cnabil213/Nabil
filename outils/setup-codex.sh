#!/usr/bin/env bash
# setup-codex.sh — script de setup pour un environnement Codex Cloud.
#
# À COLLER dans Codex : Settings → Environments → (cet environnement) → « Setup script ».
# Ce n'est pas un fichier que Codex va chercher tout seul dans le dépôt : il se colle
# dans l'interface. Il est versionné ici pour qu'on sache ce qu'on y a mis.
#
# POURQUOI TOUT EST ICI : chez Codex, « Setup scripts run with internet access » alors que
# « Agent internet access is off by default ». Donc tout ce qui a besoin du réseau — apt, pip,
# et surtout le modèle Whisper de 1,6 Go — doit être fait MAINTENANT. Pendant que l'agent
# travaille, il n'y aura peut-etre plus de reseau du tout.
#
# Le conteneur est mis en cache jusqu'a 12 h, et le cache est invalide des qu'on modifie ce
# script : une modif = une reinstallation complete.
set -uo pipefail

echo "=== 1/4 ffmpeg (indispensable : AUCUN outil video ne tourne sans lui) ==="
if ! command -v ffmpeg >/dev/null; then
  (apt-get update -qq && apt-get install -y --no-install-recommends ffmpeg) \
    || (sudo apt-get update -qq && sudo apt-get install -y --no-install-recommends ffmpeg) \
    || echo "!! ffmpeg NON INSTALLÉ — monter.py, derusher.py, sonoriser.py ne marcheront pas"
fi
command -v ffmpeg >/dev/null && ffmpeg -version | head -1

echo
echo "=== 2/4 dépendances de montage (derusher, monter, assembler, sonoriser) ==="
pip install --quiet --disable-pip-version-check \
    numpy soundfile opencv-python-headless || echo "!! pip a échoué sur les deps de montage"
python3 -c "import numpy, soundfile; print('  numpy + soundfile : OK')" \
  || echo "!! numpy/soundfile manquants"

echo
echo "=== 3/4 dépendances d'analyse de la voix (ecoute-video.py) ==="
pip install --quiet --disable-pip-version-check \
    scipy librosa praat-parselmouth matplotlib "faster-whisper==1.2.1" \
  || echo "!! pip a échoué sur les deps d'écoute (ecoute-video.py sera indisponible)"

echo
echo "=== 4/4 pré-téléchargement des modèles (le réseau n'existe QUE maintenant) ==="
# Sans ca, faster-whisper tente de telecharger 1,6 Go au premier appel — et echoue
# silencieusement si l'agent tourne sans reseau.
python3 - <<'PY' || echo "!! modèle Whisper non pré-téléchargé : ecoute-video.py échouera hors ligne"
try:
    from faster_whisper import WhisperModel
    WhisperModel("deepdml/faster-whisper-large-v3-turbo-ct2", device="cpu", compute_type="int8")
    print("  modèle Whisper turbo : en cache ✅")
except Exception as e:
    print(f"  Whisper indisponible : {e}")
    raise SystemExit(1)
PY

# Modele de visage pour retoucher.py (3,6 Mo) — inutile si on ne retouche pas de bouton.
if [ ! -f outils/face_landmarker.task ]; then
  curl -sSL -o outils/face_landmarker.task \
    "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task" \
    && echo "  modèle de visage : téléchargé ✅" || echo "  modèle de visage : non téléchargé (retoucher.py indisponible)"
fi

echo
echo "=== état final ==="
command -v ffmpeg >/dev/null && echo "  ffmpeg ........... ✅" || echo "  ffmpeg ........... ❌ BLOQUANT"
python3 -c "import numpy, soundfile" 2>/dev/null \
  && echo "  montage .......... ✅ (derusher, monter, assembler, sonoriser)" \
  || echo "  montage .......... ❌ BLOQUANT"
python3 -c "import faster_whisper, librosa, parselmouth" 2>/dev/null \
  && echo "  écoute ........... ✅ (ecoute-video.py)" \
  || echo "  écoute ........... ⚠️  indisponible"
echo
echo "RAPPEL : si « Agent internet access » est resté sur OFF, recuperer.sh et icloud.py"
echo "         ne pourront RIEN télécharger — donc aucun rush ne pourra entrer."
exit 0
