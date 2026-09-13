#!/bin/bash
# Démarrage de session : injecte la mémoire du projet dans le contexte, puis prépare
# les outils de montage. Idempotent, non interactif, jamais bloquant.
set -uo pipefail
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0

echo "=============== MÉMOIRE DU PROJET (ETAT.md) ==============="
[ -f ETAT.md ] && cat ETAT.md
echo
echo "=============== DERNIÈRE SESSION (JOURNAL.md) ==============="
[ -f JOURNAL.md ] && sed -n '/^## /,/^## /p' JOURNAL.md | sed '$d' | head -40
echo
echo "=============== RAPPEL ==============="
echo "Finir la session en réécrivant ETAT.md et en ajoutant une entrée en haut de JOURNAL.md."
echo

# --- outils : seulement en session distante, et sans jamais faire échouer le démarrage
[ "${CLAUDE_CODE_REMOTE:-}" != "true" ] && exit 0
command -v ffmpeg >/dev/null || echo "ATTENTION : ffmpeg absent — aucun outil vidéo ne tournera."
if ! python3 -c "import numpy, soundfile" 2>/dev/null; then
  echo "Installation des dépendances de montage (numpy, soundfile, opencv)…"
  pip3 install --quiet --disable-pip-version-check numpy soundfile opencv-python-headless 2>&1 | tail -2 || true
fi
python3 -c "import numpy, soundfile" 2>/dev/null \
  && echo "Outils de montage : prêts (monter.py, sonoriser.py)." \
  || echo "Outils de montage : dépendances manquantes, voir outils/README.md §Installation."
echo "Analyse de la voix (ecoute-video.py) et retouche (retoucher.py) : dépendances lourdes,"
echo "à installer à la demande — voir outils/README.md §Installation."
exit 0
